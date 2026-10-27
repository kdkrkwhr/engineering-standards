"""Ensure only two expected public files enter the Pages artifact."""

import argparse
from pathlib import Path
import re


EXPECTED = {"index.html", "wiki.md"}


def check(directory: Path, revision: str) -> list[str]:
    errors = []
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        errors.append("invalid revision")
    if not directory.is_dir() or directory.is_symlink():
        return errors + ["missing or linked site directory"]
    files = {path.relative_to(directory).as_posix() for path in directory.rglob("*")}
    if files != EXPECTED:
        errors.append(f"unexpected artifact members: {sorted(files ^ EXPECTED)}")
    for filename in EXPECTED & files:
        path = directory / filename
        if not path.is_file() or path.is_symlink():
            errors.append(f"invalid artifact file: {filename}")
            continue
        content = path.read_text(encoding="utf-8")
        if revision not in content:
            errors.append(f"missing source revision: {filename}")
        if "https://github.com/kdkrkwhr/engineering-standards/blob/" + revision not in content:
            errors.append(f"missing pinned rule links: {filename}")
    html = directory / "index.html"
    if html.is_file():
        content = html.read_text(encoding="utf-8")
        for required in ('name="viewport"', 'id="search"', 'href="./wiki.md"'):
            if required not in content:
                errors.append(f"missing mobile/navigation element: {required}")
        if 'href="/' in content or 'src="/' in content:
            errors.append("root-absolute asset path breaks project site base path")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    errors = check(args.directory, args.revision)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Pages artifact contains only index.html and wiki.md; paths and revision OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
