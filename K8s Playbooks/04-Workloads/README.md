# Workloads Playbooks

This folder contains **23 playbooks** for troubleshooting Kubernetes workload resource issues.

## What are Workloads?

Workloads are higher-level resources that manage pods. They include:
- **Deployments**: Manage stateless applications
- **StatefulSets**: Manage stateful applications with stable identities
- **DaemonSets**: Ensure pods run on all (or selected) nodes
- **Jobs**: Run tasks to completion
- **CronJobs**: Run jobs on a schedule
- **HPA (Horizontal Pod Autoscaler)**: Automatically scale pods

## Common Issues Covered

- Deployment scaling problems
- StatefulSet replica mismatches
- DaemonSet scheduling issues
- Job completion failures
- HPA not scaling
- Workload generation mismatches
- Resource request/limit issues

## Playbooks in This Folder

1. `CannotScaleDeploymentBeyondNodeCapacity-workload.md` - Cannot scale beyond node capacity
2. `DaemonSetNotDeployingPodsonAllNodes-daemonset.md` - DaemonSet not deploying on all nodes
3. `DaemonSetPodsNotDeploying-daemonset.md` - DaemonSet pods not deploying
4. `DaemonSetPodsNotRunningonSpecificNode-daemonset.md` - DaemonSet not running on specific node
5. `DeploymentNotScalingProperly-deployment.md` - Deployment not scaling correctly
6. `DeploymentNotUpdating-deployment.md` - Deployment not updating
7. `HPAHorizontalPodAutoscalerNotScaling-workload.md` - HPA not scaling pods
8. `HPANotRespondingtoCustomMetrics-workload.md` - HPA not responding to custom metrics
9. `HPANotRespondingtoMetrics-workload.md` - HPA not responding to metrics
10. `InvalidMemoryCPURequests-workload.md` - Invalid CPU/memory requests
11. `JobFailingToComplete-job.md` - Job failing to complete
12. `KubeDaemonSetMisScheduled-daemonset.md` - DaemonSet pods mis-scheduled
13. `KubeDaemonSetNotScheduled-daemonset.md` - DaemonSet pods not scheduled
14. `KubeDaemonSetRolloutStuck-daemonset.md` - DaemonSet rollout stuck
15. `KubeDeploymentGenerationMismatch-deployment.md` - Deployment generation mismatch
16. `KubeDeploymentReplicasMismatch-deployment.md` - Deployment replica count mismatch
17. `KubeHpaMaxedOut-workload.md` - HPA maxed out at maximum replicas
18. `KubeHpaReplicasMismatch-workload.md` - HPA replica count mismatch
19. `KubeJobCompletion-workload.md` - Job completion issues
20. `KubeJobFailed-workload.md` - Job failed
21. `KubeStatefulSetGenerationMismatch-statefulset.md` - StatefulSet generation mismatch
22. `KubeStatefulSetReplicasMismatch-statefulset.md` - StatefulSet replica mismatch
23. `KubeStatefulSetUpdateNotRolledOut-statefulset.md` - StatefulSet update not rolling out

## Quick Start

If you're experiencing workload issues:

1. **Deployment Problems**: Start with `DeploymentNotScalingProperly-deployment.md` or `DeploymentNotUpdating-deployment.md`
2. **StatefulSet Issues**: See `KubeStatefulSetReplicasMismatch-statefulset.md`
3. **DaemonSet Problems**: Check `DaemonSetPodsNotDeploying-daemonset.md`
4. **HPA Not Working**: See `HPAHorizontalPodAutoscalerNotScaling-workload.md`
5. **Job Failures**: Check `JobFailingToComplete-job.md` or `KubeJobFailed-workload.md`

## Related Categories

- **03-Pods/**: Individual pod issues affecting workloads
- **02-Nodes/**: Node capacity issues affecting scaling
- **09-Resource-Management/**: Resource quota issues
- **10-Monitoring-Autoscaling/**: Metrics and autoscaling issues

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve deployment `<deployment-name>` in namespace `<namespace>` and check deployment status and replica count"
- "Retrieve StatefulSet `<statefulset-name>` in namespace `<namespace>` and verify replica count matches desired state"
- "Retrieve HPA `<hpa-name>` in namespace `<namespace>` and check scaling metrics and current replica count"

AI agents interpret these instructions and execute the appropriate actions using available tools.

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**Deployments:**
```bash
# Check deployment status
kubectl get deployments -n <namespace>

# Describe deployment
kubectl describe deployment <deployment-name> -n <namespace>

# Check deployment rollout status
kubectl rollout status deployment/<deployment-name> -n <namespace>
```

**StatefulSets:**
```bash
# Check StatefulSet status
kubectl get statefulsets -n <namespace>

# Describe StatefulSet
kubectl describe statefulset <statefulset-name> -n <namespace>
```

**DaemonSets:**
```bash
# Check DaemonSet status
kubectl get daemonsets -n <namespace>

# Describe DaemonSet
kubectl describe daemonset <daemonset-name> -n <namespace>
```

**HPA:**
```bash
# Check HPA status
kubectl get hpa -n <namespace>

# Describe HPA
kubectl describe hpa <hpa-name> -n <namespace>
```

**Workload Events:**
```bash
# Check workload events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

## Best Practices

### Deployment Best Practices
- **Rolling Updates**: Use rolling update strategy for zero-downtime deployments
- **Resource Limits**: Always set resource requests and limits
- **Readiness Probes**: Configure readiness probes for proper traffic routing
- **Pod Disruption Budgets**: Use PDBs to ensure availability during updates
- **Replica Management**: Start with 2+ replicas for high availability

### StatefulSet Best Practices
- **Stable Storage**: Use PersistentVolumes for stateful data
- **Ordered Pod Management**: Understand ordered startup/termination
- **Headless Services**: Use headless services for stable network identities
- **Backup Strategy**: Implement regular backups for stateful data

### DaemonSet Best Practices
- **Node Selection**: Use node selectors or taints/tolerations for placement
- **Update Strategy**: Choose appropriate update strategy (RollingUpdate or OnDelete)
- **Resource Management**: Monitor resource usage as DaemonSets run on all nodes

### HPA Best Practices
- **Metrics Server**: Ensure Metrics Server is running and healthy
- **Resource Metrics**: Start with CPU/memory metrics before custom metrics
- **Min/Max Replicas**: Set appropriate min and max replica counts
- **Scaling Policies**: Configure scaling policies for smooth scaling

### Troubleshooting Tips
- **Check Replica Status**: Verify desired vs. current replicas
- **Review Events**: Events show why scaling or updates failed
- **Check Resource Quotas**: Quotas can prevent scaling
- **Verify Node Capacity**: Nodes must have capacity for new pods
- **Check HPA Metrics**: Ensure metrics are available for HPA decisions

## Additional Resources

### Official Documentation
- [Kubernetes Workloads](https://kubernetes.io/docs/concepts/workloads/) - Workload overview
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) - Deployment guide
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) - StatefulSet guide
- [DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) - DaemonSet guide
- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) - Job guide
- [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) - Autoscaling guide

### Learning Resources
- [Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#deployment-strategies) - Update strategies
- [StatefulSet Patterns](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/) - StatefulSet patterns
- [HPA Walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) - HPA tutorial

### Tools & Utilities
- [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/kubectl_rollout/) - Rollout management
- [kubectl scale](https://kubernetes.io/docs/reference/kubectl/kubectl_scale/) - Scaling commands
- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server) - Resource metrics

### Community Resources
- [Kubernetes Slack #sig-apps](https://slack.k8s.io/) - Application workload discussions
- [Stack Overflow - Kubernetes Deployments](https://stackoverflow.com/questions/tagged/kubernetes+deployment) - Q&A

[Back to Main K8s Playbooks](../README.md)
