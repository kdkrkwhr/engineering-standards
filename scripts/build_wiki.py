"""Build a public, dependency-free GitHub Pages index from the glossary source."""

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


def render(data: dict, revision: str) -> tuple[str, str]:
    base = f"https://github.com/kdkrkwhr/engineering-standards/blob/{revision}/"
    nav = "\n".join(f'<a href="{base}{path}">{escape(label)}</a>' for label, path in DOCS)
    cards = []
    md = ["# 용어 위키 (파생 설명)", "", f"원본: [glossary/common.json]({base}glossary/common.json) · 표준 버전: `{revision}`", "", "이 문서는 원본 규칙을 재정의하지 않습니다. 관계의 ‘제안·추론’은 실제 코드 호출 그래프가 아닙니다.", ""]
    for term in data["terms"]:
        rule_url = base + term["related_rule"]
        title = escape(term["ko"])
        search = escape(" ".join([term["id"], term["ko"], term["en"], *term["aliases"]]).lower(), quote=True)
        cards.append(f'''<article id="{term['id']}" data-search="{search}">
  <div class="meta"><span>{escape(STATUS[term['status']])}</span><span>{escape(term['scope'])}</span></div>
  <h3>{title} <small>{escape(term['en'])}</small></h3>
  <p>{escape(term['meaning'])}</p>
  <p class="code">이름 예시: <code>{escape(term['code_name_example'])}</code></p>
  <p>허용 별칭: {escape(', '.join(term['aliases']) or '없음')} · 구분할 용어: {escape(', '.join(term['avoid_mixing']) or '없음')}</p>
  <p class="links"><a href="{escape(rule_url, quote=True)}">적용 규칙</a> <a href="{escape(term['source'], quote=True)}">공개 관찰 근거</a></p>
</article>''')
        md.extend([f"## {term['ko']} · {term['en']}", "", f"상태: {STATUS[term['status']]} · 범위: {term['scope']}", "", term["meaning"], "", f"이름 예시: `{term['code_name_example']}` · 허용 별칭: {', '.join(term['aliases']) or '없음'} · 구분할 용어: {', '.join(term['avoid_mixing']) or '없음'}", "", f"[적용 규칙]({rule_url}) · [공개 관찰 근거]({term['source']})", ""])
    relations = []
    md.extend(["## 용어 관계", ""])
    for relation in data["relations"]:
        source, target = relation["from"], relation["to"]
        relations.append(f'<li><a href="#{source}">{source}</a> → {escape(relation["type"])} → <a href="#{target}">{target}</a> <em>{escape(STATUS[relation["status"]])}</em></li>')
        md.append(f"- [{source}](#{source}) → `{relation['type']}` → [{target}](#{target}) ({STATUS[relation['status']]})")
    html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Engineering Standards · 용어 위키</title>
<style>
:root {{ color-scheme: light; font-family: system-ui, sans-serif; color: #1c2936; background: #f5f7fa; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; line-height: 1.65; }}
header {{ background: #122b42; color: white; padding: 2.5rem max(1.25rem, calc((100vw - 70rem)/2)); }}
main {{ max-width: 70rem; margin: auto; padding: 1.25rem; }} h1 {{ margin: .2rem 0; font-size: clamp(1.8rem, 5vw, 3rem); }}
nav, .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); gap: .75rem; }}
nav a, article, .relations {{ background: white; border: 1px solid #dce3ea; border-radius: .7rem; padding: 1rem; }}
a {{ color: #075b91; }} nav a {{ font-weight: 650; }} article p {{ overflow-wrap: anywhere; }}
small {{ color: #546779; font-size: .8em; }} .meta {{ display: flex; flex-wrap: wrap; gap: .5rem; color: #36586f; font-size: .82rem; }}
.meta span {{ background: #e7f1f6; border-radius: 1rem; padding: .1rem .55rem; }}
input {{ width: 100%; max-width: 35rem; padding: .75rem; font: inherit; border: 1px solid #8ba2b2; border-radius: .4rem; }}
.links a {{ margin-right: 1rem; }} .relations li {{ margin: .5rem 0; }} em {{ font-style: normal; color: #685622; }}
@media (max-width: 600px) {{ header {{ padding: 1.5rem 1.25rem; }} main {{ padding: .8rem; }} }}
</style></head><body>
<header><h1>Engineering Standards</h1><p>에이전트 지침과 사람이 읽는 코드 지도 · 공개 공통 용어 인덱스</p></header>
<main><section aria-labelledby="standard-title"><h2 id="standard-title">표준 원본</h2><p>규칙은 아래 원본에서 확인합니다. 기준 커밋: <code>{revision}</code></p><nav aria-label="표준 문서">{nav}</nav></section>
<section aria-labelledby="term-title"><h2 id="term-title">용어 찾기</h2><p>관찰은 공개 코드의 이름·구조 근거이고, 제안·추론은 규칙이나 실제 호출 관계를 확정하지 않습니다.</p>
<label for="search">용어 또는 별칭 검색</label><br><input id="search" type="search" autocomplete="off" placeholder="예: DTO, controller, 저장">
<p id="count" aria-live="polite"></p><div class="cards">{''.join(cards)}</div></section>
<section class="relations" aria-labelledby="relation-title"><h2 id="relation-title">용어 관계</h2><ul>{''.join(relations)}</ul></section>
<footer><p>원본: <a href="{base}glossary/common.json">glossary/common.json</a> · <a href="./wiki.md">Markdown 설명</a></p></footer></main>
<script>const input=document.querySelector('#search');const cards=[...document.querySelectorAll('article[data-search]')];
function filter(){{const q=input.value.trim().toLocaleLowerCase();let shown=0;for(const card of cards){{card.hidden=!card.dataset.search.includes(q);if(!card.hidden)shown++;}}document.querySelector('#count').textContent=`${{shown}} / ${{cards.length}}개 용어`;}}
input.addEventListener('input',filter);filter();</script></body></html>'''
    return html, "\n".join(md) + "\n"


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
