#!/usr/bin/env python3
"""Lorengine build script — generates search_index.json and assembles _site/.

Stdlib only (Python 3.11+). No pip dependencies.
"""

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
            "description": "A Lorengine-powered wiki",
            "accent_color": "#7F77DD",
        },
        "ai": {
            "model": "claude-sonnet-4-6",
            "system_prompt_file": "CLAUDE.local.md",
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
    """Build parent/child relationships from folder structure.

    For a doc at docs/a/b/c.md, parent is docs/a/b.md if it exists.
    Adds 'parent' (None for top-level) and 'children' (list of doc IDs) to each entry.
    """
    # Create a lookup map: path -> entry
    id_map = {entry["id"]: entry for entry in entries}

    for entry in entries:
        doc_path = Path(entry["id"])

        # Compute parent: remove filename, check if a .md exists at that level
        parent_path = doc_path.parent
        potential_parent = parent_path / parent_path.name / ".md" if parent_path.name else None

        # Actually, simpler: for docs/a/b/c.md, parent is docs/a/b.md
        # Get the parent folder path and construct the parent doc path
        doc_parts = Path(entry["id"]).parts  # e.g., ('docs', 'a', 'b', 'c.md')

        if len(doc_parts) > 2:  # More than just 'docs/file.md'
            # Parent is at same folder level with folder name as .md
            parent_id = str(Path(*doc_parts[:-1]).with_name(doc_parts[-2] + ".md")).replace("\\", "/")
            entry["parent"] = parent_id if parent_id in id_map else None
        else:
            entry["parent"] = None

        # Initialize children list
        entry["children"] = []

    # Populate children
    for entry in entries:
        if entry["parent"]:
            parent_entry = id_map.get(entry["parent"])
            if parent_entry:
                parent_entry["children"].append(entry["id"])

    return entries


def compute_backlinks(entries):
    """Scan all doc bodies for markdown links and populate backlinks.

    Looks for [text](docs/...) patterns and adds referencing doc IDs to backlinks.
    """
    # Create a lookup map
    id_map = {entry["id"]: entry for entry in entries}

    # Initialize backlinks list for all entries
    for entry in entries:
        entry["backlinks"] = []

    # Scan each doc's body for links
    for entry in entries:
        # Find all markdown links: [text](path)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", entry["body"])
        for _, link_target in links:
            # Normalize path (remove leading ./ and trailing /)
            normalized = link_target.strip("./").rstrip("/")

            # Check if this is a doc link (starts with 'docs/')
            if normalized.startswith("docs/"):
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

def build_search_index(root):
    """Walk docs/ and build the search index entries."""
    docs_dir = root / "docs"
    if not docs_dir.exists():
        print("Warning: docs/ directory not found")
        return []

    entries = []
    for md_path in sorted(docs_dir.rglob("*.md")):
        rel_path = md_path.relative_to(root).as_posix()
        text = md_path.read_text(encoding="utf-8")

        metadata, body = parse_frontmatter(text)
        if metadata is None or "title" not in metadata:
            print(f"Warning: skipping {rel_path} — missing title in frontmatter")
            continue

        headings = extract_headings(body)
        plain_body = strip_markdown(body)
        excerpt = plain_body[:300]

        entry = {
            "id": rel_path,
            "title": metadata.get("title", ""),
            "tags": metadata.get("tags", []),
            "status": metadata.get("status", "draft"),
            "last_updated": str(metadata.get("last-updated", "")),
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
    docs_dir = root / "docs"

    # Copy wiki files into _site/
    if wiki_dir.exists():
        for f in wiki_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, site_dir / f.name)

    # Copy docs/ into _site/docs/
    if docs_dir.exists():
        shutil.copytree(docs_dir, site_dir / "docs")

    # Copy docs/assets/ into _site/assets/ if it exists
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
        "{{AI_SYSTEM_PROMPT_FILE}}": str(config["ai"]["system_prompt_file"]),
        "{{AI_ENABLE_PROMPT_CACHING}}": str(config["ai"]["enable_prompt_caching"]).lower(),
        "{{BASE_URL}}": str(config["github_pages"]["base_url"]),
        "{{SEARCH_MAX_RESULTS}}": str(config["search"]["max_results"]),
        "{{SEARCH_EXCERPT_LENGTH}}": str(config["search"]["excerpt_length"]),
        "{{ANTHROPIC_API_KEY}}": api_key,
        "{{BRANDING_FAVICON}}": str(config["branding"].get("favicon", "")),
        "{{BRANDING_LOGO}}": str(config["branding"].get("logo", "")),
    }

    # Inject into HTML and JS files
    for f in site_dir.iterdir():
        if f.is_file() and f.suffix in (".html", ".js", ".css"):
            content = f.read_text(encoding="utf-8")
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            f.write_text(content, encoding="utf-8")

    return site_dir


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).resolve().parent

    print("Lorengine build starting...")

    # 1. Load config
    config, defaults = load_config(root)
    validate_config(config, defaults)
    print(f"  Wiki: {config['wiki']['title']}")

    # 2. Build search index
    search_index = build_search_index(root)
    print(f"  Indexed {len(search_index)} document(s)")

    # 3. Compute hierarchy and backlinks
    search_index = compute_hierarchy(search_index)
    search_index = compute_backlinks(search_index)
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
