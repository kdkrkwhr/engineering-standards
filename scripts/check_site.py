"""Allow only the reviewed wiki and optional code-only Graphify artifact."""

import argparse
import json
from pathlib import Path
import re


EXPECTED = {"index.html", "wiki.md"}


def check(directory: Path, revision: str, graphify: bool = False) -> list[str]:
    errors = []
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        errors.append("invalid revision")
    if not directory.is_dir() or directory.is_symlink():
        return errors + ["missing or linked site directory"]
    files = {path.relative_to(directory).as_posix() for path in directory.rglob("*")}
    expected = set(EXPECTED)
    if graphify:
        index = directory / "wiki/graphify/index.json"
        try:
            pages = json.loads(index.read_text(encoding="utf-8"))
            names = [Path(item["url"]).name for item in pages]
            if not names or len(names) != len(set(names)) or "index.html" not in names or any(
                item["url"] != "./" + name or not re.fullmatch(r"[\w.·-]+\.html", name)
                for item, name in zip(pages, names)
            ):
                raise ValueError("invalid Graphify page names")
            expected.update({"architecture", "wiki", "wiki/graphify", "wiki/graphify/index.json"})
            expected.update({f"wiki/graphify/{name}" for name in names})
            expected.update({f"wiki/graphify/{name[:-5]}.md" for name in names})
            expected.update({f"architecture/{name}" for name in ("index.html", "graph.json", "graph.html", "GRAPH_REPORT.md", "metadata.json")})
        except (OSError, ValueError, KeyError, TypeError):
            errors.append("invalid Graphify index")
    if files != expected:
        errors.append(f"unexpected artifact members: {sorted(files ^ expected)}")
    for name in files:
        path = directory / name
        if path.is_symlink() or name.startswith(".") or "/." in name:
            errors.append(f"linked or hidden artifact member: {name}")
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
        for label in ("Java", "Python", "Dart", "C#", "TypeScript", "Spring Boot"):
            if label not in content:
                errors.append(f"missing selected-language or framework navigation: {label}")
    if graphify and "architecture/metadata.json" in files:
        metadata = json.loads((directory / "architecture/metadata.json").read_text(encoding="utf-8"))
        if metadata.get("revision") != revision or metadata.get("mode") != "code-only; LLM disabled":
            errors.append("Graphify provenance does not match revision or mode")
        for name in files:
            path = directory / name
            if path.is_file():
                content = path.read_text(encoding="utf-8")
                if re.search(r"/Users/|/home/runner/|standards-graph-|(?<![A-Za-z])[A-Za-z]:[\\/]", content):
                    errors.append(f"non-portable path in artifact: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--graphify", action="store_true")
    args = parser.parse_args()
    errors = check(args.directory, args.revision, args.graphify)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Pages artifact allowlist, navigation and revision OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
