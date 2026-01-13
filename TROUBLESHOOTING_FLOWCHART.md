# Troubleshooting Decision Tree

Use this flowchart to quickly identify which playbook to use for your issue.

## Start Here: What Type of Issue?

```
                    ┌─────────────────┐
                    │  What's wrong?  │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼──────┐          ┌──────▼──────┐
         │   AWS       │          │ Kubernetes  │
         │  Issue?     │          │   Issue?     │
         └──────┬──────┘          └──────┬──────┘
                │                         │
```

## AWS Issues Path

```
         ┌──────▼──────┐
         │   AWS       │
         │  Issue?     │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│ EC2   │  │ RDS   │  │ Other │
│       │  │       │  │       │
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    │          │          │
    ▼          ▼          ▼
```

### AWS EC2 Issues

```
EC2 Issue?
    │
    ├─ Can't SSH? → Connection-Timeout-SSH-Issues-EC2.md
    ├─ Not starting? → Instance-Not-Starting-EC2.md
    ├─ No internet? → Instance-Unable-to-Reach-the-Internet-EC2.md
    └─ NAT Gateway? → Instance-Cant-Reach-Internet-via-NAT-Gateway-EC2.md
```

### AWS RDS Issues

```
RDS Issue?
    │
    ├─ Can't connect? → Instance-Not-Connecting-RDS.md
    ├─ Lambda timeout? → Connection-Timeout-from-Lambda-RDS.md
    └─ Storage full? → Storage-Full-Error-RDS.md
```

### Other AWS Services

```
Other AWS Issue?
    │
    ├─ S3 access denied? → Bucket-Access-Denied-403-Error-S3.md
    ├─ Lambda timeout? → Timeout-Error-Lambda.md
    ├─ ELB unhealthy? → Target-Group-Showing-Unhealthy-Instances-ELB.md
    ├─ IAM permissions? → Policy-Not-Granting-Expected-Access-IAM.md
    ├─ VPC peering? → Peering-Not-Working-VPC.md
    └─ Route 53 DNS? → DNS-Resolution-Failing-Route-53.md
```

## Kubernetes Issues Path

```
         ┌──────▼──────┐
         │ Kubernetes  │
         │   Issue?     │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│ Pod   │  │Service│  │Other  │
│       │  │       │  │       │
└───┬───┘  └───┬───┘  └───┬───┘
```

### Pod Issues (Most Common)

```
Pod Issue?
    │
    ├─ Crashing? → 03-Pods/CrashLoopBackOff-pod.md
    ├─ Not starting? → 03-Pods/PendingPods-pod.md
    ├─ Image pull failed? → 03-Pods/ImagePullBackOff-registry.md
    ├─ Stuck terminating? → 03-Pods/PodsStuckinTerminatingState-pod.md
    ├─ Health check failing? → 03-Pods/PodFailsLivenessProbe-pod.md
    └─ Can't access logs? → 03-Pods/PodLogsNotAvailable-pod.md
```

### Service/Network Issues

```
Service/Network Issue?
    │
    ├─ Service not accessible? → 05-Networking/ServiceNotAccessible-service.md
    ├─ DNS not resolving? → 05-Networking/ServiceNotResolvingDNS-dns.md
    ├─ Ingress not working? → 05-Networking/IngressNotWorking-ingress.md
    ├─ CoreDNS down? → 05-Networking/CoreDNSPodsCrashLooping-dns.md
    └─ Network policy? → 05-Networking/NetworkPolicyBlockingTraffic-network.md
```

### Other Kubernetes Issues

```
Other K8s Issue?
    │
    ├─ Node not ready? → 02-Nodes/KubeNodeNotReady-node.md
    ├─ Deployment not scaling? → 04-Workloads/DeploymentNotScalingProperly-deployment.md
    ├─ Volume mount failed? → 06-Storage/PVCPendingDueToStorageClassIssues-storage.md
    ├─ Permission denied? → 07-RBAC/RBACPermissionDeniedError-rbac.md
    ├─ ConfigMap not found? → 08-Configuration/ConfigMapNotFound-configmap.md
    ├─ Quota exceeded? → 09-Resource-Management/KubeQuotaExceeded-namespace.md
    ├─ API Server down? → 01-Control-Plane/KubeAPIDown-control-plane.md
    └─ HPA not scaling? → 04-Workloads/HPAHorizontalPodAutoscalerNotScaling-workload.md
```

## Detailed Decision Tree

### Step 1: Identify the Component

```
What component is affected?
    │
    ├─ Pod? → Go to Pod Decision Tree
    ├─ Service? → Go to Service Decision Tree
    ├─ Node? → Go to Node Decision Tree
    ├─ Deployment? → Go to Workload Decision Tree
    ├─ Volume? → Go to Storage Decision Tree
    ├─ Permission? → Go to RBAC Decision Tree
    └─ Control Plane? → Go to Control Plane Decision Tree
```

### Step 2: Identify the Symptom

#### Pod Decision Tree

```
Pod Issue?
    │
    ├─ State: CrashLoopBackOff → CrashLoopBackOff-pod.md
    ├─ State: Pending → PendingPods-pod.md
    ├─ State: ImagePullBackOff → ImagePullBackOff-registry.md
    ├─ State: Terminating → PodsStuckinTerminatingState-pod.md
    ├─ Health: Liveness probe failing → PodFailsLivenessProbe-pod.md
    ├─ Health: Readiness probe failing → PodFailsReadinessProbe-pod.md
    ├─ Logs: Not available → PodLogsNotAvailable-pod.md
    └─ Other → Browse 03-Pods/ folder
```

#### Service Decision Tree

```
Service Issue?
    │
    ├─ Not accessible → ServiceNotAccessible-service.md
    ├─ DNS not resolving → ServiceNotResolvingDNS-dns.md
    ├─ Not forwarding traffic → ServiceNotForwardingTraffic-service.md
    ├─ Connection refused → ErrorConnectionRefusedWhenAccessingService-service.md
    └─ Intermittent → ServicesIntermittentlyUnreachable-service.md
```

#### Node Decision Tree

```
Node Issue?
    │
    ├─ Not ready → KubeNodeNotReady-node.md
    ├─ Unreachable → KubeNodeUnreachable-node.md
    ├─ Disk pressure → NodeDiskPressure-storage.md
    ├─ Too many pods → KubeletTooManyPods-node.md
    ├─ Kubelet down → KubeletDown-node.md
    └─ Can't join cluster → NodeCannotJoinCluster-node.md
```

## Quick Lookup by Error Message

| Error Message | Playbook |
|---------------|----------|
| `CrashLoopBackOff` | `03-Pods/CrashLoopBackOff-pod.md` |
| `ImagePullBackOff` | `03-Pods/ImagePullBackOff-registry.md` |
| `Pending` | `03-Pods/PendingPods-pod.md` |
| `NodeNotReady` | `02-Nodes/KubeNodeNotReady-node.md` |
| `Forbidden` | `07-RBAC/ErrorForbiddenwhenRunningkubectlCommands-rbac.md` |
| `Connection refused` | `05-Networking/ErrorConnectionRefusedWhenAccessingService-service.md` |
| `Quota exceeded` | `09-Resource-Management/KubeQuotaExceeded-namespace.md` |
| `Volume mount failed` | `06-Storage/PodCannotAccessPersistentVolume-storage.md` |

## Quick Lookup by Alert Name

| Alert Name | Playbook |
|------------|----------|
| `KubePodCrashLooping` | `03-Pods/KubePodCrashLooping-pod.md` |
| `KubeNodeNotReady` | `02-Nodes/KubeNodeNotReady-node.md` |
| `KubeAPIDown` | `01-Control-Plane/KubeAPIDown-control-plane.md` |
| `KubeQuotaExceeded` | `09-Resource-Management/KubeQuotaExceeded-namespace.md` |
| `KubeDeploymentReplicasMismatch` | `04-Workloads/KubeDeploymentReplicasMismatch-deployment.md` |

## Still Not Sure?

1. **Check the main README**: [K8s Playbooks/README.md](K8s%20Playbooks/README.md)
2. **Browse by category**: Each folder has a README explaining what it covers
3. **Search the repository**: Use GitHub's search or Ctrl+F
4. **Ask the community**: [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)

## Pro Tips

1. **Start with Pods**: Most issues manifest as pod problems
2. **Check Events**: `kubectl get events` often points to the right playbook
3. **Read Category READMEs**: Each folder README explains what it covers
4. **Use Search**: GitHub search is your friend

---

**Need help navigating?** Check the [Quick Reference Card](QUICK_REFERENCE.md) or [FAQ](FAQ.md)!
