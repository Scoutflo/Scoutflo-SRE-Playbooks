# Resource Management Playbooks

This folder contains **8 playbooks** for troubleshooting Kubernetes resource quota and capacity issues.

## What is Resource Management?

Kubernetes resource management controls how compute resources (CPU, memory) are allocated and limited:
- **Resource Quotas**: Limit resource consumption per namespace
- **Resource Requests**: Minimum resources a pod needs
- **Resource Limits**: Maximum resources a pod can use
- **Overcommit**: Allowing more requests than available resources

## Common Issues Covered

- Resource quota exceeded
- CPU and memory overcommit
- Quota exhaustion
- Compute resource constraints
- High CPU/memory usage

## Playbooks in This Folder

1. `HighCPUUsage-compute.md` - High CPU usage
2. `KubeCPUOvercommit-compute.md` - CPU overcommit issues
3. `KubeCPUQuotaOvercommit-namespace.md` - CPU quota overcommit
4. `KubeMemoryOvercommit-compute.md` - Memory overcommit issues
5. `KubeMemoryQuotaOvercommit-namespace.md` - Memory quota overcommit
6. `KubeQuotaAlmostFull-namespace.md` - Resource quota almost full
7. `KubeQuotaExceeded-namespace.md` - Resource quota exceeded
8. `KubeQuotaFullyUsed-namespace.md` - Resource quota fully used

## Quick Start

If you're experiencing resource management issues:

1. **Quota Exceeded**: Start with `KubeQuotaExceeded-namespace.md` or `KubeQuotaFullyUsed-namespace.md`
2. **Overcommit Issues**: See `KubeCPUOvercommit-compute.md` or `KubeMemoryOvercommit-compute.md`
3. **High Usage**: Check `HighCPUUsage-compute.md`
4. **Quota Warnings**: See `KubeQuotaAlmostFull-namespace.md`

## Related Categories

- **03-Pods/**: Pod resource issues
- **02-Nodes/**: Node capacity issues
- **04-Workloads/**: Workload scaling issues related to resources
- **10-Monitoring-Autoscaling/**: Metrics and autoscaling

## Useful Commands

### Resource Quotas
```bash
# Check resource quotas
kubectl get resourcequota -n <namespace>
kubectl get quota -n <namespace>  # Short form

# Describe resource quota
kubectl describe resourcequota <quota-name> -n <namespace>

# Check quota usage
kubectl get resourcequota <quota-name> -n <namespace> -o yaml

# Check all quotas in namespace
kubectl get resourcequota -n <namespace> -o jsonpath='{.items[*].status.used}'
```

### Resource Usage
```bash
# Check pod resource usage
kubectl top pods -n <namespace>

# Check node resource usage
kubectl top nodes

# Check specific pod usage
kubectl top pod <pod-name> -n <namespace>

# Check resource usage for all namespaces
kubectl top pods --all-namespaces
```

### Resource Requests and Limits
```bash
# Check pod resource requests/limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Limits:"

# Get resource requests/limits in JSON
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].resources}'

# Check deployment resource requests/limits
kubectl get deployment <deployment-name> -n <namespace> -o jsonpath='{.spec.template.spec.containers[*].resources}'
```

### Namespace Resources
```bash
# Check namespace resource usage
kubectl describe namespace <namespace>

# Check namespace resource quota
kubectl get namespace <namespace> -o jsonpath='{.status}'

# Check all resource quotas
kubectl get resourcequota --all-namespaces
```

### Limit Ranges
```bash
# Check limit ranges
kubectl get limitrange -n <namespace>

# Describe limit range
kubectl describe limitrange <limitrange-name> -n <namespace>

# View limit range rules
kubectl get limitrange <limitrange-name> -n <namespace> -o yaml
```

### Resource Analysis
```bash
# Check total resource requests in namespace
kubectl get pods -n <namespace> -o json | jq '[.items[].spec.containers[].resources.requests.cpu // "0" | rtrimstr("m") | tonumber] | add'

# Check total resource limits in namespace
kubectl get pods -n <namespace> -o json | jq '[.items[].spec.containers[].resources.limits.memory // "0" | rtrimstr("Mi") | tonumber] | add'

# Compare requests vs limits
kubectl get pods -n <namespace> -o custom-columns=NAME:.metadata.name,CPU-REQ:.spec.containers[*].resources.requests.cpu,CPU-LIM:.spec.containers[*].resources.limits.cpu
```

## Best Practices

### Resource Management
- **Set Requests**: Always set resource requests for better scheduling
- **Set Limits**: Set limits to prevent resource exhaustion
- **Right-sizing**: Regularly review and adjust resource requests/limits
- **Resource Quotas**: Use quotas to prevent resource exhaustion in namespaces

### Quota Design
- **Namespace Quotas**: Set quotas per namespace based on needs
- **Quota Scope**: Use quota scopes for fine-grained control
- **Quota Monitoring**: Monitor quota usage and set up alerts
- **Quota Planning**: Plan quotas based on workload requirements

### Performance Optimization
- **CPU Requests**: Set CPU requests based on baseline usage
- **Memory Requests**: Set memory requests based on average usage
- **Burst Capacity**: Allow limits higher than requests for burst capacity
- **Node Affinity**: Use node affinity for resource-intensive workloads

### Troubleshooting Tips
- **Check Quota Status**: Verify quota usage vs. hard limits
- **Resource Requests**: Ensure pods have resource requests set
- **Node Capacity**: Check if nodes have capacity for new pods
- **Quota Scope**: Verify quota scope matches your use case
- **Limit Ranges**: Check if limit ranges are preventing pod creation

## Additional Resources

### Official Documentation
- [Kubernetes Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) - Quota guide
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) - Resource management
- [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/) - Limit range guide
- [Resource Quota API](https://kubernetes.io/docs/reference/kubernetes-api/policy-resources/resource-quota-v1/) - API reference

### Learning Resources
- [Resource Quota Examples](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes) - Quota examples
- [Resource Requests Best Practices](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-requests-and-limits-of-pod-and-container) - Best practices
- [Quota Scopes](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes) - Scope explanation

### Tools & Utilities
- [kubectl-top](https://kubernetes.io/docs/reference/kubectl/kubectl_top/) - Resource usage monitoring
- [Kubecost](https://www.kubecost.com/) - Cost and resource monitoring
- [Goldilocks](https://github.com/FairwindsOps/goldilocks) - Resource right-sizing tool

### Community Resources
- [Kubernetes Slack #sig-scheduling](https://slack.k8s.io/) - Scheduling and resource discussions
- [Stack Overflow - Kubernetes Resource Quota](https://stackoverflow.com/questions/tagged/kubernetes+resource-quota) - Q&A

[Back to Main K8s Playbooks](../README.md)
