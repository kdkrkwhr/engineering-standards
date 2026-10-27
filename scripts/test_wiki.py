"""Check glossary rejection cases and the project-site artifact using temp files."""

import copy
import json
from pathlib import Path
import tempfile
from urllib.parse import urljoin, urlparse

from build_wiki import render
from check_glossary import SOURCE, PROFILE_SOURCE, validate
from check_site import check


def main() -> int:
    common = json.loads(SOURCE.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE_SOURCE.read_text(encoding="utf-8"))
    assert not validate(common), validate(common)
    assert not validate(profile), validate(profile)
    assert all(term["category"] == "common" for term in common["terms"])
    assert all(term["category"] != "common" for term in profile["terms"])
    assert not common["relations"]
    assert "glossary root must be an object" in validate([])
    duplicate = copy.deepcopy(profile)
    duplicate["terms"].append(copy.deepcopy(duplicate["terms"][0]))
    assert any("duplicate id" in x for x in validate(duplicate))
    broken = copy.deepcopy(profile)
    broken["relations"][0]["to"] = "missing-term"
    assert any("unresolved endpoint" in x for x in validate(broken))
    wrong_status = copy.deepcopy(common)
    wrong_status["terms"][0]["status"] = "certain"
    assert any("invalid status" in x for x in validate(wrong_status))
    missing_rule = copy.deepcopy(common)
    missing_rule["terms"][0]["related_rule"] = "standards/missing.md"
    assert any("unresolved related_rule" in x for x in validate(missing_rule))
    unpinned_source = copy.deepcopy(profile)
    unpinned_source["terms"][0]["source"] = "https://github.com/example/repo/blob/main/file.py"
    assert any("pinned public GitHub source" in x for x in validate(unpinned_source))
    misplaced = copy.deepcopy(common)
    misplaced["terms"][0]["category"] = "spring"
    assert any("invalid category" in x for x in validate(misplaced))
    data = copy.deepcopy(common)
    data["terms"].extend(profile["terms"])
    data["relations"].extend(profile["relations"])
    revision = "a" * 40
    html, markdown = render(data, revision)
    assert "spring-controller" in html and "제안·추론" in html
    assert 'data-category="common"' in html and 'data-category="spring"' in html
    assert all(language in html for language in ("Java", "Python", "Dart", "C#", "TypeScript"))
    assert "특정 언어, 프레임워크, 네 계층 구조를 모든 프로젝트에 강제하지 않습니다" in html
    assert "프로필별 관찰 예시" in markdown
    assert "__REVISION_URL__" not in html
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
        (site / ".env").unlink()
        architecture = site / "architecture"
        architecture.mkdir()
        graphify = site / "wiki" / "graphify"
        graphify.mkdir(parents=True)
        metadata = {"revision": revision, "mode": "code-only; LLM disabled"}
        for name in ("index.html", "graph.json", "graph.html", "GRAPH_REPORT.md"):
            (architecture / name).write_text("reviewed fixture", encoding="utf-8")
        (architecture / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        (graphify / "index.json").write_text(json.dumps([{"url": "./index.html"}]), encoding="utf-8")
        (graphify / "index.html").write_text("reviewed fixture", encoding="utf-8")
        (graphify / "index.md").write_text("# reviewed fixture", encoding="utf-8")
        assert not check(site, revision, graphify=True), check(site, revision, graphify=True)
        (graphify / "debug.log").write_text("fixture", encoding="utf-8")
        assert any("unexpected artifact" in x for x in check(site, revision, graphify=True))
        (graphify / "debug.log").unlink()
        (architecture / "graph.html").write_text("/home/runner/private", encoding="utf-8")
        assert any("non-portable path" in x for x in check(site, revision, graphify=True))
    print("Wiki schema rejection and project-site artifact smoke checks OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
