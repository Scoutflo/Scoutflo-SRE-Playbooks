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

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and other pressure conditions
   - Events section showing NodeNotReady, KubeletNotReady events with timestamps
   - Allocated resources showing current usage

2. List events filtered by involved object name <node-name> and kind Node, sorted by last timestamp to see the sequence of node issues.

3. Retrieve node <node-name> conditions to see Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable status and lastTransitionTime.

4. Retrieve resource usage metrics for node <node-name> to see current CPU and memory utilization.

5. Access node via SSH and check kubelet status:
   - Verify if kubelet service is running
   - Retrieve recent kubelet logs from the last 10 minutes
   - Check kubelet logs for error messages

6. Check disk and memory on node (SSH required):
   - Verify disk space usage
   - Check memory availability
   - Analyse process resource usage

7. Check container runtime health (SSH required):
   - Verify containerd or docker service status
   - Confirm runtime is responding

8. Check API server connectivity from node (SSH required): Verify network path to control plane by testing API server health endpoint.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify the primary cause of NotReady. Events with reason "KubeletNotReady" or "KubeletStopped" indicate kubelet service issues. Events with reason "NodeHasDiskPressure", "NodeHasMemoryPressure", or "NodeHasPIDPressure" indicate resource exhaustion.

2. If node events indicate kubelet issues (KubeletNotReady), verify kubelet service status from Playbook step 5. Check if kubelet is running, stopped, or in a crash loop. Review kubelet logs for error messages explaining the failure.

3. If node events indicate resource pressure conditions, correlate with node conditions from Playbook step 3 to identify which resource is exhausted. Verify using disk and memory checks from Playbook step 6 to confirm the specific resource constraint.

4. If node events show no kubelet or resource issues, check API server connectivity results from Playbook step 8. Network connectivity failures prevent kubelet from reporting node status, causing NotReady state.

5. If node events indicate container runtime issues (ContainerRuntimeDown), verify container runtime health from Playbook step 7. Kubelet depends on the container runtime and cannot function if runtime is unhealthy.

6. If node events are inconclusive, compare resource usage metrics from Playbook step 4 with node capacity to identify if CPU or memory exhaustion is affecting kubelet health checks.

7. Analyze node condition lastTransitionTime from Playbook step 3 to determine if NotReady is persistent (consistent timestamps) or intermittent (recent transitions), which helps distinguish between node failure and network instability.

**If no root cause is identified from events**: Extend analysis to node system logs, check for hardware failures or kernel issues, verify if multiple nodes are affected (indicating cluster-wide problems), and review infrastructure change records for recent modifications that may have affected node health.
