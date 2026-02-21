# Kubernetes Playbooks

> **232 playbooks** for Kubernetes cluster incident response and proactive monitoring.

## Categories

| Category | Playbooks | Description |
|----------|-----------|-------------|
| [01 - Control Plane](/k8s/01-control-plane) | 24 | API Server, etcd, scheduler, CertManager |
| [02 - Nodes](/k8s/02-nodes) | 24 | Node health, kubelet, NodeExporter |
| [03 - Pods](/k8s/03-pods) | 41 | Pod lifecycle, containers, restarts |
| [04 - Workloads](/k8s/04-workloads) | 25 | Deployments, StatefulSets, DaemonSets, Jobs |
| [05 - Networking](/k8s/05-networking) | 27 | Services, Ingress, CoreDNS, NetworkPolicies |
| [06 - Storage](/k8s/06-storage) | 9 | PersistentVolumes, PVCs, StorageClasses |
| [07 - RBAC](/k8s/07-rbac) | 6 | Roles, RoleBindings, ServiceAccounts |
| [08 - Configuration](/k8s/08-configuration) | 6 | ConfigMaps, Secrets |
| [09 - Resource Management](/k8s/09-resource-management) | 8 | ResourceQuotas, LimitRanges |
| [10 - Monitoring & Autoscaling](/k8s/10-monitoring-autoscaling) | 3 | HPA, VPA, Metrics Server |
| [11 - Installation & Setup](/k8s/11-installation-setup) | 1 | Helm, cluster setup |
| [12 - Namespaces](/k8s/12-namespaces) | 2 | Namespace issues |
| [13 - Proactive](/k8s/13-proactive) | 56 | Proactive monitoring |

## Quick Navigation

### Most Common Issues

| Issue | Playbook |
|-------|----------|
| Pod in CrashLoopBackOff | [CrashLoopBackOff](/k8s/03-pods?id=crashloopbackoff-pod) |
| Pod stuck Pending | [PendingPods](/k8s/03-pods?id=pendingpods-pod) |
| ImagePullBackOff error | [ImagePullBackOff](/k8s/03-pods?id=imagepullbackoff-registry) |
| Node NotReady | [Node NotReady](/k8s/02-nodes?id=nodenotready-node) |
| Service not accessible | [Service Not Accessible](/k8s/05-networking?id=servicenotaccessible-service) |
| Deployment not updating | [Deployment Not Updating](/k8s/04-workloads?id=deploymentnotupdating-deployment) |
| PVC stuck Pending | [PVC Pending](/k8s/06-storage?id=pvcpending-storage) |
| RBAC permission denied | [RBAC Forbidden](/k8s/07-rbac?id=forbidden-rbac) |

### By Symptom

**Container Issues:**
- CrashLoopBackOff → [03-Pods](/k8s/03-pods)
- OOMKilled → [03-Pods](/k8s/03-pods)
- ImagePullBackOff → [03-Pods](/k8s/03-pods)

**Scheduling Issues:**
- Pod Pending → [03-Pods](/k8s/03-pods)
- Node affinity problems → [02-Nodes](/k8s/02-nodes)
- Resource quota exceeded → [09-Resource-Management](/k8s/09-resource-management)

**Network Issues:**
- Service unreachable → [05-Networking](/k8s/05-networking)
- DNS resolution failed → [05-Networking](/k8s/05-networking)
- Ingress not working → [05-Networking](/k8s/05-networking)

**Storage Issues:**
- PVC stuck pending → [06-Storage](/k8s/06-storage)
- Volume mount failed → [06-Storage](/k8s/06-storage)

## Understanding Kubernetes Playbook Steps

Playbooks use NLP-friendly instructions like:

> "Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status"

Each step includes CLI equivalents:

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

</details>

## All Categories

<details>
<summary><strong>01 - Control Plane (24 playbooks)</strong></summary>

API Server, etcd, scheduler, controller-manager, and CertManager issues.

See [01 - Control Plane](/k8s/01-control-plane) for the full list.

</details>

<details>
<summary><strong>02 - Nodes (24 playbooks)</strong></summary>

Node health, kubelet issues, NodeExporter alerts.

See [02 - Nodes](/k8s/02-nodes) for the full list.

</details>

<details>
<summary><strong>03 - Pods (41 playbooks)</strong></summary>

Pod lifecycle, container issues, restarts, probes.

See [03 - Pods](/k8s/03-pods) for the full list.

</details>

<details>
<summary><strong>04 - Workloads (25 playbooks)</strong></summary>

Deployments, StatefulSets, DaemonSets, Jobs, CronJobs.

See [04 - Workloads](/k8s/04-workloads) for the full list.

</details>

<details>
<summary><strong>05 - Networking (27 playbooks)</strong></summary>

Services, Ingress, CoreDNS, NetworkPolicies.

See [05 - Networking](/k8s/05-networking) for the full list.

</details>

<details>
<summary><strong>06 - Storage (9 playbooks)</strong></summary>

PersistentVolumes, PVCs, StorageClasses.

See [06 - Storage](/k8s/06-storage) for the full list.

</details>

<details>
<summary><strong>07 - RBAC (6 playbooks)</strong></summary>

Roles, RoleBindings, ClusterRoles, ServiceAccounts.

See [07 - RBAC](/k8s/07-rbac) for the full list.

</details>

<details>
<summary><strong>08 - Configuration (6 playbooks)</strong></summary>

ConfigMaps, Secrets.

See [08 - Configuration](/k8s/08-configuration) for the full list.

</details>

<details>
<summary><strong>09 - Resource Management (8 playbooks)</strong></summary>

ResourceQuotas, LimitRanges.

See [09 - Resource Management](/k8s/09-resource-management) for the full list.

</details>

<details>
<summary><strong>10 - Monitoring & Autoscaling (3 playbooks)</strong></summary>

HPA, VPA, Metrics Server.

See [10 - Monitoring & Autoscaling](/k8s/10-monitoring-autoscaling) for the full list.

</details>

<details>
<summary><strong>13 - Proactive (56 playbooks)</strong></summary>

Proactive monitoring and optimization.

See [13 - Proactive](/k8s/13-proactive) for the full list.

</details>
