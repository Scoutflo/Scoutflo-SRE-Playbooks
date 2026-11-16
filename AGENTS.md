# Scoutflo SRE Playbooks — Agent Instructions

Markdown incident-response playbooks for Kubernetes, AWS and Sentry, served as a
Docsify site from `docs/`. Canonical repo: `github.com/Scoutflo/Scoutflo-SRE-Playbooks`.

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r scripts/requirements.txt
python scripts/validate_dual_format.py --summary        # validate all playbooks
python scripts/validate_dual_format.py --provider k8s   # or aws / sentry
python scripts/convert_to_dual_format.py --file "<path/to/playbook.md>"   # needs ANTHROPIC_API_KEY
python3 -m http.server 3000 --directory docs            # preview the Docsify site
```

Done check: `validate_dual_format.py --summary` shows no new failures for the
files you touched, and links/sidebar entries resolve in the preview.

## Layout

- `K8s Playbooks/`, `AWS Playbooks/`, `Sentry Playbooks/` — numbered category folders holding one `.md` per alert/issue.
- `docs/` — Docsify site (`_sidebar.md`, `_navbar.md`, mirrored provider pages). Update the sidebar when adding or renaming playbooks.
- `scripts/` — dual-format converter and validator.
- Standards: `CONTRIBUTING.md` and `docs/format.md` (required sections: Meaning, Impact, Playbook, Diagnosis).

## Rules

- Always: keep the standard section structure and the dual-format sections (`### For AI Agents (NLP)` and `### For DevOps/SREs (CLI)`); use events-first diagnosis; follow existing file naming (`AlertName-component.md`).
- Ask first: bulk edits across categories, running the converter with `--all` (uses paid API calls), restructuring folders, changing counts in README/docs.
- Never: commit API keys, put customer names or environment data in playbooks, or run commands from playbooks against live clusters/accounts without explicit scope.
- Local-only files (`CLAUDE.md`, `.claude/`, `DUAL_FORMAT_PROGRESS.md`) are gitignored; do not force-add them.
- PRs: the remote currently has only `master`; confirm the base branch with the user before `gh pr create`.
