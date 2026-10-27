"""Validate the public terminology source without third-party packages."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "glossary/common.json"
STATUSES = {"observed", "proposed", "confirmed"}
ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
RELATION_TYPE = re.compile(r"[a-z]+(?:_[a-z]+)*\Z")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
PUBLIC_BLOB = re.compile(r"/[^/]+/[^/]+/blob/[0-9a-f]{40}/.+\Z")


def validate(data: dict) -> list[str]:
    if not isinstance(data, dict):
        return ["glossary root must be an object"]
    errors = []
    if data.get("schema_version") != 1 or data.get("scope") != "public-common-technical":
        errors.append("unsupported schema or scope")
    if not isinstance(data.get("updated"), str) or not DATE.fullmatch(data["updated"]):
        errors.append("invalid updated date")
    terms = data.get("terms")
    if not isinstance(terms, list):
        return errors + ["terms must be a list"]
    ids = set()
    for number, term in enumerate(terms, 1):
        label = f"term {number}"
        if not isinstance(term, dict):
            errors.append(f"{label}: must be an object")
            continue
        term_id = term.get("id", "")
        if not isinstance(term_id, str) or not ID.fullmatch(term_id):
            errors.append(f"{label}: invalid id")
            continue
        if term_id in ids:
            errors.append(f"{label}: duplicate id {term_id}")
        ids.add(term_id)
        for key in ("ko", "en", "meaning", "scope", "code_name_example"):
            if not isinstance(term.get(key), str) or not term[key].strip():
                errors.append(f"{label}: missing {key}")
        for key in ("aliases", "avoid_mixing"):
            if not isinstance(term.get(key), list) or not all(isinstance(x, str) and x.strip() for x in term[key]):
                errors.append(f"{label}: invalid {key}")
        if not isinstance(term.get("status"), str) or term["status"] not in STATUSES:
            errors.append(f"{label}: invalid status")
        source = term.get("source", "")
        parsed = urlparse(source) if isinstance(source, str) else None
        if term.get("status") == "observed" and not (parsed and parsed.scheme == "https" and parsed.netloc == "github.com" and PUBLIC_BLOB.fullmatch(parsed.path)):
            errors.append(f"{label}: observed term needs a pinned public GitHub source")
        rule_name = term.get("related_rule")
        rule = ROOT / rule_name if isinstance(rule_name, str) else ROOT
        if not isinstance(rule_name, str) or not rule.is_file() or not rule.resolve().is_relative_to(ROOT):
            errors.append(f"{label}: unresolved related_rule")
    relations = data.get("relations")
    if not isinstance(relations, list):
        return errors + ["relations must be a list"]
    relation_keys = set()
    for number, relation in enumerate(relations, 1):
        if not isinstance(relation, dict):
            errors.append(f"relation {number}: must be an object")
            continue
        source, target = relation.get("from"), relation.get("to")
        relation_type = relation.get("type")
        if not isinstance(source, str) or not isinstance(target, str) or source not in ids or target not in ids:
            errors.append(f"relation {number}: unresolved endpoint")
        if not isinstance(relation_type, str) or not RELATION_TYPE.fullmatch(relation_type):
            errors.append(f"relation {number}: invalid type")
        if all(isinstance(value, str) for value in (source, relation_type, target)):
            key = (source, relation_type, target)
            if key in relation_keys:
                errors.append(f"relation {number}: duplicate relation")
            relation_keys.add(key)
        if not isinstance(relation.get("status"), str) or relation["status"] not in STATUSES:
            errors.append(f"relation {number}: invalid status")
    return errors


def main() -> int:
    try:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, ValueError) as exc:
        print(f"Could not parse glossary: {type(exc).__name__}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(data['terms'])} terms and {len(data['relations'])} relations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
