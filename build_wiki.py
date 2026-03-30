#!/usr/bin/env python3
"""LorEngine build script — generates search_index.json and assembles _site/.

Stdlib only (Python 3.11+). No pip dependencies.
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal YAML parser (2-level deep, simple scalars/lists only)
# ---------------------------------------------------------------------------

def parse_yaml(text):
    """Parse a simple 2-level YAML structure into a dict of dicts.

    Handles: strings (quoted or unquoted), integers, booleans,
    inline lists like ["a", "b"], and empty strings.
    """
    result = {}
    current_section = None

    for line in text.splitlines():
        # Skip blank lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Top-level key (no leading whitespace)
        if not line[0].isspace() and ":" in line:
            key = stripped.split(":")[0].strip()
            value_part = stripped[len(key) + 1:].strip()
            if not value_part:
                # Section header
                current_section = key
                result[current_section] = {}
            else:
                result[key] = _parse_value(value_part)
            continue

        # Indented key (child of current section)
        if current_section is not None and ":" in stripped:
            key = stripped.split(":")[0].strip()
            value_part = stripped[len(key) + 1:].strip()
            result[current_section][key] = _parse_value(value_part)

    return result


def _parse_value(raw):
    """Convert a raw YAML value string to a Python type."""
    if not raw:
        return ""

    # Strip inline comments (but not inside quotes)
    if not raw.startswith('"') and not raw.startswith("'") and not raw.startswith("["):
        comment_pos = raw.find(" #")
        if comment_pos != -1:
            raw = raw[:comment_pos].strip()

    # Booleans
    if raw.lower() in ("true", "yes"):
        return True
    if raw.lower() in ("false", "no"):
        return False

    # Integers
    try:
        return int(raw)
    except ValueError:
        pass

    # Quoted strings
    if (raw.startswith('"') and raw.endswith('"')) or \
       (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]

    # Inline list: ["a", "b", "c"]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip().strip('"').strip("'")
            if item:
                items.append(item)
        return items

    return raw


# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Extract YAML frontmatter and body from a markdown file.

    Returns (metadata_dict, body_string). If no valid frontmatter found,
    returns (None, text).
    """
    if not text.startswith("---"):
        return None, text

    # Find the closing ---
    end = text.find("---", 3)
    if end == -1:
        return None, text

    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()

    metadata = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key = line.split(":")[0].strip()
        value_part = line[len(key) + 1:].strip()
        metadata[key] = _parse_value(value_part)

    return metadata, body


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def extract_headings(body):
    """Extract ## and ### headings from markdown body."""
    headings = []
    for line in body.splitlines():
        m = re.match(r"^#{2,3}\s+(.+)$", line)
        if m:
            headings.append(m.group(1).strip())
    return headings


def strip_markdown(text):
    """Strip common markdown syntax to produce plain text."""
    # Remove code blocks
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    # Remove headings markers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
    # Remove links but keep text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove images
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Collapse whitespace
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(root):
    """Load config.yml and return (parsed dict with defaults, defaults dict)."""
    config_path = root / "config.yml"
    defaults = {
        "wiki": {
            "title": "My Wiki",
            "description": "A LorEngine-powered wiki",
            "accent_color": "#7F77DD",
        },
        "ai": {
            "model": "claude-sonnet-4-6",
            "max_tokens": 1024,
            "enable_prompt_caching": True,
        },
        "search": {
            "max_results": 20,
            "excerpt_length": 160,
        },
        "github_pages": {
            "base_url": "",
        },
        "branding": {
            "favicon": "",
            "logo": "",
        },
        "pages_dir": "pages",
        "github": {
            "repo": "",
        },
    }

    if not config_path.exists():
        print("Warning: config.yml not found, using defaults")
        return defaults, defaults

    raw = config_path.read_text(encoding="utf-8")
    parsed = parse_yaml(raw)

    # Merge parsed over defaults
    for section, section_defaults in defaults.items():
        if section not in parsed:
            parsed[section] = section_defaults
        elif isinstance(section_defaults, dict):
            for key, val in section_defaults.items():
                if key not in parsed[section]:
                    parsed[section][key] = val

    return parsed, defaults


def validate_config(parsed, defaults):
    """Warn on unknown top-level config keys."""
    valid_keys = set(defaults.keys())
    for key in parsed.keys():
        if key not in valid_keys:
            print(f"Warning: unknown config key '{key}' (not in defaults)")


# ---------------------------------------------------------------------------
# Hierarchy and backlinks
# ---------------------------------------------------------------------------

def compute_hierarchy(entries):
    """Build parent/child relationships from frontmatter 'parent' slug field.

    Each page may set parent: <slug> in frontmatter. The slug is the filename
    stem (e.g. 'getting-started' for pages/getting-started.md).
    Resolves slug references to full IDs stored in the search index.
    """
    slug_map = {entry["slug"]: entry["id"] for entry in entries}

    for entry in entries:
        parent_slug = entry.pop("parent_slug", "")
        if parent_slug and parent_slug in slug_map:
            entry["parent"] = slug_map[parent_slug]
        else:
            if parent_slug:
                print(f"Warning: '{entry['id']}' references unknown parent slug '{parent_slug}'")
            entry["parent"] = None
        entry["children"] = []

    id_map = {entry["id"]: entry for entry in entries}
    for entry in entries:
        if entry["parent"] and entry["parent"] in id_map:
            id_map[entry["parent"]]["children"].append(entry["id"])

    return entries


def compute_backlinks(entries, pages_dir="pages"):
    """Scan all doc bodies for markdown links and populate backlinks.

    Looks for [text](pages/...) patterns and adds referencing doc IDs to backlinks.
    """
    # Create a lookup map
    id_map = {entry["id"]: entry for entry in entries}

    # Initialize backlinks list for all entries
    for entry in entries:
        entry["backlinks"] = []

    prefix = pages_dir.rstrip("/") + "/"

    # Scan each doc's body for links
    for entry in entries:
        # Find all markdown links: [text](path)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", entry["body"])
        for _, link_target in links:
            # Normalize path (remove leading ./ and trailing /)
            normalized = link_target.strip("./").rstrip("/")

            # Check if this is a doc link (starts with the pages dir)
            if normalized.startswith(prefix):
                # Make sure it has .md extension
                if not normalized.endswith(".md"):
                    normalized = normalized + ".md"

                # If target exists, add this doc to its backlinks
                if normalized in id_map:
                    id_map[normalized]["backlinks"].append(entry["id"])

    return entries


# ---------------------------------------------------------------------------
# Search index generation
# ---------------------------------------------------------------------------

# Pages excluded from the search index (reference artifacts, not content).
# These are served as static files but not indexed or shown in navigation.
EXCLUDED_FROM_INDEX = {"brief-example.md"}


def build_search_index(root, pages_dir="pages"):
    """Walk the pages directory and build the search index entries.

    Validates slug uniqueness (hard exit on duplicate) and title uniqueness (soft warn).
    Extracts slug (filename stem), sort_order, and parent_slug from frontmatter.
    """
    docs_dir = root / pages_dir
    if not docs_dir.exists():
        print(f"Warning: {pages_dir}/ directory not found")
        return []

    entries = []
    slug_seen = {}    # slug -> rel_path, hard-fail on duplicate
    title_seen = {}   # title_lower -> rel_path, soft-warn on duplicate

    for md_path in sorted(docs_dir.rglob("*.md")):
        rel_path = md_path.relative_to(root).as_posix()
        slug = md_path.stem  # filename stem = slug (e.g. "getting-started")

        if md_path.name in EXCLUDED_FROM_INDEX:
            continue

        # Hard fail: duplicate slug
        if slug in slug_seen:
            print(f"ERROR: Duplicate slug '{slug}' in {rel_path} (already defined by {slug_seen[slug]})")
            sys.exit(1)
        slug_seen[slug] = rel_path

        text = md_path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        if metadata is None or "title" not in metadata:
            print(f"Warning: skipping {rel_path} — missing title in frontmatter")
            continue

        # Soft warn: duplicate title
        title_key = metadata["title"].lower()
        if title_key in title_seen:
            print(f"Warning: duplicate title '{metadata['title']}' in {rel_path} (also in {title_seen[title_key]})")
        title_seen[title_key] = rel_path

        headings = extract_headings(body)
        plain_body = strip_markdown(body)
        excerpt = plain_body[:300]

        entry = {
            "id": rel_path,
            "slug": slug,
            "title": metadata.get("title", ""),
            "sort_order": int(metadata.get("sort_order", 100)),
            "parent_slug": str(metadata.get("parent", "")).strip(),
            "tags": metadata.get("tags", []),
            "status": metadata.get("status", "draft"),
            "last_updated": str(metadata.get("last-updated", "")),
            "file_mtime": md_path.stat().st_mtime,
            "headings": headings,
            "excerpt": excerpt,
            "body": plain_body,
        }
        entries.append(entry)

    return entries


# ---------------------------------------------------------------------------
# Site assembly
# ---------------------------------------------------------------------------

def assemble_site(root, config, search_index):
    """Copy wiki templates + docs into _site/, inject config values."""
    site_dir = root / "_site"

    # Clean previous build
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir()

    wiki_dir = root / "wiki"
    pages_dir_name = config["pages_dir"]
    docs_dir = root / pages_dir_name

    # Copy wiki files into _site/
    if wiki_dir.exists():
        shutil.copytree(wiki_dir, site_dir, dirs_exist_ok=True)

    # Copy pages dir into _site/{pages_dir}/
    if docs_dir.exists():
        shutil.copytree(docs_dir, site_dir / pages_dir_name)

    # Copy {pages_dir}/assets/ into _site/assets/ if it exists
    assets_dir = docs_dir / "assets" if docs_dir.exists() else None
    if assets_dir and assets_dir.exists():
        shutil.copytree(assets_dir, site_dir / "assets")

    # Write search_index.json into _site/
    index_path = site_dir / "search_index.json"
    index_path.write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Build replacement map from config
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    replacements = {
        "{{WIKI_TITLE}}": str(config["wiki"]["title"]),
        "{{WIKI_DESCRIPTION}}": str(config["wiki"]["description"]),
        "{{ACCENT_COLOR}}": str(config["wiki"]["accent_color"]),
        "{{AI_MODEL}}": str(config["ai"]["model"]),
        "{{AI_MAX_TOKENS}}": str(config["ai"]["max_tokens"]),
        "{{AI_ENABLE_PROMPT_CACHING}}": str(config["ai"]["enable_prompt_caching"]).lower(),
        "{{BASE_URL}}": str(config["github_pages"]["base_url"]),
        "{{SEARCH_MAX_RESULTS}}": str(config["search"]["max_results"]),
        "{{SEARCH_EXCERPT_LENGTH}}": str(config["search"]["excerpt_length"]),
        "{{ANTHROPIC_API_KEY}}": api_key,
        "{{BRANDING_FAVICON}}": str(config["branding"].get("favicon", "")),
        "{{BRANDING_LOGO}}": str(config["branding"].get("logo", "")),
        "{{GITHUB_REPO}}": str(config.get("github", {}).get("repo", "")),
    }

    # Inject into HTML and JS files (recursive)
    for f in site_dir.rglob("*.html"):
        content = f.read_text(encoding="utf-8")
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        f.write_text(content, encoding="utf-8")
    for f in site_dir.rglob("*.js"):
        content = f.read_text(encoding="utf-8")
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        f.write_text(content, encoding="utf-8")
    for f in site_dir.rglob("*.css"):
        content = f.read_text(encoding="utf-8")
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        f.write_text(content, encoding="utf-8")

    # Copy Decap CMS config into _site/admin/
    admin_dir = site_dir / "admin"
    admin_dir.mkdir(exist_ok=True)
    decap_config = root / "decap.yml"
    if decap_config.exists():
        decap_content = decap_config.read_text(encoding="utf-8")
        github_repo = str(config.get("github", {}).get("repo", ""))
        decap_content = decap_content.replace("{{GITHUB_REPO}}", github_repo)
        (admin_dir / "config.yml").write_text(decap_content, encoding="utf-8")

    return site_dir


# ---------------------------------------------------------------------------
# Auto-timestamp helpers
# ---------------------------------------------------------------------------

def load_content_hashes(root):
    """Load content_hashes.json if it exists."""
    path = root / "content_hashes.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def update_frontmatter_field(text, field, value):
    """Surgically update one field in YAML frontmatter without re-serializing."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    fm_text = text[3:end]
    body = text[end:]
    updated, count = re.subn(
        rf'^({re.escape(field)}\s*:).*$',
        rf'\1 {value}',
        fm_text,
        flags=re.MULTILINE
    )
    if count == 0:
        updated = fm_text.rstrip() + f'\n{field}: {value}\n'
    return f"---{updated}{body}"


def auto_update_timestamps(root, entries, pages_dir="pages"):
    """Compare body content hashes; rewrite last-updated frontmatter if changed."""
    stored = load_content_hashes(root)
    new_hashes = {}
    updated_count = 0

    for entry in entries:
        page_id = entry["id"]
        body_hash = hashlib.sha256(entry["body"].encode()).hexdigest()[:16]
        new_hashes[page_id] = body_hash

        if stored.get(page_id) != body_hash:
            today = datetime.date.today().isoformat()
            md_path = root / page_id
            original = md_path.read_text(encoding="utf-8")
            patched = update_frontmatter_field(original, "last-updated", today)
            if patched != original:
                md_path.write_text(patched, encoding="utf-8")
                entry["last_updated"] = today
                updated_count += 1

    (root / "content_hashes.json").write_text(
        json.dumps(new_hashes, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if updated_count:
        print(f"  Auto-updated last-updated on {updated_count} page(s)")
    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).resolve().parent

    print("LorEngine build starting...")

    # 1. Load config
    config, defaults = load_config(root)
    validate_config(config, defaults)
    print(f"  Wiki: {config['wiki']['title']}")

    # 2. Build search index
    pages_dir = config["pages_dir"]
    search_index = build_search_index(root, pages_dir)
    print(f"  Indexed {len(search_index)} document(s)")

    # 3. Auto-update timestamps and compute hierarchy/backlinks
    search_index = auto_update_timestamps(root, search_index, pages_dir)
    search_index = compute_hierarchy(search_index)
    search_index = compute_backlinks(search_index, pages_dir)
    print(f"  Computed hierarchy and backlinks")

    # 4. Write search_index.json to repo root (committed artifact)
    index_path = root / "search_index.json"
    index_path.write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  Wrote {index_path}")

    # 5. Assemble _site/
    site_dir = assemble_site(root, config, search_index)
    print(f"  Assembled site in {site_dir}")

    print("Build complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
