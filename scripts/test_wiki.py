"""Check glossary rejection cases and the project-site artifact using temp files."""

import copy
import json
from pathlib import Path
import tempfile
from urllib.parse import urljoin, urlparse

from build_wiki import render
from check_glossary import SOURCE, validate
from check_site import check


def main() -> int:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert not validate(data), validate(data)
    assert "glossary root must be an object" in validate([])
    duplicate = copy.deepcopy(data)
    duplicate["terms"].append(copy.deepcopy(duplicate["terms"][0]))
    assert any("duplicate id" in x for x in validate(duplicate))
    broken = copy.deepcopy(data)
    broken["relations"][0]["to"] = "missing-term"
    assert any("unresolved endpoint" in x for x in validate(broken))
    wrong_status = copy.deepcopy(data)
    wrong_status["terms"][0]["status"] = "certain"
    assert any("invalid status" in x for x in validate(wrong_status))
    missing_rule = copy.deepcopy(data)
    missing_rule["terms"][0]["related_rule"] = "standards/missing.md"
    assert any("unresolved related_rule" in x for x in validate(missing_rule))
    unpinned_source = copy.deepcopy(data)
    unpinned_source["terms"][0]["source"] = "https://github.com/example/repo/blob/main/file.py"
    assert any("pinned public GitHub source" in x for x in validate(unpinned_source))
    revision = "a" * 40
    html, markdown = render(data, revision)
    assert "spring-controller" in html and "제안·추론" in html
    assert 'class="graph-node"' in html and 'class="graph-edge"' in html
    assert 'data-from-label="Spring 컨트롤러"' in html
    assert "Graphify 코드 추출과 구분합니다" in html
    assert "JavaScript가 필요합니다" in html
    with tempfile.TemporaryDirectory() as tmp:
        site = Path(tmp) / "engineering-standards"
        site.mkdir()
        (site / "index.html").write_text(html, encoding="utf-8")
        (site / "wiki.md").write_text(markdown, encoding="utf-8")
        assert not check(site, revision), check(site, revision)
        project_url = "https://kdkrkwhr.github.io/engineering-standards/"
        resolved = urlparse(urljoin(project_url, "./wiki.md"))
        assert resolved.path == "/engineering-standards/wiki.md"
        assert (site / resolved.path.rsplit("/", 1)[-1]).is_file()
        (site / ".env").write_text("placeholder", encoding="utf-8")
        assert any("unexpected artifact" in x for x in check(site, revision))
    print("Wiki schema rejection and project-site artifact smoke checks OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
