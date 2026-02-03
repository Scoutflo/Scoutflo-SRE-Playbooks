---
title: Kube Node Readiness Flapping
weight: 20
---

# KubeNodeReadinessFlapping

## Meaning

The readiness status of a node has changed multiple times in the last 15 minutes (triggering KubeNodeReadinessFlapping alerts) because the node Ready condition is transitioning between True and False repeatedly, indicating unstable node health, intermittent connectivity issues, or resource pressure causing repeated health check failures. Nodes show repeated Ready condition transitions in cluster dashboards, node events show NodeNotReady and NodeReady transitions, and node conditions may show intermittent MemoryPressure, DiskPressure, or NetworkUnavailable. This affects the data plane and indicates node instability that may cause pod scheduling and workload disruption, typically caused by network instability, resource pressure fluctuations, or kubelet health check issues; applications running on affected nodes may experience disruption.

## Impact

KubeNodeReadinessFlapping alerts fire; performance of cluster deployments is affected; node condition transitions between Ready and NotReady repeatedly; pods may be rescheduled repeatedly; workloads experience disruption; node capacity availability fluctuates; service endpoints may be added and removed repeatedly; node instability causes pod scheduling and workload disruption. Nodes show repeated Ready condition transitions; pods may be rescheduled repeatedly; service endpoints may be added and removed repeatedly; applications running on affected nodes may experience disruption or performance degradation.

## Playbook

1. Describe node <node-name> to see:
   - Conditions section showing Ready status, transition history, and timestamps
   - Events section showing NodeNotReady and NodeReady transitions
   - Pressure conditions (MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable)

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of condition transitions including 'NodeNotReady', 'NodeReady', 'KubeletNotReady'.

3. Check node conditions for node <node-name> to see Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable status and lastTransitionTime.

4. Check kubelet status and health on the Node <node-name> by accessing via Pod Exec tool or SSH if node access is available to verify kubelet instability.

5. Verify network connectivity stability between the Node <node-name> and API server endpoints to identify intermittent connectivity issues.

6. Retrieve resource usage metrics for node <node-name> to see CPU and memory utilization and identify resource pressure patterns.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify the pattern of readiness transitions. Count events showing "NodeNotReady" and "NodeReady" transitions and note the timestamps to understand the flapping frequency and pattern.

2. If node events show rapid transitions (multiple within minutes), this typically indicates network connectivity instability between kubelet and API server. Verify network connectivity stability from Playbook step 5 and correlate network test results with event timestamps.

3. If node events show slower transitions with resource pressure conditions (NodeHasMemoryPressure, NodeHasDiskPressure, NodeHasPIDPressure), check node conditions from Playbook step 3. Resource pressure fluctuating near thresholds causes readiness to flap as conditions toggle.

4. If node events indicate kubelet health check failures (KubeletNotReady followed by KubeletReady), check kubelet status and health from Playbook step 4. Kubelet instability or resource constraints can cause intermittent health check failures.

5. If node events show flapping correlated with resource metrics, verify CPU and memory utilization from Playbook step 6. Sustained high resource usage near capacity causes intermittent health check timeouts.

6. If node events show readiness flapping on multiple nodes simultaneously, this indicates cluster-wide issues such as API server performance problems, network infrastructure instability, or control plane resource constraints rather than individual node issues.

7. Analyze the node condition lastTransitionTime frequency from Playbook step 3 to determine if flapping is ongoing or has stabilized, which helps assess whether the issue is actively occurring or has resolved.

**If no root cause is identified from events**: Review kubelet logs for warnings between flapping transitions, check for intermittent hardware issues (disk I/O spikes, memory pressure), verify network infrastructure stability, and examine if node autoscaling or pod scheduling patterns are causing resource fluctuations.
