import os
import re
import time
from typing import Tuple
from git import Repo


def _words_count(markdown: str) -> Tuple[int, int, int]:
    chinese, english, codes = _split_markdown(markdown)
    code_lines = 0
    words = len(chinese) + len(english.split())
    for code in codes:
        code_lines += max(len(code.splitlines()) - 2, 0)
    read_time = round(words / 300 + code_lines / 80)
    return words, code_lines, read_time


def _split_markdown(markdown: str) -> Tuple[str, str, list]:
    markdown, codes = _clean_markdown(markdown)
    chinese = "".join(re.findall(r"[\u4e00-\u9fa5]", markdown))
    english = " ".join(re.findall(r"[a-zA-Z0-9]*?(?![a-zA-Z0-9])", markdown))
    return chinese, english, codes


def _clean_markdown(markdown: str) -> Tuple[str, list]:
    codes = re.findall(r"```[^\n].*?```", markdown, re.S)
    markdown = re.sub(r"```[^\n].*?```", "", markdown, flags=re.DOTALL | re.MULTILINE)
    markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL | re.MULTILINE)
    markdown = markdown.replace("\t", "    ")
    markdown = re.sub(r"[ ]{2,}", "    ", markdown)
    markdown = re.sub(r"^\[[^]]*\][^(].*", "", markdown, flags=re.MULTILINE)
    markdown = re.sub(r"{#.*}", "", markdown)
    markdown = markdown.replace("\n", " ")
    markdown = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", markdown)
    markdown = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", markdown)
    markdown = re.sub(r"</?[^>]*>", "", markdown)
    markdown = re.sub(r"[#*`~\-–^=<>+|/:]", "", markdown)
    markdown = re.sub(r"\[[0-9]*\]", "", markdown)
    markdown = re.sub(r"[0-9#]*\.", "", markdown)
    return markdown, codes


def get_statistics(path: str, base: str):
    words, codes, read_time = 0, 0, 0
    full = os.path.join(base, path)
    if os.path.exists(full):
        if os.path.isdir(full):
            for root, _dirs, files in os.walk(full):
                for file in files:
                    if file.endswith(".md"):
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            markdown = f.read()
                            w, c, r = _words_count(markdown)
                            words += w
                            codes += c
                            read_time += r
        else:
            # file may be non-md; if dir_toc points exactly to file
            if full.endswith(".md"):
                with open(full, "r", encoding="utf-8") as f:
                    markdown = f.read()
                    words, codes, read_time = _words_count(markdown)
    else:
        # try add .md
        candidate = full[:-1] + ".md" if full.endswith("/") else full + ".md"
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                markdown = f.read()
                words, codes, read_time = _words_count(markdown)
    return words, codes, read_time


_repo_cache = {}


def _get_repo(path: str) -> Repo | None:
    """Find git repo for path searching parent directories."""
    if path in _repo_cache:
        return _repo_cache[path]
    p = os.path.abspath(path)
    while True:
        if os.path.isdir(os.path.join(p, ".git")):
            try:
                repo = Repo(p)
                _repo_cache[path] = repo
                return repo
            except Exception:
                return None
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    return None


def get_update_time(path: str, base: str, ignore_commits: list[str]) -> int:
    repo = _get_repo(base)
    full = os.path.join(base, path)
    # normalize to file path if pointing to directory or missing .md
    if not os.path.exists(full):
        if full.endswith("/"):
            full = full[:-1] + ".md"
        else:
            full = full + ".md"

    try:
        if repo is None:
            ts = os.path.getmtime(full)
            return int(ts)
        rel = os.path.relpath(full, repo.working_tree_dir)
        for commit in repo.iter_commits(paths=rel, max_count=200):
            if commit.hexsha in ignore_commits:
                continue
            # Prefer integer unix timestamp from GitPython
            if hasattr(commit, "committed_date"):
                return int(commit.committed_date)
            else:
                dt = commit.committed_datetime
                return int(dt.timestamp())
        # fallback to mtime
        ts = os.path.getmtime(full)
        return int(ts)
    except Exception:
        try:
            ts = os.path.getmtime(full)
            return int(ts)
        except Exception:
            return 0