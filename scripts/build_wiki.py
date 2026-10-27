"""Build the public site from reviewed terminology and optional code evidence."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import quote, unquote, urlsplit

from check_glossary import ROOT, SOURCE, PROFILE_SOURCE, validate


DOCS = (
    ("시작과 적용", "README.md"),
    ("공통 원칙", "standards/core.md"),
    ("명명", "standards/naming.md"),
    ("구조 선택", "standards/architecture.md"),
    ("API·DTO", "standards/api-dto.md"),
    ("트랜잭션", "standards/transactions.md"),
    ("에이전트 지침", "agents/implementation.md"),
    ("Java", "profiles/languages/java.md"),
    ("Python", "profiles/languages/python.md"),
    ("Dart", "profiles/languages/dart.md"),
    ("C#", "profiles/languages/csharp.md"),
    ("TypeScript", "profiles/languages/typescript.md"),
    ("Spring Boot 선택 프로필", "profiles/frameworks/spring-boot.md"),
    ("프로젝트 적용", "templates/AGENTS.md"),
)
STATUS = {"observed": "공개 코드에서 관찰", "proposed": "제안·추론", "confirmed": "표준에서 확정"}
RELATION_LABEL = {"may_call": "호출할 수 있음", "accepts": "입력으로 받음", "may_use": "사용할 수 있음"}
SITE = ROOT / "site"


def category(term: dict) -> str:
    return term["category"]


def graph_svg(data: dict) -> str:
    terms = [term for term in data["terms"] if term["category"] != "common"]
    positions = [(48, 48), (298, 48), (48, 208), (548, 48), (548, 208)]
    while len(positions) < len(terms):
        n = len(positions)
        positions.append((48 + n % 3 * 250, 368 + (n - 5) // 3 * 160))
    coordinates = {term["id"]: positions[i] for i, term in enumerate(terms)}
    height = max(y for _, y in positions[:len(terms)]) + 120
    edges = []
    for relation in data["relations"]:
        x1, y1 = coordinates[relation["from"]]
        x2, y2 = coordinates[relation["to"]]
        if y1 == y2:
            start, end = (x1 + 204, y1 + 36), (x2 - 9, y2 + 36)
        elif x1 == x2:
            start, end = (x1 + 102, y1 + 74), (x2 + 102, y2 - 9)
        else:
            start, end = (x1 + 204, y1 + 58), (x2 - 9, y2 + 22)
        edges.append(
            f'<line class="graph-edge" data-from="{relation["from"]}" data-to="{relation["to"]}" '
            f'x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" marker-end="url(#arrow)"/>'
        )
    nodes = []
    for term in terms:
        x, y = coordinates[term["id"]]
        nodes.append(f'''<a class="graph-node" data-node="{term['id']}" data-category="{category(term)}" href="#{term['id']}" aria-label="{escape(term['ko'], quote=True)} 상세 보기">
  <rect x="{x}" y="{y}" width="204" height="74" rx="12"/>
  <text class="node-title" x="{x + 15}" y="{y + 32}">{escape(term['ko'])}</text>
  <text class="node-sub" x="{x + 15}" y="{y + 55}">{escape(term['en'])}</text>
</a>''')
    return f'''<svg viewBox="0 0 800 {height}" role="img" aria-labelledby="graph-title graph-desc" xmlns="http://www.w3.org/2000/svg">
<title id="graph-title">스택별 용어 예시 관계 그래프</title><desc id="graph-desc">선은 수동으로 제안한 Spring 예시 관계입니다. 노드를 누르면 근거와 규칙을 볼 수 있습니다.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8"/></marker></defs>
{''.join(edges)}{''.join(nodes)}</svg>'''


def render(data: dict, revision: str, graph_metadata: dict | None = None) -> tuple[str, str]:
    base = f"https://github.com/kdkrkwhr/engineering-standards/blob/{revision}/"
    nav = "\n".join(f'<a href="{base}{path}">{escape(label)}</a>' for label, path in DOCS)
    cards = []
    markdown = ["# 용어 위키 (원본에서 생성)", "", f"원본: [공통 개념]({base}glossary/common.json) · [프로필별 관찰 예시]({base}glossary/profile-examples.json) · 표준 버전: `{revision}`", "", "이 문서는 원본 규칙을 재정의하지 않습니다. 관계의 ‘제안·추론’은 실제 코드 호출 그래프가 아닙니다.", ""]
    for term in data["terms"]:
        rule_url = base + term["related_rule"]
        source_url = term["source"]
        query = " ".join([term["id"], term["ko"], term["en"], term["meaning"], term["scope"], term["code_name_example"], *term["aliases"]]).lower()
        cards.append(f'''<article class="term-card" id="{term['id']}" tabindex="-1" data-search="{escape(query, quote=True)}" data-category="{category(term)}">
  <div class="term-meta"><span class="eyebrow">{escape(term['scope'])}</span><span class="badge">{escape(STATUS[term['status']])}</span></div>
  <h3>{escape(term['ko'])}<span>{escape(term['en'])}</span></h3>
  <p>{escape(term['meaning'])}</p>
  <dl><div><dt>표현 예시</dt><dd><code>{escape(term['code_name_example'])}</code></dd></div><div><dt>허용 별칭</dt><dd>{escape(', '.join(term['aliases']) or '없음')}</dd></div><div><dt>구분할 용어</dt><dd>{escape(', '.join(term['avoid_mixing']) or '없음')}</dd></div></dl>
  <div class="term-links"><a href="{escape(rule_url, quote=True)}">적용 규칙 ↗</a><a href="{escape(source_url, quote=True)}">{('표준 근거' if term['category'] == 'common' else '관찰 근거')} ↗</a></div>
</article>''')
        markdown.extend([f"## {term['ko']} · {term['en']}", "", f"상태: {STATUS[term['status']]} · 범위: {term['scope']}", "", term["meaning"], "", f"표현 예시: `{term['code_name_example']}` · 허용 별칭: {', '.join(term['aliases']) or '없음'} · 구분할 용어: {', '.join(term['avoid_mixing']) or '없음'}", "", f"[적용 규칙]({rule_url}) · [공개 근거]({source_url})", ""])
    relations = []
    names = {term["id"]: term["ko"] for term in data["terms"]}
    markdown.extend(["## 용어 관계", ""])
    for relation in data["relations"]:
        source, target = relation["from"], relation["to"]
        relation_label = RELATION_LABEL.get(relation["type"], relation["type"])
        relations.append(f'<button type="button" class="relation" data-from="{source}" data-to="{target}" data-from-label="{escape(names[source], quote=True)}" data-to-label="{escape(names[target], quote=True)}"><span>{escape(names[source])}</span><strong>{escape(relation_label)}</strong><span>{escape(names[target])}</span><em>{escape(STATUS[relation["status"]])}</em></button>')
        markdown.append(f"- [{source}](#{source}) → `{relation['type']}` → [{target}](#{target}) ({STATUS[relation['status']]})")
    template = (SITE / "index.template.html").read_text(encoding="utf-8")
    if graph_metadata:
        graphify_section = (
            f'<p>이 저장소의 공개 Python 검사·위키 생성 스크립트 {graph_metadata["fileCount"]}개를 '
            f'Graphify {escape(graph_metadata["graphifyVersion"])}의 로컬 코드 분석으로 읽었습니다. '
            f'{graph_metadata["nodeCount"]}개 코드 항목과 {graph_metadata["edgeCount"]}개 관계가 추출됐습니다. '
            '문서 의미 분석과 외부 LLM 호출은 실행하지 않았습니다.</p>'
            '<p><a href="./architecture/">코드 구조 지도 보기 ↗</a> · '
            '<a href="./wiki/graphify/index.html">Graphify 자동 문서 읽기 ↗</a></p>'
        )
    else:
        graphify_section = "<p>Graphify 코드 분석은 이 로컬 위키 빌드에 포함되지 않았습니다.</p>"
    substitutions = {
        "__STYLE__": (SITE / "style.css").read_text(encoding="utf-8"),
        "__SCRIPT__": (SITE / "app.js").read_text(encoding="utf-8"),
        "__REVISION__": revision,
        "__SOURCE_URL__": base + "glossary/common.json",
        "__PROFILE_SOURCE_URL__": base + "glossary/profile-examples.json",
        "__REVISION_URL__": base,
        "__NAV__": nav,
        "__CARDS__": "\n".join(cards),
        "__GRAPH__": graph_svg(data),
        "__RELATIONS__": "\n".join(relations),
        "__TERM_COUNT__": str(len(data["terms"])),
        "__RELATION_COUNT__": str(len(data["relations"])),
        "__AUTO_SECTION__": graphify_section,
        "__ARCH_LINK__": '<a href="./architecture/">Graphify 구조 지도 ↗</a>' if graph_metadata else "",
    }
    for token, value in substitutions.items():
        template = template.replace(token, value)
    if re.search(r"__[A-Z_]+__", template):
        raise ValueError("unresolved site template token")
    return template, "\n".join(markdown) + "\n"


def publish_graphify(out: Path, graph_dir: Path, revision: str) -> None:
    """Render only reviewed Graphify files into the static Pages artifact."""
    from markdown_it import MarkdownIt

    metadata = json.loads((graph_dir / "metadata.json").read_text(encoding="utf-8"))
    graph = json.loads((graph_dir / "graph.json").read_text(encoding="utf-8"))
    if metadata.get("revision") != revision or metadata.get("mode") != "code-only; LLM disabled":
        raise ValueError("Graphify evidence does not match this source commit and code-only policy")
    if graph.get("graph", {}).get("schema_version") != 1 or not graph.get("nodes") or not graph.get("links"):
        raise ValueError("Graphify graph is missing expected schema, nodes, or links")
    if len(graph["nodes"]) != metadata["nodeCount"] or len(graph["links"]) != metadata["edgeCount"]:
        raise ValueError("Graphify metadata counts differ from graph.json")
    allowed = ("graph.json", "graph.html", "GRAPH_REPORT.md", "metadata.json")
    architecture = out / "architecture"
    architecture.mkdir()
    for name in allowed:
        source = graph_dir / name
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"missing or linked Graphify output: {name}")
        shutil.copyfile(source, architecture / name)
    source_links = "".join(
        f'<li><a href="https://github.com/kdkrkwhr/engineering-standards/blob/{revision}/{quote(name)}">{escape(name)}</a></li>'
        for name in metadata["files"]
    )
    template = (SITE / "architecture.template.html").read_text(encoding="utf-8")
    replacements = {
        "__STYLE__": (SITE / "style.css").read_text(encoding="utf-8"),
        "__REVISION__": revision,
        "__GRAPHIFY_VERSION__": escape(metadata["graphifyVersion"]),
        "__FILE_COUNT__": str(metadata["fileCount"]),
        "__NODE_COUNT__": str(metadata["nodeCount"]),
        "__EDGE_COUNT__": str(metadata["edgeCount"]),
        "__SOURCE_LIST__": source_links,
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    (architecture / "index.html").write_text(template, encoding="utf-8")

    generated = sorted((graph_dir / "wiki").glob("*.md"))
    if not generated or not any(path.name == "index.md" for path in generated):
        raise ValueError("Graphify wiki index was not generated")
    names = {path.name for path in generated}
    parser = MarkdownIt("commonmark", {"html": False}).enable("table")
    destination = out / "wiki" / "graphify"
    destination.mkdir(parents=True)
    site_template = (SITE / "graphify.template.html").read_text(encoding="utf-8")
    pages = []
    for path in generated:
        if path.is_symlink() or path.parent != graph_dir / "wiki":
            raise ValueError("unexpected Graphify wiki path")
        original = path.read_text(encoding="utf-8")
        # Exact source names become links to the analyzed commit.
        linked = re.sub(
            r"`([^`\n]+)`",
            lambda match: f'[`{match[1]}`](https://github.com/kdkrkwhr/engineering-standards/blob/{revision}/{quote(match[1])})'
            if match[1] in metadata["files"] else match[0],
            original,
        )
        tokens = parser.parse(linked)
        for token in tokens:
            for child in token.children or []:
                if child.type != "link_open":
                    continue
                href = child.attrGet("href")
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = unquote(parsed.path)
                if target not in names:
                    raise ValueError(f"unresolved Graphify wiki link in {path.name}: {href}")
                child.attrSet("href", quote(target[:-3] + ".html") + ("#" + parsed.fragment if parsed.fragment else ""))
        title = next((line[2:].strip() for line in original.splitlines() if line.startswith("# ")), path.stem)
        pages.append((path.name[:-3] + ".html", title))
        body = parser.renderer.render(tokens, parser.options, {})
        html = site_template.replace("__STYLE__", replacements["__STYLE__"]).replace("__TITLE__", escape(title))
        html = html.replace("__REVISION__", revision).replace("__BODY__", body)
        (destination / (path.stem + ".html")).write_text(html, encoding="utf-8")
        shutil.copyfile(path, destination / path.name)
    search_index = [{"title": title, "url": "./" + name, "kind": "Graphify 자동 문서"} for name, title in pages]
    (destination / "index.json").write_text(json.dumps(search_index, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / ".site-build")
    parser.add_argument("--revision")
    parser.add_argument("--graphify-dir", type=Path, help="validated code-only Graphify output directory")
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    profile_data = json.loads(PROFILE_SOURCE.read_text(encoding="utf-8"))
    errors = validate(data) + validate(profile_data)
    if errors:
        parser.error("invalid glossary: " + "; ".join(errors))
    if {term["id"] for term in data["terms"]} & {term["id"] for term in profile_data["terms"]}:
        parser.error("duplicate glossary id across source files")
    data["terms"].extend(profile_data["terms"])
    data["relations"].extend(profile_data["relations"])
    revision = args.revision or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        parser.error("revision must be a full commit SHA")
    out = args.out.resolve()
    if out == ROOT or not out.is_relative_to(ROOT) or out.is_symlink():
        parser.error("output must be a dedicated directory inside this repository")
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        parser.error("output directory must be empty")
    graph_metadata = None
    if args.graphify_dir:
        graph_metadata = json.loads((args.graphify_dir / "metadata.json").read_text(encoding="utf-8"))
    html, markdown = render(data, revision, graph_metadata)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / "wiki.md").write_text(markdown, encoding="utf-8")
    if args.graphify_dir:
        publish_graphify(out, args.graphify_dir.resolve(), revision)
    print(f"Built public wiki in {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
