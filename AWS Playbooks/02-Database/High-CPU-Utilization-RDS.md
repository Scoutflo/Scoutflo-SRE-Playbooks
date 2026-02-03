# RDS High CPU Utilization

## Meaning

An RDS instance experiences sustained high CPU utilization (triggering alarms like CPUUtilizationHigh or RDSHighCPU) because database queries are inefficient, connection pool exhaustion causes CPU contention, instance type is undersized for workload, background maintenance tasks consume CPU, database parameter group settings are suboptimal, or read replica lag processing increases CPU usage. Database performance degrades, query response times increase, and CPU utilization consistently exceeds thresholds. This affects the database layer and impacts application performance, typically caused by query optimization issues, instance sizing problems, or workload increases; if using RDS Aurora, storage model differences may affect CPU behavior and applications may experience database performance degradation.

## Impact

CPUUtilizationHigh alarms fire; database performance degrades; query response times increase; application connections timeout; database becomes unresponsive; read and write operations slow down; connection pool exhaustion occurs; database replication lag increases; application performance is severely impacted. RDSHighCPU alarms may fire; if using RDS Aurora, CPU utilization patterns may differ due to shared storage model; applications may experience errors or performance degradation due to database slowdown; user-facing services experience increased latency.

## Playbook

1. Verify RDS instance `<db-instance-id>` exists and is in "available" state, and AWS service health for RDS in region `<region>` is normal.
2. Retrieve CloudWatch metrics for RDS instance `<db-instance-id>` including CPUUtilization over the last 1 hour to identify CPU usage patterns and spikes, analyzing CPU trend over time.
3. Retrieve the RDS Instance `<db-instance-id>` in region `<region>` and inspect its instance class, parameter group configuration, and performance insights status, verifying instance type is appropriate for workload.
4. Query CloudWatch Logs for log groups containing RDS performance insights or slow query logs for instance `<db-instance-id>` and filter for high CPU query patterns, including query execution time indicators.
5. Retrieve CloudWatch alarms associated with RDS instance `<db-instance-id>` with metric CPUUtilization and check for alarms in ALARM state, verifying alarm threshold configurations.
6. Retrieve CloudWatch metrics for RDS instance `<db-instance-id>` including DatabaseConnections and verify connection count patterns, checking if connection pool exhaustion contributes to CPU contention.
7. List RDS instances in region `<region>` with the same instance class as `<db-instance-id>` and compare CPU utilization patterns to determine if the issue is instance-specific, analyzing CPU utilization across similar instances.
8. Retrieve the RDS Instance `<db-instance-id>` parameter group settings and verify parameter group configuration, checking for parameter settings affecting query performance.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for RDS parameter group modification events related to instance `<db-instance-id>` within the last 24 hours, checking for parameter changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when CPUUtilizationHigh or RDSHighCPU alarm first entered ALARM state. This timestamp serves as the correlation baseline for all subsequent analysis.

2. If Performance Insights or slow query logs (from Playbook step 4) show specific queries consuming high CPU around the alarm time, those inefficient queries are the likely root cause. Focus on queries with high CPU time or full table scans.

3. If no specific queries are identified, check connection count patterns (from Playbook step 6). If DatabaseConnections spiked around the alarm time, connection pool exhaustion or connection storms are causing CPU contention.

4. If connection counts are normal, compare CPU spike with parameter group changes in CloudTrail (from Playbook step 9). Recent parameter modifications may have affected query optimizer behavior or buffer pool sizing.

5. If no parameter changes occurred, analyze CPU trend over 24 hours (from Playbook step 2). Gradual increase indicates workload growth requiring larger instance class; sudden spike indicates query pattern change or batch job execution.

6. If instance class comparison (from Playbook step 7) shows similar instances with lower CPU, the issue is likely workload-specific rather than instance sizing. Examine Performance Insights (from Playbook step 3) for wait events.

7. If using Aurora (from Playbook step 3), shared storage model may show different CPU patterns during heavy read operations compared to standard RDS.

If no correlation is found: extend analysis to 4 hours, review Performance Insights for wait events and top queries, check for index fragmentation or table bloat, verify Multi-AZ replication overhead during failover events, and examine query execution plans for optimization opportunities.
