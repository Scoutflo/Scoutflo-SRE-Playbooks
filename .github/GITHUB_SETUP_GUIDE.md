# GitHub Repository Setup Guide

This guide documents the manual GitHub settings that need to be configured for this repository.

## Required Manual Configuration

### 1. Enable GitHub Discussions

**Path:** Settings > General > Features

- [x] Check "Discussions"
- Categories will auto-populate from `.github/discussions/categories.json`

### 2. Configure Labels

**Path:** Settings > Labels

Create these labels (or use the `labels.yml` file with github-label-sync):

#### Category Labels
| Label | Color | Description |
|-------|-------|-------------|
| `aws-playbook` | `#FF9900` | Related to AWS playbooks |
| `k8s-playbook` | `#326CE5` | Related to Kubernetes playbooks |
| `sentry-playbook` | `#362D59` | Related to Sentry playbooks |
| `documentation` | `#0075CA` | Documentation improvements |

#### Type Labels
| Label | Color | Description |
|-------|-------|-------------|
| `bug` | `#D73A4A` | Something isn't working correctly |
| `enhancement` | `#A2EEEF` | Improvement to existing playbook |
| `new-playbook` | `#0E8A16` | Request or PR for new playbook |
| `question` | `#D876E3` | Further information requested |

#### Status Labels
| Label | Color | Description |
|-------|-------|-------------|
| `good first issue` | `#7057FF` | Good for newcomers |
| `help wanted` | `#008672` | Community help welcome |
| `in-progress` | `#FBCA04` | Currently being worked on |
| `needs-review` | `#0052CC` | Ready for maintainer review |

#### Priority Labels
| Label | Color | Description |
|-------|-------|-------------|
| `priority: critical` | `#B60205` | Needs immediate attention |
| `priority: high` | `#D93F0B` | Important |
| `priority: medium` | `#FBCA04` | Normal priority |
| `priority: low` | `#0E8A16` | Nice to have |

### 3. Configure Branch Protection

**Path:** Settings > Branches > Add branch protection rule

**Branch name pattern:** `master`

**Recommended settings:**
- [x] Require a pull request before merging
  - [x] Require approvals: 1
  - [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require status checks to pass before merging
  - [x] Require branches to be up to date before merging
  - Status checks: `validate-structure`, `Community Health Check`
- [x] Require conversation resolution before merging
- [ ] Require signed commits (optional)
- [x] Do not allow bypassing the above settings
- [ ] Allow force pushes: **Disabled**
- [ ] Allow deletions: **Disabled**

### 4. Activate GitHub Sponsors (Optional)

**Path:** Settings > Sponsors

1. Click "Join the waitlist" or "Set up Sponsors"
2. Complete the onboarding process
3. Update `.github/FUNDING.yml` with your sponsor username

### 5. Create Starter Issues

Create these issues for newcomers:

#### Issue 1: Good First Issue Example
```
Title: [Good First Issue] Fix typos in K8s Playbooks README

Labels: good first issue, documentation, k8s-playbook

Body:
## Description
Review the K8s Playbooks/README.md for any typos or grammatical errors.

## Acceptance Criteria
- [ ] Review the entire README
- [ ] Fix any typos found
- [ ] Ensure links are working

## Getting Started
See our [Getting Started Guide](.github/GETTING_STARTED.md) for contribution instructions.
```

#### Issue 2: Help Wanted Example
```
Title: [Help Wanted] Add playbook for EKS Pod Identity issues

Labels: help wanted, new-playbook, aws-playbook

Body:
## Description
We need a playbook for troubleshooting AWS EKS Pod Identity configuration issues.

## Suggested Structure
- Meaning: What Pod Identity is and common misconfiguration symptoms
- Impact: Application authentication failures, permission errors
- Playbook: 8-10 diagnostic steps
- Diagnosis: Correlation with IAM policy changes

## Resources
- [EKS Pod Identity Docs](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)

## Getting Started
See our [Contributing Guide](CONTRIBUTING.md) for playbook structure requirements.
```

### 6. Configure Repository Settings

**Path:** Settings > General

**Features:**
- [x] Issues
- [x] Discussions
- [x] Projects (optional)
- [x] Wiki (optional)

**Pull Requests:**
- [x] Allow merge commits
- [x] Allow squash merging
- [x] Allow rebase merging
- [x] Always suggest updating pull request branches
- [x] Automatically delete head branches

### 7. Set Up Topics/Tags

**Path:** Repository main page > gear icon next to "About"

**Suggested topics:**
```
sre
site-reliability-engineering
devops
kubernetes
aws
incident-response
runbooks
playbooks
troubleshooting
on-call
sentry
monitoring
observability
infrastructure
```

### 8. Update About Section

**Path:** Repository main page > gear icon next to "About"

**Description:**
```
SRE incident response playbooks for AWS, Kubernetes & Sentry. 376 step-by-step troubleshooting guides to help on-call engineers resolve infrastructure issues faster.
```

**Website:** `https://scoutflo.com`

---

## Verification Checklist

After completing setup:

- [ ] GitHub Discussions is enabled and shows categories
- [ ] All labels are created (check Settings > Labels)
- [ ] Branch protection is active (check Settings > Branches)
- [ ] "Sponsor" button appears (if GitHub Sponsors activated)
- [ ] At least 2 issues exist with `good first issue` label
- [ ] Topics appear under repository name
- [ ] About section shows description and website

---

## Automated Sync (Optional)

To automate label sync, use:

```bash
npm install -g github-label-sync
github-label-sync --access-token YOUR_TOKEN --labels .github/labels.yml Scoutflo/scoutflo-SRE-Playbooks
```

---

*Last updated: February 2026*
