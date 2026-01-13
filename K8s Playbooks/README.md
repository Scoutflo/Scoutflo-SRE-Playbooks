# Kubernetes (K8s) Playbooks

[![Kubernetes](https://img.shields.io/badge/Kubernetes-138%20playbooks-blue)](README.md)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](../../CONTRIBUTING.md)

> **138 comprehensive Kubernetes incident response playbooks** organized into 12 categorized folders - Systematic troubleshooting guides for common Kubernetes cluster and workload issues to help SREs diagnose and resolve problems faster.

## 📋 Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Playbook Structure](#playbook-structure)
- [Playbook Categories](#playbook-categories)
- [Getting Started](#getting-started)
- [Usage Guidelines](#usage-guidelines)
- [Quick Navigation Guide](#quick-navigation-guide)
- [Contributing](#contributing)
- [Connect with Us](#connect-with-us)
- [Related Resources](#related-resources)

## Overview

This directory contains **138 Kubernetes incident response playbooks** organized into **12 categorized folders** to help Site Reliability Engineers (SREs) quickly find and diagnose common Kubernetes cluster and workload issues. Each playbook follows a structured format to provide systematic troubleshooting guidance.

### Services & Components Covered

- **Control Plane**: API Server, Scheduler, Controller Manager, etcd
- **Nodes**: Node readiness, kubelet issues, resource constraints
- **Pods**: Scheduling, lifecycle, health checks, resource limits
- **Workloads**: Deployments, StatefulSets, DaemonSets, Jobs
- **Networking**: Services, Ingress, DNS, Network Policies
- **Storage**: PersistentVolumes, PersistentVolumeClaims, StorageClasses
- **RBAC**: ServiceAccounts, Roles, RoleBindings, ClusterRoles
- **Configuration**: ConfigMaps and Secrets
- **Resource Management**: Quotas, ResourceQuotas, overcommit
- **Monitoring**: Metrics Server, HPA, resource quotas
- **Autoscaling**: Cluster Autoscaler, HPA scaling

## Directory Structure

Playbooks are organized into numbered folders by category for easy navigation:

```
K8s Playbooks/
├── 01-Control-Plane/          (18 playbooks)
├── 02-Nodes/                   (12 playbooks)
├── 03-Pods/                    (31 playbooks)
├── 04-Workloads/               (23 playbooks)
├── 05-Networking/              (19 playbooks)
├── 06-Storage/                 (9 playbooks)
├── 07-RBAC/                    (6 playbooks)
├── 08-Configuration/           (6 playbooks)
├── 09-Resource-Management/      (8 playbooks)
├── 10-Monitoring-Autoscaling/     (3 playbooks)
├── 11-Installation-Setup/       (1 playbook)
└── 12-Namespaces/              (2 playbooks)
```

## Playbook Structure

All playbooks in this directory follow a consistent markdown structure:

### 1. **Front Matter** (YAML)
Metadata at the top of each file:
```yaml
---
title: Issue Name - Resource Type
weight: 201
categories:
  - kubernetes
  - resource-type
---
```

### 2. **Title** (H1)
The playbook identifier (e.g., "CrashLoopBackOff-pod")

### 3. **Meaning** (H2)
A comprehensive explanation of what the issue means, including:
- What triggers the issue
- Common symptoms and error messages
- Which Kubernetes component or layer is affected
- Typical root causes

### 4. **Impact** (H2)
Description of the business and technical impact, including:
- Service availability implications
- User-facing effects
- Related alerts (e.g., KubePodCrashLooping)
- Cascading effects on dependent workloads

### 5. **Playbook** (H2)
Numbered, actionable steps to diagnose the issue:
- Each step includes specific Kubernetes resource identifiers (e.g., `<pod-name>`, `<namespace>`)
- Steps reference kubectl commands, resource specifications, and cluster state
- Ordered from most common to more specific diagnostic steps

### 6. **Diagnosis** (H2)
Correlation analysis framework:
- Time-based correlation between events and symptoms
- Comparison of resource changes with failure timestamps
- Analysis patterns to determine if issues are constant or intermittent
- Guidance for extending time windows if initial correlations aren't found
- Alternative evidence sources and gradual issue identification

## Playbook Categories

### 01-Control-Plane/ (18 playbooks)
Control plane component issues: API Server, Scheduler, Controller Manager, etcd, certificates

**Key Topics:**
- API Server issues (high latency, downtime, errors)
- Scheduler failures
- Controller Manager problems
- Certificate expiration
- Version mismatches
- Upgrade failures

**Example Playbooks:**
- `APIServerHighLatency-control-plane.md`
- `KubeAPIDown-control-plane.md`
- `KubeSchedulerDown-control-plane.md`
- `CertificateExpired-control-plane.md`
- `UpgradeFails-control-plane.md`

### 02-Nodes/ (12 playbooks)
Node readiness, kubelet issues, node capacity, node connectivity

**Key Topics:**
- Node not ready
- Kubelet failures
- Node unreachable
- Resource pressure
- Certificate rotation issues
- Node joining cluster issues

**Example Playbooks:**
- `KubeletDown-node.md`
- `KubeNodeNotReady-node.md`
- `NodeCannotJoinCluster-node.md`
- `NodeDiskPressure-storage.md`
- `KubeletTooManyPods-node.md`

### 03-Pods/ (31 playbooks)
Pod lifecycle, scheduling, health checks, pod states, resource issues

**Key Topics:**
- CrashLoopBackOff
- Pending pods
- Pod scheduling failures
- Health check failures
- Resource quota issues
- Termination issues
- Image pull failures
- Pod logs issues

**Example Playbooks:**
- `CrashLoopBackOff-pod.md`
- `PendingPods-pod.md`
- `KubePodCrashLooping-pod.md`
- `PodFailsLivenessProbe-pod.md`
- `PodsStuckinTerminatingState-pod.md`
- `ImagePullBackOff-registry.md`

### 04-Workloads/ (23 playbooks)
Deployments, StatefulSets, DaemonSets, Jobs, HPA scaling issues

**Key Topics:**
- Deployment scaling issues
- StatefulSet replica mismatches
- DaemonSet scheduling problems
- Job completion failures
- HPA scaling issues
- Workload generation mismatches

**Example Playbooks:**
- `DeploymentNotScalingProperly-deployment.md`
- `KubeStatefulSetReplicasMismatch-statefulset.md`
- `DaemonSetPodsNotDeploying-daemonset.md`
- `HPAHorizontalPodAutoscalerNotScaling-workload.md`
- `JobFailingToComplete-job.md`

### 05-Networking/ (19 playbooks)
Services, Ingress, DNS, Network Policies, kube-proxy, external connectivity

**Key Topics:**
- Service connectivity issues
- Ingress configuration problems
- DNS resolution failures
- Network policy blocking
- kube-proxy failures
- External service access

**Example Playbooks:**
- `ServiceNotResolvingDNS-dns.md`
- `IngressNotWorking-ingress.md`
- `CoreDNSPodsCrashLooping-dns.md`
- `NetworkPolicyBlockingTraffic-network.md`
- `KubeProxyDown-network.md`

### 06-Storage/ (9 playbooks)
PersistentVolumes, PVCs, volume mounts, storage classes

**Key Topics:**
- PersistentVolume issues
- PVC pending states
- Volume mount failures
- Storage class problems
- Volume attachment failures

**Example Playbooks:**
- `PVCPendingDueToStorageClassIssues-storage.md`
- `PersistentVolumeStuckinReleasedState-storage.md`
- `VolumeMountPermissionsDenied-storage.md`
- `KubePersistentVolumeFillingUp-storage.md`

### 07-RBAC/ (6 playbooks)
Permissions, ServiceAccounts, Roles, RoleBindings, authorization errors

**Key Topics:**
- Permission denied errors
- ServiceAccount issues
- Role binding problems
- Unauthorized access
- API server authorization

**Example Playbooks:**
- `RBACPermissionDeniedError-rbac.md`
- `ServiceAccountNotFound-rbac.md`
- `ErrorForbiddenwhenRunningkubectlCommands-rbac.md`
- `UnauthorizedErrorWhenAccessingKubernetesAPI-rbac.md`

### 08-Configuration/ (6 playbooks)
ConfigMaps and Secrets access issues

**Key Topics:**
- ConfigMap access and size issues
- Secret access problems
- Pod configuration access failures

**Example Playbooks:**
- `ConfigMapNotFound-configmap.md`
- `ConfigMapTooLarge-configmap.md`
- `SecretsNotAccessible-secret.md`
- `PodCannotAccessSecret-secret.md`

### 09-Resource-Management/ (8 playbooks)
Resource Quotas, ResourceQuotas, overcommit, compute resource issues

**Key Topics:**
- Resource quota issues
- CPU and memory overcommit
- Quota exhaustion
- Compute resource constraints

**Example Playbooks:**
- `KubeQuotaExceeded-namespace.md`
- `KubeCPUOvercommit-compute.md`
- `KubeMemoryQuotaOvercommit-namespace.md`
- `HighCPUUsage-compute.md`

### 10-Monitoring-Autoscaling/ (3 playbooks)
Metrics Server, Cluster Autoscaler

**Key Topics:**
- Metrics Server issues
- Cluster Autoscaler problems
- HPA metric collection

**Example Playbooks:**
- `MetricsServerShowsNoData-monitoring.md`
- `AutoscalerNotAddingNodes-autoscaler.md`
- `AutoscalerScalingTooSlowly-autoscaler.md`

### 11-Installation-Setup/ (1 playbook)
Helm and installation issues

**Key Topics:**
- Helm release issues
- Installation failures

**Example Playbooks:**
- `HelmReleaseStuckInPending-install.md`

### 12-Namespaces/ (2 playbooks)
Namespace management issues

**Key Topics:**
- Namespace deletion issues
- Namespace stuck states

**Example Playbooks:**
- `CannotDeleteNamespace-namespace.md`
- `NamespaceDeletionStuck-namespace.md`

## Getting Started

### 1. Documentation

This directory contains 138 Kubernetes incident response playbooks organized into 12 categorized folders. Each playbook provides systematic troubleshooting guidance for common Kubernetes cluster and workload issues.

**Quick Navigation:**
- Browse by category folder (e.g., `03-Pods/` for pod issues)
- Use GitHub's search to find specific playbooks
- Match your symptoms to playbook titles

### 2. Installation

Clone this repository to access the Kubernetes playbooks:

```bash
# Clone the repository
git clone https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git

# Navigate to K8s playbooks
cd scoutflo-SRE-Playbooks/K8s\ Playbooks/

# Browse by category
ls 01-Control-Plane/
ls 03-Pods/
ls 05-Networking/

# View a specific playbook
cat 03-Pods/CrashLoopBackOff-pod.md
```

**Quick Access Options:**
- **Bookmark category folders** based on your most common issues
- **Add to your SRE runbook collection** for easy access
- **Use GitHub web interface** to search and view playbooks online
- **Clone locally** for offline access and customization

**Using with kubectl**: These playbooks complement kubectl commands. Keep them handy while troubleshooting:

```bash
# Example: Troubleshooting pod issues
kubectl get pods -n <namespace>
# Then refer to playbooks in 03-Pods/ folder
```

### 3. Learn More

- **Watch Tutorials**: Check our [YouTube channel](https://www.youtube.com/@scoutflo6727) for Kubernetes troubleshooting walkthroughs
- **AI SRE Demo**: Watch the [Scoutflo AI SRE Demo](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) to see AI-powered incident response
- **Kubernetes Docs**: Refer to [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- **kubectl Reference**: Use [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- **Scoutflo Documentation**: Visit [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) for platform guides
- **Community**: Join discussions in our [Slack workspace](https://scoutflo.slack.com)

## Usage Guidelines

### Step-by-Step Process

1. **Identify the Category**: Determine which category your issue falls into (Control Plane, Pods, Networking, etc.)
2. **Navigate to Folder**: Go to the appropriate numbered folder (e.g., `03-Pods/` for pod issues)
3. **Find the Playbook**: Locate the playbook matching your specific issue
4. **Follow the Playbook**: Execute the numbered steps in order, replacing placeholder values (e.g., `<pod-name>`, `<namespace>`) with your actual resource identifiers
5. **Review Diagnosis Section**: Use the correlation analysis to identify root causes
6. **Extend Time Windows**: If initial correlations don't reveal the cause, extend time windows as suggested (e.g., 30 minutes → 1 hour)
7. **Check Alternative Sources**: Review alternative evidence sources mentioned in the Diagnosis section

### Example Workflow

**Scenario**: Pod stuck in CrashLoopBackOff state

1. Navigate to `03-Pods/` folder
2. Open `CrashLoopBackOff-pod.md`
3. Read the **Meaning** section to understand the issue
4. Review the **Impact** section to assess severity
5. Follow **Playbook** steps:
   - Step 1: Retrieve pod logs
   - Step 2: Check container image
   - Step 3: Verify resource limits
   - ... (continue through all steps)
6. Use **Diagnosis** section to correlate events:
   - Compare pod crash timestamps with deployment changes
   - Check if crashes correlate with resource limit changes
7. Apply the identified fix

### Common Placeholders

Playbooks use the following placeholder format that should be replaced with actual values:
- `<pod-name>` - Pod name
- `<namespace>` - Kubernetes namespace
- `<deployment-name>` - Deployment name
- `<node-name>` - Node name
- `<service-name>` - Service name
- `<ingress-name>` - Ingress name
- `<pvc-name>` - PersistentVolumeClaim name
- `<configmap-name>` - ConfigMap name
- `<secret-name>` - Secret name

## Terminology & Glossary

### Core Kubernetes Concepts

**Pod**
- The smallest deployable unit in Kubernetes. A pod contains one or more containers that share storage and network. Think of it as a wrapper around your application container(s).

**Namespace**
- A way to divide cluster resources between multiple users or teams. Like folders for organizing resources. Common namespaces: `default`, `kube-system`, `production`, `staging`.

**Node**
- A worker machine in Kubernetes that runs pods. Can be a physical or virtual machine. Nodes are managed by the control plane.

**Deployment**
- A Kubernetes resource that manages a set of identical pods and ensures they're running correctly. Handles updates, rollbacks, and scaling.

**Service**
- A way to expose an application running on pods as a network service. Provides a stable IP address and DNS name that doesn't change even if pods are recreated.

**Ingress**
- An API object that manages external access to services, typically HTTP/HTTPS. Routes traffic from outside the cluster to services inside.

**ConfigMap**
- A Kubernetes object used to store non-confidential configuration data in key-value pairs. Pods can consume ConfigMaps as environment variables or files.

**Secret**
- A Kubernetes object for storing sensitive information like passwords, tokens, or keys. Similar to ConfigMap but for sensitive data.

**PVC (PersistentVolumeClaim)**
- A request for storage by a user. Like requesting a hard drive for your application. The cluster provisions storage to match the claim.

**PV (PersistentVolume)**
- A piece of storage in the cluster that has been provisioned. Can be used by pods through PVCs.

**StorageClass**
- Describes different classes of storage available in the cluster. Different classes might map to different quality-of-service levels or backup policies.

### Kubernetes Resources

**StatefulSet**
- A workload resource that manages stateful applications. Maintains a sticky identity for each pod (like database instances).

**DaemonSet**
- Ensures that a copy of a pod runs on all (or selected) nodes in the cluster. Useful for system daemons like log collectors.

**Job**
- Creates one or more pods and ensures they complete successfully. Used for batch work that runs to completion.

**CronJob**
- A Job that runs on a time-based schedule, similar to cron in Linux.

**HPA (Horizontal Pod Autoscaler)**
- Automatically scales the number of pods based on CPU, memory, or custom metrics. Adds or removes pods as needed.

### Kubernetes Components

**Control Plane**
- The set of components that manage the Kubernetes cluster:
  - **API Server**: The front-end for the Kubernetes control plane
  - **Scheduler**: Assigns pods to nodes
  - **Controller Manager**: Runs controller processes
  - **etcd**: Consistent and highly-available key-value store

**kubelet**
- The agent that runs on each node and ensures containers are running in pods. Communicates with the control plane.

**kube-proxy**
- Network proxy that maintains network rules on nodes, enabling communication to pods from network sessions.

**Container Runtime**
- The software responsible for running containers (e.g., Docker, containerd, CRI-O).

### Common Pod States

**CrashLoopBackOff**
- Pod state indicating the container keeps crashing and Kubernetes is waiting before restarting it. Usually indicates a configuration or application error.

**ImagePullBackOff**
- Pod state indicating Kubernetes cannot pull the container image. Often due to authentication issues, network problems, or image doesn't exist.

**Pending**
- Pod state indicating the pod has been accepted but hasn't been scheduled to a node yet. Could be waiting for resources or node availability.

**Terminating**
- Pod state indicating the pod is being shut down. Kubernetes is gracefully stopping containers.

**Running**
- Pod state indicating all containers are running and healthy.

**Succeeded**
- Pod state indicating all containers have terminated successfully (for Jobs).

**Failed**
- Pod state indicating at least one container has terminated in failure.

### Networking Terms

**Service Type: ClusterIP**
- Default service type. Exposes the service on an internal IP, only accessible within the cluster.

**Service Type: NodePort**
- Exposes the service on each node's IP at a static port. Accessible from outside the cluster.

**Service Type: LoadBalancer**
- Exposes the service externally using a cloud provider's load balancer.

**DNS**
- Domain Name System. In Kubernetes, services get DNS names like `service-name.namespace.svc.cluster.local`.

**CoreDNS**
- The default DNS server in Kubernetes that provides DNS services for pods.

**Network Policy**
- Rules that control network traffic between pods. Like a firewall for pod-to-pod communication.

### RBAC Terms

**RBAC (Role-Based Access Control)**
- Kubernetes authorization system that controls who can do what in the cluster.

**ServiceAccount**
- An identity for processes running in pods. Used to authenticate to the Kubernetes API.

**Role**
- Defines permissions within a specific namespace.

**ClusterRole**
- Defines permissions across the entire cluster.

**RoleBinding**
- Grants the permissions defined in a Role to a user or set of users within a namespace.

**ClusterRoleBinding**
- Grants permissions across the entire cluster.

### Common Abbreviations

- **K8s**: Short for Kubernetes (K + 8 letters + s)
- **PVC**: PersistentVolumeClaim
- **PV**: PersistentVolume
- **HPA**: Horizontal Pod Autoscaler
- **RBAC**: Role-Based Access Control
- **DNS**: Domain Name System
- **API**: Application Programming Interface

### Playbook Terms

**Diagnosis Section**
- Part of each playbook that helps you correlate events (like resource changes) with failures using time-based analysis.

**Placeholder**
- A value in playbooks (like `<pod-name>`) that you replace with your actual Kubernetes resource name.

**Correlation Window**
- A time period you examine to find relationships between events and failures (e.g., "check events from the last 30 minutes").

**Root Cause**
- The underlying reason why an issue occurred, as opposed to just the symptoms you're seeing.

**kubectl**
- The command-line tool for interacting with Kubernetes clusters. Used in most playbook steps.

**kubectl describe**
- Command that shows detailed information about a resource, including events and current state.

**kubectl get events**
- Command that shows recent events in a namespace, helpful for understanding what happened.

---

**Need more help?** Check out:
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation)

### Best Practices

- **Start with the category folder**: Use the numbered folders to quickly navigate to relevant playbooks
- **Start with common causes**: Begin with the most common causes (earlier steps in the Playbook section)
- **Use kubectl effectively**: Use `kubectl describe` and `kubectl get events` for detailed resource information
- **Check pod logs**: Use `kubectl logs` to examine pod logs
- **Correlate timestamps**: Correlate timestamps between resource changes and failures
- **Review component logs**: Review scheduler logs if pods are stuck in Pending state, API server logs for control plane issues
- **Check node conditions**: Check node conditions and resource availability
- **Document findings**: Document findings for future reference
- **Consider gradual issues**: Consider gradual issues if immediate correlations aren't found

## Quick Navigation Guide

| Issue Type | Folder | Example Playbooks |
|------------|--------|-------------------|
| API Server down/slow | `01-Control-Plane/` | `KubeAPIDown-control-plane.md`, `APIServerHighLatency-control-plane.md` |
| Pod won't start | `03-Pods/` | `PendingPods-pod.md`, `CrashLoopBackOff-pod.md` |
| Service not accessible | `05-Networking/` | `ServiceNotAccessible-service.md`, `ServiceNotResolvingDNS-dns.md` |
| Volume mount failed | `06-Storage/` | `PVCPendingDueToStorageClassIssues-storage.md`, `VolumeMountPermissionsDenied-storage.md` |
| Permission denied | `07-RBAC/` | `RBACPermissionDeniedError-rbac.md`, `ErrorForbiddenwhenRunningkubectlCommands-rbac.md` |
| Deployment not scaling | `04-Workloads/` | `DeploymentNotScalingProperly-deployment.md`, `HPAHorizontalPodAutoscalerNotScaling-workload.md` |
| Node not ready | `02-Nodes/` | `KubeNodeNotReady-node.md`, `KubeletDown-node.md` |
| ConfigMap not found | `08-Configuration/` | `ConfigMapNotFound-configmap.md`, `PodCannotAccessConfigMap-configmap.md` |
| Quota exceeded | `09-Resource-Management/` | `KubeQuotaExceeded-namespace.md`, `KubeCPUQuotaOvercommit-namespace.md` |

## Contributing

We welcome contributions to improve Kubernetes playbooks! Your contributions help the entire SRE community.

### How to Contribute

#### 1. Raising Issues

If you find an error, unclear instructions, or have suggestions:

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) first
2. **Create a New Issue**:
   - Use clear, descriptive title (e.g., "Fix: Incorrect kubectl command in CrashLoopBackOff-pod.md")
   - Describe the problem or suggestion
   - Include relevant Kubernetes component, error messages, or kubectl output
   - Tag with `k8s-playbook` label and appropriate category (pods, networking, etc.)

#### 2. Updating Existing Playbooks

To improve or fix existing Kubernetes playbooks:

1. **Fork the Repository**: Create your own fork
2. **Create a Branch**:
   ```bash
   git checkout -b fix/k8s-playbook-name
   ```
3. **Locate the Playbook**: Find it in the appropriate category folder
4. **Make Your Changes**:
   - Follow the established structure (Front Matter, Title, Meaning, Impact, Playbook, Diagnosis)
   - Maintain YAML front matter format
   - Use consistent placeholder naming (`<pod-name>`, `<namespace>`, etc.)
   - Keep kubectl commands accurate
5. **Test Your Changes**: Verify the playbook works with real Kubernetes scenarios
6. **Commit and Push**:
   ```bash
   git add K8s\ Playbooks/XX-Category/Your-Playbook-Name.md
   git commit -m "Fix: Improve [playbook-name] - [description]"
   git push origin fix/k8s-playbook-name
   ```
7. **Create a Pull Request**: 
   - Reference the issue (if applicable)
   - Describe your changes clearly
   - Request review from maintainers

#### 3. Adding New Kubernetes Playbooks

To add a new playbook for an uncovered Kubernetes issue:

1. **Check for Duplicates**: Ensure a similar playbook doesn't exist
2. **Choose the Right Category**: Place in the appropriate numbered folder:
   - Control plane issues → `01-Control-Plane/`
   - Pod issues → `03-Pods/`
   - Networking issues → `05-Networking/`
   - Storage issues → `06-Storage/`
   - etc.
3. **Follow Naming Convention**: `<AlertName>-<Resource>.md`
   - Example: `KubePodCrashLooping-pod.md`
4. **Include YAML Front Matter**:
   ```yaml
   ---
   title: Issue Name - Resource Type
   weight: 201
   categories:
     - kubernetes
     - resource-type
   ---
   ```
5. **Include All Required Sections**:
   - **Title** (H1): Playbook identifier
   - **Meaning** (H2): What the issue means, triggers, symptoms, affected component
   - **Impact** (H2): Business and technical impact, related alerts
   - **Playbook** (H2): 8-10 numbered diagnostic steps with kubectl commands
   - **Diagnosis** (H2): 5 correlation analysis steps with time windows
6. **Update README**: Add the new playbook to the appropriate category section above
7. **Create Pull Request**: Follow standard contribution process

### Contribution Guidelines

- **Follow Structure**: Maintain consistency with existing playbooks
- **Use Placeholders**: Replace specific values with placeholders
- **Be Actionable**: Provide clear kubectl commands and steps
- **Include Correlation**: Add time-based correlation in Diagnosis section
- **Test Accuracy**: Verify playbooks work with real Kubernetes clusters
- **Document Changes**: Clearly describe what and why you changed
- **Respect Categories**: Place playbooks in the correct category folder

### Review Process

1. All contributions require maintainer review
2. Feedback provided within 2-3 business days
3. Address requested changes promptly
4. Once approved, your contribution will be merged

📖 For detailed contribution guidelines, see [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Connect with Us

**Want to contribute?** Read our [Contributing Guidelines](#contributing) above.

**For Feedback or Feature Requests**: 
- Share with us in [Slack](https://scoutflo.slack.com) or create a [GitHub Issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)

**Bug Report?** 
- Create a detailed issue and share it with us on [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) or [Slack](https://scoutflo.slack.com)

**Links:**
- [Slack Community](https://scoutflo.slack.com) | [Roadmap](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/projects) | [Documentation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/wiki)

**Scoutflo Resources:**
- [Official Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) | [Website](https://scoutflo.com/) | [AI SRE Tool](https://ai.scoutflo.com/get-started)
- [Infra Management Tool](https://deploy.scoutflo.com/) | [YouTube Channel](https://www.youtube.com/@scoutflo6727) | [LinkedIn](https://www.linkedin.com/company/scoutflo/)
- [Twitter/X](https://x.com/scout_flo) | [Blog](https://scoutflo.com/blog) | [Pricing](https://scoutflo.com/pricing)

## Related Resources

### Kubernetes Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Troubleshooting Guide](https://kubernetes.io/docs/tasks/debug/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

### Kubernetes Tools
- [kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/)
- [k9s - Terminal UI](https://k9scli.io/)
- [Lens - Kubernetes IDE](https://k8slens.dev/)

### SRE Resources
- [Google SRE Book](https://sre.google/books/)
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/)

## Statistics

- **Total Playbooks**: 138
- **Categories**: 12
- **Organization**: Numbered folders for easy navigation
- **Coverage**: All major Kubernetes components and common issues

---

**Back to [Main Repository](../../README.md)** | **View [AWS Playbooks](../AWS%20Playbooks/README.md)**
