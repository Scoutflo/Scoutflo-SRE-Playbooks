---
title: Kubelet Too Many Pods
weight: 20
---

# KubeletTooManyPods

## Meaning

A specific node is running more than 95% of its pod capacity limit (110 by default, configurable) (triggering KubeletTooManyPods alerts) because the node has reached or is approaching the maximum number of pods it can support. Nodes show high pod count approaching capacity limits in cluster dashboards, node metrics indicate resource pressure from high pod density, and pod scheduling may fail for additional pods. This affects the data plane and indicates that pod density is too high, which may strain the Container Runtime Interface (CRI), Container Network Interface (CNI), and operating system resources, typically caused by scheduling imbalances, cluster capacity constraints, or workload distribution issues; applications running on affected nodes may experience performance degradation.

## Impact

KubeletTooManyPods alerts fire; running many pods on a single node places strain on CRI, CNI, and operating system; approaching pod limit may affect performance and availability of that node; node may become unable to schedule additional pods; node performance may degrade; container runtime operations may slow down; CRI, CNI, and operating system resources are strained. Nodes show high pod count approaching capacity limits; pod scheduling fails for additional pods; node performance degrades; applications running on affected nodes may experience performance degradation or resource contention.

## Playbook

1. List Pod resources scheduled on the Node `<node-name>` and check the number of pods on node to verify high pod density.

2. Retrieve the Node `<node-name>` and retrieve node capacity metrics including maximum pods configuration and current pod count to verify pod capacity limits.

3. Retrieve metrics for the Node `<node-name>` and check node resource usage including CPU, memory, and network to identify resource pressure from high pod density.

4. Retrieve the Node `<node-name>` and verify node conditions and performance metrics to assess impact of high pod density.

5. List Pod resources across the cluster and check pod distribution across the cluster to identify if pod density is concentrated on specific nodes.

6. Verify cluster autoscaler status and node availability for redistributing pod load by checking cluster autoscaler configuration and node pool status.

## Diagnosis

Compare pod count increase timestamps on node `<node-name>` with deployment or HPA scaling event timestamps within 30 minutes and verify whether pod count increased when workloads scaled, using pod count metrics and deployment scaling history as supporting evidence.

Correlate high pod count detection with node performance degradation timestamps within 5 minutes and verify whether high pod density caused node performance issues, using node performance metrics and pod count as supporting evidence.

Compare pod count on node `<node-name>` with other node pod counts to determine if high pod density is isolated (scheduling issue) or cluster-wide (capacity issue), using pod distribution across nodes and node capacity data as supporting evidence.

Analyze pod count growth trends on node `<node-name>` over the last 24 hours to identify if growth is gradual (normal scaling) or sudden (scheduling imbalance), using pod count history and scheduling events as supporting evidence.

Correlate high pod count with pod scheduling failure timestamps on other nodes within 30 minutes and verify whether scheduling constraints caused pods to concentrate on node `<node-name>`, using pod scheduling events and node availability as supporting evidence.

Compare current pod count with node maximum pod capacity configuration to verify whether pod count is approaching or exceeding limits, using node capacity settings and current pod count as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 24 hours for capacity analysis, review pod scheduling policies, check for cluster capacity limitations, verify node pool configurations, examine historical pod distribution patterns. High pod count may result from scheduling imbalances, cluster capacity constraints, or workload distribution issues rather than immediate changes.
