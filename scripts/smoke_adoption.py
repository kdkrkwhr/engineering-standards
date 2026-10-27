"""Exercise copied project templates and bundled relative links with fake projects."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
PATH = re.compile(r"`(docs/engineering-standards/[^`]+\.md|docs/engineering-profile\.md)`")
PLACEHOLDER = re.compile(r"<[A-Z][A-Z_]+>")


def exercise(kind: str, language: str, framework: Optional[str]) -> None:
    with tempfile.TemporaryDirectory(prefix=f"standards-{kind}-") as temporary:
        project = Path(temporary) / "project"
        bundle = project / "docs" / "engineering-standards"
        bundle.parent.mkdir(parents=True)
        shutil.copytree(ROOT, bundle, ignore=shutil.ignore_patterns(".git", "__pycache__", ".site-build", ".wiki-cache", "graphify-out"))
        (project / "docs" / "requirements.md").write_text("# 가상 요구\n")
        profile = project / "docs" / "engineering-profile.md"
        shutil.copyfile(bundle / "templates" / "project-profile.md", profile)
        profile_content = profile.read_text()
        profile_content = profile_content.replace(
            "<docs/engineering-standards/standards/core.md 등 필요한 경로만>",
            "docs/engineering-standards/standards/core.md",
        )
        selected = f"docs/engineering-standards/profiles/languages/{language}.md"
        if framework:
            selected += f"`, `docs/engineering-standards/profiles/frameworks/{framework}.md"
        profile_content = profile_content.replace("<선택한 실제 경로와 제외한 프로필>", selected)
        profile_content = re.sub(r"<[^<>\n]+>", "가상 fixture 값", profile_content)
        profile.write_text(profile_content)

        values = {
            "PROJECT_NAME": f"fake-{kind}",
            "PROJECT_CONTRACT": "docs/requirements.md (가상 fixture)",
            "LANGUAGE_PROFILE_PATH": f"docs/engineering-standards/profiles/languages/{language}.md",
            "FRAMEWORK_PROFILE_PATH_OR_DELETE_LINE": (
                f"docs/engineering-standards/profiles/frameworks/{framework}.md" if framework else None
            ),
            "API_DTO_PATH_OR_DELETE_LINE": (
                "docs/engineering-standards/standards/api-dto.md" if framework else None
            ),
            "TRANSACTION_PATH_OR_DELETE_LINE": (
                "docs/engineering-standards/standards/transactions.md" if framework else None
            ),
            "PROJECT_GLOSSARY_PATH_OR_DELETE_LINE": None,
            "ENTRYPOINT_PATH": "src/example (가상 fixture)",
            "BUILD_COMMAND_OR_NONE": "없음 (가상 fixture)",
            "TEST_COMMAND": "미정 (가상 fixture)",
            "INTEGRATION_COMMAND_OR_NONE": "없음 (가상 fixture)",
        }
        lines = (bundle / "templates" / "AGENTS.md").read_text().splitlines()
        filled = []
        for line in lines:
            if any(value is None and f"<{key}>" in line for key, value in values.items()):
                continue
            for key, value in values.items():
                if value is not None:
                    line = line.replace(f"<{key}>", value)
            filled.append(line)
        agents = project / "AGENTS.md"
        agents.write_text("\n".join(filled) + "\n")
        content = agents.read_text()
        if PLACEHOLDER.search(content):
            raise ValueError(f"{kind}: unresolved AGENTS placeholder")
        if re.search(r"<[^<>\n]+>", profile.read_text()):
            raise ValueError(f"{kind}: unresolved profile placeholder")
        for target in PATH.findall(content + "\n" + profile.read_text()):
            if not (project / target).is_file():
                raise ValueError(f"{kind}: missing copied path {target}")
        if framework and f"frameworks/{framework}.md" not in content:
            raise ValueError(f"{kind}: selected framework missing")
        if not framework and "선택한 프레임워크:" in content:
            raise ValueError(f"{kind}: unused framework was not removed")
        result = subprocess.run(
            [sys.executable, str(bundle / "scripts" / "check_docs.py")],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise ValueError(f"{kind}: copied bundle links failed: {result.stderr}")


def main() -> int:
    exercise("spring", "java", "spring-boot")
    exercise("python", "python", None)
    print("Spring and Python copied-template smoke checks OK (documents and paths only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
