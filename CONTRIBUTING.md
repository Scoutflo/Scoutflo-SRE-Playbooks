# Contributing to SRE Playbooks

Thank you for your interest in contributing to the SRE Playbooks repository! This document provides guidelines and instructions for contributing to this open-source project.

> **New to contributing?** Check out our [Getting Started Guide](.github/GETTING_STARTED.md) for a quick onboarding experience.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Playbook Standards](#playbook-standards)
- [Exemplary Playbooks](#exemplary-playbooks)
- [Pull Request Process](#pull-request-process)
- [Review Process](#review-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful, inclusive, and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

If you find a bug or error in a playbook:

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) to see if the bug has already been reported
2. **Create a Bug Report**:
   - Use the bug report template
   - Provide clear description of the issue
   - Include steps to reproduce
   - Specify which playbook is affected
   - Include relevant error messages or logs
   - Tag with `bug` label

### Suggesting Enhancements

Have an idea to improve a playbook or add a new one?

1. **Check Existing Issues**: Search for similar suggestions
2. **Create an Enhancement Request**:
   - Use the feature request template
   - Clearly describe the enhancement
   - Explain why it would be useful
   - Provide examples if possible
   - Tag with `enhancement` label

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or grammatical errors
- Clarify unclear instructions
- Add missing information
- Improve examples
- Update outdated content

### Adding New Playbooks

See [Playbook Standards](#playbook-standards) below for detailed guidelines on creating new playbooks.

## Development Process

### Getting Started

1. **Fork the Repository**: Click the "Fork" button on GitHub
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/scoutflo-SRE-Playbooks.git
   cd scoutflo-SRE-Playbooks
   ```
3. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git
   ```

### Making Changes

1. **Create a Branch**:
   ```bash
   git checkout -b fix/playbook-name-improvement
   # or
   git checkout -b feature/new-playbook-name
   ```

2. **Make Your Changes**: 
   - Follow the playbook structure (see below)
   - Test your changes
   - Ensure consistency with existing playbooks

3. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Fix: Improve [playbook-name] - [description]"
   # or
   git commit -m "Add: New playbook for [issue]"
   ```

   **Commit Message Guidelines:**
   - Use present tense ("Add" not "Added")
   - Use imperative mood ("Fix" not "Fixes")
   - Keep first line under 72 characters
   - Reference issue numbers if applicable: "Fix: Improve playbook (#123)"

4. **Push to Your Fork**:
   ```bash
   git push origin fix/playbook-name-improvement
   ```

5. **Create a Pull Request**:
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Request review from maintainers

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

## Playbook Standards

### Structure Requirements

All playbooks must follow this structure:

1. **Title** (H1)
   - Clear, descriptive title
   - AWS: `<IssueOrSymptom>-<Component>.md`
   - K8s: `<AlertName>-<Resource>.md`

2. **Meaning** (H2)
   - What the issue means
   - Common triggers and symptoms
   - Affected service/component
   - Typical root causes
   - Minimum 3-5 sentences

3. **Impact** (H2)
   - Business implications
   - Technical effects
   - Related alarms/alerts
   - Cascading effects
   - Minimum 3-5 sentences

4. **Playbook** (H2) - **Dual Format Required**
   - 8-10 numbered steps
   - Ordered from most common to specific
   - Use placeholders for resource identifiers (e.g., `<pod-name>`, `<namespace>`)
   - **Must include both formats** (see [Dual Format Guidelines](#dual-format-guidelines) below)

5. **Diagnosis** (H2)
   - 5 correlation analysis steps
   - Time-based correlations
   - Comparison of events with failures
   - Guidance for extending time windows
   - Alternative evidence sources

### Content Guidelines

- **Be Specific**: Provide actionable, step-by-step instructions
- **Use Placeholders**: Replace specific values with placeholders (e.g., `<instance-id>`, `<pod-name>`)
- **Include Commands**: Provide actual commands where applicable
- **Be Accurate**: Ensure all information is correct and up-to-date
- **Be Clear**: Use simple, direct language
- **Be Complete**: Cover the most common scenarios

### Dual Format Guidelines

All playbooks must include **both** NLP (AI agent) and CLI (DevOps/SRE) versions of the Playbook section.

**Structure:**

```markdown
## Playbook

### For AI Agents (NLP)

1. Describe pod `<pod-name>` in namespace `<namespace>` to see pod status...

2. Retrieve events in namespace `<namespace>` for pod `<pod-name>`...

### For DevOps/SREs (CLI)

1. Check pod status and events:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. Get events sorted by timestamp:
   ```bash
   kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
   ```
```

**Key Rules:**

| Rule | Description |
|------|-------------|
| Same step numbers | Steps 1, 2, 3... must match between NLP and CLI |
| Consistent placeholders | Use `<placeholder-name>` format in both sections |
| CLI code blocks | Always use ` ```bash ` for CLI commands |
| Production-ready | CLI commands should be copy-paste ready |

**Contributing:**

You can contribute either format and the maintainers will generate the other:

- **Submit NLP only** → We'll add CLI commands
- **Submit CLI only** → We'll add NLP descriptions
- **Submit both** → Preferred for faster merge

**Provider-Specific Commands:**

| Provider | Primary CLI Tool | Example |
|----------|------------------|---------|
| Kubernetes | `kubectl` | `kubectl get pods -n <namespace>` |
| AWS | `aws` | `aws ec2 describe-instances --instance-ids <instance-id>` |
| Sentry | `sentry-cli` / `curl` | `sentry-cli issues list --project <project>` |

**GitHub Pages Toggle:**

The documentation site includes a toggle (NLP / CLI / Both) that lets users view their preferred format. This is powered by CSS classes added by a Docsify plugin.

### AWS Playbook Requirements

- Must use only available AWS MCP tools
- Include CloudWatch Logs queries where relevant
- Reference specific AWS service documentation
- Include IAM permission requirements if applicable

### Kubernetes Playbook Requirements

- Include YAML front matter with metadata
- Use correct kubectl commands
- Reference Kubernetes API versions if relevant
- Include namespace considerations
- Place in appropriate category folder

### Naming Conventions

**AWS Playbooks:**
- Format: `<IssueOrSymptom>-<Component>.md`
- Examples:
  - `Connection-Timeout-SSH-Issues-EC2.md`
  - `Bucket-Access-Denied-403-Error-S3.md`

**Kubernetes Playbooks:**
- Format: `<AlertName>-<Resource>.md`
- Examples:
  - `KubePodCrashLooping-pod.md`
  - `ServiceNotResolvingDNS-dns.md`

**Sentry Playbooks:**
- Format: `<ErrorType>-<SubType>-<Component>-Error-application.md`
- Examples:
  - `ConnectionError-ConnectionRefused-Database-Error-application.md`
  - `TimeoutError-QueryTimeout-Database-Error-application.md`

### Location Guidelines

- **AWS Playbooks**: Place in appropriate category folder:
  - Compute issues (EC2, Lambda, ECS, EKS) → `AWS Playbooks/01-Compute/`
  - Database issues (RDS, DynamoDB) → `AWS Playbooks/02-Database/`
  - Storage issues (S3) → `AWS Playbooks/03-Storage/`
  - Networking issues (VPC, ELB, Route 53) → `AWS Playbooks/04-Networking/`
  - Security issues (IAM, KMS, WAF) → `AWS Playbooks/05-Security/`
  - Monitoring issues (CloudWatch, CloudTrail) → `AWS Playbooks/06-Monitoring/`
  - CI/CD issues (CodePipeline, CloudFormation) → `AWS Playbooks/07-CI-CD/`
  - Proactive monitoring → `AWS Playbooks/08-Proactive/`

- **K8s Playbooks**: Place in appropriate category folder:
  - Control plane issues → `K8s Playbooks/01-Control-Plane/`
  - Node issues → `K8s Playbooks/02-Nodes/`
  - Pod issues → `K8s Playbooks/03-Pods/`
  - Workload issues → `K8s Playbooks/04-Workloads/`
  - Networking issues → `K8s Playbooks/05-Networking/`
  - Storage issues → `K8s Playbooks/06-Storage/`
  - RBAC issues → `K8s Playbooks/07-RBAC/`
  - Configuration issues → `K8s Playbooks/08-Configuration/`
  - Resource management → `K8s Playbooks/09-Resource-Management/`
  - Monitoring/Autoscaling → `K8s Playbooks/10-Monitoring-Autoscaling/`
  - Installation/Setup → `K8s Playbooks/11-Installation-Setup/`
  - Namespace issues → `K8s Playbooks/12-Namespaces/`
  - Proactive monitoring → `K8s Playbooks/13-Proactive/`

- **Sentry Playbooks**: Place in appropriate category folder:
  - Error tracking issues → `Sentry Playbooks/01-Error-Tracking/`
  - Performance issues → `Sentry Playbooks/02-Performance/`
  - Release health issues → `Sentry Playbooks/03-Release-Health/`

## Exemplary Playbooks

Study these well-structured playbooks as reference examples before creating your own:

### AWS Example: EC2 SSH Connection Timeout

**File:** [`AWS Playbooks/01-Compute/Connection-Timeout-SSH-Issues-EC2.md`](AWS%20Playbooks/01-Compute/Connection-Timeout-SSH-Issues-EC2.md)

**Why it's exemplary:**
- Clear, descriptive title following naming convention
- Comprehensive Meaning section with multiple root causes
- Well-structured Impact section with business implications
- 10 numbered diagnostic steps ordered from common to specific
- Thorough Diagnosis section with time-based correlation

### Kubernetes Example: CrashLoopBackOff

**File:** [`K8s Playbooks/03-Pods/CrashLoopBackOff-pod.md`](K8s%20Playbooks/03-Pods/CrashLoopBackOff-pod.md)

**Why it's exemplary:**
- Standard alert-based naming convention
- Covers all common causes in Meaning section
- Clear severity indicators in Impact section
- Actionable steps using kubectl commands
- Conditional logic in Diagnosis ("If X, then Y")

### Sentry Example: Unhandled Exception

**File:** [`Sentry Playbooks/01-Error-Tracking/UnhandledException-Error-application.md`](Sentry%20Playbooks/01-Error-Tracking/UnhandledException-Error-application.md)

**Why it's exemplary:**
- Follows Sentry naming convention exactly
- Cross-domain keywords for multi-source matching
- Clear diagnostic flow for error tracking
- Integration-aware troubleshooting steps

### Proactive Example: Cost Anomaly Detection

**File:** [`AWS Playbooks/08-Proactive/04-Cost-Optimization/Cost-Anomaly-Detection-AWS.md`](AWS%20Playbooks/08-Proactive/04-Cost-Optimization/Cost-Anomaly-Detection-AWS.md)

**Why it's exemplary:**
- Proactive monitoring focus (not reactive)
- Threshold-based alerting guidance
- Integration with AWS Cost Explorer
- Business impact clearly stated

## Pull Request Process

### Before Submitting

- [ ] Playbook follows the required structure
- [ ] All placeholders are used correctly
- [ ] Steps are numbered and ordered logically
- [ ] Diagnosis section includes correlation analysis
- [ ] README is updated (if adding new playbook)
- [ ] No typos or grammatical errors
- [ ] Commits are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New playbook (addition of new playbook)
- [ ] Enhancement (improvement to existing playbook)
- [ ] Documentation (documentation changes only)

## Related Issue
Closes #(issue number)

## Testing
Describe how you tested your changes

## Checklist
- [ ] Follows playbook structure
- [ ] Uses placeholders correctly
- [ ] Includes correlation analysis
- [ ] README updated (if applicable)
- [ ] No typos or errors
```

### PR Review Criteria

Maintainers will review PRs based on:

1. **Structure**: Follows required playbook structure
2. **Accuracy**: Information is correct and up-to-date
3. **Clarity**: Instructions are clear and actionable
4. **Completeness**: Covers the issue comprehensively
5. **Consistency**: Matches style of existing playbooks
6. **Testing**: Has been tested in real scenarios (if applicable)

## Review Process

1. **Initial Review**: Maintainers review within 2-3 business days
2. **Feedback**: Any requested changes will be communicated
3. **Revisions**: Address feedback and update PR
4. **Approval**: Once approved, PR will be merged
5. **Merge**: Changes will be merged to master branch

### Common Feedback Points

- Structure not followed correctly
- Missing required sections
- Placeholders not used consistently
- Steps not actionable enough
- Diagnosis section incomplete
- Typos or grammatical errors
- Inconsistent formatting

## Questions?

- **GitHub Issues**: Create an issue with the `question` label
- **Slack**: Ask in our [Slack workspace](https://scoutflo.slack.com)
- **Discussions**: Use [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)

## Scoutflo Resources

- **Official Documentation**: [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation)
- **Website**: [scoutflo.com](https://scoutflo.com/)
- **AI SRE Tool**: [ai.scoutflo.com](https://ai.scoutflo.com/get-started)
- **Infra Management Tool**: [deploy.scoutflo.com](https://deploy.scoutflo.com/)
- **YouTube**: [@scoutflo6727](https://www.youtube.com/@scoutflo6727)
- **LinkedIn**: [Scoutflo](https://www.linkedin.com/company/scoutflo/)
- **Twitter/X**: [@scout_flo](https://x.com/scout_flo)
- **Blog**: [scoutflo.com/blog](https://scoutflo.com/blog) | [blog.scoutflo.com](https://blog.scoutflo.com/)

## Recognition

Contributors will be recognized in:
- GitHub Contributors page
- Release notes (for significant contributions)
- Project acknowledgments

Thank you for contributing to the SRE Playbooks repository! Your contributions help the entire SRE community.
