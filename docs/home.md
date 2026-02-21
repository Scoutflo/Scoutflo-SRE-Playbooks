# SRE Playbooks

> **414 production-ready incident response playbooks** for Kubernetes, AWS, and Sentry environments.

<div class="stats-container">
  <div class="stat-card aws">
    <div class="stat-number">157</div>
    <div class="stat-label">AWS Playbooks</div>
  </div>
  <div class="stat-card k8s">
    <div class="stat-number">232</div>
    <div class="stat-label">K8s Playbooks</div>
  </div>
  <div class="stat-card sentry">
    <div class="stat-number">25</div>
    <div class="stat-label">Sentry Playbooks</div>
  </div>
</div>

## What are SRE Playbooks?

SRE Playbooks are **step-by-step guides** for diagnosing and resolving incidents. Each playbook covers a specific alert or error condition and provides:

- **Meaning**: What the issue is and why it occurs
- **Impact**: Business and technical consequences
- **Playbook**: Step-by-step diagnostic procedures
- **Diagnosis**: Root cause analysis with conditional logic

## Quick Start

### By Provider

| Provider | Use Case | Get Started |
|----------|----------|-------------|
| **AWS** | EC2, Lambda, RDS, S3, IAM issues | [AWS Playbooks](/aws/) |
| **Kubernetes** | Pods, Deployments, Services, Nodes | [K8s Playbooks](/k8s/) |
| **Sentry** | Application errors, performance | [Sentry Playbooks](/sentry/) |

### By Issue Type

| Issue | Recommended Playbook |
|-------|---------------------|
| Pod crashing repeatedly | [CrashLoopBackOff](/k8s/03-pods?id=crashloopbackoff) |
| Pod stuck pending | [PendingPods](/k8s/03-pods?id=pendingpods) |
| EC2 unreachable | [Connection Timeout](/aws/01-compute?id=connection-timeout) |
| High Lambda latency | [Lambda Timeout](/aws/01-compute?id=lambda-timeout) |
| Application exceptions | [Unhandled Exception](/sentry/01-error-tracking) |

## Playbook Categories

### AWS Playbooks

<div class="category-grid">
  <a href="#/aws/01-compute" class="category-card">
    <h4>01 - Compute</h4>
    <p>27 playbooks for EC2, Lambda, ECS, EKS, Fargate</p>
  </a>
  <a href="#/aws/02-database" class="category-card">
    <h4>02 - Database</h4>
    <p>8 playbooks for RDS, DynamoDB</p>
  </a>
  <a href="#/aws/03-storage" class="category-card">
    <h4>03 - Storage</h4>
    <p>7 playbooks for S3</p>
  </a>
  <a href="#/aws/04-networking" class="category-card">
    <h4>04 - Networking</h4>
    <p>17 playbooks for VPC, ELB, Route53</p>
  </a>
  <a href="#/aws/05-security" class="category-card">
    <h4>05 - Security</h4>
    <p>16 playbooks for IAM, KMS, GuardDuty</p>
  </a>
  <a href="#/aws/06-monitoring" class="category-card">
    <h4>06 - Monitoring</h4>
    <p>8 playbooks for CloudTrail, CloudWatch</p>
  </a>
  <a href="#/aws/07-cicd" class="category-card">
    <h4>07 - CI/CD</h4>
    <p>9 playbooks for CodePipeline, CodeBuild</p>
  </a>
  <a href="#/aws/08-proactive" class="category-card">
    <h4>08 - Proactive</h4>
    <p>65 proactive monitoring playbooks</p>
  </a>
</div>

### Kubernetes Playbooks

<div class="category-grid">
  <a href="#/k8s/01-control-plane" class="category-card">
    <h4>01 - Control Plane</h4>
    <p>24 playbooks for API Server, etcd, CertManager</p>
  </a>
  <a href="#/k8s/02-nodes" class="category-card">
    <h4>02 - Nodes</h4>
    <p>24 playbooks for Node issues, NodeExporter</p>
  </a>
  <a href="#/k8s/03-pods" class="category-card">
    <h4>03 - Pods</h4>
    <p>41 playbooks for Pod lifecycle, Containers</p>
  </a>
  <a href="#/k8s/04-workloads" class="category-card">
    <h4>04 - Workloads</h4>
    <p>25 playbooks for Deployments, Jobs</p>
  </a>
  <a href="#/k8s/05-networking" class="category-card">
    <h4>05 - Networking</h4>
    <p>27 playbooks for Services, Ingress, CoreDNS</p>
  </a>
  <a href="#/k8s/06-storage" class="category-card">
    <h4>06 - Storage</h4>
    <p>9 playbooks for PV, PVC</p>
  </a>
  <a href="#/k8s/07-rbac" class="category-card">
    <h4>07 - RBAC</h4>
    <p>6 playbooks for Permissions</p>
  </a>
  <a href="#/k8s/08-configuration" class="category-card">
    <h4>08 - Configuration</h4>
    <p>6 playbooks for ConfigMaps, Secrets</p>
  </a>
  <a href="#/k8s/09-resource-management" class="category-card">
    <h4>09 - Resource Management</h4>
    <p>8 playbooks for Quotas</p>
  </a>
  <a href="#/k8s/10-monitoring-autoscaling" class="category-card">
    <h4>10 - Monitoring</h4>
    <p>3 playbooks for HPA, Metrics</p>
  </a>
  <a href="#/k8s/13-proactive" class="category-card">
    <h4>13 - Proactive</h4>
    <p>56 proactive monitoring playbooks</p>
  </a>
</div>

### Sentry Playbooks

<div class="category-grid">
  <a href="#/sentry/01-error-tracking" class="category-card">
    <h4>01 - Error Tracking</h4>
    <p>19 playbooks for Exception handling</p>
  </a>
  <a href="#/sentry/02-performance" class="category-card">
    <h4>02 - Performance</h4>
    <p>6 playbooks for Timeout, latency</p>
  </a>
  <a href="#/sentry/03-release-health" class="category-card">
    <h4>03 - Release Health</h4>
    <p>Release correlation playbooks</p>
  </a>
</div>

## Understanding Playbook Steps

These playbooks are designed for **AI agents** using natural language processing. The steps use action verbs like:

- "Retrieve pod `<pod-name>` in namespace `<namespace>` and check status"
- "List events for deployment `<deployment-name>` and analyze failures"
- "Describe EC2 instance `<instance-id>` and verify security groups"

Each step includes a collapsible **CLI Equivalent** section for manual troubleshooting:

<details>
<summary>Example: CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

</details>

## Contributing

We welcome contributions! See our [Contributing Guide](/contributing) to get started.

**Quick ways to contribute:**
- Add CLI equivalents to existing playbooks
- Create new playbooks for uncovered scenarios
- Improve documentation and examples
- Report issues and suggest improvements

## Links

- [GitHub Repository](https://github.com/Scoutflo/scoutflo-SRE-Playbooks)
- [Changelog](/changelog)
- [Roadmap](/roadmap)
- [Code of Conduct](/code-of-conduct)

---

<p style="text-align: center; color: #64748b;">
  Made with care by <a href="https://scoutflo.com">Scoutflo</a> | MIT License
</p>
