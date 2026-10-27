"""Test ignore choices and hygiene checks using synthetic files in temporary Git repos."""

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_hygiene.py"
FRAGMENTS = ("common", "java", "python", "node")


def run(repo: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    if ok and result.returncode:
        raise AssertionError(f"command failed: {args[0]} {args[1:3]}")
    return result


def write(repo: Path, name: str, content: str) -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="hygiene-fixture-") as temporary:
        repo = Path(temporary)
        run(repo, "git", "init", "-q")
        fragments = [
            (ROOT / "templates" / "gitignore" / f"{name}.gitignore").read_text()
            for name in FRAGMENTS
        ]
        write(repo, ".gitignore", "\n".join(fragments))
        safe = {
            "README.md": "# Synthetic fixture\n",
            ".env.example": "API_KEY=replace_me\n",
            ".env.test.example": "API_KEY=replace_me\n",
            "gradle/wrapper/gradle-wrapper.jar": "synthetic wrapper fixture\n",
            "package-lock.json": "{}\n",
            "uv.lock": "synthetic lock fixture\n",
            "tests/fixtures/sample.log": "synthetic log fixture\n",
        }
        for name, value in safe.items():
            write(repo, name, value)
        ignored = (".env", "node_modules/pkg/index.js", ".venv/bin/python", "logs/run.log")
        allowed = (".env.example", ".env.test.example", "gradle/wrapper/gradle-wrapper.jar", "package-lock.json", "uv.lock", "tests/fixtures/sample.log")
        for name in ignored:
            if run(repo, "git", "check-ignore", "-q", "--", name, ok=False).returncode != 0:
                raise AssertionError(f"expected ignore: {name}")
        for name in allowed:
            if run(repo, "git", "check-ignore", "-q", "--", name, ok=False).returncode == 0:
                raise AssertionError(f"unexpected ignore: {name}")
        run(repo, "git", "add", "--", ".gitignore", *safe)
        for scope in ("--staged", "--tracked"):
            result = run(repo, sys.executable, str(CHECKER), scope, ok=False)
            if result.returncode:
                raise AssertionError(f"safe fixture failed {scope}: {result.stderr}")

        fake_aws = "AKIA" + "A" * 16
        fake_private_header = "-----BEGIN " + "PRIVATE KEY-----"
        write(repo, ".env", "LOCAL_ONLY=fake\n")
        write(repo, ".DS_Store", "synthetic OS output\n")
        write(repo, "docs/synthetic.txt", fake_aws + "\n" + fake_private_header + "\nnot-a-key\n")
        run(repo, "git", "add", "-f", "--", ".env", ".DS_Store")
        run(repo, "git", "add", "--", "docs/synthetic.txt")
        for scope in ("--staged", "--tracked"):
            result = run(repo, sys.executable, str(CHECKER), scope, ok=False)
            if result.returncode != 1:
                raise AssertionError(f"unsafe fixture was not rejected: {scope}")
            if fake_aws in result.stderr or "not-a-key" in result.stderr:
                raise AssertionError("a synthetic secret value was printed")
            if not all(name in result.stderr for name in (".env", ".DS_Store", "docs/synthetic.txt")):
                raise AssertionError(f"missing path-only finding: {scope}")
    print("Ignore and hygiene positive/negative fixture checks OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
