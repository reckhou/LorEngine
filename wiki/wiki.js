/* Lorengine — wiki.js
   Shared logic: search index, Lunr, markdown rendering, AI sidebar.
   Vanilla JS, ES2020+. No frameworks.
   All HTML inserted via innerHTML is sanitized through DOMPurify. */

// Config injected at build time
const WIKI_CONFIG = {
  title: "{{WIKI_TITLE}}",
  description: "{{WIKI_DESCRIPTION}}",
  baseUrl: "{{BASE_URL}}",
  ai: {
    model: "{{AI_MODEL}}",
    maxTokens: parseInt("{{AI_MAX_TOKENS}}", 10) || 1024,
    systemPromptFile: "{{AI_SYSTEM_PROMPT_FILE}}",
    enablePromptCaching: "{{AI_ENABLE_PROMPT_CACHING}}" === "true",
  },
  search: {
    maxResults: parseInt("{{SEARCH_MAX_RESULTS}}", 10) || 20,
    excerptLength: parseInt("{{SEARCH_EXCERPT_LENGTH}}", 10) || 160,
  },
  apiKey: "{{ANTHROPIC_API_KEY}}",
};

// ---------------------------------------------------------------------------
// Safe HTML helpers — all dynamic HTML goes through DOMPurify
// ---------------------------------------------------------------------------

function sanitize(html) {
  return DOMPurify.sanitize(html);
}

function safeSetInnerHTML(el, html) {
  el.innerHTML = DOMPurify.sanitize(html);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Search index
// ---------------------------------------------------------------------------

let _searchIndexCache = null;

async function loadSearchIndex() {
  if (_searchIndexCache) return _searchIndexCache;
  const base = WIKI_CONFIG.baseUrl ? WIKI_CONFIG.baseUrl + "/" : "";
  const resp = await fetch(`${base}search_index.json`);
  if (!resp.ok) throw new Error("Failed to load search index");
  _searchIndexCache = await resp.json();
  return _searchIndexCache;
}

function buildLunrIndex(data) {
  return lunr(function () {
    this.ref("id");
    this.field("title", { boost: 10 });
    this.field("tags", { boost: 5 });
    this.field("headings", { boost: 3 });
    this.field("body");

    data.forEach((doc) => {
      this.add({
        id: doc.id,
        title: doc.title,
        tags: (doc.tags || []).join(" "),
        headings: (doc.headings || []).join(" "),
        body: doc.body,
      });
    });
  });
}

// ---------------------------------------------------------------------------
// Rendering helpers
// ---------------------------------------------------------------------------

function makeBadge(status) {
  const s = escapeHtml(status || "draft");
  return `<span class="badge badge-${s}">${s}</span>`;
}

function makeTags(tags) {
  if (!tags || !tags.length) return "";
  return tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join(" ");
}

function docUrl(id) {
  const base = WIKI_CONFIG.baseUrl ? WIKI_CONFIG.baseUrl + "/" : "";
  return `${base}page.html?doc=${encodeURIComponent(id)}`;
}

// ---------------------------------------------------------------------------
// Index page: render doc list
// ---------------------------------------------------------------------------

function renderDocList(data, container) {
  if (!data.length) {
    container.textContent = "No documents found. Add markdown files to the docs/ directory to get started.";
    container.className = "empty-state";
    return;
  }

  // Sort by last_updated (most recent first), then show only top 5
  const sorted = [...data]
    .sort((a, b) => (b.last_updated || "").localeCompare(a.last_updated || ""))
    .slice(0, 5);

  const html = sorted
    .map((doc) => {
      const excerpt = (doc.excerpt || "").slice(0, WIKI_CONFIG.search.excerptLength);
      // Convert newlines to <br> for proper line wrapping
      const excerptHtml = escapeHtml(excerpt).replace(/\n/g, "<br>");
      return `
      <article class="doc-card">
        <h2 class="doc-card-title"><a href="${escapeHtml(docUrl(doc.id))}">${escapeHtml(doc.title)}</a></h2>
        <div class="doc-card-meta">
          ${makeBadge(doc.status)}
          ${makeTags(doc.tags)}
          ${doc.last_updated ? `<span>${escapeHtml(doc.last_updated)}</span>` : ""}
        </div>
        <p class="doc-card-excerpt">${excerptHtml}</p>
      </article>`;
    })
    .join("");

  safeSetInnerHTML(container, html);
}

// ---------------------------------------------------------------------------
// Search page
// ---------------------------------------------------------------------------

function renderSearch(query, lunrIndex, data, container) {
  if (!query.trim()) {
    container.textContent = "Type to search across all documents.";
    container.className = "empty-state";
    return;
  }

  let results;
  try {
    results = lunrIndex.search(query);
  } catch {
    try {
      results = lunrIndex.search(query.replace(/[:\*\~\^]/g, ""));
    } catch {
      container.textContent = "Invalid search query.";
      container.className = "empty-state";
      return;
    }
  }

  if (!results.length) {
    container.textContent = `No results for "${query}".`;
    container.className = "empty-state";
    return;
  }

  const dataMap = Object.fromEntries(data.map((d) => [d.id, d]));
  const limited = results.slice(0, WIKI_CONFIG.search.maxResults);

  const html = limited
    .map((r) => {
      const doc = dataMap[r.ref];
      if (!doc) return "";
      const excerpt = (doc.excerpt || "").slice(0, WIKI_CONFIG.search.excerptLength);
      return `
      <div class="search-result">
        <h3 class="search-result-title"><a href="${escapeHtml(docUrl(doc.id))}">${escapeHtml(doc.title)}</a></h3>
        <div class="doc-card-meta">
          ${makeBadge(doc.status)}
          ${makeTags(doc.tags)}
        </div>
        <p class="search-result-excerpt">${escapeHtml(excerpt)}</p>
      </div>`;
    })
    .join("");

  safeSetInnerHTML(container, html);
}

// ---------------------------------------------------------------------------
// Markdown rendering (page viewer)
// ---------------------------------------------------------------------------

function renderMarkdown(md) {
  marked.setOptions({
    gfm: true,
    breaks: false,
    highlight: function (code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
  });
  return sanitize(marked.parse(md));
}

function buildToc(md) {
  const headings = [];
  const lines = md.split("\n");
  for (const line of lines) {
    const m = line.match(/^(#{2,3})\s+(.+)$/);
    if (m) {
      const level = m[1].length;
      const text = m[2].trim();
      const id = text
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-");
      headings.push({ level, text, id });
    }
  }
  return headings;
}

function renderToc(headings) {
  if (!headings.length) return "";
  const items = headings
    .map((h) => {
      const cls = h.level === 3 ? ' class="toc-h3"' : "";
      return `<li${cls}><a href="#${escapeHtml(h.id)}">${escapeHtml(h.text)}</a></li>`;
    })
    .join("");
  return sanitize(`
    <nav class="toc">
      <div class="toc-title">Contents</div>
      <ul>${items}</ul>
    </nav>`);
}

// ---------------------------------------------------------------------------
// Tree Sidebar
// ---------------------------------------------------------------------------

function buildDocTree(data) {
  // Create a map for quick lookup
  const docMap = Object.fromEntries(data.map((d) => [d.id, { ...d }]));

  // Build tree structure
  const roots = [];
  for (const doc of Object.values(docMap)) {
    if (doc.parent === null || !docMap[doc.parent]) {
      roots.push(doc.id);
    }
  }

  return { docMap, roots };
}

function renderTreeNode(docId, tree, docMap, filterText, sortOrder) {
  const doc = docMap[docId];
  if (!doc) return "";

  // Filter: hide non-matching, but keep parents visible
  const titleMatches = doc.title.toLowerCase().includes(filterText.toLowerCase());
  const childDocs = (doc.children || []).map(childId => docMap[childId]).filter(d => d);
  const children = childDocs
    .map(childDoc => renderTreeNode(childDoc.id, tree, docMap, filterText, sortOrder))
    .filter((html) => html.length > 0);
  const hasVisibleChildren = children.length > 0;

  // Show this node if: matches filter OR has visible children
  if (!titleMatches && !hasVisibleChildren && filterText.trim()) {
    return "";
  }

  // Default to expanded (true) if no localStorage value, only collapse if explicitly set to "false"
  const storageKey = `tree-expanded-${doc.id}`;
  const storedValue = localStorage.getItem(storageKey);
  const isExpanded = storedValue === null || storedValue !== "false";
  const toggleClass = `tree-toggle${isExpanded ? " expanded" : ""}`;
  const childrenClass = `tree-children${isExpanded ? " visible" : ""}`;

  return `
    <li class="tree-item">
      <div class="tree-item-row">
        ${doc.children && doc.children.length > 0
          ? `<button class="${toggleClass}" data-doc-id="${escapeHtml(doc.id)}" aria-expanded="${isExpanded}">▶</button>`
          : `<span class="tree-toggle-spacer"></span>`}
        <a href="${escapeHtml(docUrl(doc.id))}" class="tree-link">${escapeHtml(doc.title)}</a>
      </div>
      ${children.length > 0
        ? `<ul class="${childrenClass}">${children.join("")}</ul>`
        : ""}
    </li>`;
}

function initTreeSidebar(data, container) {
  if (!container) return;

  const { docMap, roots } = buildDocTree(data);

  // Create tree controls
  const controlsHtml = `
    <div class="tree-controls">
      <input type="text" class="tree-filter" placeholder="Filter pages...">
      <select class="tree-sort">
        <option value="alpha-asc">A-Z</option>
        <option value="alpha-desc">Z-A</option>
        <option value="date-asc">Oldest first</option>
        <option value="date-desc">Newest first</option>
      </select>
    </div>
  `;

  const treeHtml = `
    <ul class="tree-list">
      ${roots
        .map((id) => renderTreeNode(id, { docMap, roots }, docMap, "", "alpha-asc"))
        .join("")}
    </ul>
  `;

  safeSetInnerHTML(container, controlsHtml + treeHtml);

  // Handle toggle clicks
  const toggles = container.querySelectorAll(".tree-toggle");
  toggles.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const docId = btn.dataset.docId;
      const childrenEl = btn.parentElement.nextElementSibling;

      if (childrenEl && childrenEl.classList.contains("tree-children")) {
        const isExpanded = childrenEl.classList.contains("visible");
        childrenEl.classList.toggle("visible");
        btn.classList.toggle("expanded");
        localStorage.setItem(`tree-expanded-${docId}`, isExpanded ? "false" : "true");
      }
    });
  });

  // Handle filter
  const filterInput = container.querySelector(".tree-filter");
  const sortSelect = container.querySelector(".tree-sort");

  function updateTree() {
    const filterText = filterInput?.value || "";
    const sortOrder = sortSelect?.value || "alpha-asc";

    const treeHtml = `
      <ul class="tree-list">
        ${roots
          .map((id) => renderTreeNode(id, { docMap, roots }, docMap, filterText, sortOrder))
          .join("")}
      </ul>
    `;

    const treeListEl = container.querySelector(".tree-list");
    if (treeListEl) {
      safeSetInnerHTML(treeListEl, treeHtml.replace(/<[^>]*>/g, (match) => {
        // This is a workaround to just update the list without re-creating controls
        if (match.includes("ul")) return match;
        return match;
      }));

      // Re-attach toggle listeners
      const newToggles = container.querySelectorAll(".tree-toggle");
      newToggles.forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.preventDefault();
          const docId = btn.dataset.docId;
          const childrenEl = btn.parentElement.nextElementSibling;

          if (childrenEl && childrenEl.classList.contains("tree-children")) {
            const isExpanded = childrenEl.classList.contains("visible");
            childrenEl.classList.toggle("visible");
            btn.classList.toggle("expanded");
            localStorage.setItem(`tree-expanded-${docId}`, isExpanded ? "false" : "true");
          }
        });
      });
    }
  }

  filterInput?.addEventListener("input", updateTree);
  sortSelect?.addEventListener("change", updateTree);
}

// ---------------------------------------------------------------------------
// Backlinks and page references
// ---------------------------------------------------------------------------

function renderBacklinks(backlinks, searchIndex) {
  if (!backlinks || backlinks.length === 0) {
    return "";
  }

  const docMap = Object.fromEntries(searchIndex.map((d) => [d.id, d]));
  const links = backlinks
    .map((id) => {
      const doc = docMap[id];
      if (!doc) return "";
      return `<li><a href="${escapeHtml(docUrl(id))}">${escapeHtml(doc.title)}</a></li>`;
    })
    .filter((html) => html.length > 0)
    .join("");

  if (!links) return "";

  return `
    <div class="backlinks-section">
      <h3>Referenced by</h3>
      <ul class="backlinks-list">
        ${links}
      </ul>
    </div>`;
}

function buildTitleAutocomplete(searchIndex) {
  // Create a map of lowercase title → doc id
  const titleMap = new Map();
  for (const doc of searchIndex) {
    const key = doc.title.toLowerCase();
    titleMap.set(key, doc.id);
  }
  return titleMap;
}

function autocompleteTitle(input, titleMap) {
  // Return matching doc IDs for partial input (case-insensitive)
  if (!input.trim()) return [];

  const search = input.toLowerCase();
  const matches = [];

  for (const [title, id] of titleMap) {
    if (title.includes(search)) {
      matches.push({ title, id });
    }
  }

  // Sort by relevance: starts with search first, then contains
  return matches.sort((a, b) => {
    const aStarts = a.title.startsWith(search);
    const bStarts = b.title.startsWith(search);
    if (aStarts !== bStarts) return bStarts ? 1 : -1;
    return a.title.localeCompare(b.title);
  });
}

// ---------------------------------------------------------------------------
// API Key Modal
// ---------------------------------------------------------------------------

function showAPIKeyModal(callback) {
  // Create overlay and modal
  const overlay = document.createElement("div");
  overlay.className = "api-key-modal-overlay";

  const modal = document.createElement("div");
  modal.className = "api-key-modal";

  const html = `
    <div class="api-key-modal-content">
      <h2>Claude API Key Required</h2>
      <p>Enter your Anthropic API key to use the AI sidebar. Your key is stored locally in your browser and never sent to our servers.</p>
      <div class="api-key-input-group">
        <input type="password" class="api-key-input" placeholder="sk-..." autocomplete="off" aria-label="API key">
      </div>
      <label class="api-key-remember">
        <input type="checkbox" class="api-key-remember-checkbox" checked>
        <span>Remember on this device</span>
      </label>
      <div class="api-key-buttons">
        <button class="api-key-submit">Enable AI Sidebar</button>
      </div>
    </div>
  `;

  safeSetInnerHTML(modal, html);
  overlay.appendChild(modal);
  document.body.appendChild(overlay);

  const input = modal.querySelector(".api-key-input");
  const checkbox = modal.querySelector(".api-key-remember-checkbox");
  const submitBtn = modal.querySelector(".api-key-submit");

  function submit() {
    const key = input.value.trim();
    if (!key) {
      input.focus();
      return;
    }
    const remember = checkbox.checked;
    overlay.remove();
    callback(key, remember);
  }

  input.focus();
  submitBtn.addEventListener("click", submit);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      submit();
    }
  });

  // Prevent closing by clicking overlay
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      e.preventDefault();
    }
  });
}

// ---------------------------------------------------------------------------
// AI Sidebar
// ---------------------------------------------------------------------------

function initAISidebar(currentDocContent, searchIndex) {
  const header = document.querySelector(".ai-sidebar-header");
  const body = document.querySelector(".ai-sidebar-body");
  const input = document.querySelector(".ai-input");
  const sendBtn = document.querySelector(".ai-send-btn");
  const messagesEl = document.querySelector(".ai-messages");

  if (!header || !body) return;

  // Collapse/expand
  header.addEventListener("click", () => {
    body.classList.toggle("collapsed");
    const arrow = header.querySelector(".ai-toggle");
    if (arrow) arrow.textContent = body.classList.contains("collapsed") ? "+" : "\u2212";
  });

  // Determine API key: config > localStorage > modal
  let apiKey = WIKI_CONFIG.apiKey;
  let keySource = "config"; // "config" | "stored" | "user"

  if (!apiKey) {
    const stored = localStorage.getItem("lorengine-api-key");
    if (stored) {
      apiKey = stored;
      keySource = "stored";
    }
  }

  if (!apiKey) {
    // Show blocking modal
    showAPIKeyModal((key, remember) => {
      apiKey = key;
      keySource = "user";
      if (remember) {
        localStorage.setItem("lorengine-api-key", key);
      }
      // Update global config and continue
      WIKI_CONFIG.apiKey = key;
      initAISidebar(currentDocContent, searchIndex);
    });
    return;
  }

  // Update global config if we got the key from localStorage
  if (!WIKI_CONFIG.apiKey) {
    WIKI_CONFIG.apiKey = apiKey;
  }

  // Add delete button if key was stored or provided by user
  if (keySource !== "config" && header) {
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "ai-key-delete-btn";
    deleteBtn.setAttribute("aria-label", "Delete saved API key");
    deleteBtn.textContent = "⌫";
    deleteBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (confirm("Delete saved API key?")) {
        localStorage.removeItem("lorengine-api-key");
        location.reload();
      }
    });
    header.appendChild(deleteBtn);
  }

  const conversation = [];

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    conversation.push({ role: "user", content: text });

    // Keep only last 4 turns (8 messages)
    while (conversation.length > 8) conversation.shift();

    appendMessage("user", text);

    sendBtn.disabled = true;
    input.disabled = true;

    try {
      const response = await makeAPICall(conversation, currentDocContent, searchIndex);
      conversation.push({ role: "assistant", content: response });
      appendMessage("assistant", response);
    } catch (err) {
      appendMessage("assistant", `Error: ${err.message}`);
    } finally {
      sendBtn.disabled = false;
      input.disabled = false;
      input.focus();
    }
  }

  function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = `ai-message ai-message-${role}`;
    if (role === "assistant") {
      safeSetInnerHTML(div, renderMarkdown(text));
    } else {
      div.textContent = text;
    }
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

async function makeAPICall(conversation, currentDocContent, searchIndex) {
  const docSummary = searchIndex
    .map((d) => `- ${d.title} [${(d.tags || []).join(", ")}]: ${d.excerpt.slice(0, 80)}`)
    .join("\n");

  let systemPrompt = "";
  try {
    const base = WIKI_CONFIG.baseUrl ? WIKI_CONFIG.baseUrl + "/" : "";
    const resp = await fetch(`${base}${WIKI_CONFIG.ai.systemPromptFile}`);
    if (resp.ok) systemPrompt = await resp.text();
  } catch {
    // System prompt file not available
  }

  const systemContent = [
    {
      type: "text",
      text: systemPrompt || "You are an AI assistant embedded in a documentation wiki. Be helpful, concise, and reference the current document when relevant.",
      ...(WIKI_CONFIG.ai.enablePromptCaching ? { cache_control: { type: "ephemeral" } } : {}),
    },
    {
      type: "text",
      text: `## Document Index\n${docSummary}`,
      ...(WIKI_CONFIG.ai.enablePromptCaching ? { cache_control: { type: "ephemeral" } } : {}),
    },
  ];

  const messages = [
    { role: "user", content: `[Current page content]\n${currentDocContent}\n\n---` },
    ...conversation,
  ];

  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": WIKI_CONFIG.apiKey,
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true",
    },
    body: JSON.stringify({
      model: WIKI_CONFIG.ai.model,
      max_tokens: WIKI_CONFIG.ai.maxTokens,
      system: systemContent,
      messages: messages,
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`API error ${resp.status}: ${err}`);
  }

  const data = await resp.json();
  return data.content.map((b) => b.text).join("");
}

// ---------------------------------------------------------------------------
// Theme panel (accent picker + dark/light toggle)
// ---------------------------------------------------------------------------

const ACCENT_PALETTE = [
  { name: "Purple",  value: "#7F77DD" },
  { name: "Blue",    value: "#3B82F6" },
  { name: "Indigo",  value: "#6366F1" },
  { name: "Teal",    value: "#14B8A6" },
  { name: "Green",   value: "#10B981" },
  { name: "Orange",  value: "#F59E0B" },
  { name: "Red",     value: "#EF4444" },
  { name: "Pink",    value: "#EC4899" },
];

function applyTheme(mode, accent) {
  // Mode: "light" | "dark" | null (follow system)
  if (mode) {
    document.documentElement.setAttribute("data-theme", mode);
  } else {
    document.documentElement.removeAttribute("data-theme");
  }
  if (accent) {
    document.documentElement.style.setProperty("--accent", accent);
    document.documentElement.style.setProperty(
      "--accent-hover",
      `color-mix(in srgb, ${accent} 80%, black)`
    );
  }
}

function initThemePanel() {
  const btn = document.querySelector(".theme-toggle");
  if (!btn) return;

  // Restore persisted preferences
  const storedMode   = localStorage.getItem("lorengine-theme");
  const storedAccent = localStorage.getItem("lorengine-accent");
  applyTheme(storedMode, storedAccent);

  // Build popover element (once, appended to body)
  const panel = document.createElement("div");
  panel.className = "theme-panel";
  panel.setAttribute("aria-label", "Theme settings");

  const isDark = () => {
    const attr = document.documentElement.getAttribute("data-theme");
    if (attr === "dark") return true;
    if (attr === "light") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  };

  function buildPanel() {
    const currentAccent = localStorage.getItem("lorengine-accent") || ACCENT_PALETTE[0].value;
    panel.innerHTML = DOMPurify.sanitize(`
      <div class="theme-panel-section theme-panel-label">Accent colour</div>
      <div class="theme-panel-swatches">
        ${ACCENT_PALETTE.map(c => `
          <button class="theme-swatch${c.value === currentAccent ? " active" : ""}"
                  data-accent="${escapeHtml(c.value)}"
                  title="${escapeHtml(c.name)}"
                  style="background:${escapeHtml(c.value)}"></button>
        `).join("")}
      </div>
      <div class="theme-panel-section theme-panel-label">Mode</div>
      <div class="theme-panel-mode">
        <span class="theme-mode-label">Light</span>
        <label class="theme-mode-switch" aria-label="Toggle dark mode">
          <input type="checkbox" class="theme-mode-checkbox" ${isDark() ? "checked" : ""}>
          <span class="theme-mode-slider"></span>
        </label>
        <span class="theme-mode-label">Dark</span>
      </div>
    `);

    // Swatch clicks
    panel.querySelectorAll(".theme-swatch").forEach(sw => {
      sw.addEventListener("click", () => {
        const accent = sw.dataset.accent;
        localStorage.setItem("lorengine-accent", accent);
        applyTheme(document.documentElement.getAttribute("data-theme"), accent);
        panel.querySelectorAll(".theme-swatch").forEach(s => s.classList.remove("active"));
        sw.classList.add("active");
      });
    });

    // Dark/light toggle
    const checkbox = panel.querySelector(".theme-mode-checkbox");
    checkbox.addEventListener("change", () => {
      const mode = checkbox.checked ? "dark" : "light";
      localStorage.setItem("lorengine-theme", mode);
      applyTheme(mode, null);
    });
  }

  document.body.appendChild(panel);

  // Show/hide panel
  let open = false;
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    open = !open;
    if (open) {
      buildPanel();
      // Position below the button
      const rect = btn.getBoundingClientRect();
      panel.style.top  = `${rect.bottom + 8 + window.scrollY}px`;
      panel.style.right = `${document.documentElement.clientWidth - rect.right}px`;
      panel.classList.add("visible");
    } else {
      panel.classList.remove("visible");
    }
  });

  // Close on outside click
  document.addEventListener("pointerdown", (e) => {
    if (open && !panel.contains(e.target) && e.target !== btn) {
      open = false;
      panel.classList.remove("visible");
    }
  });
}
