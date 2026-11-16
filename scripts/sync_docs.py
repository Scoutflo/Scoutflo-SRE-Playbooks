#!/usr/bin/env python3
"""Regenerate the proactive category pages in docs/ from the playbook folders.

Updates card counts and rebuilds each "## <Category> (N playbooks)" table with
links to the real playbook files (first sentence of each Meaning as description).

Usage: python scripts/sync_docs.py [--check]
"""
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/"
PAGES = {"docs/aws/08-proactive.md": "AWS Playbooks/08-Proactive", "docs/k8s/13-proactive.md": "K8s Playbooks/13-Proactive"}
NAMES = {  # heading text -> sub-folder
    "Capacity & Performance": "01-Capacity-Performance", "Security & Compliance": "02-Security-Compliance",
    "Backup & DR": "03-Backup-DR", "Cost Optimization": "04-Cost-Optimization",
    "Observability": "05-Observability", "Data Integrity": "06-Data-Integrity",
    "Operational Readiness": "07-Operational-Readiness",
}


def desc(path: Path) -> str:
    m = re.search(r"## Meaning\s+(.+?)(?:\n\n|\Z)", path.read_text(errors="ignore"), re.S)
    text = " ".join(m.group(1).split()) if m else ""
    text = re.sub(r"[|`]", "", text)
    first = re.split(r"(?<=[.;])\s", text)[0]
    return (first[:140].rstrip() + "…") if len(first) > 140 else first


def build(page: Path, base: Path) -> str:
    s = page.read_text()
    counts = {}
    for title, sub in NAMES.items():
        files = sorted((f for f in (base / sub).glob("*.md") if f.name != "README.md"), key=lambda f: f.name.lower())
        counts[title] = len(files)
        rows = "\n".join(
            f"| [{f.stem}]({REPO}{quote(f.relative_to(ROOT).as_posix())}) | {desc(f)} |" for f in files
        )
        table = f"| Playbook | Description |\n|----------|-------------|\n{rows}\n"
        pat = re.compile(rf"(## {re.escape(title)} \()\d+( playbooks\)\n\n)(?:\|.*\n)+", re.M)
        s = pat.sub(lambda m: f"{m.group(1)}{len(files)}{m.group(2)}{table}", s)
        card = re.compile(rf"(<h4>{re.escape(title)}</h4>\s*<p>)\d+( playbooks)")
        s = card.sub(lambda m: f"{m.group(1)}{len(files)}{m.group(2)}", s)
    total = sum(counts.values())
    s = re.sub(r"> \*\*\d+ playbooks\*\*", f"> **{total} playbooks**", s, count=1)
    return s


def main() -> int:
    changed = False
    for page, folder in PAGES.items():
        p = ROOT / page
        new = build(p, ROOT / folder)
        if new != p.read_text():
            changed = True
            print(("would update: " if "--check" in sys.argv else "updated: ") + page)
            if "--check" not in sys.argv:
                p.write_text(new)
    return 1 if changed and "--check" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
