# Kubernetes Workload Playbooks

> **25 playbooks** for Deployments, DaemonSets, StatefulSets, Jobs, and HPA issues.

## Deployment Playbooks

| Playbook | Description |
|----------|-------------|
| [DeploymentNotUpdating](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/DeploymentNotUpdating-deployment.md) | Deployment update failures |
| [DeploymentNotScalingProperly](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/DeploymentNotScalingProperly-deployment.md) | Scaling issues |
| [KubeDeploymentGenerationMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDeploymentGenerationMismatch-deployment.md) | Generation mismatch alert |
| [KubeDeploymentReplicasMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDeploymentReplicasMismatch-deployment.md) | Replica count mismatch |
| [KubeDeploymentRolloutStuck](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDeploymentRolloutStuck-deployment.md) | Stuck rollout |
| [CannotScaleDeploymentBeyondNodeCapacity](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/CannotScaleDeploymentBeyondNodeCapacity-workload.md) | Capacity scaling limits |

## DaemonSet Playbooks

| Playbook | Description |
|----------|-------------|
| [DaemonSetNotDeployingPodsOnAllNodes](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/DaemonSetNotDeployingPodsonAllNodes-daemonset.md) | Incomplete DaemonSet deployment |
| [DaemonSetPodsNotDeploying](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/DaemonSetPodsNotDeploying-daemonset.md) | DaemonSet pod deployment failures |
| [DaemonSetPodsNotRunningOnSpecificNode](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/DaemonSetPodsNotRunningonSpecificNode-daemonset.md) | Node-specific DaemonSet issues |
| [KubeDaemonSetMisScheduled](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDaemonSetMisScheduled-daemonset.md) | Misscheduled DaemonSet alert |
| [KubeDaemonSetNotReady](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDaemonSetNotReady-daemonset.md) | DaemonSet not ready |
| [KubeDaemonSetNotScheduled](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDaemonSetNotScheduled-daemonset.md) | DaemonSet scheduling failures |
| [KubeDaemonSetRolloutStuck](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeDaemonSetRolloutStuck-daemonset.md) | Stuck DaemonSet rollout |

## StatefulSet Playbooks

| Playbook | Description |
|----------|-------------|
| [KubeStatefulSetGenerationMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeStatefulSetGenerationMismatch-statefulset.md) | Generation mismatch alert |
| [KubeStatefulSetReplicasMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeStatefulSetReplicasMismatch-statefulset.md) | Replica count mismatch |
| [KubeStatefulSetUpdateNotRolledOut](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeStatefulSetUpdateNotRolledOut-statefulset.md) | Update not rolled out |

## Job Playbooks

| Playbook | Description |
|----------|-------------|
| [JobFailingToComplete](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/JobFailingToComplete-job.md) | Job completion failures |
| [KubeJobCompletion](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeJobCompletion-workload.md) | Job completion monitoring |
| [KubeJobFailed](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeJobFailed-workload.md) | Job failure alert |

## HPA Playbooks

| Playbook | Description |
|----------|-------------|
| [HPANotScaling](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/HPAHorizontalPodAutoscalerNotScaling-workload.md) | HPA not scaling |
| [HPANotRespondingToMetrics](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/HPANotRespondingtoMetrics-workload.md) | HPA metrics issues |
| [HPANotRespondingToCustomMetrics](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/HPANotRespondingtoCustomMetrics-workload.md) | Custom metrics failures |
| [KubeHpaMaxedOut](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeHpaMaxedOut-workload.md) | HPA at maximum replicas |
| [KubeHpaReplicasMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/KubeHpaReplicasMismatch-workload.md) | HPA replica mismatch |

## Resource Playbooks

| Playbook | Description |
|----------|-------------|
| [InvalidMemoryCPURequests](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/04-Workloads/InvalidMemoryCPURequests-workload.md) | Invalid resource requests |

---

[Back to K8s Overview](/k8s/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/K8s%20Playbooks/04-Workloads)
