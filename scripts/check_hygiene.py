"""Check Git's index for obvious unsafe paths and secret shapes; never print values."""

import argparse
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Optional


LIMIT = 2 * 1024 * 1024
GENERATED_DIRS = {
    "__pycache__", ".gradle", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".site-build", ".wiki-cache", ".venv", "build", "coverage", "dist", "graphify-out", "logs", "node_modules", "target",
}
SECRET_SHAPES = (
    ("private-key header", re.compile(rb"-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY-----")),
    ("AWS key ID shape", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token shape", re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("API key shape", re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    (
        "long credential assignment",
        re.compile(rb"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{24,}"),
    ),
)


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError("Git index could not be read")
    return result.stdout


def unsafe_path(path: str) -> Optional[str]:
    parts = [part.lower() for part in PurePosixPath(path).parts]
    name = parts[-1]
    if any(part in GENERATED_DIRS for part in parts[:-1]):
        return "generated/cache directory"
    if name in {".ds_store", "thumbs.db"} or name.endswith((".pyc", ".pyo", ".swp")):
        return "OS/cache file"
    if name == ".env" or (name.startswith(".env.") and not name.endswith(".example")):
        return "local environment file"
    if name in {"id_rsa", "id_ed25519"} or name.endswith((".p12", ".pfx", ".keystore")):
        return "private key or keystore path"
    if len(parts) >= 2 and parts[-2:] == [".aws", "credentials"]:
        return "credential store path"
    return None


def check(root: Path, scope: str) -> tuple[int, list[tuple[str, str]]]:
    if scope == "staged":
        names = git(root, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR")
    else:
        names = git(root, "ls-files", "-z")
    paths = sorted({os.fsdecode(name) for name in names.split(b"\0") if name})
    findings: list[tuple[str, str]] = []
    for path in paths:
        kind = unsafe_path(path)
        if kind:
            findings.append((path, kind))
        try:
            size = int(git(root, "cat-file", "-s", f":{path}").strip())
            if size > LIMIT:
                findings.append((path, "over 2 MiB; content not fully checked"))
                continue
            blob = git(root, "show", f":{path}")
        except (RuntimeError, ValueError):
            findings.append((path, "index blob could not be checked"))
            continue
        for label, pattern in SECRET_SHAPES:
            if pattern.search(blob):
                findings.append((path, label))
    return len(paths), findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--staged", action="store_true", help="check staged additions and modifications in the index")
    choice.add_argument("--tracked", action="store_true", help="check every tracked path in the index")
    args = parser.parse_args()
    try:
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
        scope = "staged" if args.staged else "tracked"
        count, findings = check(root, scope)
    except RuntimeError:
        print("Git repository or index unavailable", file=sys.stderr)
        return 2
    for path, kind in findings:
        print(f"{path}: {kind}", file=sys.stderr)
    print(f"Checked {count} {scope} index files; findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
