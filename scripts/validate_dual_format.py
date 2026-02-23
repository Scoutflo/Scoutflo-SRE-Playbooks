#!/usr/bin/env python3
"""
Dual-Format Playbook Validator

Validates that playbooks have the correct dual-format structure:
- ### For AI Agents (NLP) section
- ### For DevOps/SREs (CLI) section

Usage:
    python validate_dual_format.py                    # Validate all
    python validate_dual_format.py --provider k8s    # Validate K8s only
    python validate_dual_format.py --summary         # Show summary only
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Base path for playbooks
BASE_PATH = Path(__file__).parent.parent

PROVIDERS = {
    "k8s": BASE_PATH / "K8s Playbooks",
    "aws": BASE_PATH / "AWS Playbooks",
    "sentry": BASE_PATH / "Sentry Playbooks"
}


def validate_playbook(file_path: Path) -> Tuple[bool, bool, List[str]]:
    """
    Validate a single playbook.
    Returns: (has_nlp, has_cli, issues)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, False, [f"Read error: {e}"]

    issues = []
    has_nlp = "### For AI Agents (NLP)" in content
    has_cli = "### For DevOps/SREs (CLI)" in content

    # Check for required sections
    if "## Meaning" not in content:
        issues.append("Missing ## Meaning section")
    if "## Impact" not in content:
        issues.append("Missing ## Impact section")
    if "## Playbook" not in content:
        issues.append("Missing ## Playbook section")
    if "## Diagnosis" not in content:
        issues.append("Missing ## Diagnosis section")

    # Check for CLI code blocks if has CLI section
    if has_cli:
        cli_section_match = content.find("### For DevOps/SREs (CLI)")
        if cli_section_match > -1:
            cli_content = content[cli_section_match:]
            diagnosis_start = cli_content.find("## Diagnosis")
            if diagnosis_start > -1:
                cli_content = cli_content[:diagnosis_start]
            if "```bash" not in cli_content and "```" not in cli_content:
                issues.append("CLI section has no code blocks")

    return has_nlp, has_cli, issues


def get_playbook_files(provider: str = None) -> List[Tuple[Path, str]]:
    """Get list of playbook files."""
    files = []

    providers_to_check = [provider] if provider else PROVIDERS.keys()

    for p in providers_to_check:
        if p not in PROVIDERS:
            continue
        provider_path = PROVIDERS[p]
        if provider_path.exists():
            for md_file in provider_path.rglob("*.md"):
                if md_file.name.lower() == "readme.md":
                    continue
                files.append((md_file, p))

    return files


def main():
    parser = argparse.ArgumentParser(description="Validate dual-format playbooks")
    parser.add_argument("--provider", choices=["k8s", "aws", "sentry"], help="Check specific provider")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    args = parser.parse_args()

    files = get_playbook_files(provider=args.provider)

    if not files:
        print("No playbook files found")
        sys.exit(1)

    print(f"Validating {len(files)} playbook(s)...\n")

    # Stats
    stats: Dict[str, Dict] = {
        "k8s": {"total": 0, "dual": 0, "nlp_only": 0, "issues": 0},
        "aws": {"total": 0, "dual": 0, "nlp_only": 0, "issues": 0},
        "sentry": {"total": 0, "dual": 0, "nlp_only": 0, "issues": 0}
    }

    issues_list = []

    for file_path, provider in files:
        has_nlp, has_cli, issues = validate_playbook(file_path)

        stats[provider]["total"] += 1

        if has_nlp and has_cli:
            stats[provider]["dual"] += 1
        elif not has_cli:
            stats[provider]["nlp_only"] += 1

        if issues:
            stats[provider]["issues"] += 1
            issues_list.append((file_path.name, issues))

    # Print summary
    print("=" * 60)
    print("DUAL-FORMAT VALIDATION SUMMARY")
    print("=" * 60)

    for provider in ["k8s", "aws", "sentry"]:
        s = stats[provider]
        if s["total"] == 0:
            continue

        dual_pct = (s["dual"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"\n{provider.upper()}:")
        print(f"  Total playbooks: {s['total']}")
        print(f"  Dual format:     {s['dual']} ({dual_pct:.1f}%)")
        print(f"  NLP only:        {s['nlp_only']}")
        print(f"  With issues:     {s['issues']}")

    total_playbooks = sum(s["total"] for s in stats.values())
    total_dual = sum(s["dual"] for s in stats.values())
    total_pct = (total_dual / total_playbooks * 100) if total_playbooks > 0 else 0

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total_dual}/{total_playbooks} ({total_pct:.1f}%) have dual format")
    print("=" * 60)

    # Print issues if not summary mode
    if not args.summary and issues_list:
        print(f"\nISSUES FOUND ({len(issues_list)} files):")
        for filename, issues in issues_list[:20]:  # Limit output
            print(f"\n  {filename}:")
            for issue in issues:
                print(f"    - {issue}")

        if len(issues_list) > 20:
            print(f"\n  ... and {len(issues_list) - 20} more files with issues")

    # Exit code
    if total_dual == total_playbooks:
        print("\n All playbooks have dual format!")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
