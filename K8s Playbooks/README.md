# Kubernetes (K8s) Playbooks

This directory contains **138 Kubernetes incident response playbooks** designed to help Site Reliability Engineers (SREs) diagnose and resolve common Kubernetes cluster and workload issues. Each playbook follows a structured format to provide systematic troubleshooting guidance.

## Overview

These playbooks cover critical Kubernetes components and scenarios including:
- **Control Plane**: API Server, Scheduler, Controller Manager, etcd
- **Nodes**: Node readiness, kubelet issues, resource constraints
- **Pods**: Scheduling, lifecycle, health checks, resource limits
- **Workloads**: Deployments, StatefulSets, DaemonSets, Jobs
- **Networking**: Services, Ingress, DNS, Network Policies
- **Storage**: PersistentVolumes, PersistentVolumeClaims, StorageClasses
- **RBAC**: ServiceAccounts, Roles, RoleBindings, ClusterRoles
- **Monitoring**: Metrics Server, HPA, resource quotas
- **Autoscaling**: Cluster Autoscaler, HPA scaling issues

Each playbook provides step-by-step instructions for identifying root causes and resolving issues quickly.

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

Playbooks are organized by resource type and issue category:

### Control Plane (`-control-plane.md`)
- API Server issues (high latency, downtime, errors)
- Scheduler failures
- Controller Manager problems
- Certificate expiration
- Version mismatches

### Pods (`-pod.md`)
- CrashLoopBackOff
- Pending pods
- Pod scheduling failures
- Health check failures
- Resource quota issues
- Termination issues

### Nodes (`-node.md`)
- Node not ready
- Kubelet failures
- Node unreachable
- Resource pressure
- Certificate rotation issues

### Workloads (`-workload.md`, `-deployment.md`, `-statefulset.md`, `-daemonset.md`, `-job.md`)
- Deployment scaling issues
- StatefulSet replica mismatches
- DaemonSet scheduling problems
- Job completion failures
- HPA scaling issues

### Networking (`-network.md`, `-service.md`, `-ingress.md`, `-dns.md`)
- Service connectivity issues
- Ingress configuration problems
- DNS resolution failures
- Network policy blocking
- kube-proxy failures

### Storage (`-storage.md`)
- PersistentVolume issues
- PVC pending states
- Volume mount failures
- Storage class problems

### RBAC (`-rbac.md`)
- Permission denied errors
- ServiceAccount issues
- Role binding problems
- Unauthorized access

### Monitoring (`-monitoring.md`)
- Metrics Server issues
- HPA metric collection problems

### Autoscaling (`-autoscaler.md`)
- Cluster autoscaler not adding nodes
- Scaling too slowly

### Other Categories
- `-namespace.md` - Namespace deletion and quota issues
- `-configmap.md` - ConfigMap access and size issues
- `-secret.md` - Secret access problems
- `-registry.md` - Image pull failures
- `-install.md` - Helm and installation issues
- `-compute.md` - CPU and memory overcommit

## Complete Playbook List

### Control Plane (15 playbooks)
- APIServerHighLatency-control-plane.md
- AutoscalerNotAddingNodes-autoscaler.md
- AutoscalerScalingTooSlowly-autoscaler.md
- CannotAccessAPI-control-plane.md
- CertificateExpired-control-plane.md
- ConnectionRefused-control-plane.md
- ContextDeadlineExceeded-control-plane.md
- ControlPlaneComponentsNotStarting-control-plane.md
- KubeAggregatedAPIDown-control-plane.md
- KubeAggregatedAPIErrors-control-plane.md
- KubeAPIDown-control-plane.md
- KubeAPIErrorBudgetBurn-control-plane.md
- KubeAPITerminatedRequests-control-plane.md
- KubeClientCertificateExpiration-control-plane.md
- KubeClientErrors-control-plane.md
- KubeControllerManagerDown-control-plane.md
- KubeSchedulerDown-control-plane.md
- KubeVersionMismatch-control-plane.md
- Timeout-control-plane.md
- UpgradeFails-control-plane.md

### Pods (30+ playbooks)
- CrashLoopBackOff-pod.md
- EvictedPods-pod.md
- FailedtoStartPodSandbox-pod.md
- ImagePullBackOff-registry.md
- KubeContainerWaiting-pod.md
- KubePodCrashLooping-pod.md
- KubePodNotReady-pod.md
- PendingPods-pod.md
- PodCannotAccessConfigMap-configmap.md
- PodCannotAccessPersistentVolume-storage.md
- PodCannotAccessSecret-secret.md
- PodCannotConnecttoExternalServices-network.md
- PodFailsLivenessProbe-pod.md
- PodFailsReadinessProbe-pod.md
- PodIPConflict-network.md
- PodIPNotReachable-network.md
- PodLogsNotAvailable-pod.md
- PodLogsTruncated-pod.md
- PodsCannotPullSecrets-secret.md
- PodsExceedingResourceQuota-workload.md
- PodsNotBeingScheduled-pod.md
- PodsOverloadedDuetoMissingHPA-workload.md
- PodsRestartingFrequently-pod.md
- PodsStuckinContainerCreatingState-pod.md
- PodsStuckinEvictedState-pod.md
- PodsStuckinImagePullBackOff-registry.md
- PodsStuckinInitState-pod.md
- PodsStuckinTerminatingState-pod.md
- PodsStuckInUnknownState-pod.md
- PodSchedulingIgnoredNodeSelector-pod.md
- PodSecurityContext-pod.md
- PodStuckinPendingDuetoNodeAffinity-pod.md
- PodStuckInTerminatingState-pod.md
- PodTerminatedWithExitCode137-pod.md

### Nodes (10+ playbooks)
- KubeletCertificateRotationFailing-node.md
- KubeletDown-node.md
- KubeletPlegDurationHigh-node.md
- KubeletPodStartUpLatencyHigh-node.md
- KubeletServiceNotRunning-node.md
- KubeletTooManyPods-node.md
- KubeNodeNotReady-node.md
- KubeNodeReadinessFlapping-node.md
- KubeNodeUnreachable-node.md
- NodeCannotJoinCluster-node.md
- NodeDiskPressure-storage.md
- NodeNotReady-node.md
- NodesUnreachable-network.md

### Workloads (20+ playbooks)
- CannotScaleDeploymentBeyondNodeCapacity-workload.md
- DeploymentNotScalingProperly-deployment.md
- DeploymentNotUpdating-deployment.md
- HPAHorizontalPodAutoscalerNotScaling-workload.md
- HPANotRespondingtoCustomMetrics-workload.md
- HPANotRespondingtoMetrics-workload.md
- InvalidMemoryCPURequests-workload.md
- JobFailingToComplete-job.md
- KubeCPUOvercommit-compute.md
- KubeCPUQuotaOvercommit-namespace.md
- KubeDaemonSetMisScheduled-daemonset.md
- KubeDaemonSetNotScheduled-daemonset.md
- KubeDaemonSetRolloutStuck-daemonset.md
- KubeDeploymentGenerationMismatch-deployment.md
- KubeDeploymentReplicasMismatch-deployment.md
- KubeHpaMaxedOut-workload.md
- KubeHpaReplicasMismatch-workload.md
- KubeJobCompletion-workload.md
- KubeJobFailed-workload.md
- KubeMemoryOvercommit-compute.md
- KubeMemoryQuotaOvercommit-namespace.md
- KubeQuotaAlmostFull-namespace.md
- KubeQuotaExceeded-namespace.md
- KubeQuotaFullyUsed-namespace.md
- KubeStatefulSetGenerationMismatch-statefulset.md
- KubeStatefulSetReplicasMismatch-statefulset.md
- KubeStatefulSetUpdateNotRolledOut-statefulset.md

### Networking (15+ playbooks)
- CoreDNSPodsCrashLooping-dns.md
- DNSResolutionIntermittent-dns.md
- ErrorConnectionRefusedWhenAccessingService-service.md
- IngressControllerPodsCrashLooping-ingress.md
- IngressNotWorking-ingress.md
- IngressRedirectLoop-ingress.md
- IngressReturning502BadGateway-ingress.md
- IngressShows404-ingress.md
- IngressSSLTLSConfigurationFails-ingress.md
- Kube-proxyFailing-network.md
- KubeProxyDown-network.md
- NetworkPolicyBlockingTraffic-network.md
- PodCannotAccessClusterInternalDNS-dns.md
- ServiceExternal-IPPending-service.md
- ServiceNodePortNotAccessible-service.md
- ServiceNotAccessible-service.md
- ServiceNotForwardingTraffic-service.md
- ServiceNotResolvingDNS-dns.md
- ServicesIntermittentlyUnreachable-service.md

### Storage (10+ playbooks)
- FailedAttachVolume-storage.md
- KubePersistentVolumeErrors-storage.md
- KubePersistentVolumeFillingUp-storage.md
- PersistentVolumeNotResizing-storage.md
- PersistentVolumeStuckinReleasedState-storage.md
- PodCannotAccessPersistentVolume-storage.md
- PVCinLostState-storage.md
- PVCPendingDueToStorageClassIssues-storage.md
- VolumeMountPermissionsDenied-storage.md

### RBAC (8 playbooks)
- ClusterRoleBindingMissingPermissions-rbac.md
- ErrorForbiddenwhenRunningkubectlCommands-rbac.md
- ErrorUnauthorizedwhenAccessingAPIServer-rbac.md
- RBACPermissionDeniedError-rbac.md
- ServiceAccountNotFound-rbac.md
- UnauthorizedErrorWhenAccessingKubernetesAPI-rbac.md

### Other Categories
- CannotDeleteNamespace-namespace.md
- ConfigMapNotFound-configmap.md
- ConfigMapTooLarge-configmap.md
- DaemonSetNotDeployingPodsonAllNodes-daemonset.md
- DaemonSetPodsNotDeploying-daemonset.md
- DaemonSetPodsNotRunningonSpecificNode-daemonset.md
- HelmReleaseStuckInPending-install.md
- HighCPUUsage-compute.md
- MetricsServerShowsNoData-monitoring.md
- NamespaceDeletionStuck-namespace.md
- PodCannotAccessConfigMap-configmap.md
- PodCannotAccessSecret-secret.md
- SecretsNotAccessible-secret.md

## Usage Guidelines

1. **Identify the Issue**: Match your symptoms to the appropriate playbook title
2. **Follow the Playbook**: Execute the numbered steps in order, replacing placeholder values (e.g., `<pod-name>`, `<namespace>`) with your actual resource identifiers
3. **Review Diagnosis Section**: Use the correlation analysis to identify root causes
4. **Extend Time Windows**: If initial correlations don't reveal the cause, extend time windows as suggested (e.g., 30 minutes → 1 hour)
5. **Check Alternative Sources**: Review alternative evidence sources mentioned in the Diagnosis section

## Common Placeholders

Playbooks use the following placeholder format that should be replaced with actual values:
- `<pod-name>` - Pod name
- `<namespace>` - Kubernetes namespace
- `<deployment-name>` - Deployment name
- `<node-name>` - Node name
- `<service-name>` - Service name
- `<ingress-name>` - Ingress name

## Best Practices

- Start with the most common causes (earlier steps in the Playbook section)
- Use `kubectl describe` and `kubectl get events` for detailed resource information
- Check pod logs using `kubectl logs`
- Correlate timestamps between resource changes and failures
- Review scheduler logs if pods are stuck in Pending state
- Check node conditions and resource availability
- Document findings for future reference
- Consider gradual issues if immediate correlations aren't found

## Related Resources

- Kubernetes Documentation: https://kubernetes.io/docs/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- Kubernetes Troubleshooting Guide: https://kubernetes.io/docs/tasks/debug/
