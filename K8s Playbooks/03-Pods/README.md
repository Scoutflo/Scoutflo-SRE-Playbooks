# Pods Playbooks

This folder contains **31 playbooks** for troubleshooting Kubernetes pod-related issues.

## What are Pods?

Pods are the smallest deployable units in Kubernetes. A pod contains one or more containers that share storage and network. Most issues you'll encounter in Kubernetes are pod-related.

## Common Issues Covered

- CrashLoopBackOff (containers crashing)
- Pending pods (not scheduled)
- Pod scheduling failures
- Health check failures (liveness/readiness probes)
- Resource quota issues
- Termination problems
- Image pull failures
- Pod logs issues
- Pod stuck in various states

## Playbooks in This Folder

1. `CrashLoopBackOff-pod.md` - Pod containers crashing repeatedly
2. `EvictedPods-pod.md` - Pods being evicted from nodes
3. `FailedtoStartPodSandbox-pod.md` - Pod sandbox creation failed
4. `ImagePullBackOff-registry.md` - Cannot pull container image
5. `KubeContainerWaiting-pod.md` - Container stuck in waiting state
6. `KubePodCrashLooping-pod.md` - Pod in crash loop state
7. `KubePodNotReady-pod.md` - Pod not ready
8. `PendingPods-pod.md` - Pods stuck in pending state
9. `PodCannotAccessClusterInternalDNS-dns.md` - Pod cannot resolve DNS
10. `PodCannotConnecttoExternalServices-network.md` - Pod cannot reach external services
11. `PodFailsLivenessProbe-pod.md` - Pod failing liveness probe
12. `PodFailsReadinessProbe-pod.md` - Pod failing readiness probe
13. `PodIPConflict-network.md` - Pod IP address conflict
14. `PodIPNotReachable-network.md` - Pod IP not reachable
15. `PodLogsNotAvailable-pod.md` - Cannot access pod logs
16. `PodLogsTruncated-pod.md` - Pod logs being truncated
17. `PodSchedulingIgnoredNodeSelector-pod.md` - Pod not matching node selector
18. `PodSecurityContext-pod.md` - Pod security context issues
19. `PodsExceedingResourceQuota-workload.md` - Pods exceeding resource quota
20. `PodsNotBeingScheduled-pod.md` - Pods not being scheduled
21. `PodsOverloadedDuetoMissingHPA-workload.md` - Pods overloaded, HPA not working
22. `PodsRestartingFrequently-pod.md` - Pods restarting too often
23. `PodsStuckinContainerCreatingState-pod.md` - Pods stuck creating containers
24. `PodsStuckinEvictedState-pod.md` - Pods stuck in evicted state
25. `PodsStuckinImagePullBackOff-registry.md` - Pods stuck pulling images
26. `PodsStuckinInitState-pod.md` - Pods stuck in init container phase
27. `PodsStuckinTerminatingState-pod.md` - Pods stuck terminating
28. `PodsStuckInUnknownState-pod.md` - Pods in unknown state
29. `PodStuckinPendingDuetoNodeAffinity-pod.md` - Pod pending due to node affinity
30. `PodStuckInTerminatingState-pod.md` - Pod stuck terminating
31. `PodTerminatedWithExitCode137-pod.md` - Pod terminated (OOM killed)

## Quick Start

If you're experiencing pod issues:

1. **Pod Crashing**: Start with `CrashLoopBackOff-pod.md` or `KubePodCrashLooping-pod.md`
2. **Pod Not Starting**: See `PendingPods-pod.md` or `PodsNotBeingScheduled-pod.md`
3. **Image Issues**: Check `ImagePullBackOff-registry.md` or `PodsStuckinImagePullBackOff-registry.md`
4. **Health Checks**: See `PodFailsLivenessProbe-pod.md` or `PodFailsReadinessProbe-pod.md`
5. **Termination Issues**: Check `PodsStuckinTerminatingState-pod.md`

## Related Categories

- **02-Nodes/**: Node issues affecting pod scheduling
- **04-Workloads/**: Workload-level issues (Deployments, StatefulSets)
- **05-Networking/**: Network connectivity issues
- **06-Storage/**: Storage/volume issues affecting pods
- **08-Configuration/**: ConfigMap/Secret access issues
- **09-Resource-Management/**: Resource quota issues

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve logs from pod `<pod-name>` in namespace `<namespace>` and analyze error messages"
- "Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status and restart count"
- "Retrieve deployment `<deployment-name>` in namespace `<namespace>` and check container image name"

AI agents interpret these instructions and execute the appropriate actions using available tools (like Kubernetes MCP tools).

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**Pod Status and Information:**
```bash
# Get pod status
kubectl get pods -n <namespace>

# Describe pod for details
kubectl describe pod <pod-name> -n <namespace>
```

**Pod Logs:**
```bash
# Check pod logs
kubectl logs <pod-name> -n <namespace>

# Check previous container logs (if crashed)
kubectl logs <pod-name> -n <namespace> --previous

# Follow logs in real-time
kubectl logs <pod-name> -n <namespace> -f
```

**Pod Events:**
```bash
# Get pod events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Check pod events specifically
kubectl describe pod <pod-name> -n <namespace> | grep -A 20 "Events:"
```

**Pod Resources:**
```bash
# Check pod resource usage
kubectl top pod <pod-name> -n <namespace>

# Check pod resource requests and limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Limits:"
```

## Best Practices

### Pod Health and Monitoring
- **Health Probes**: Always configure liveness and readiness probes
- **Resource Limits**: Set appropriate CPU and memory limits
- **Log Management**: Implement proper log rotation and retention
- **Monitoring**: Set up alerts for pod restarts and failures

### Pod Design
- **Single Responsibility**: One container per concern when possible
- **Init Containers**: Use init containers for setup tasks
- **Sidecar Pattern**: Use sidecars for logging, monitoring, or proxies
- **Security Context**: Set appropriate security contexts and runAsNonRoot

### Troubleshooting Tips
- **Start with Events**: `kubectl get events` shows what happened
- **Check Logs**: Always check logs first, especially previous container logs
- **Describe Pod**: `kubectl describe` provides comprehensive information
- **Check Resource Limits**: OOM kills are common causes of pod failures
- **Verify Image**: Ensure container image exists and is accessible

### Performance Optimization
- **Resource Requests**: Set accurate resource requests for better scheduling
- **Pod Disruption Budgets**: Use PDBs to ensure availability during updates
- **Anti-Affinity**: Use anti-affinity to spread pods across nodes
- **Pod Priority**: Use priority classes for important workloads

## Additional Resources

### Official Documentation
- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/) - Pod concepts
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) - Lifecycle details
- [Troubleshooting Pods](https://kubernetes.io/docs/tasks/debug/) - Debugging guide
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) - Security guidelines

### Learning Resources
- [Pod Design Patterns](https://kubernetes.io/docs/concepts/workloads/pods/) - Design patterns
- [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) - Init container usage
- [Ephemeral Containers](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/) - Debugging with ephemeral containers

### Tools & Utilities
- [kubectl debug](https://kubernetes.io/docs/tasks/debug/) - Debug running pods
- [stern](https://github.com/stern/stern) - Multi-pod log tailing
- [kubectl-logs](https://github.com/jonmosco/kube-ps1) - Enhanced log viewing

### Community Resources
- [Kubernetes Slack #sig-apps](https://slack.k8s.io/) - Application workload discussions
- [Stack Overflow - Kubernetes Pods](https://stackoverflow.com/questions/tagged/kubernetes+pods) - Q&A

[Back to Main K8s Playbooks](../README.md)
