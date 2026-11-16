#!/usr/bin/env python3
"""Keep provider README playbook counts and file listings in sync with the folders.

Rewrites, in "K8s Playbooks/README.md" and "AWS Playbooks/README.md":
  - tree lines        ├── 04-Workloads/   (N playbooks)
  - section headers   ### 04-Workloads/ (N playbooks)  and  #### 01-Capacity-Performance (N playbooks)
  - the `- \\`File.md\\`` bullet list under each section

Usage: python scripts/sync_readmes.py [--check]   (--check exits 1 if changes are needed)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BULLET = re.compile(r"^- `[^`]+\.md`\s*$")
H3 = re.compile(r"^### (\d\d-[^/ ]+)/? \(\d+ playbooks?\)\s*$")
H4 = re.compile(r"^#### (\d\d-[^/ ]+) \(\d+ playbooks?\)\s*$")
TREE = re.compile(r"^(?P<pre>(?:[│ ]{4})?[├└]── (?P<name>\d\d-[^/ ]+)/\s+)\(\d+ playbooks?\)\s*$")


def files(d: Path):
    return sorted((p.name for p in d.rglob("*.md") if p.name != "README.md"), key=str.lower)


def plural(n):
    return f"{n} playbook" + ("" if n == 1 else "s")


def sync(readme: Path) -> str:
    base = readme.parent
    lines = readme.read_text().split("\n")
    out, cur3, cur4, i = [], None, None, 0
    while i < len(lines):
        ln = lines[i]
        m3, m4 = H3.match(ln), H4.match(ln)
        mt = TREE.match(ln)
        if m3:
            cur3, cur4 = m3.group(1), None
            out.append(f"### {cur3}/ ({plural(len(files(base / cur3)))})")
        elif m4 and cur3:
            cur4 = m4.group(1)
            out.append(f"#### {cur4} ({plural(len(files(base / cur3 / cur4)))})")
        elif mt:
            name = mt.group("name")
            d = base / name if not ln.startswith((" ", "│")) else base / (cur3 or "") / name
            if ln[0] in "├└":
                cur3 = name
                d = base / name
            else:
                d = base / cur3 / name
            out.append(f"{mt.group('pre')}({plural(len(files(d)))})")
        elif BULLET.match(ln) and cur3:
            d = base / cur3 / (cur4 or "")
            while i < len(lines) and BULLET.match(lines[i]):
                i += 1
            out.extend(f"- `{f}`" for f in files(d))
            continue
        else:
            out.append(ln)
        i += 1
    return "\n".join(out)


def main() -> int:
    changed = False
    for name in ("K8s Playbooks", "AWS Playbooks"):
        readme = ROOT / name / "README.md"
        new = sync(readme)
        if new != readme.read_text():
            changed = True
            print(f"{'would update' if '--check' in sys.argv else 'updated'}: {readme.relative_to(ROOT)}")
            if "--check" not in sys.argv:
                readme.write_text(new)
    return 1 if changed and "--check" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
