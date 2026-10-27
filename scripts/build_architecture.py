"""Build a public, code-only Graphify snapshot from committed wiki tooling.

Graphify runs in the Pages job. This script never installs an agent skill, hook,
LLM backend, or persistent Mac tool.
"""

from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".graphify-build" / "graphify-out"
VERSION = "0.9.93"
SOURCES = (
    "scripts/build_wiki.py",
    "scripts/check_glossary.py",
    "scripts/check_site.py",
    "scripts/check_docs.py",
    "scripts/smoke_adoption.py",
)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def portable(value, scratch: Path):
    if isinstance(value, dict):
        return {key: portable(item, scratch) for key, item in value.items()}
    if isinstance(value, list):
        return [portable(item, scratch) for item in value]
    if isinstance(value, str):
        return value.replace(str(scratch).replace("\\", "/") + "/", "").replace(
            str(scratch) + "\\", ""
        ).replace(str(scratch), ".")
    return value


def main() -> None:
    cli = shutil.which("graphify")
    if not cli:
        raise SystemExit(f"graphifyy=={VERSION} is required in the build job")
    version = subprocess.check_output([cli, "--version"], text=True).strip()
    if version != f"graphify {VERSION}":
        raise SystemExit(f"Expected graphify {VERSION}; got {version}")
    revision = git("rev-parse", "HEAD").decode().strip()
    tracked = set(git("ls-tree", "-rz", "--name-only", revision).decode().split("\0"))
    if not set(SOURCES) <= tracked:
        raise SystemExit("Graphify source allowlist is not fully committed")
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit("Graphify output must start empty")
    OUT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(GRAPHIFY_BACKEND="none", GRAPHIFY_QUERY_LOG_DISABLE="1", GRAPHIFY_NO_TIPS="1", GRAPHIFY_NO_AUTO_REFRESH="1")
    with tempfile.TemporaryDirectory(prefix="standards-graph-") as temporary:
        source = Path(temporary) / "engineering-standards"
        for name in SOURCES:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git("show", f"{revision}:{name}"))
        subprocess.run(
            [cli, "extract", str(source), "--code-only", "--no-cluster", "--max-workers", "2"],
            cwd=source,
            env=env,
            check=True,
        )
        original = json.loads((source / "graphify-out" / "graph.json").read_text(encoding="utf-8"))
        graph = portable(original, source)
        if not graph.get("nodes") or not graph.get("links"):
            raise SystemExit("Graphify returned no code nodes or relations")
        if graph.get("graph", {}).get("schema_version") != 1:
            raise SystemExit("Unsupported Graphify graph schema")
        (OUT / "graph.json").write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [cli, "cluster-only", str(OUT.parent), "--graph", str(OUT / "graph.json"), "--no-label", "--no-viz"],
        cwd=ROOT,
        env=env,
        check=True,
    )
    graph = json.loads((OUT / "graph.json").read_text(encoding="utf-8"))
    analysis = json.loads((OUT / ".graphify_analysis.json").read_text(encoding="utf-8"))
    sources = {node["id"]: node.get("source_file", "") for node in graph["nodes"]}
    labels = {}
    for community, members in analysis["communities"].items():
        counts = Counter(sources.get(member, "") for member in members)
        counts.pop("", None)
        labels[community] = f"{counts.most_common(1)[0][0]} · {community}" if counts else f"Group {community}"
    labels_path = OUT / ".graphify_labels.json"
    labels_path.write_text(json.dumps(labels, ensure_ascii=False), encoding="utf-8")
    subprocess.run([cli, "export", "wiki", "--graph", str(OUT / "graph.json"), "--labels", str(labels_path)], cwd=ROOT, env=env, check=True)
    subprocess.run([cli, "export", "html", "--graph", str(OUT / "graph.json"), "--labels", str(labels_path), "--node-limit", "1000"], cwd=ROOT, env=env, check=True)
    if not (OUT / "wiki" / "index.md").is_file():
        raise SystemExit("Graphify did not produce its wiki index")
    metadata = {
        "revision": revision,
        "graphifyVersion": VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "mode": "code-only; LLM disabled",
        "files": list(SOURCES),
        "fileCount": len(SOURCES),
        "nodeCount": len(graph["nodes"]),
        "edgeCount": len(graph["links"]),
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    for path in [OUT / "graph.json", OUT / "graph.html", OUT / "GRAPH_REPORT.md", *(OUT / "wiki").glob("*.md")]:
        content = path.read_text(encoding="utf-8")
        if re.search(r"/Users/|/home/runner/|standards-graph-|(?<![A-Za-z])[A-Za-z]:[\\/]", content):
            raise SystemExit(f"Non-portable path in Graphify output: {path.name}")
    print(f"Graphify: {metadata['fileCount']} files, {metadata['nodeCount']} nodes, {metadata['edgeCount']} relations")


if __name__ == "__main__":
    main()
