# SRE Playbooks Repository

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/Scoutflo/scoutflo-SRE-Playbooks)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)
[![GitHub Stars](https://img.shields.io/github/stars/Scoutflo/scoutflo-SRE-Playbooks)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Scoutflo/scoutflo-SRE-Playbooks)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/network/members)
[![GitHub Discussions](https://img.shields.io/github/discussions/Scoutflo/scoutflo-SRE-Playbooks)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
[![GitHub Contributors](https://img.shields.io/github/contributors/Scoutflo/scoutflo-SRE-Playbooks)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/graphs/contributors)

> **Comprehensive incident response playbooks for AWS, Kubernetes, and Sentry environments** - Helping SREs diagnose and resolve infrastructure issues faster with systematic, step-by-step troubleshooting guides.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Contents](#contents)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Terminology & Glossary](#terminology--glossary)
- [Quick Reference](#quick-reference)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Examples & Use Cases](#examples--use-cases)
- [FAQ](#faq)
- [Video Tutorials](#video-tutorials)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Connect with Us](#connect-with-us)
- [Support](#support)
- [Related Resources](#related-resources)
- [License](#license)

## Overview

This repository contains **414 comprehensive incident response playbooks** designed to help Site Reliability Engineers (SREs) systematically diagnose and resolve common infrastructure and application issues in AWS, Kubernetes, and Sentry environments.

### Why This Repository?

- **Systematic Approach**: Each playbook follows a consistent structure with clear diagnostic steps
- **Time-Saving**: Quickly identify root causes with correlation analysis frameworks
- **Community-Driven**: Continuously improved by the open-source community
- **Production-Ready**: Based on real-world incident response scenarios
- **Comprehensive Coverage**: 232 Kubernetes playbooks + 157 AWS playbooks + 25 Sentry playbooks
- **Proactive Monitoring**: 56 K8s + 65 AWS proactive playbooks for capacity planning and compliance

### Diagnosis Improvements

All playbooks use an **events-first approach** for root cause analysis:
- Diagnosis sections prioritize checking recent events and changes before diving into configuration details
- Conditional logic patterns help narrow down causes based on observed symptoms
- Time-based correlation analysis connects events to failures systematically

### Use Cases

- **During Incidents**: Quick reference for troubleshooting common issues
- **On-Call Rotation**: Essential runbook collection for on-call engineers
- **Knowledge Sharing**: Standardize troubleshooting procedures across teams
- **Training**: Learn systematic incident response methodologies
- **Documentation**: Build your own runbook library

## Repository Structure

```
scoutflo-SRE-Playbooks/
├── AWS Playbooks/                    # 157 AWS playbooks
│   ├── 01-Compute/                   # 27 playbooks (EC2, Lambda, ECS, EKS)
│   ├── 02-Database/                  # 8 playbooks (RDS, DynamoDB)
│   ├── 03-Storage/                   # 7 playbooks (S3)
│   ├── 04-Networking/                # 17 playbooks (VPC, ELB, Route53)
│   ├── 05-Security/                  # 16 playbooks (IAM, KMS, GuardDuty)
│   ├── 06-Monitoring/                # 8 playbooks (CloudTrail, CloudWatch)
│   ├── 07-CI-CD/                     # 9 playbooks (CodePipeline, CodeBuild)
│   ├── 08-Proactive/                 # 65 proactive monitoring playbooks
│   └── README.md
├── K8s Playbooks/                    # 232 Kubernetes playbooks
│   ├── 01-Control-Plane/             # 24 playbooks
│   ├── 02-Nodes/                     # 24 playbooks
│   ├── 03-Pods/                      # 41 playbooks
│   ├── 04-Workloads/                 # 25 playbooks
│   ├── 05-Networking/                # 27 playbooks
│   ├── 06-Storage/                   # 9 playbooks
│   ├── 07-RBAC/                      # 6 playbooks
│   ├── 08-Configuration/             # 6 playbooks
│   ├── 09-Resource-Management/       # 8 playbooks
│   ├── 10-Monitoring-Autoscaling/    # 3 playbooks
│   ├── 11-Installation-Setup/        # 1 playbook
│   ├── 12-Namespaces/                # 2 playbooks
│   ├── 13-Proactive/                 # 56 proactive monitoring playbooks
│   └── README.md
├── Sentry Playbooks/                 # 25 Sentry playbooks
│   ├── 01-Error-Tracking/            # 19 playbooks
│   ├── 02-Performance/               # 6 playbooks
│   ├── 03-Release-Health/            # Placeholder
│   └── README.md
├── CONTRIBUTING.md
└── README.md
```

## Contents

### AWS Playbooks (`AWS Playbooks/`)

**157 playbooks** covering 7 service categories + proactive monitoring:

- **Compute Services** (27 playbooks): EC2, Lambda, ECS, EKS
- **Database** (8 playbooks): RDS, DynamoDB
- **Storage** (7 playbooks): S3
- **Networking** (17 playbooks): VPC, ELB, Route 53, NAT Gateway
- **Security** (16 playbooks): IAM, KMS, GuardDuty, CloudTrail
- **Monitoring** (8 playbooks): CloudTrail, CloudWatch
- **CI/CD** (9 playbooks): CodePipeline, CodeBuild
- **Proactive** (65 playbooks): Capacity planning, compliance, cost optimization

**Key Topics:**
- Connection timeouts and network issues
- Access denied and permission problems
- Resource unavailability and capacity issues
- Security breaches and threat detection
- Service integration failures
- Proactive capacity and compliance monitoring

See [AWS Playbooks/README.md](AWS%20Playbooks/README.md) for complete documentation and playbook list.

### Kubernetes Playbooks (`K8s Playbooks/`)

**194 playbooks** organized into **13 categorized folders** covering Kubernetes cluster and workload issues:

**Folder Structure:**
- `01-Control-Plane/` (18 playbooks) - API Server, Scheduler, Controller Manager, etcd
- `02-Nodes/` (12 playbooks) - Node readiness, kubelet issues, resource constraints
- `03-Pods/` (31 playbooks) - Scheduling, lifecycle, health checks, resource limits
- `04-Workloads/` (23 playbooks) - Deployments, StatefulSets, DaemonSets, Jobs, HPA
- `05-Networking/` (19 playbooks) - Services, Ingress, DNS, Network Policies, kube-proxy
- `06-Storage/` (9 playbooks) - PersistentVolumes, PersistentVolumeClaims, StorageClasses
- `07-RBAC/` (6 playbooks) - ServiceAccounts, Roles, RoleBindings, authorization
- `08-Configuration/` (6 playbooks) - ConfigMaps and Secrets access issues
- `09-Resource-Management/` (8 playbooks) - Resource Quotas, overcommit, compute resources
- `10-Monitoring-Autoscaling/` (3 playbooks) - Metrics Server, Cluster Autoscaler
- `11-Installation-Setup/` (1 playbook) - Helm and installation issues
- `12-Namespaces/` (2 playbooks) - Namespace management issues
- `13-Proactive/` (56 playbooks) - Proactive monitoring, capacity planning, compliance

**Key Topics:**
- Pod lifecycle issues (CrashLoopBackOff, Pending, Terminating)
- Control plane component failures
- Network connectivity and DNS resolution
- Storage and volume mounting problems
- RBAC and permission errors
- Resource quota and capacity constraints
- Proactive capacity and compliance monitoring

See [K8s Playbooks/README.md](K8s%20Playbooks/README.md) for complete documentation and playbook list.

### Sentry Playbooks (`Sentry Playbooks/`)

**25 playbooks** covering error tracking and performance monitoring:

**Folder Structure:**
- `01-Error-Tracking/` (19 playbooks) - Error capture, grouping, alerting, and debugging
- `02-Performance/` (6 playbooks) - Transaction monitoring, performance issues, tracing
- `03-Release-Health/` - Release tracking and health monitoring (placeholder)

**Key Topics:**
- Error capture and reporting issues
- Issue grouping and deduplication
- Alert configuration and routing
- Performance transaction monitoring
- SDK integration troubleshooting
- Release health tracking

See [Sentry Playbooks/README.md](Sentry%20Playbooks/README.md) for complete documentation and playbook list.

## Getting Started

### Prerequisites

- Basic knowledge of AWS services, Kubernetes, or Sentry
- Access to AWS Console, Kubernetes cluster, or Sentry dashboard (for using playbooks)
- Git (for cloning the repository)

### Installation

#### Option 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git

# Navigate to the repository
cd scoutflo-SRE-Playbooks

# View available playbooks
ls AWS\ Playbooks/
ls K8s\ Playbooks/
ls Sentry\ Playbooks/
```

#### Option 2: Use as Git Submodule

Include playbooks in your own projects:

```bash
git submodule add https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git playbooks
```

#### Option 3: Download Specific Playbooks

Browse and download individual playbooks directly from GitHub web interface.

### Quick Start

1. **Identify Your Issue**: Determine if it's an AWS, Kubernetes, or Sentry issue
2. **Navigate to Playbooks**:
   - AWS issues -> `AWS Playbooks/`
   - K8s issues -> `K8s Playbooks/[category-folder]/`
   - Sentry issues -> `Sentry Playbooks/[category-folder]/`
3. **Find the Playbook**: Match your symptoms to a playbook title
4. **Follow the Steps**: Execute diagnostic steps in order
5. **Use Diagnosis Section**: Apply correlation analysis for root cause identification

### Learn More

- **Watch Tutorials**: Check our [YouTube channel](https://www.youtube.com/@scoutflo6727) for video walkthroughs and best practices
- **AI SRE Demo**: Watch the [Scoutflo AI SRE Demo](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) to see AI-powered incident response
- **Scoutflo Documentation**: Visit [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) for platform guides
- **Join the Community**: Connect with other SREs in our [Slack workspace](https://scoutflo.slack.com)

### Example Usage

**Scenario**: EC2 instance SSH connection timeout

1. Navigate to `AWS Playbooks/`
2. Open `Connection-Timeout-SSH-Issues-EC2.md`
3. Follow the Playbook steps, replacing `<instance-id>` with your actual instance ID
4. Use the Diagnosis section to correlate events with failures
5. Apply the identified fix

## Usage

### How Playbooks Work

**Important**: These playbooks are designed for **AI agents** using natural language processing (NLP). They use natural language instructions that AI agents interpret and execute using available tools (like AWS MCP tools, Kubernetes MCP tools, or kubectl).

**Example Playbook Step:**
- Natural Language: "Retrieve logs from pod `<pod-name>` in namespace `<namespace>` and analyze error messages"
- AI Agent Action: Interprets this instruction and uses appropriate tools to fetch and analyze pod logs

**For Manual Use:**
- While playbooks are optimized for AI agents, you can also use them manually
- The README files in each category folder include equivalent kubectl/AWS CLI commands for manual verification
- Replace placeholders with actual resource identifiers when following steps manually

### Playbook Structure

All playbooks follow a consistent structure:

1. **Title** - Clear, descriptive issue identification
2. **Meaning** - What the issue means, triggers, symptoms, root causes
3. **Impact** - Business and technical implications
4. **Playbook** - 8-10 numbered diagnostic steps in natural language (ordered from common to specific)
5. **Diagnosis** - Correlation analysis framework with time windows using events-first approach and conditional logic patterns

### Best Practices

- **For AI Agents**: Playbooks are optimized for AI interpretation - use natural language instructions
- **For Manual Use**: See category README files for equivalent kubectl/AWS CLI commands
- **Replace Placeholders**: All playbooks use placeholders (e.g., `<instance-id>`, `<pod-name>`) that must be replaced with actual values
- **Follow Order**: Execute steps sequentially unless you have strong evidence pointing to a specific step
- **Correlate Timestamps**: Use the Diagnosis section to correlate events with failures
- **Extend Windows**: If initial correlations don't reveal causes, extend time windows as suggested

### Placeholder Reference

**AWS Playbooks:**
- `<instance-id>`, `<bucket-name>`, `<region>`, `<function-name>`, `<role-name>`, `<user-name>`, `<security-group-id>`, `<vpc-id>`, `<rds-instance-id>`, `<load-balancer-name>`

**Kubernetes Playbooks:**
- `<pod-name>`, `<namespace>`, `<deployment-name>`, `<node-name>`, `<service-name>`, `<ingress-name>`, `<pvc-name>`, `<configmap-name>`, `<secret-name>`

**Sentry Playbooks:**
- `<project-slug>`, `<organization-slug>`, `<issue-id>`, `<transaction-name>`, `<release-version>`, `<environment>`

## Terminology & Glossary

Understanding the terms used in these playbooks will help you use them more effectively. For detailed glossaries, see:
- [AWS Terminology](AWS%20Playbooks/README.md#terminology--glossary)
- [Kubernetes Terminology](K8s%20Playbooks/README.md#terminology--glossary)

### Quick Reference

**SRE (Site Reliability Engineering)**
- A discipline combining software engineering and operations to build reliable systems.

**Playbook / Runbook**
- A step-by-step guide for diagnosing and resolving specific issues.

**Incident**
- An event that disrupts or degrades a service, requiring immediate attention.

**On-Call**
- Engineers available to respond to incidents outside normal business hours.

**MTTR (Mean Time To Recovery)**
- Average time to restore a service after an incident. Playbooks help reduce MTTR.

**Correlation Analysis**
- Finding relationships between events (like configuration changes) and symptoms (like service failures) by comparing timestamps.

**Root Cause**
- The underlying reason why an issue occurred, as opposed to just the symptoms.

**Placeholder**
- A value in playbooks (like `<instance-id>`) that you replace with your actual resource identifier.

**Diagnosis Section**
- Part of each playbook that helps you correlate events with failures using time-based analysis.

### Common Abbreviations

- **K8s**: Kubernetes (K + 8 letters + s)
- **SRE**: Site Reliability Engineering
- **MTTR**: Mean Time To Recovery
- **API**: Application Programming Interface
- **DNS**: Domain Name System
- **RBAC**: Role-Based Access Control
- **PVC**: PersistentVolumeClaim
- **HPA**: Horizontal Pod Autoscaler

---

**For detailed explanations of AWS and Kubernetes terms, see the respective README files above.**

## Quick Reference

Need a quick cheat sheet? Check out our [Quick Reference Card](QUICK_REFERENCE.md) for:
- One-page overview
- Common commands
- Quick lookup tables
- Essential links

## Troubleshooting Guide

Not sure which playbook to use? Use our [Troubleshooting Decision Tree](TROUBLESHOOTING_FLOWCHART.md) to:
- Quickly identify the right playbook
- Navigate by issue type
- Look up by error message or alert name

## Examples & Use Cases

See real-world scenarios in [EXAMPLES.md](EXAMPLES.md):
- Step-by-step examples
- Common workflows
- Success stories
- Best practices

## FAQ

Have questions? Check our [FAQ](FAQ.md) for answers to:
- General questions
- Usage questions
- Technical questions
- Contributing questions

## Video Tutorials

Learn how to use these playbooks effectively:

- **YouTube Channel**: [@scoutflo6727](https://www.youtube.com/@scoutflo6727) - Subscribe for tutorials and walkthroughs
- **AI SRE Demo**: [Watch Demo Video](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) - See Scoutflo AI SRE in action
- **Tutorials**: Step-by-step video guides on using playbooks
- **Best Practices**: Learn SRE incident response best practices

**Coming Soon**: Video tutorials for:
- How to use playbooks effectively
- Common troubleshooting scenarios
- Contributing to playbooks
- Advanced correlation analysis

## Roadmap

Check out our [ROADMAP.md](ROADMAP.md) to see:
- Planned features and new playbook categories
- Short-term and long-term goals
- How to suggest new features
- Release history

## Contributing

We welcome contributions from the community! Your contributions help make these playbooks better for everyone. See our [Contributors](CONTRIBUTORS.md) page to see who has helped build this project.

> **First-time contributor?** Start with our [Getting Started Guide](.github/GETTING_STARTED.md) for a quick onboarding experience, then look for issues labeled `good first issue`.

### How to Contribute

#### 1. Reporting Issues

Found a bug, unclear instruction, or have a suggestion?

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) first
2. **Create a New Issue**:
   - Use clear, descriptive title
   - Describe the problem or suggestion
   - Include relevant service/component, error messages, or examples
   - Tag with appropriate labels (`aws-playbook`, `k8s-playbook`, `sentry-playbook`, `bug`, `enhancement`, etc.)

#### 2. Improving Existing Playbooks

To fix or enhance existing playbooks:

1. **Fork the Repository**: Create your own fork
2. **Create a Branch**:
   ```bash
   git checkout -b fix/playbook-name-improvement
   ```
3. **Make Your Changes**:
   - Follow the established playbook structure
   - Maintain consistency with existing formatting
   - Update placeholders and examples as needed
4. **Test Your Changes**: Verify the playbook is accurate and helpful
5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Fix: Improve [playbook-name] with [description]"
   git push origin fix/playbook-name-improvement
   ```
6. **Create a Pull Request**:
   - Provide clear description of changes
   - Reference any related issues
   - Request review from maintainers

#### 3. Adding New Playbooks

To add a new playbook for an uncovered issue:

1. **Check for Duplicates**: Ensure a similar playbook doesn't already exist
2. **Follow the Structure**: Use existing playbooks as templates
3. **Choose the Right Location**:
   - AWS playbooks -> `AWS Playbooks/`
   - K8s playbooks -> Appropriate category folder in `K8s Playbooks/`
   - Sentry playbooks -> Appropriate category folder in `Sentry Playbooks/`
4. **Follow Naming Conventions**:
   - AWS: `<IssueOrSymptom>-<Component>.md`
   - K8s: `<AlertName>-<Resource>.md`
   - Sentry: `<IssueType>-<Component>.md`
5. **Include All Sections**: Title, Meaning, Impact, Playbook (8-10 steps), Diagnosis (5 correlations)
6. **Update README**: Add the new playbook to the appropriate README's playbook list
7. **Create Pull Request**: Follow standard contribution process

### Contribution Guidelines

- **Follow the Structure**: Maintain consistency with existing playbooks
- **Use Placeholders**: Replace specific values with placeholders
- **Be Specific**: Provide actionable, step-by-step instructions
- **Include Correlation**: Add time-based correlation analysis in the Diagnosis section
- **Test Thoroughly**: Ensure playbooks are accurate and helpful
- **Document Changes**: Clearly describe what you changed and why

### Review Process

1. All contributions require review from maintainers
2. Feedback will be provided within 2-3 business days
3. Address any requested changes promptly
4. Once approved, your contribution will be merged

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## Connect with Us

We'd love to hear from you! Here are the best ways to connect:

### Community Channels

- **Slack Community**: [Join our Slack workspace](https://scoutflo.slack.com) for real-time discussions
- **GitHub Discussions**: [Start a discussion](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions) for questions and ideas
- **GitHub Issues**: [Report bugs or request features](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)
- **LinkedIn**: Follow [Scoutflo on LinkedIn](https://www.linkedin.com/company/scoutflo/) for updates and insights
- **Twitter/X**: Follow [@scout_flo](https://x.com/scout_flo) for latest news and announcements

### Feedback & Feature Requests

Have an idea for improvement or a new playbook topic?

- **GitHub Issues**: Create a [feature request](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=feature_request.md)
- **Slack**: Share your ideas in our `#playbooks` channel

### Bug Reports

Found a bug or error in a playbook?

- **GitHub Issues**: Create a [bug report](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=bug_report.md)
- **Slack**: Report in our `#playbooks` channel for quick response

### Scoutflo Resources

- **Official Documentation**: [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) - Complete guide to Scoutflo platform
- **Website**: [scoutflo.com](https://scoutflo.com/) - Learn more about Scoutflo
- **AI SRE Tool**: [ai.scoutflo.com](https://ai.scoutflo.com/get-started) - AI-powered SRE assistant
- **Infra Management Tool**: [deploy.scoutflo.com](https://deploy.scoutflo.com/) - Kubernetes deployment platform
- **YouTube Channel**: [@scoutflo6727](https://www.youtube.com/@scoutflo6727) - Tutorials and demos
- **AI SRE Demo**: [Watch Demo Video](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) - See Scoutflo AI SRE in action
- **Blog**: [scoutflo.com/blog](https://scoutflo.com/blog) and [blog.scoutflo.com](https://blog.scoutflo.com/) - Latest articles and insights
- **Pricing**: [scoutflo.com/pricing](https://scoutflo.com/pricing) - Pricing information

### Additional Resources

- **Roadmap**: Check out our [project roadmap](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/projects) to see what's coming
- **Documentation**: Visit our [wiki](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/wiki) for detailed guides
- **Legal**: [Privacy Policy](https://blog.scoutflo.com/privacy/) | [Terms of Service](https://blog.scoutflo.com/terms/)

## Support

Need help? Check out our [Support Guide](.github/SUPPORT.md) or:

- **Questions**: [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
- **Bugs**: [Report an issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=bug_report.md)
- **Features**: [Request a feature](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=feature_request.md)
- **Security**: See [SECURITY.md](SECURITY.md)

## Related Resources

### AWS Resources

**Official Documentation:**
- [AWS Documentation](https://docs.aws.amazon.com/) - Complete AWS service documentation
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) - Best practices for building on AWS
- [AWS Troubleshooting Guides](https://docs.aws.amazon.com/general/latest/gr/aws_troubleshooting.html) - Official troubleshooting guides
- [AWS Service Health Dashboard](https://status.aws.amazon.com/) - Check AWS service status

**Learning & Best Practices:**
- [AWS Architecture Center](https://aws.amazon.com/architecture/) - Reference architectures
- [AWS Security Best Practices](https://aws.amazon.com/security/security-resources/) - Security guidelines
- [AWS re:Post](https://repost.aws/) - AWS community Q&A
- [AWS Training](https://aws.amazon.com/training/) - Free and paid training courses

**Tools & Utilities:**
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/) - Command-line interface
- [AWS CloudShell](https://aws.amazon.com/cloudshell/) - Browser-based shell
- [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/) - Operations management
- [AWS CloudWatch](https://docs.aws.amazon.com/cloudwatch/) - Monitoring and observability

### Kubernetes Resources

**Official Documentation:**
- [Kubernetes Documentation](https://kubernetes.io/docs/) - Complete Kubernetes documentation
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) - Quick command reference
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug/) - Official troubleshooting guide
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/) - API documentation

**Learning & Best Practices:**
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/) - Cluster administration
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/) - Security guidelines
- [CNCF Cloud Native Trail Map](https://github.com/cncf/trailmap) - Learning path
- [Kubernetes.io Blog](https://kubernetes.io/blog/) - Latest updates and tutorials

**Tools & Utilities:**
- [k9s](https://k9scli.io/) - Terminal UI for Kubernetes
- [Lens](https://k8slens.dev/) - Kubernetes IDE
- [Helm](https://helm.sh/) - Package manager for Kubernetes
- [kubectx & kubens](https://github.com/ahmetb/kubectx) - Context and namespace switching

**Community Resources:**
- [Kubernetes Slack](https://slack.k8s.io/) - Community chat
- [Stack Overflow - Kubernetes](https://stackoverflow.com/questions/tagged/kubernetes) - Q&A
- [r/kubernetes](https://www.reddit.com/r/kubernetes/) - Reddit community
- [Kubernetes Forum](https://discuss.kubernetes.io/) - Discussion forum

### SRE Resources

**Books & Guides:**
- [Google SRE Book](https://sre.google/books/) - Site Reliability Engineering book
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) - SRE practices
- [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) - Practical SRE guide
- [Building Secure & Reliable Systems](https://sre.google/books/building-secure-reliable-systems/) - Security and reliability

**Learning Resources:**
- [SRE Foundation Course](https://www.cncf.io/certification/training/) - CNCF training
- [SRE Weekly](https://sreweekly.com/) - Weekly newsletter
- [SREcon](https://www.usenix.org/conferences/byname/srecon) - SRE conferences
- [Incident Response Guide](https://response.pagerduty.com/) - PagerDuty's incident response guide

**Tools & Platforms:**
- [Prometheus](https://prometheus.io/) - Monitoring and alerting
- [Grafana](https://grafana.com/) - Visualization and dashboards
- [Jaeger](https://www.jaegertracing.io/) - Distributed tracing
- [ELK Stack](https://www.elastic.co/what-is/elk-stack) - Logging and analysis

### Incident Response & Runbooks

**Runbook Resources:**
- [PagerDuty Incident Response](https://response.pagerduty.com/) - Incident response best practices
- [Atlassian Incident Management](https://www.atlassian.com/incident-management) - Incident management guide
- [GitLab Runbooks](https://about.gitlab.com/handbook/engineering/infrastructure/runbooks/) - Example runbooks
- [Google's SRE Runbook Template](https://sre.google/workbook/runbooks/) - Runbook structure

**Incident Management:**
- [Incident.io](https://incident.io/) - Incident management platform
- [FireHydrant](https://www.firehydrant.com/) - Incident response platform
- [Statuspage](https://www.statuspage.io/) - Status page management

### Community & Forums

**General DevOps:**
- [DevOps Reddit](https://www.reddit.com/r/devops/) - DevOps community
- [DevOps Stack Exchange](https://devops.stackexchange.com/) - Q&A platform
- [HashiCorp Learn](https://learn.hashicorp.com/) - Infrastructure tutorials

**Cloud Native:**
- [CNCF Resources](https://www.cncf.io/) - Cloud Native Computing Foundation
- [Cloud Native Landscape](https://landscape.cncf.io/) - CNCF project landscape
- [CNCF Webinars](https://www.cncf.io/webinars/) - Educational webinars

## Statistics

- **Total Playbooks**: 376
  - AWS: 157 playbooks (92 reactive + 65 proactive)
  - Kubernetes: 194 playbooks (138 reactive + 56 proactive)
  - Sentry: 25 playbooks
- **Coverage**: Major AWS services, Kubernetes components, and Sentry monitoring
- **Format**: Markdown with structured sections
- **Language**: English
- **Community**: Open source, community-driven

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Maintainers

This project is maintained by:

- [@AtharvaBondreScoutflo](https://github.com/AtharvaBondreScoutflo)
- [@Vedant-Vyawahare](https://github.com/Vedant-Vyawahare)

For maintainer information, see [MAINTAINERS.md](MAINTAINERS.md).

## Acknowledgments

- **Contributors**: Thank you to all contributors who help improve these playbooks
- **Community**: The SRE community for sharing knowledge and best practices
- **Organizations**: Companies and teams using these playbooks in production

---

**Made with love by the SRE community for the SRE community**

If you find these playbooks helpful, please consider giving us a star on GitHub!
