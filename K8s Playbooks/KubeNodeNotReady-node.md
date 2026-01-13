---
title: Kube Node Not Ready
weight: 20
---

# KubeNodeNotReady

## Meaning

A node has its Ready condition marked False or Unknown (triggering alerts like KubeNodeNotReady or KubeNodeUnreachable) because kubelet health checks are failing, the node is under resource pressure (MemoryPressure, DiskPressure, PIDPressure), or the kubelet cannot reliably communicate with the control plane. Nodes show NotReady condition in cluster dashboards, kubelet logs show connection timeout errors or health check failures, and node metrics indicate resource pressure or connectivity issues. This affects the data plane and prevents the node from scheduling new pods or maintaining existing workloads, typically caused by kubelet failures, resource exhaustion, network connectivity issues, or node hardware problems; applications running on affected nodes may experience errors or become unreachable.

## Impact

KubeNodeNotReady alerts fire; node cannot host new pods; existing pods may become unreachable; workloads may be rescheduled to other nodes; node condition transitions to NotReady state; pod scheduling fails for this node; node capacity is unavailable; pods on affected node may become unreachable or be evicted; service degradation or unavailability for pods on affected node. Pods remain in Pending state waiting for node resources; node shows NotReady condition indefinitely in kubectl; cluster capacity is reduced; deployments may show replica count mismatches; applications running on affected nodes may experience errors or performance degradation.

## Playbook

1. Retrieve the Node `<node-name>` and inspect its status to check Ready condition status, reason, and message to verify NotReady state.

2. Retrieve the Node `<node-name>` and check node conditions including MemoryPressure, DiskPressure, PIDPressure, and NetworkUnavailable to identify resource pressure.

3. Retrieve events for the Node `<node-name>` and filter for error patterns including 'NodeNotReady', 'KubeletNotReady', 'NodeHasInsufficientMemory', 'NodeHasDiskPressure' to identify node health issues.

4. Check kubelet status and health on the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available to verify kubelet operation.

5. Verify network connectivity between the Node `<node-name>` and API server endpoints to identify connectivity issues.

6. Retrieve metrics for the Node `<node-name>` and check node resource usage metrics for CPU, memory, and disk to identify resource pressure.

## Diagnosis

Compare node NotReady condition transition timestamps with kubelet failure or restart timestamps within 5 minutes and verify whether node became NotReady when kubelet failed, using node conditions and kubelet status as supporting evidence.

Correlate node NotReady detection with node resource pressure condition transitions within 5 minutes and verify whether NotReady state aligns with MemoryPressure, DiskPressure, or PIDPressure conditions, using node conditions and resource metrics as supporting evidence.

Compare node NotReady timestamps with API server connectivity failure times within 5 minutes and verify whether node lost connectivity to control plane, using kubelet logs and API server connection metrics as supporting evidence.

Analyze node condition transition patterns over the last 15 minutes to determine if NotReady is persistent (node failure) or intermittent (network issues), using node condition history and kubelet status as supporting evidence.

Correlate node NotReady with network policy or firewall rule change timestamps within 10 minutes and verify whether connectivity issues began after network configuration changes, using network policy events and node network metrics as supporting evidence.

Compare node resource usage metrics with resource capacity at NotReady times and verify whether resource exhaustion caused node health check failures, using node metrics and resource thresholds as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review node system logs, check for hardware failures, verify container runtime health, examine historical node stability patterns. Node NotReady may result from node hardware issues, operating system problems, or persistent network partitions rather than immediate configuration changes.
