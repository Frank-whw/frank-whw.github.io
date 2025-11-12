import os
import re
import logging

import yaml
from jinja2 import Template

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files

from utils.toc import get_statistics, get_update_time

enabled = os.getenv("TOC", "1") == "1" or os.getenv("FULL", "0") == "true"
logger = logging.getLogger("mkdocs.hooks.toc")

if enabled:
    logger.info("hook - toc is loaded and enabled")
else:
    logger.info("hook - toc is disabled")

HOOKS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(HOOKS_DIR, "templates/toc.html")
IGNORE_PATH = os.path.join(HOOKS_DIR, "..", ".ignored-commits")

with open(TEMPLATE_DIR, "r", encoding="utf-8") as file:
    TEMPLATE = file.read()

# IGNORE_COMMITS = [
#     {"cs/system/cs1/topic1.md": "859970b504aa527030420ff9fbfffdb1b62d71f1"},
# ]

if os.path.exists(IGNORE_PATH):
    with open(IGNORE_PATH, "r", encoding="utf-8") as file:
        IGNORE_COMMITS = [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]
else:
    IGNORE_COMMITS = []
    logger.info(
        "hook - toc: ignore commits file not found at %s; proceeding without ignore rules",
        IGNORE_PATH,
    )

def on_page_markdown(
    markdown: str, page: Page, config: MkDocsConfig, files: Files, **kwargs
) -> str:
    if not enabled:
        return markdown
    if "{{ BEGIN_TOC }}" not in markdown or "{{ END_TOC }}" not in markdown:
        return markdown
    toc_yml = markdown.split("{{ BEGIN_TOC }}")[1].split("{{ END_TOC }}")[0]
    toc = yaml.load(toc_yml, Loader=yaml.FullLoader)
    toc_items = _get_toc_items(toc, os.path.dirname(page.file.abs_src_path))
    toc_html = Template(TEMPLATE).render(items=toc_items)
    markdown = re.sub(
        r"\{\{ BEGIN_TOC \}\}.*\{\{ END_TOC \}\}",
        toc_html,
        markdown,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return markdown


def _get_toc_items(toc: dict, base: str) -> list:
    def _flatten_entries(entries, base, prefix=""):
        flattened = []
        for node in entries:
            if isinstance(node, str):
                link = node
                name = os.path.basename(node.rstrip("/"))
                title = prefix.rstrip("/") if prefix else os.path.splitext(name)[0]
                detail = {
                    "title": title,
                    "link": link,
                }
                detail["words"], detail["codes"], detail["read_time"] = get_statistics(
                    link, base
                )
                detail["update_time"] = get_update_time(link, base, IGNORE_COMMITS)
                flattened.append(detail)
            elif isinstance(node, dict):
                k = list(node.keys())[0]
                sk = str(k)
                v = node[k]
                if k == "index":
                    if prefix:
                        link = v
                        title = prefix.rstrip("/")
                        detail = {
                            "title": title,
                            "link": link,
                        }
                        detail["words"], detail["codes"], detail["read_time"] = get_statistics(
                            link, base
                        )
                        detail["update_time"] = get_update_time(link, base, IGNORE_COMMITS)
                        flattened.append(detail)
                    continue
                if isinstance(v, list):
                    subprefix = f"{prefix}{sk}/" if prefix else f"{sk}/"
                    flattened.extend(_flatten_entries(v, base, subprefix))
                else:
                    link = v
                    title = f"{prefix}{sk}" if prefix else sk
                    detail = {
                        "title": title,
                        "link": link,
                    }
                    detail["words"], detail["codes"], detail["read_time"] = get_statistics(
                        link, base
                    )
                    detail["update_time"] = get_update_time(link, base, IGNORE_COMMITS)
                    if "🔒" in sk:
                        detail["lock"] = True
                    flattened.append(detail)
        return flattened

    ret = []
    for i, part in enumerate(toc):
        item = {}
        item["n"] = i
        title = list(part.keys())[0]
        item["title"] = str(title)
        entries = part[title]
        index_link = None
        filtered = []
        for d in entries:
            if isinstance(d, dict) and "index" in d:
                index_link = d["index"]
            else:
                filtered.append(d)
        details = _flatten_entries(filtered, base)
        details.sort(key=lambda x: x["update_time"], reverse=True)
        item["contents"] = details
        if index_link:
            item["link"] = index_link
        ret.append(item)
    return ret
