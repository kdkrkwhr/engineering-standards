"""Check local Markdown links and a few structural mistakes without dependencies."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6} +\S")


def check(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        errors.append(f"{path.relative_to(ROOT)}: missing first-level title")

    fence_open = False
    for number, line in enumerate(lines, start=1):
        if line.startswith("```"):
            fence_open = not fence_open
        if fence_open or line.startswith("```"):
            continue
        for match in LINK.finditer(line):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}:{number}: broken link {target}")

    if fence_open:
        errors.append(f"{path.relative_to(ROOT)}: unclosed code fence")
    if not any(HEADING.match(line) for line in lines):
        errors.append(f"{path.relative_to(ROOT)}: missing heading")
    return errors


def main() -> int:
    generated = {".site-build", ".wiki-cache", "graphify-out"}
    paths = sorted(path for path in ROOT.rglob("*.md") if not generated.intersection(path.relative_to(ROOT).parts))
    errors = [error for path in paths for error in check(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(paths)} Markdown files: links and structure OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
