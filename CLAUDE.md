# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

**scoutflo-SRE-Playbooks** is an open-source collection of 376 SRE incident response playbooks for Kubernetes, AWS, and Sentry environments. This is the public GitHub repository maintained by Scoutflo.

### Related Repositories (Internal)
- **Internal Working Folder**: `C:\Users\Atharva Scoutflo\Trivy\RunBooks\All-For-Cursor` - Internal development and SSOT documents
- **Kepler Server**: `C:\Users\vedan\Scoutflo\keplar-memory\kepler` - AI Memory server that uses these playbooks
- **Voyager Server**: `C:\Users\vedan\Scoutflo\Voyager\voyager` - AI Agent Orchestration
- **Context Document**: `C:\Users\vedan\Scoutflo\VOYAGER_KEPLER_COMPLETE_CONTEXT.md` - Full platform context

## Repository Structure

```
scoutflo-SRE-Playbooks/
├── AWS Playbooks/                    # 157 AWS playbooks
│   ├── 01-Compute/                   # EC2, Lambda, ECS, EKS (27)
│   ├── 02-Database/                  # RDS, DynamoDB (8)
│   ├── 03-Storage/                   # S3 (7)
│   ├── 04-Networking/                # VPC, ELB, Route53 (17)
│   ├── 05-Security/                  # IAM, KMS, GuardDuty (16)
│   ├── 06-Monitoring/                # CloudTrail, CloudWatch (8)
│   ├── 07-CI-CD/                     # CodePipeline, CodeBuild (9)
│   └── 08-Proactive/                 # Proactive monitoring (65)
│
├── K8s Playbooks/                    # 194 Kubernetes playbooks
│   ├── 01-Control-Plane/ → 12-Namespaces/  # Reactive (138)
│   └── 13-Proactive/                 # Proactive monitoring (56)
│
├── Sentry Playbooks/                 # 25 Sentry playbooks
│   ├── 01-Error-Tracking/            # Exception handling (19)
│   ├── 02-Performance/               # Timeout, latency (6)
│   └── 03-Release-Health/            # Release correlation
│
├── .github/                          # GitHub templates and workflows
├── README.md                         # Main documentation
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                      # Version history
├── QUICK_REFERENCE.md                # Quick reference card
└── [Other supporting docs]
```

## Playbook Statistics

| Provider | Reactive | Proactive | Total |
|----------|----------|-----------|-------|
| AWS | 92 | 65 | **157** |
| K8s | 138 | 56 | **194** |
| Sentry | 25 | 0 | **25** |
| **Total** | **255** | **121** | **376** |

## Playbook Format

All playbooks follow a 4-section structure:

```markdown
# Alert/Error Name

## Meaning
What this issue means, triggers, and root causes.
Includes cross-domain keywords for multi-source matching.

## Impact
Business and technical implications.
States consequences clearly.

## Playbook
8-10 numbered diagnostic steps in natural language.
Ordered from common to specific causes.
Uses NLP-friendly instructions (no raw commands).

## Diagnosis
Conditional logic for root cause analysis:
- Events-first approach
- "If X, then Y. If inconclusive, then Z." patterns
- Permission checks early (RBAC/IAM/Release)
- Logical ordering (most likely causes first)
```

## Development Guidelines

### Modifying Playbooks
1. Preserve the 4-section structure (Meaning, Impact, Playbook, Diagnosis)
2. Use NLP-friendly language (action verbs, no raw commands)
3. Keep Diagnosis steps conditional and evidence-based
4. Update CHANGELOG.md with changes

### Adding New Playbooks
1. Follow the naming convention:
   - K8s: `<AlertName>-<resource>.md`
   - AWS: `<Issue>-<Service>.md`
   - Sentry: `<ExceptionType>-<Category>-application.md`
2. Place in appropriate subfolder
3. Include all 4 sections
4. Update the folder's README.md

### Syncing with Internal Folder
This repo syncs from the internal working folder:
- Source: `C:\Users\Atharva Scoutflo\Trivy\RunBooks\All-For-Cursor\Playbooks\`
- Target: This repo's playbook folders

Only playbook .md files are synced (no SSOTs, Searchables, or scripts).

## Key Files

| File | Purpose |
|------|---------|
| README.md | Main documentation with overview and usage |
| CONTRIBUTING.md | How to contribute to the repo |
| CHANGELOG.md | Version history and changes |
| QUICK_REFERENCE.md | Quick lookup for finding playbooks |
| FAQ.md | Frequently asked questions |
| EXAMPLES.md | Real-world usage examples |
| TROUBLESHOOTING_FLOWCHART.md | Decision tree for finding playbooks |
| ROADMAP.md | Project roadmap and future plans |
| .github/GETTING_STARTED.md | First-time contributor onboarding guide |
| .github/labels.yml | GitHub labels configuration |
| .github/GITHUB_SETUP_GUIDE.md | Manual GitHub settings documentation |

## Recent Changes (v2.0.0 - 2026-02-03)

### Added
- **Sentry Playbooks**: 25 new playbooks for application error tracking
- **AWS Proactive**: 65 proactive monitoring playbooks
- **K8s Proactive**: 56 proactive monitoring playbooks

### Changed
- **AWS Restructured**: From flat to 8 service-based subfolders
- **Diagnosis Improved**: All 376 playbooks updated with events-first approach
- **K8s Structure**: Added 13-Proactive folder

### Statistics
- Total: 163 → **376** (+213 playbooks)
- AWS: 25 → **157** (+132 playbooks)
- K8s: 138 → **194** (+56 playbooks)
- Sentry: 0 → **25** (new provider)

## Git Workflow

```bash
# Clone the repo
git clone https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git

# Create feature branch
git checkout -b feature/new-playbook

# Make changes and commit
git add .
git commit -m "Add: New playbook for [issue]"

# Push and create PR
git push origin feature/new-playbook
```

## Contact

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Community Q&A
- **Slack**: [scoutflo.slack.com](https://scoutflo.slack.com)
