# Nodes Playbooks

This folder contains **24 playbooks** for troubleshooting Kubernetes node-related issues.

## What are Nodes?

Nodes are worker machines in Kubernetes that run your pods. Each node contains:
- **kubelet**: Agent that communicates with the control plane
- **kube-proxy**: Network proxy maintaining network rules
- **Container Runtime**: Software that runs containers (Docker, containerd, etc.)

## Common Issues Covered

- Node not ready
- Kubelet failures
- Node unreachable
- Resource pressure (CPU, memory, disk)
- Certificate rotation issues
- Node joining cluster problems
- Too many pods on a node
- Node Exporter metrics and monitoring issues

## Playbooks in This Folder

1. `KubeletCertificateRotationFailing-node.md` - Kubelet certificate rotation failing
2. `KubeletDown-node.md` - Kubelet service down
3. `KubeletPlegDurationHigh-node.md` - Kubelet taking too long to check pod status
4. `KubeletPodStartUpLatencyHigh-node.md` - Pods taking too long to start
5. `KubeletServiceNotRunning-node.md` - Kubelet service not running
6. `KubeletTooManyPods-node.md` - Node has too many pods
7. `KubeNodeNotReady-node.md` - Node not in ready state
8. `KubeNodeReadinessFlapping-node.md` - Node readiness state changing frequently
9. `KubeNodeUnreachable-node.md` - Node unreachable from control plane
10. `NodeCannotJoinCluster-node.md` - Node cannot join the cluster
11. `NodeDiskPressure-storage.md` - Node running out of disk space
12. `NodeNotReady-node.md` - Node not ready (general)
13. `NodeClockSkewDetected-node.md` - Node clock skew detected
14. `NodeDiskIOSaturation-node.md` - Node disk I/O saturation
15. `NodeExporterDown-node.md` - Node Exporter down
16. `NodeFileDescriptorLimit-node.md` - Node file descriptor limit reached
17. `NodeFilesystemAlmostOutOfSpace-node.md` - Node filesystem almost out of space
18. `NodeHighCPUUsage-node.md` - Node high CPU usage
19. `NodeHighLoadAverage-node.md` - Node high load average
20. `NodeHighMemoryUsage-node.md` - Node high memory usage
21. `NodeMemoryMajorPagesFaults-node.md` - Node memory major page faults
22. `NodeNetworkReceiveErrors-node.md` - Node network receive errors
23. `NodeRAIDDegraded-node.md` - Node RAID degraded
24. `NodeSystemdServiceFailed-node.md` - Node systemd service failed

## Quick Start

If you're experiencing node issues:

1. **Node Not Ready**: Start with `KubeNodeNotReady-node.md` or `NodeNotReady-node.md`
2. **Kubelet Problems**: See `KubeletDown-node.md` or `KubeletServiceNotRunning-node.md`
3. **Resource Pressure**: Check `NodeDiskPressure-storage.md` or `KubeletTooManyPods-node.md`
4. **Connection Issues**: See `KubeNodeUnreachable-node.md` or `NodeCannotJoinCluster-node.md`

## Related Categories

- **03-Pods/**: Pod scheduling issues often related to node problems
- **09-Resource-Management/**: Resource quota and capacity issues
- **01-Control-Plane/**: Control plane issues affecting node communication

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve the Node `<node-name>` and check node status and network connectivity"
- "Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status and restart count"

AI agents interpret these instructions and execute the appropriate actions using available tools.

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**Node Status and Information:**
```bash
# Check node status
kubectl get nodes

# Get detailed node information
kubectl describe node <node-name>

# Check node conditions
kubectl get nodes -o wide
kubectl get nodes -o jsonpath='{.items[*].status.conditions}'
```

**Node Resources:**
```bash
# Check node resource usage
kubectl top nodes

# Check node capacity and allocatable
kubectl describe node <node-name> | grep -A 5 "Capacity:\|Allocatable:"
```

**Kubelet and Services:**
```bash
# Check kubelet status (on the node)
systemctl status kubelet

# Check kubelet logs (on the node)
journalctl -u kubelet -f
```

**Pods and Scheduling:**
```bash
# Check pods on a node
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name>

# Check node taints and tolerations
kubectl describe node <node-name> | grep -A 5 "Taints:"
```

## Best Practices

### Node Health Monitoring
- **Regular Health Checks**: Monitor node conditions (Ready, MemoryPressure, DiskPressure, PIDPressure)
- **Resource Monitoring**: Track CPU, memory, and disk usage on nodes
- **Kubelet Health**: Monitor kubelet heartbeat and status
- **Node Capacity**: Ensure nodes have adequate resources for workloads

### Node Management
- **Taints and Tolerations**: Use taints to control pod scheduling
- **Node Labels**: Use labels for node selection and organization
- **Drain Before Maintenance**: Always drain nodes before maintenance
- **Cordon/Uncordon**: Use cordon to prevent new pods from scheduling

### Troubleshooting Tips
- **Check Node Conditions**: Start with `kubectl describe node` to see all conditions
- **Review Kubelet Logs**: Kubelet logs provide detailed information about node issues
- **Check Resource Pressure**: Memory, disk, or PID pressure can cause node issues
- **Verify Network**: Ensure node can communicate with control plane
- **Check Certificates**: Node certificates must be valid for kubelet to function

### Performance Optimization
- **Resource Requests**: Set appropriate resource requests for pods
- **Node Affinity**: Use node affinity for workload placement
- **Pod Density**: Monitor pod density per node (kubelet has limits)
- **Disk Space**: Regularly clean up unused images and containers

## Additional Resources

### Official Documentation
- [Kubernetes Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) - Node architecture
- [Node Troubleshooting](https://kubernetes.io/docs/tasks/debug/) - Debugging guide
- [Kubelet Configuration](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/) - Kubelet config
- [Node Lifecycle](https://kubernetes.io/docs/concepts/architecture/nodes/#node-lifecycle) - Node lifecycle management

### Learning Resources
- [Kubelet Deep Dive](https://kubernetes.io/docs/concepts/architecture/nodes/#kubelet) - Kubelet details
- [Node Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) - Resource management
- [Node Maintenance](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) - Safe node draining

### Tools & Utilities
- [kubectl debug](https://kubernetes.io/docs/tasks/debug/) - Debug pods on nodes
- [Node Problem Detector](https://github.com/kubernetes/node-problem-detector) - Automated problem detection
- [kubectl top](https://kubernetes.io/docs/reference/kubectl/kubectl_top/) - Resource usage monitoring

### Community Resources
- [Kubernetes Slack #sig-node](https://slack.k8s.io/) - Node-related discussions
- [Stack Overflow - Kubernetes Nodes](https://stackoverflow.com/questions/tagged/kubernetes+nodes) - Q&A

[Back to Main K8s Playbooks](../README.md)
