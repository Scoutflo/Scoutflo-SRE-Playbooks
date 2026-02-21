# Contributing Guide

> Thank you for your interest in contributing to SRE Playbooks!

## Quick Start

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your changes
4. **Make changes** following our guidelines
5. **Submit a PR** with a clear description

## Ways to Contribute

### 1. Add CLI Equivalents (Easiest)

Help make playbooks accessible to DevOps engineers by adding CLI sections:

```markdown
1. Retrieve pod `<pod-name>` in namespace `<namespace>` and check status.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

</details>
```

### 2. Create New Playbooks

Add playbooks for uncovered scenarios. Follow the [Playbook Format](/format).

### 3. Improve Documentation

- Fix typos and clarify instructions
- Add real-world examples
- Improve the Quick Reference

### 4. Report Issues

- Bug reports
- Feature requests
- Playbook corrections

## Playbook Structure

All playbooks must have 4 sections:

```markdown
# Alert/Error Name

## Meaning
What this issue means and why it occurs.

## Impact
Business and technical consequences.

## Playbook
1. Step one...
2. Step two...
3. Step three...

## Diagnosis
- If X condition, then Y action.
- If inconclusive, check Z.
```

## Naming Conventions

| Provider | Format | Example |
|----------|--------|---------|
| K8s | `<AlertName>-<resource>.md` | `CrashLoopBackOff-pod.md` |
| AWS | `<Issue>-<Service>.md` | `Connection-Timeout-EC2.md` |
| Sentry | `<Exception>-<Category>-application.md` | `NullPointer-Error-application.md` |

## File Locations

| Provider | Folder |
|----------|--------|
| AWS Compute | `AWS Playbooks/01-Compute/` |
| AWS Database | `AWS Playbooks/02-Database/` |
| K8s Pods | `K8s Playbooks/03-Pods/` |
| K8s Networking | `K8s Playbooks/05-Networking/` |
| Sentry Errors | `Sentry Playbooks/01-Error-Tracking/` |

## Pull Request Process

1. **Create a descriptive PR title**
   - `Add: New playbook for Lambda cold starts`
   - `Fix: Typo in CrashLoopBackOff playbook`
   - `Improve: Add CLI examples to Pod playbooks`

2. **Fill out the PR template**

3. **Wait for review** (2-3 business days)

4. **Address feedback** if requested

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). Be respectful and inclusive.

## Questions?

- Open a [Discussion](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
- Check the [FAQ](/faq)
- Email: support@scoutflo.com

---

[Back to Home](/)
