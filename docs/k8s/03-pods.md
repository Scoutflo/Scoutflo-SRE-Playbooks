# 03 - Pods

> **41 playbooks** for Kubernetes pod lifecycle and container issues.

## Overview

Pods are the smallest deployable units in Kubernetes. This category covers:
- Container crashes and restarts
- Image pull issues
- Resource constraints (CPU, memory)
- Health probe failures
- Scheduling problems

## Playbooks

### Container Lifecycle Issues

| Playbook | Description |
|----------|-------------|
| [CrashLoopBackOff-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/CrashLoopBackOff-pod.md) | Pod containers crashing repeatedly |
| [KubePodCrashLooping-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodCrashLooping-pod.md) | Pod in crash loop state |
| [KubePodFrequentlyRestarting-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodFrequentlyRestarting-pod.md) | Pod frequently restarting |
| [PodsRestartingFrequently-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsRestartingFrequently-pod.md) | Pods restarting too often |
| [ContainerRestartsFrequent-container](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/ContainerRestartsFrequent-container.md) | Container restarts frequently |

### Pending/Scheduling Issues

| Playbook | Description |
|----------|-------------|
| [PendingPods-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PendingPods-pod.md) | Pods stuck in pending state |
| [KubePodPending-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodPending-pod.md) | Pod pending |
| [PodsNotBeingScheduled-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsNotBeingScheduled-pod.md) | Pods not being scheduled |
| [PodStuckinPendingDuetoNodeAffinity-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodStuckinPendingDuetoNodeAffinity-pod.md) | Pod pending due to node affinity |
| [PodSchedulingIgnoredNodeSelector-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodSchedulingIgnoredNodeSelector-pod.md) | Pod not matching node selector |

### Image Pull Issues

| Playbook | Description |
|----------|-------------|
| [ImagePullBackOff-registry](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/ImagePullBackOff-registry.md) | Cannot pull container image |
| [KubePodImagePullBackOff-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodImagePullBackOff-pod.md) | Pod image pull backoff |
| [PodsStuckinImagePullBackOff-registry](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckinImagePullBackOff-registry.md) | Pods stuck pulling images |

### Resource/Memory Issues

| Playbook | Description |
|----------|-------------|
| [KubeContainerOOMKilled-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubeContainerOOMKilled-pod.md) | Container OOM killed |
| [PodTerminatedWithExitCode137-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodTerminatedWithExitCode137-pod.md) | Pod terminated (OOM killed) |
| [ContainerHighMemoryUsage-container](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/ContainerHighMemoryUsage-container.md) | Container high memory usage |
| [ContainerMemoryNearLimit-container](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/ContainerMemoryNearLimit-container.md) | Container memory near limit |
| [ContainerHighCPUThrottling-container](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/ContainerHighCPUThrottling-container.md) | Container high CPU throttling |
| [CPUThrottlingHigh-container](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/CPUThrottlingHigh-container.md) | CPU throttling high |

### Health Probe Issues

| Playbook | Description |
|----------|-------------|
| [PodFailsLivenessProbe-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodFailsLivenessProbe-pod.md) | Pod failing liveness probe |
| [PodFailsReadinessProbe-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodFailsReadinessProbe-pod.md) | Pod failing readiness probe |
| [KubePodNotReady-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodNotReady-pod.md) | Pod not ready |

### Stuck/Terminating Issues

| Playbook | Description |
|----------|-------------|
| [PodsStuckinTerminatingState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckinTerminatingState-pod.md) | Pods stuck terminating |
| [PodStuckInTerminatingState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodStuckInTerminatingState-pod.md) | Pod stuck terminating |
| [PodsStuckinContainerCreatingState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckinContainerCreatingState-pod.md) | Pods stuck creating containers |
| [PodsStuckinInitState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckinInitState-pod.md) | Pods stuck in init container phase |
| [PodsStuckInUnknownState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckInUnknownState-pod.md) | Pods in unknown state |
| [KubeContainerWaiting-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubeContainerWaiting-pod.md) | Container stuck in waiting state |
| [KubePodContainerWaiting-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/KubePodContainerWaiting-pod.md) | Pod container waiting |

### Network/DNS Issues

| Playbook | Description |
|----------|-------------|
| [PodCannotAccessClusterInternalDNS-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodCannotAccessClusterInternalDNS-dns.md) | Pod cannot resolve DNS |
| [PodCannotConnecttoExternalServices-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodCannotConnecttoExternalServices-network.md) | Pod cannot reach external services |
| [PodIPConflict-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodIPConflict-network.md) | Pod IP address conflict |
| [PodIPNotReachable-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodIPNotReachable-network.md) | Pod IP not reachable |

### Other Issues

| Playbook | Description |
|----------|-------------|
| [EvictedPods-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/EvictedPods-pod.md) | Pods being evicted from nodes |
| [PodsStuckinEvictedState-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsStuckinEvictedState-pod.md) | Pods stuck in evicted state |
| [FailedtoStartPodSandbox-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/FailedtoStartPodSandbox-pod.md) | Pod sandbox creation failed |
| [PodLogsNotAvailable-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodLogsNotAvailable-pod.md) | Cannot access pod logs |
| [PodLogsTruncated-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodLogsTruncated-pod.md) | Pod logs being truncated |
| [PodSecurityContext-pod](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodSecurityContext-pod.md) | Pod security context issues |
| [PodsExceedingResourceQuota-workload](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsExceedingResourceQuota-workload.md) | Pods exceeding resource quota |
| [PodsOverloadedDuetoMissingHPA-workload](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/03-Pods/PodsOverloadedDuetoMissingHPA-workload.md) | Pods overloaded, HPA not working |

## Quick Troubleshooting

### CrashLoopBackOff Quick Check

<details>
<summary>CLI Commands</summary>

```bash
# Get pod status
kubectl get pod <pod-name> -n <namespace>

# Check events
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Events

# Get logs (current container)
kubectl logs <pod-name> -n <namespace>

# Get logs (previous crashed container)
kubectl logs <pod-name> -n <namespace> --previous
```

</details>

### Pending Pod Quick Check

<details>
<summary>CLI Commands</summary>

```bash
# Check why pod is pending
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Events:"

# Check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check resource quotas
kubectl get resourcequota -n <namespace>
```

</details>

---

[Back to Kubernetes Playbooks](/k8s/)
