"""Build the public site from reviewed terminology and optional code evidence."""

import argparse
from html import escape
import json
from pathlib import Path
import re
import subprocess

from check_glossary import ROOT, SOURCE, validate


DOCS = (
    ("시작과 적용", "README.md"),
    ("공통 원칙", "standards/core.md"),
    ("명명", "standards/naming.md"),
    ("구조 선택", "standards/architecture.md"),
    ("API·DTO", "standards/api-dto.md"),
    ("트랜잭션", "standards/transactions.md"),
    ("에이전트 지침", "agents/implementation.md"),
    ("Spring Boot", "profiles/frameworks/spring-boot.md"),
    ("Python", "profiles/languages/python.md"),
)
STATUS = {"observed": "공개 코드에서 관찰", "proposed": "제안·추론", "confirmed": "표준에서 확정"}
RELATION_LABEL = {"may_call": "호출할 수 있음", "accepts": "입력으로 받음", "may_use": "사용할 수 있음"}
SITE = ROOT / "site"


def category(term: dict) -> str:
    if term["id"].startswith("spring-"):
        return "spring"
    if "dto" in term["id"]:
        return "api"
    return "python"


def graph_svg(data: dict) -> str:
    positions = [(48, 48), (298, 48), (48, 208), (548, 48), (548, 208)]
    while len(positions) < len(data["terms"]):
        n = len(positions)
        positions.append((48 + n % 3 * 250, 368 + (n - 5) // 3 * 160))
    coordinates = {term["id"]: positions[i] for i, term in enumerate(data["terms"])}
    height = max(y for _, y in positions[:len(data["terms"])]) + 120
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
    for term in data["terms"]:
        x, y = coordinates[term["id"]]
        nodes.append(f'''<a class="graph-node" data-node="{term['id']}" data-category="{category(term)}" href="#{term['id']}" aria-label="{escape(term['ko'], quote=True)} 상세 보기">
  <rect x="{x}" y="{y}" width="204" height="74" rx="12"/>
  <text class="node-title" x="{x + 15}" y="{y + 32}">{escape(term['ko'])}</text>
  <text class="node-sub" x="{x + 15}" y="{y + 55}">{escape(term['en'])}</text>
</a>''')
    return f'''<svg viewBox="0 0 800 {height}" role="img" aria-labelledby="graph-title graph-desc" xmlns="http://www.w3.org/2000/svg">
<title id="graph-title">공통 용어 관계 그래프</title><desc id="graph-desc">선은 수동으로 제안한 관계입니다. 노드를 누르면 근거와 규칙을 볼 수 있습니다.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8"/></marker></defs>
{''.join(edges)}{''.join(nodes)}</svg>'''


def render(data: dict, revision: str) -> tuple[str, str]:
    base = f"https://github.com/kdkrkwhr/engineering-standards/blob/{revision}/"
    nav = "\n".join(f'<a href="{base}{path}">{escape(label)}</a>' for label, path in DOCS)
    cards = []
    markdown = ["# 용어 위키 (원본에서 생성)", "", f"원본: [glossary/common.json]({base}glossary/common.json) · 표준 버전: `{revision}`", "", "이 문서는 원본 규칙을 재정의하지 않습니다. 관계의 ‘제안·추론’은 실제 코드 호출 그래프가 아닙니다.", ""]
    for term in data["terms"]:
        rule_url = base + term["related_rule"]
        source_url = term["source"]
        query = " ".join([term["id"], term["ko"], term["en"], term["meaning"], term["scope"], term["code_name_example"], *term["aliases"]]).lower()
        cards.append(f'''<article class="term-card" id="{term['id']}" tabindex="-1" data-search="{escape(query, quote=True)}" data-category="{category(term)}">
  <div class="term-meta"><span class="eyebrow">{escape(term['scope'])}</span><span class="badge">{escape(STATUS[term['status']])}</span></div>
  <h3>{escape(term['ko'])}<span>{escape(term['en'])}</span></h3>
  <p>{escape(term['meaning'])}</p>
  <dl><div><dt>코드 이름</dt><dd><code>{escape(term['code_name_example'])}</code></dd></div><div><dt>허용 별칭</dt><dd>{escape(', '.join(term['aliases']) or '없음')}</dd></div><div><dt>구분할 용어</dt><dd>{escape(', '.join(term['avoid_mixing']) or '없음')}</dd></div></dl>
  <div class="term-links"><a href="{escape(rule_url, quote=True)}">적용 규칙 ↗</a><a href="{escape(source_url, quote=True)}">관찰 근거 ↗</a></div>
</article>''')
        markdown.extend([f"## {term['ko']} · {term['en']}", "", f"상태: {STATUS[term['status']]} · 범위: {term['scope']}", "", term["meaning"], "", f"이름 예시: `{term['code_name_example']}` · 허용 별칭: {', '.join(term['aliases']) or '없음'} · 구분할 용어: {', '.join(term['avoid_mixing']) or '없음'}", "", f"[적용 규칙]({rule_url}) · [공개 관찰 근거]({source_url})", ""])
    relations = []
    names = {term["id"]: term["ko"] for term in data["terms"]}
    markdown.extend(["## 용어 관계", ""])
    for relation in data["relations"]:
        source, target = relation["from"], relation["to"]
        relation_label = RELATION_LABEL.get(relation["type"], relation["type"])
        relations.append(f'<button type="button" class="relation" data-from="{source}" data-to="{target}" data-from-label="{escape(names[source], quote=True)}" data-to-label="{escape(names[target], quote=True)}"><span>{escape(names[source])}</span><strong>{escape(relation_label)}</strong><span>{escape(names[target])}</span><em>{escape(STATUS[relation["status"]])}</em></button>')
        markdown.append(f"- [{source}](#{source}) → `{relation['type']}` → [{target}](#{target}) ({STATUS[relation['status']]})")
    template = (SITE / "index.template.html").read_text(encoding="utf-8")
    substitutions = {
        "__STYLE__": (SITE / "style.css").read_text(encoding="utf-8"),
        "__SCRIPT__": (SITE / "app.js").read_text(encoding="utf-8"),
        "__REVISION__": revision,
        "__SOURCE_URL__": base + "glossary/common.json",
        "__NAV__": nav,
        "__CARDS__": "\n".join(cards),
        "__GRAPH__": graph_svg(data),
        "__RELATIONS__": "\n".join(relations),
        "__TERM_COUNT__": str(len(data["terms"])),
        "__RELATION_COUNT__": str(len(data["relations"])),
    }
    for token, value in substitutions.items():
        template = template.replace(token, value)
    if re.search(r"__[A-Z_]+__", template):
        raise ValueError("unresolved site template token")
    return template, "\n".join(markdown) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / ".site-build")
    parser.add_argument("--revision")
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        parser.error("invalid glossary: " + "; ".join(errors))
    revision = args.revision or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        parser.error("revision must be a full commit SHA")
    out = args.out.resolve()
    if out == ROOT or not out.is_relative_to(ROOT) or out.is_symlink():
        parser.error("output must be a dedicated directory inside this repository")
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        parser.error("output directory must be empty")
    html, markdown = render(data, revision)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / "wiki.md").write_text(markdown, encoding="utf-8")
    print(f"Built 2 public wiki files in {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
