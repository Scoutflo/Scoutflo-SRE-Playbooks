# Overview

Production-ready incident response playbooks for Kubernetes, AWS, and Sentry environments.

---

> **NEW: Dual-Format Playbooks!** Each playbook now includes both NLP (AI Agent) and CLI (DevOps/SRE) versions. Use the **NLP / CLI / Both** toggle in the top-right corner to switch formats. [Try the demo →](/dual-format-demo)

---

## Browse Playbooks

| Provider | Playbooks | Categories |
|----------|-----------|------------|
| [Kubernetes](/k8s/) | 232 | Control Plane, Nodes, Pods, Workloads, Networking, Storage |
| [AWS](/aws/) | 157 | Compute, Database, Storage, Networking, Security, CI/CD |
| [Sentry](/sentry/) | 25 | Error Tracking, Performance, Release Health |

---

## Kubernetes

<div class="category-grid">
  <a href="#/k8s/01-control-plane" class="category-card">
    <h4>Control Plane</h4>
    <p>API Server, etcd, CertManager — 24 playbooks</p>
  </a>
  <a href="#/k8s/02-nodes" class="category-card">
    <h4>Nodes</h4>
    <p>Node health, Kubelet, NodeExporter — 24 playbooks</p>
  </a>
  <a href="#/k8s/03-pods" class="category-card">
    <h4>Pods</h4>
    <p>Pod lifecycle, Containers — 41 playbooks</p>
  </a>
  <a href="#/k8s/04-workloads" class="category-card">
    <h4>Workloads</h4>
    <p>Deployments, Jobs, DaemonSets — 25 playbooks</p>
  </a>
  <a href="#/k8s/05-networking" class="category-card">
    <h4>Networking</h4>
    <p>Services, Ingress, CoreDNS — 27 playbooks</p>
  </a>
  <a href="#/k8s/06-storage" class="category-card">
    <h4>Storage</h4>
    <p>PV, PVC, StorageClass — 9 playbooks</p>
  </a>
</div>

[View all Kubernetes playbooks →](/k8s/)

---

## AWS

<div class="category-grid">
  <a href="#/aws/01-compute" class="category-card">
    <h4>Compute</h4>
    <p>EC2, Lambda, ECS, EKS — 27 playbooks</p>
  </a>
  <a href="#/aws/02-database" class="category-card">
    <h4>Database</h4>
    <p>RDS, DynamoDB — 8 playbooks</p>
  </a>
  <a href="#/aws/04-networking" class="category-card">
    <h4>Networking</h4>
    <p>VPC, ELB, Route53 — 17 playbooks</p>
  </a>
  <a href="#/aws/05-security" class="category-card">
    <h4>Security</h4>
    <p>IAM, KMS, GuardDuty — 16 playbooks</p>
  </a>
</div>

[View all AWS playbooks →](/aws/)

---

## Sentry

<div class="category-grid">
  <a href="#/sentry/01-error-tracking" class="category-card">
    <h4>Error Tracking</h4>
    <p>Exception handling — 19 playbooks</p>
  </a>
  <a href="#/sentry/02-performance" class="category-card">
    <h4>Performance</h4>
    <p>Timeout, latency — 6 playbooks</p>
  </a>
</div>

[View all Sentry playbooks →](/sentry/)

---

## Playbook Structure

Each playbook includes four sections:

| Section | Description |
|---------|-------------|
| **Meaning** | What the issue is and why it occurs |
| **Impact** | Business and technical consequences |
| **Playbook** | Step-by-step procedures (NLP + CLI formats) |
| **Diagnosis** | Root cause analysis with conditional logic |

### Dual-Format Playbook Section

The Playbook section now includes **two formats**:

| Format | Audience | Description |
|--------|----------|-------------|
| **For AI Agents (NLP)** | AI automation tools | Natural language instructions |
| **For DevOps/SREs (CLI)** | Human operators | Copy-paste ready CLI commands |

Use the toggle in the top-right to switch between formats.

---

## Contributing

See the [Contributing Guide](/contributing) to add new playbooks or improve existing ones.

---

<p style="text-align: center; color: var(--muted-foreground); font-size: 0.8125rem;">
  Open source by <a href="https://scoutflo.com">Scoutflo</a>
</p>
