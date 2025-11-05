import os
import logging
from pathlib import Path
import fnmatch
import re
import yaml
from jinja2 import Template
from pathlib import Path

# ===== Module-level config for YAML TOC hook =====
HOOKS_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = HOOKS_DIR / "templates" / "toc.html"
IGNORED_COMMITS_FILE = HOOKS_DIR.parent / ".ignored-commits"

enabled = os.getenv("TOC", "1") == "1" or os.getenv("FULL", "0").lower() == "true"
logger = logging.getLogger("mkdocs.hooks.toc")

try:
    TEMPLATE_HTML = TEMPLATE_PATH.read_text(encoding="utf-8")
except Exception:
    TEMPLATE_HTML = "<div class=\"toc\"></div>"

try:
    IGNORE_COMMITS = [
        line.strip() for line in IGNORED_COMMITS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
except Exception:
    IGNORE_COMMITS = []

try:
    from .utils.toc import get_statistics, get_update_time  # relative import
except Exception:
    # Fallback stubs
    def get_statistics(path: str, base: str):
        return 0, 0, 0

    def get_update_time(path: str, base: str, ignore_commits: list[str]):
        p = Path(base)
        f = (p / path)
        if not f.exists() and not str(f).endswith(".md"):
            f = Path(str(f) + ".md")
        try:
            ts = f.stat().st_mtime
            from datetime import datetime
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "N/A"


def _read_front_matter_title(md_text: str) -> str | None:
    # Try YAML front matter: ---\n title: ... \n---
    if md_text.startswith("---\n"):
        end = md_text.find("\n---\n", 4)
        if end != -1:
            fm = md_text[4:end]
            m = re.search(r"^title:\s*(.+)$", fm, re.M)
            if m:
                return m.group(1).strip()
    return None


def _read_h1_title(md_text: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else None


def _strip_ext(name: str) -> str:
    return re.sub(r"\.md$", "", name)


def _numeric_key(name: str) -> tuple:
    # Sort like: 1.xxx.md, 02-foo.md, 9. bar.md → (num, name)
    m = re.match(r"^(\d+)[._\-\s]", name)
    if m:
        return (int(m.group(1)), name.lower())
    return (10**9, name.lower())


def define_env(env):
    """Register macros and page hooks for directory-based TOC and YAML-driven TOC block.

    Markdown usage:
      - Macro: {{ dir_toc(path='cs_base', depth=2, numbered=True, group_by_dir=True) }}
      - Placeholder: [[DIR_TOC|path=cs_base|depth=2|numbered|group]]
      - YAML TOC block:
        {{ BEGIN_TOC }}
        - Section:
            - index: cs_base/index.md
            - Title A: cs_base/foo.md
            - Title B: cs_base/bar/
        {{ END_TOC }}
    """

    docs_dir = Path(env.conf.get("docs_dir", "docs")).resolve()

    # hook enable switch
    enabled = os.getenv("TOC", "1") == "1" or os.getenv("FULL", "0").lower() == "true"
    logger = logging.getLogger("mkdocs.hooks.toc")
    logger.info("hook - toc is %s", "enabled" if enabled else "disabled")

    HOOKS_DIR = Path(__file__).resolve().parent
    TEMPLATE_PATH = HOOKS_DIR / "templates" / "toc.html"
    IGNORED_COMMITS_FILE = HOOKS_DIR.parent / ".ignored-commits"

    try:
        TEMPLATE_HTML = TEMPLATE_PATH.read_text(encoding="utf-8")
    except Exception:
        TEMPLATE_HTML = "<div class=\"toc\">{% for item in items %}<h3>{{ item.title }}</h3><ul>{% for d in item.contents %}<li><a href=\"{{ d.link }}\">{{ d.title }}</a> <small>字数 {{ d.words }} · 代码行 {{ d.codes }} · 预计阅读 {{ d.read_time }} 分钟 · 更新 {{ d.update_time }}</small></li>{% endfor %}</ul>{% endfor %}</div>"

    try:
        IGNORE_COMMITS = [
            line.strip() for line in IGNORED_COMMITS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    except Exception:
        IGNORE_COMMITS = []

    # Load ignore patterns from docs/.tocignore (one pattern per line)
    ignore_file = docs_dir / ".tocignore"
    ignore_patterns: list[str] = []
    if ignore_file.exists():
        for line in ignore_file.read_text(encoding="utf-8").splitlines():
            pat = line.strip()
            if pat and not pat.startswith("#"):
                ignore_patterns.append(pat)

    def _is_ignored(relpath: Path) -> bool:
        rp = relpath.as_posix()
        for pat in ignore_patterns:
            if fnmatch.fnmatch(rp, pat):
                return True
        return False

    def _read_title(path: Path) -> str:
        try:
            md_text = path.read_text(encoding="utf-8")
        except Exception:
            return _strip_ext(path.name)
        # Prefer front matter title, then H1, else filename
        return (
            _read_front_matter_title(md_text)
            or _read_h1_title(md_text)
            or _strip_ext(path.name)
        )

    def _collect_dir(path: Path, depth: int) -> dict:
        """Collect markdown files grouped by immediate subdirectory.
        Returns { group_name: [ (title, rel_link) ] }
        """
        data: dict[str, list[tuple[str, str]]] = {}
        base_rel_root = path.relative_to(docs_dir)

        # Files directly under path
        files = [p for p in path.glob("*.md") if p.name.lower() != "index.md"]
        files.sort(key=lambda p: _numeric_key(p.name))
        data[base_rel_root.as_posix()] = [
            (_read_title(p), base_rel_root.joinpath(p.name).as_posix()) for p in files
        ]

        if depth >= 2:
            for sub in sorted([d for d in path.iterdir() if d.is_dir()], key=lambda d: d.name.lower()):
                sub_rel = sub.relative_to(docs_dir).as_posix()
                if _is_ignored(sub.relative_to(docs_dir)):
                    continue
                sub_files = [p for p in sub.glob("*.md") if p.name.lower() != "index.md"]
                sub_files.sort(key=lambda p: _numeric_key(p.name))
                data[sub_rel] = [(_read_title(p), Path(sub_rel).joinpath(p.name).as_posix()) for p in sub_files]
        return data

    def _render_markdown(groups: dict, numbered: bool, group_by_dir: bool) -> str:
        lines: list[str] = []
        for group, items in groups.items():
            if group_by_dir:
                # Group heading (relative path as title)
                if items:
                    disp = Path(group).name if group else group
                    lines.append(f"### {disp}")
                    lines.append("")
            if numbered:
                for i, (title, link) in enumerate(items, 1):
                    lines.append(f"{i}. [{title}]({link})")
            else:
                for title, link in items:
                    lines.append(f"- [{title}]({link})")
            if items:
                lines.append("")
        return "\n".join(lines).strip()

    def dir_toc(path: str = ".", depth: int = 1, numbered: bool = False, group_by_dir: bool = True) -> str:
        base = (docs_dir / path).resolve()
        if not base.exists():
            return f"<!-- dir_toc: path '{path}' not found -->"
        groups = _collect_dir(base, depth=depth)
        # Filter by ignore patterns
        filtered = {}
        for g, items in groups.items():
            rel_g = Path(g)
            if _is_ignored(rel_g):
                continue
            filtered[g] = [(t, l) for (t, l) in items if not _is_ignored(Path(l))]
        return _render_markdown(filtered, numbered=numbered, group_by_dir=group_by_dir)

    env.macro(dir_toc)

    # ===== YAML TOC block rendering (TonyCrane-like) =====
    # Note: Current mkdocs-macros-plugin version does not expose a decorator for on_page_markdown.
    # YAML TOC blocks will not render until the plugin supports registration or we add a dedicated MkDocs plugin.
    logger.warning("YAML TOC hook not registered: mkdocs-macros-plugin lacks on_page_markdown decorator in this environment.")

def _get_toc_items(toc: list, base_dir: Path) -> list:
    items = []
    for i, part in enumerate(toc):
        # part is a dict: {"Section Title": [ {"index": "path"}, {"Item": "path"}, ... ]}
        section_title = list(part.keys())[0]
        item = {"n": i, "note": False}
        if "[note]" in section_title:
            item["note"] = True
            section_title = section_title.replace("[note]", "").strip()
        item["title"] = section_title
        details = []
        for d in part[ list(part.keys())[0] ]:
            key = list(d.keys())[0]
            value = d[key]
            if key == "index":
                item["link"] = value
                continue
            t = key
            detail = {"note": False, "lab": False, "lock": False}
            if "[note]" in t:
                detail["note"] = True
                t = t.replace("[note]", "")
            if "[lab]" in t:
                detail["lab"] = True
                t = t.replace("[lab]", "")
            if "🔒" in t:
                detail["lock"] = True
            detail["title"] = t.strip()
            detail["link"] = value
            w, c, r = get_statistics(value, str(base_dir))
            detail["words"], detail["codes"], detail["read_time"] = w, c, r
            detail["update_time"] = get_update_time(value, str(base_dir), IGNORE_COMMITS)
            details.append(detail)
        # sort by update_time desc (integer unix timestamp when available)
        try:
            details.sort(key=lambda x: int(x.get("update_time") or 0), reverse=True)
        except Exception:
            pass
        item["contents"] = details
        items.append(item)
    return items

def on_page_markdown(markdown: str, page, config, files, **kwargs):
    if not enabled:
        return markdown
    if "{{ BEGIN_TOC }}" not in markdown or "{{ END_TOC }}" not in markdown:
        return markdown
    try:
        toc_yml = markdown.split("{{ BEGIN_TOC }}", 1)[1].split("{{ END_TOC }}", 1)[0]
        toc = yaml.load(toc_yml, Loader=yaml.FullLoader)
        items = _get_toc_items(toc, Path(page.file.abs_src_path).parent)
        html = Template(TEMPLATE_HTML).render(items=items)
        new_md = re.sub(r"\{\{ BEGIN_TOC \}\}.*\{\{ END_TOC \}\}", html, markdown, flags=re.IGNORECASE | re.DOTALL)
        return new_md
    except Exception as e:
        logger.exception("toc: failed to render YAML TOC: %s", e)
        return markdown