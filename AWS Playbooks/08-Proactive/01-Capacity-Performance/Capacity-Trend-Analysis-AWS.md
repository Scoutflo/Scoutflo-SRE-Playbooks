# Capacity Trend Analysis

## Meaning

Capacity trend analysis indicates that capacity utilization trends cannot be analyzed or capacity growth patterns are not identified (triggering alarms like CapacityTrendUnavailable or CapacityAnalysisFailed) because capacity trend data is unavailable, capacity growth patterns are not detected, capacity utilization trends show anomalies, capacity analysis tools fail, or capacity trend metrics are inaccurate. Capacity trend metrics show unavailable data, capacity growth patterns cannot be identified, capacity utilization trends show anomalies, and capacity analysis fails. This affects the capacity planning layer and resource optimization, typically caused by capacity monitoring failures, trend analysis tool unavailability, capacity data collection issues, or capacity pattern detection failures; if capacity trends affect container workloads, container capacity needs may not be identified and applications may experience capacity planning failures.

## Impact

CapacityTrendUnavailable alarms fire; CapacityAnalysisFailed alarms fire; capacity trends cannot be analyzed; capacity growth patterns are not identified; capacity planning decisions cannot be made; capacity constraints may occur unexpectedly. Capacity trend analysis is unavailable; if capacity trends affect container workloads, container capacity needs may not be identified, pod scaling trends may be unknown, and container applications may experience capacity planning failures; applications may experience capacity shortages or unexpected capacity constraints.

## Playbook

1. Retrieve CloudWatch metrics for EC2 instance capacity utilization including CPUUtilization and MemoryUtilization over the last 180 days to analyze capacity trends and identify growth patterns.
2. Retrieve CloudWatch metrics for RDS DB instance capacity utilization including CPUUtilization and StorageUtilization over the last 180 days to analyze database capacity trends.
3. Retrieve Cost Explorer data for resource capacity by service in region `<region>` over the last 180 days and analyze capacity trends to identify growth patterns.
4. Query CloudWatch Logs for log groups containing capacity monitoring events and filter for patterns indicating capacity growth or capacity constraints within the last 180 days.
5. Retrieve CloudWatch metrics for Auto Scaling Group capacity including DesiredCapacity and ActualCapacity over the last 180 days to analyze scaling capacity trends.
6. Compare capacity utilization trend data with capacity growth pattern detection results and verify whether growth patterns are accurately identified, using CloudWatch metrics as supporting evidence.
7. Retrieve CloudWatch metrics for service quota capacity including quota usage trends over the last 180 days to identify capacity quota trends.
8. Analyze capacity utilization distribution patterns over the last 180 days to identify seasonal capacity trends or capacity spikes that affect planning.

## Diagnosis

1. **Analyze long-term utilization trends from Step 1 and Step 2**: If CPU/Memory utilization shows consistent upward trend, plan for capacity expansion. If trends are flat, current capacity is adequate. If trends show decline, consider right-sizing or decommissioning.

2. **Evaluate Cost Explorer capacity data from Step 3**: If cost growth rate exceeds business growth rate, capacity may be over-provisioned. If costs are flat but utilization is increasing, efficiency is improving. If seasonal patterns exist, align capacity with business cycles.

3. **Review Auto Scaling behavior from Step 5**: If DesiredCapacity frequently equals max capacity, scaling limits may constrain capacity. If DesiredCapacity is consistently low, over-provisioning exists. If scaling events are frequent, consider larger base capacity.

4. **Cross-reference with quota utilization from Step 7**: If quota utilization is approaching limits, request quota increases proactively. If quota utilization is low, current quotas are adequate. If quota growth rate is accelerating, plan for future increases.

5. **Identify seasonal patterns from Step 8**: If capacity spikes occur at predictable times, schedule capacity changes proactively. If spikes are unpredictable, implement auto-scaling. If no patterns exist, trends are driven by organic growth.

If the above analysis is inconclusive: Correlate capacity trends with business metrics (users, transactions). Review historical capacity incidents to identify leading indicators. Consider machine learning-based forecasting for complex patterns. Engage application teams for future demand projections.
