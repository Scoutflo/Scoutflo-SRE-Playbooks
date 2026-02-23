#!/usr/bin/env python3
"""
Dual-Format Playbook Converter

Converts NLP-style playbooks to dual-format (NLP + CLI) by:
1. Parsing the existing playbook into sections
2. Extracting the Playbook section (NLP instructions)
3. Using Claude API to generate CLI equivalents
4. Reconstructing the file with both formats

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python convert_to_dual_format.py --provider k8s --limit 10  # Pilot
    python convert_to_dual_format.py --all                      # Full run
    python convert_to_dual_format.py --file "path/to/playbook.md"  # Single file
"""

import os
import re
import sys
import argparse
import time
from pathlib import Path
from typing import Optional, Tuple, Dict
from tqdm import tqdm

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

# Base path for playbooks
BASE_PATH = Path(__file__).parent.parent

# Provider configurations
PROVIDERS = {
    "k8s": {
        "path": BASE_PATH / "K8s Playbooks",
        "cli_prefix": "kubectl",
        "context": "Kubernetes cluster management using kubectl CLI"
    },
    "aws": {
        "path": BASE_PATH / "AWS Playbooks",
        "cli_prefix": "aws",
        "context": "AWS cloud management using AWS CLI"
    },
    "sentry": {
        "path": BASE_PATH / "Sentry Playbooks",
        "cli_prefix": "curl/sentry-cli",
        "context": "Sentry error tracking using sentry-cli or REST API"
    }
}

# System prompt for CLI conversion
SYSTEM_PROMPT = """You are an expert SRE who converts NLP-style playbook instructions into executable CLI commands.

Your task: Convert the given NLP playbook steps into equivalent CLI commands.

Rules:
1. Keep the same step numbering (1, 2, 3, etc.)
2. Preserve placeholders in the format <placeholder-name> (e.g., <pod-name>, <namespace>, <instance-id>)
3. Each step should have:
   - A brief description of what the command does
   - The actual CLI command in a bash code block
4. Commands should be production-ready and follow best practices
5. For Kubernetes: use kubectl with appropriate flags (-o wide, -o yaml, etc.)
6. For AWS: use aws cli with appropriate subcommands and --output flags
7. For Sentry: use sentry-cli or curl with the REST API
8. Include common flags that would be useful (e.g., --namespace, --region)
9. If a step involves multiple related commands, include all of them
10. Keep the CLI section concise but complete

Output format example:
1. Check pod status and events:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. Get pod logs:
   ```bash
   kubectl logs <pod-name> -n <namespace>
   kubectl logs <pod-name> -n <namespace> --previous
   ```
"""


def parse_playbook(content: str) -> Dict[str, str]:
    """Parse playbook content into sections."""
    sections = {
        "frontmatter": "",
        "title": "",
        "meaning": "",
        "impact": "",
        "playbook": "",
        "diagnosis": ""
    }

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        sections["frontmatter"] = frontmatter_match.group(0)
        content = content[frontmatter_match.end():]

    # Extract title (first # heading)
    title_match = re.match(r'^(# .+?\n)', content)
    if title_match:
        sections["title"] = title_match.group(1)
        content = content[title_match.end():]

    # Split by ## headers
    section_pattern = r'## (Meaning|Impact|Playbook|Diagnosis)\n'
    parts = re.split(section_pattern, content)

    # parts will be: [pre-content, 'Meaning', meaning_content, 'Impact', impact_content, ...]
    current_section = None
    for i, part in enumerate(parts):
        part_lower = part.lower().strip()
        if part_lower in ['meaning', 'impact', 'playbook', 'diagnosis']:
            current_section = part_lower
        elif current_section:
            # Find where the next section starts (or end of content)
            sections[current_section] = part.strip()

    return sections


def is_already_dual_format(playbook_content: str) -> bool:
    """Check if playbook already has dual format."""
    return "### For AI Agents (NLP)" in playbook_content or "### For DevOps/SREs (CLI)" in playbook_content


def generate_cli_section(client: anthropic.Anthropic, nlp_content: str, provider: str) -> str:
    """Use Claude API to generate CLI equivalent of NLP playbook steps."""
    provider_config = PROVIDERS.get(provider, PROVIDERS["k8s"])

    user_prompt = f"""Context: {provider_config['context']}
Primary CLI tool: {provider_config['cli_prefix']}

Convert these NLP playbook steps to CLI commands:

{nlp_content}

Generate the CLI equivalent following the rules in your instructions. Output ONLY the CLI steps, nothing else."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text.strip()
    except anthropic.RateLimitError:
        print("\nRate limited, waiting 60 seconds...")
        time.sleep(60)
        return generate_cli_section(client, nlp_content, provider)
    except Exception as e:
        print(f"\nAPI Error: {e}")
        return None


def reconstruct_playbook(sections: Dict[str, str], cli_content: str) -> str:
    """Reconstruct playbook with dual-format Playbook section."""

    # Build the dual-format playbook section
    dual_playbook = f"""### For AI Agents (NLP)

{sections['playbook']}

### For DevOps/SREs (CLI)

{cli_content}"""

    # Reconstruct full document
    parts = []

    if sections["frontmatter"]:
        parts.append(sections["frontmatter"])

    if sections["title"]:
        parts.append(sections["title"])

    parts.append(f"## Meaning\n\n{sections['meaning']}\n")
    parts.append(f"## Impact\n\n{sections['impact']}\n")
    parts.append(f"## Playbook\n\n{dual_playbook}\n")
    parts.append(f"## Diagnosis\n\n{sections['diagnosis']}\n")

    return "\n".join(parts)


def convert_playbook(client: anthropic.Anthropic, file_path: Path, provider: str, dry_run: bool = False) -> Tuple[bool, str]:
    """Convert a single playbook to dual format."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Read error: {e}"

    # Skip if already converted
    if is_already_dual_format(content):
        return True, "Already converted"

    # Parse sections
    sections = parse_playbook(content)

    if not sections["playbook"]:
        return False, "No Playbook section found"

    # Generate CLI section
    cli_content = generate_cli_section(client, sections["playbook"], provider)

    if not cli_content:
        return False, "API generation failed"

    # Reconstruct
    new_content = reconstruct_playbook(sections, cli_content)

    if dry_run:
        print(f"\n--- Preview: {file_path.name} ---")
        print(new_content[:1500] + "..." if len(new_content) > 1500 else new_content)
        return True, "Dry run - not saved"

    # Write back
    try:
        file_path.write_text(new_content, encoding='utf-8')
        return True, "Converted"
    except Exception as e:
        return False, f"Write error: {e}"


def get_playbook_files(provider: str = None, limit: int = None) -> list:
    """Get list of playbook files to process."""
    files = []

    providers_to_process = [provider] if provider else PROVIDERS.keys()

    for p in providers_to_process:
        if p not in PROVIDERS:
            continue
        provider_path = PROVIDERS[p]["path"]
        if provider_path.exists():
            for md_file in provider_path.rglob("*.md"):
                # Skip README files
                if md_file.name.lower() == "readme.md":
                    continue
                files.append((md_file, p))

    if limit:
        files = files[:limit]

    return files


def main():
    parser = argparse.ArgumentParser(description="Convert NLP playbooks to dual-format (NLP + CLI)")
    parser.add_argument("--provider", choices=["k8s", "aws", "sentry"], help="Process specific provider")
    parser.add_argument("--limit", type=int, help="Limit number of files to process")
    parser.add_argument("--file", type=str, help="Process a single file")
    parser.add_argument("--all", action="store_true", help="Process all playbooks")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Run: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Get files to process
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        # Detect provider from path
        provider = "k8s"
        path_str = str(file_path).lower()
        if "aws" in path_str:
            provider = "aws"
        elif "sentry" in path_str:
            provider = "sentry"
        files = [(file_path, provider)]
    elif args.all:
        files = get_playbook_files()
    elif args.provider:
        files = get_playbook_files(provider=args.provider, limit=args.limit)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python convert_to_dual_format.py --provider k8s --limit 10  # Pilot")
        print("  python convert_to_dual_format.py --all                      # Full run")
        print("  python convert_to_dual_format.py --file 'path/to/file.md'   # Single file")
        sys.exit(0)

    if not files:
        print("No playbook files found")
        sys.exit(1)

    print(f"Processing {len(files)} playbook(s)...")
    if args.dry_run:
        print("(Dry run mode - no files will be modified)\n")

    # Process files
    success_count = 0
    skip_count = 0
    error_count = 0

    for file_path, provider in tqdm(files, desc="Converting"):
        success, message = convert_playbook(client, file_path, provider, dry_run=args.dry_run)

        if success:
            if message == "Already converted":
                skip_count += 1
            else:
                success_count += 1
        else:
            error_count += 1
            tqdm.write(f"Error: {file_path.name}: {message}")

        # Small delay to avoid rate limits
        if not args.dry_run and success_count > 0:
            time.sleep(0.5)

    print(f"\nResults:")
    print(f"  Converted: {success_count}")
    print(f"  Skipped (already converted): {skip_count}")
    print(f"  Errors: {error_count}")


if __name__ == "__main__":
    main()
