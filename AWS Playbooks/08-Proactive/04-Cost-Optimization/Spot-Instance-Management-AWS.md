# Spot Instance Management

## Meaning

Spot instance management indicates that Spot instance interruptions are frequent, Spot instance capacity is unavailable, or Spot instance usage is not optimized (triggering alarms like SpotInstanceInterrupted or SpotInstanceCapacityUnavailable) because Spot instance interruption rates exceed thresholds, Spot instance capacity requests fail, Spot instance termination notices are frequent, Spot instance price fluctuations cause interruptions, or Spot instance allocation strategies are suboptimal. Spot instance interruption metrics show high rates, Spot instance capacity requests show failures, Spot instance termination notices are frequent, and Spot instance price metrics indicate volatility. This affects the cost management layer and Spot instance lifecycle management, typically caused by Spot instance capacity constraints, Spot instance price volatility, Spot instance interruption handling failures, or Spot instance allocation strategy misconfigurations; if Spot instances host container workloads, container workloads may be interrupted and applications may experience availability issues.

## Impact

SpotInstanceInterrupted alarms fire; SpotInstanceCapacityUnavailable alarms fire; Spot instance interruptions cause workload disruptions; Spot instance capacity is unavailable; Spot instance termination notices are frequent; cost optimization from Spot instances is not achieved. Spot instance interruption metrics show high rates; if Spot instances host container workloads, container workloads may be interrupted, pod evictions may occur frequently, and container applications may experience availability issues; applications may experience workload disruptions or Spot instance interruption failures.

## Playbook

1. List EC2 Spot instances in region `<region>` and retrieve Spot instance status including interruption status and termination notices to identify interrupted or at-risk instances.
2. Retrieve CloudWatch metrics for EC2 Spot instances including SpotInstanceInterruptionRate and SpotInstanceTerminationCount over the last 7 days to identify interruption patterns.
3. Query CloudWatch Logs for log groups containing EC2 Spot instance events and filter for interruption patterns or termination notices within the last 7 days.
4. Retrieve EC2 Spot instance price history for instance type `<instance-type>` in availability zone `<az>` over the last 7 days to identify price volatility patterns.
5. List EC2 Spot instance requests in region `<region>` and retrieve request status including fulfillment status and capacity availability to identify capacity constraints.
6. Retrieve the Auto Scaling Group `<asg-name>` Spot instance configuration and inspect its Spot instance allocation strategy and interruption handling settings, verifying Spot instance management configuration.
7. Compare Spot instance interruption timestamps with Spot instance price change timestamps within 5 minutes and verify whether interruptions correlate with price increases, using Spot instance price history as supporting evidence.
8. Retrieve CloudWatch metrics for EC2 Spot instance capacity including AvailableCapacity and RequestedCapacity over the last 7 days to identify capacity availability patterns.

## Diagnosis

1. **Analyze interruption patterns from Step 2**: If interruptions occur at specific times, correlate with demand patterns (e.g., business hours when overall EC2 demand is higher). If interruptions are random, price volatility is the cause. If interruptions are increasing, consider diversifying instance types.

2. **Evaluate price history from Step 4 and Step 7**: If price spikes correlate with interruptions, set higher max Spot price to reduce interruption risk. If prices are stable but interruptions occur, capacity is being reclaimed regardless of price. If prices are consistently high, Spot may not provide value for that instance type.

3. **Review allocation strategy from Step 6**: If using single instance type, diversify to multiple types for better capacity access. If using single AZ, distribute across AZs. If allocation strategy is not capacity-optimized, switch to reduce interruption risk.

4. **Cross-reference with capacity data from Step 5 and Step 8**: If capacity requests are frequently unfulfilled, that instance type/AZ has limited Spot capacity. If capacity is available but interruptions still occur, the pricing strategy needs adjustment.

5. **Assess interruption handling from Step 3 and Step 6**: If termination notices are not being processed, interruption handling automation is failing. If workloads are not gracefully draining, implement proper Spot termination handling. If replacement capacity is not launching, ASG configuration needs review.

If the above analysis is inconclusive: Consider Spot Fleet with diversified instance pools. Review AWS Spot Instance Advisor for interruption frequency data. Implement checkpointing for stateful workloads. Evaluate whether Spot is appropriate for the workload's availability requirements.
