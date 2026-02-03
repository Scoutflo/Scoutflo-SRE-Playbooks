# Spot Instance Management

## Meaning

Spot instance management indicates that spot node interruptions are frequent, spot node capacity is unavailable, or spot node usage is not optimized (triggering alerts like SpotNodeInterrupted or SpotNodeCapacityUnavailable) because spot node interruption rates exceed thresholds, spot node capacity requests fail, spot node termination notices are frequent, spot node price fluctuations cause interruptions, or spot node allocation strategies are suboptimal. Spot node interruption metrics show high rates, spot node capacity requests show failures, spot node termination notices are frequent, and spot node price metrics indicate volatility. This affects the cost management layer and spot node lifecycle management, typically caused by spot node capacity constraints, spot node price volatility, spot node interruption handling failures, or spot node allocation strategy misconfigurations; if spot nodes host container workloads, container workloads may be interrupted and applications may experience availability issues.

## Impact

SpotNodeInterrupted alerts fire; SpotNodeCapacityUnavailable alerts fire; spot node interruptions cause workload disruptions; spot node capacity is unavailable; spot node termination notices are frequent; cost optimization from spot nodes is not achieved. Spot node interruption metrics show high rates; if spot nodes host container workloads, container workloads may be interrupted, pod evictions may occur frequently, and container applications may experience availability issues; applications may experience workload disruptions or spot node interruption failures.

## Playbook

1. List nodes with label node.kubernetes.io/instance-type=spot and wide output to retrieve all spot nodes in the cluster with their status, capacity, and conditions.
2. List recent events across all namespaces sorted by timestamp and filter for spot, preempt, or interrupt patterns to identify spot node interruptions, preemption warnings, or termination notices.
3. Describe node <spot-node-name> to inspect the spot node details including conditions, allocatable resources, and any termination notices.
4. Retrieve Prometheus metrics for spot nodes including spot_node_interruption_rate and spot_node_termination_count over the last 7 days to identify interruption patterns.
5. Retrieve logs from node monitoring pods and filter for interruption patterns or termination notices within the last 7 days.
6. Retrieve spot node price history for node type `<node-type>` in availability zone `<az>` over the last 7 days to identify price volatility patterns.
7. List spot node requests in cluster and retrieve request status including fulfillment status and capacity availability to identify capacity constraints.
8. Retrieve the node group `<node-group-name>` spot node configuration and inspect its spot node allocation strategy and interruption handling settings, verifying spot node management configuration.
9. Compare spot node interruption timestamps with spot node price change timestamps within 5 minutes and verify whether interruptions correlate with price increases, using spot node price history as supporting evidence.

## Diagnosis

1. Review the spot node interruption metrics from Step 4. If interruption rates are high, identify whether interruptions correlate with specific node types or availability zones based on the node details from Step 3.

2. Analyze the spot price history from Step 6. If prices show high volatility or frequent exceeding of on-demand prices, then price-driven interruptions are occurring. Consider diversifying node types or availability zones.

3. If Step 5 node monitoring logs show termination notices without successful workload migration, then interruption handling automation is failing. If workloads migrate successfully, then the impact is operational noise rather than availability issues.

4. Review the spot node capacity requests from Step 7. If requests are failing due to capacity unavailability, then alternative node types or fallback to on-demand may be needed. If capacity is available but not being used, then allocation strategy needs review.

5. If Step 8 node group configuration shows suboptimal allocation strategies (e.g., single node type, single AZ), then diversification would reduce interruption frequency.

If analysis is inconclusive: Examine events from Step 2 for spot interruption patterns and workload impact. Determine whether interruptions affect specific workloads disproportionately (suggesting workload placement issues) or all workloads equally (suggesting cluster-wide spot configuration issues). Verify that interruption handling automation is correctly configured to gracefully migrate workloads.
