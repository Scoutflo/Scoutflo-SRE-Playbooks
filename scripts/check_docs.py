#!/usr/bin/env python3
"""Docs consistency checker.

Reports:
  1. Links in docs/ and READMEs that point at playbook files which do not exist
  2. Playbooks not linked from their docs/ category page
  3. Actual playbook counts per provider (compare with README/ROADMAP numbers)

Usage: python scripts/check_docs.py [--strict]   (--strict exits 1 on any finding)
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
PROVIDERS = {"K8s Playbooks": "k8s", "AWS Playbooks": "aws", "Sentry Playbooks": "sentry"}
LINK = re.compile(r"blob/(?:master|main)/((?:K8s|AWS|Sentry)(?:%20| )Playbooks/[^)\s#\"']+\.md)")


def playbooks():
    for folder in PROVIDERS:
        for p in sorted((ROOT / folder).rglob("*.md")):
            if p.name != "README.md":
                yield p


def main() -> int:
    findings = 0
    existing = {p.relative_to(ROOT).as_posix() for p in playbooks()}

    texts = [p for p in ROOT.rglob("*.md") if ".venv" not in p.parts and ".git" not in p.parts]
    linked = {}
    for md in texts:
        for m in LINK.finditer(md.read_text(errors="ignore")):
            target = unquote(m.group(1))
            linked.setdefault(md.relative_to(ROOT).as_posix(), set()).add(target)
            if target not in existing:
                print(f"BROKEN LINK  {md.relative_to(ROOT)} -> {target}")
                findings += 1

    for pb in sorted(existing):
        parts = pb.split("/")
        provider = PROVIDERS[parts[0]]
        cat_page = ROOT / "docs" / provider / (parts[1].lower().replace("-ci-cd", "-cicd") + ".md")
        key = cat_page.relative_to(ROOT).as_posix()
        if "Proactive" in parts[1]:
            continue  # proactive pages link to sub-category folders, not files
        if cat_page.exists() and pb not in linked.get(key, set()):
            print(f"NOT LISTED   {key} is missing {pb}")
            findings += 1

    print("\nActual counts:")
    total = 0
    for folder, prov in PROVIDERS.items():
        n = sum(1 for p in existing if p.startswith(folder))
        total += n
        print(f"  {prov}: {n}")
    print(f"  total: {total}\n{findings} finding(s)")
    return 1 if findings and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
