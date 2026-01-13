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

1. Retrieve the Node `<node-name>` and inspect its status to check Ready condition status, transition history, and condition timestamps to verify readiness flapping.

2. Retrieve the Node `<node-name>` and check node conditions including MemoryPressure, DiskPressure, PIDPressure, and NetworkUnavailable that may cause readiness flapping.

3. Retrieve events for the Node `<node-name>` and filter for condition transition patterns including 'NodeNotReady', 'NodeReady', 'KubeletNotReady' to identify flapping causes.

4. Check kubelet status and health on the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available to verify kubelet instability.

5. Verify network connectivity stability between the Node `<node-name>` and API server endpoints to identify intermittent connectivity issues.

6. Retrieve metrics for the Node `<node-name>` and check node resource usage metrics for CPU, memory, and disk to identify resource pressure patterns.

## Diagnosis

Compare node readiness flapping detection timestamps with node resource pressure condition transition times within 5 minutes and verify whether readiness flapping coincides with resource pressure fluctuations, using node conditions and readiness transitions as supporting evidence.

Correlate node readiness flapping with network connectivity instability timestamps within 5 minutes and verify whether intermittent network issues cause readiness to flap, using network metrics and kubelet connection logs as supporting evidence.

Compare node readiness flapping patterns with kubelet health check failure timestamps within 5 minutes and verify whether kubelet health check instability causes readiness flapping, using kubelet logs and readiness probe results as supporting evidence.

Analyze node readiness transition frequency over the last 15 minutes to determine if flapping is rapid (network issues) or slower (resource pressure), using node condition history and transition timestamps as supporting evidence.

Correlate node readiness flapping with API server connectivity instability timestamps within 5 minutes and verify whether API server connectivity issues cause readiness to flap, using API server connection metrics and kubelet logs as supporting evidence.

Compare node readiness flapping with other node readiness issues within the same timeframe and verify whether flapping is isolated to single node or affects multiple nodes (cluster-wide issue), using node status across cluster and flapping patterns as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review node system logs, check for hardware instabilities, verify network infrastructure health, examine historical node stability patterns. Node readiness flapping may result from network instability, hardware issues, or node-level resource management problems rather than immediate configuration changes.
