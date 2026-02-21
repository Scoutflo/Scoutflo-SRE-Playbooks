# Kubernetes Node Playbooks

> **24 playbooks** for Node health, Kubelet, and NodeExporter issues.

## Node Health Playbooks

| Playbook | Description |
|----------|-------------|
| [KubeNodeNotReady](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeNodeNotReady-node.md) | Node not ready alert response |
| [KubeNodeReadinessFlapping](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeNodeReadinessFlapping-node.md) | Unstable node readiness |
| [KubeNodeUnreachable](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeNodeUnreachable-node.md) | Unreachable node troubleshooting |
| [NodeNotReady](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeNotReady-node.md) | General node not ready issues |
| [NodeCannotJoinCluster](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeCannotJoinCluster-node.md) | Node join failures |
| [NodeClockSkewDetected](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeClockSkewDetected-node.md) | Time synchronization issues |

## Kubelet Playbooks

| Playbook | Description |
|----------|-------------|
| [KubeletDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletDown-node.md) | Kubelet service down |
| [KubeletServiceNotRunning](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletServiceNotRunning-node.md) | Kubelet service stopped |
| [KubeletCertificateRotationFailing](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletCertificateRotationFailing-node.md) | Certificate rotation failures |
| [KubeletPlegDurationHigh](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletPlegDurationHigh-node.md) | High PLEG duration |
| [KubeletPodStartUpLatencyHigh](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletPodStartUpLatencyHigh-node.md) | Slow pod startup |
| [KubeletTooManyPods](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/KubeletTooManyPods-node.md) | Pod limit exceeded |

## Node Resource Playbooks

| Playbook | Description |
|----------|-------------|
| [NodeHighCPUUsage](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeHighCPUUsage-node.md) | High CPU utilization |
| [NodeHighMemoryUsage](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeHighMemoryUsage-node.md) | High memory utilization |
| [NodeHighLoadAverage](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeHighLoadAverage-node.md) | High system load |
| [NodeMemoryMajorPagesFaults](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeMemoryMajorPagesFaults-node.md) | Memory page faults |
| [NodeDiskPressure](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeDiskPressure-storage.md) | Disk pressure condition |
| [NodeDiskIOSaturation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeDiskIOSaturation-node.md) | Disk I/O saturation |
| [NodeFilesystemAlmostOutOfSpace](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeFilesystemAlmostOutOfSpace-node.md) | Low disk space |
| [NodeFileDescriptorLimit](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeFileDescriptorLimit-node.md) | File descriptor exhaustion |

## Node System Playbooks

| Playbook | Description |
|----------|-------------|
| [NodeNetworkReceiveErrors](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeNetworkReceiveErrors-node.md) | Network receive errors |
| [NodeRAIDDegraded](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeRAIDDegraded-node.md) | RAID degradation alert |
| [NodeSystemdServiceFailed](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeSystemdServiceFailed-node.md) | Systemd service failures |
| [NodeExporterDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/02-Nodes/NodeExporterDown-node.md) | Node exporter not running |

---

[Back to K8s Overview](/k8s/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/K8s%20Playbooks/02-Nodes)
