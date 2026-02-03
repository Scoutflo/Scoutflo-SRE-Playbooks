# Capacity Trend Analysis

## Meaning

Capacity trend analysis indicates that capacity utilization trends cannot be analyzed or capacity growth patterns are not identified (triggering alerts like CapacityTrendUnavailable or CapacityAnalysisFailed) because capacity trend data is unavailable, capacity growth patterns are not detected, capacity utilization trends show anomalies, capacity analysis tools fail, or capacity trend metrics are inaccurate. Capacity trend metrics show unavailable data, capacity growth patterns cannot be identified, capacity utilization trends show anomalies, and capacity analysis fails. This affects the capacity planning layer and resource optimization, typically caused by capacity monitoring failures, trend analysis tool unavailability, capacity data collection issues, or capacity pattern detection failures; if capacity trends affect container workloads, container capacity needs may not be identified and applications may experience capacity planning failures.

## Impact

CapacityTrendUnavailable alerts fire; CapacityAnalysisFailed alerts fire; capacity trends cannot be analyzed; capacity growth patterns are not identified; capacity planning decisions cannot be made; capacity constraints may occur unexpectedly. Capacity trend analysis is unavailable; if capacity trends affect container workloads, container capacity needs may not be identified, pod scaling trends may be unknown, and container applications may experience capacity planning failures; applications may experience capacity shortages or unexpected capacity constraints.

## Playbook

1. Describe all nodes to understand current capacity utilization and resource allocation across the cluster.

2. List recent events across all namespaces sorted by timestamp to identify any recent scaling issues or resource constraints.

3. Describe resource quota in namespace <namespace> to analyze current capacity utilization against quotas.

4. Retrieve Prometheus metrics for pod capacity utilization including CPU utilization and memory utilization over the last 180 days to analyze capacity trends and identify growth patterns.

5. List horizontal pod autoscalers in namespace <namespace> to analyze scaling capacity trends and autoscaler behavior.

6. Compare capacity utilization trend data with capacity growth pattern detection results and verify whether growth patterns are accurately identified, using Prometheus metrics as supporting evidence.

7. Retrieve Prometheus metrics for resource quota capacity including quota usage trends over the last 180 days to identify capacity quota trends.

8. Analyze capacity utilization distribution patterns over the last 180 days to identify seasonal capacity trends or capacity spikes that affect planning.

## Diagnosis

1. Review the node capacity from Step 1 and quota utilization from Step 3. If utilization is high relative to capacity, then capacity expansion is needed. If utilization is low, then current capacity is adequate.

2. Analyze the 180-day utilization trends from Step 4. If trends show consistent growth, identify the growth rate to forecast when capacity limits will be reached. If trends are flat, capacity planning is less urgent.

3. If Step 5 HPA behavior shows frequent scaling to maximum replicas, then capacity constraints are occurring and trend analysis should have identified this. If HPAs rarely reach limits, then capacity is adequate.

4. Review the quota trend analysis from Step 7. If quota utilization is growing faster than expected, then capacity provisioning needs to accelerate. If growth is as expected, then current planning is on track.

5. If Step 8 distribution analysis shows seasonal patterns or spikes, incorporate these patterns into capacity planning to avoid seasonal capacity constraints.

If analysis is inconclusive: Examine events from Step 2 for scaling issues or resource constraints. Review the growth pattern detection from Step 6 to verify patterns are being identified. Determine whether capacity trends are consistent across resource types or concentrated in specific resources requiring targeted expansion.
