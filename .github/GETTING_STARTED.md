# Getting Started as a Contributor

Welcome to the SRE Playbooks community! This guide will help you make your first contribution.

## Quick Start (5 minutes)

### 1. Fork & Clone

```bash
# Fork via GitHub UI, then:
git clone https://github.com/YOUR-USERNAME/scoutflo-SRE-Playbooks.git
cd scoutflo-SRE-Playbooks
git remote add upstream https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git
```

### 2. Find Something to Work On

**New contributors should look for:**
- Issues labeled `good-first-issue`
- Issues labeled `help-wanted`
- Typos or small documentation fixes

**Browse issues:** [github.com/Scoutflo/scoutflo-SRE-Playbooks/issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

### 3. Make Your Change

```bash
git checkout -b fix/your-change-description
# Make your edits
git add .
git commit -m "Fix: Description of your change"
git push origin fix/your-change-description
```

### 4. Submit a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template
4. Submit!

---

## Types of Contributions

### Easy (Good First Issues)

| Type | Example | Time |
|------|---------|------|
| Fix typos | Correct spelling in playbooks | 5-15 min |
| Improve clarity | Reword confusing sentences | 15-30 min |
| Add links | Add relevant external resources | 15-30 min |
| Update placeholders | Standardize placeholder format | 15-30 min |

### Medium

| Type | Example | Time |
|------|---------|------|
| Improve playbook steps | Add missing diagnostic steps | 30-60 min |
| Add examples | Include real-world examples | 30-60 min |
| Update documentation | Improve README sections | 30-60 min |
| Review PRs | Help review other contributions | 30-60 min |

### Advanced

| Type | Example | Time |
|------|---------|------|
| New playbook | Create a new incident playbook | 1-2 hours |
| New category | Add playbooks for new service | 2-4 hours |
| Workflow automation | Add GitHub Actions workflows | 1-2 hours |

---

## Playbook Structure Reference

Every playbook has 4 required sections:

```markdown
# Issue Title

## Meaning
What the issue means, symptoms, and root causes.
(3-5 sentences minimum)

## Impact
Business and technical implications.
(3-5 sentences minimum)

## Playbook
1. First diagnostic step
2. Second diagnostic step
...
8-10. Final steps
(Ordered from common to specific causes)

## Diagnosis
Correlation analysis with time windows.
Use "If X, then Y" conditional patterns.
(5 correlation steps minimum)
```

---

## Exemplary Playbooks

Study these well-structured playbooks as examples:

### AWS Example
**File:** `AWS Playbooks/01-Compute/Connection-Timeout-SSH-Issues-EC2.md`
- Clear problem description
- Comprehensive diagnostic steps
- Good use of placeholders (`<instance-id>`)

### Kubernetes Example
**File:** `K8s Playbooks/03-Pods/CrashLoopBackOff-pod.md`
- Well-organized sections
- Actionable troubleshooting steps
- Time-based correlation analysis

### Sentry Example
**File:** `Sentry Playbooks/01-Error-Tracking/UnhandledException-Error-application.md`
- Consistent naming convention
- Cross-domain keyword matching
- Clear diagnostic flow

---

## Common Placeholders

Use these standard placeholders:

### AWS
```
<instance-id>     - EC2 instance ID (i-xxx)
<bucket-name>     - S3 bucket name
<region>          - AWS region (us-east-1)
<function-name>   - Lambda function name
<role-name>       - IAM role name
<vpc-id>          - VPC ID (vpc-xxx)
<security-group-id> - Security group ID (sg-xxx)
```

### Kubernetes
```
<pod-name>        - Pod name
<namespace>       - Namespace
<deployment-name> - Deployment name
<node-name>       - Node name
<service-name>    - Service name
<pvc-name>        - PersistentVolumeClaim name
```

### Sentry
```
<project-slug>    - Sentry project slug
<issue-id>        - Sentry issue ID
<environment>     - Environment name
```

---

## Commit Message Format

```
Type: Short description (max 72 chars)

Longer description if needed.

Fixes #123
```

**Types:**
- `Fix:` - Bug fixes
- `Add:` - New playbooks or features
- `Update:` - Improvements to existing content
- `Docs:` - Documentation only changes
- `Chore:` - Maintenance tasks

---

## Getting Help

**Stuck or have questions?**

1. **Search existing issues** - Someone may have asked before
2. **GitHub Discussions** - Ask the community
3. **Slack** - Real-time help at [scoutflo.slack.com](https://scoutflo.slack.com)
4. **Create an issue** - Use the question template

---

## Contributor Checklist

Before submitting your PR:

- [ ] Followed the playbook structure (4 sections)
- [ ] Used standard placeholders
- [ ] Checked for typos
- [ ] Tested any commands/steps
- [ ] Updated relevant README if adding new playbook
- [ ] Wrote clear commit message
- [ ] Filled out PR template

---

## Recognition

Contributors are recognized in:
- GitHub Contributors page
- Release notes for significant contributions
- CONTRIBUTORS.md (for repeat contributors)
- Social media shoutouts

---

## Next Steps

1. **Join Slack**: [scoutflo.slack.com](https://scoutflo.slack.com)
2. **Star the repo**: Help others discover us
3. **Find an issue**: Look for `good-first-issue` label
4. **Make your first PR**: We'll help you through it!

---

**Welcome to the community! We're excited to have you.**

Questions? Reach out on [Slack](https://scoutflo.slack.com) or [Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions).
