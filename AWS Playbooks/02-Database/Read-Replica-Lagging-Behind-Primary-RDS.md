# RDS Read Replica Lagging Behind Primary

## Meaning

An RDS read replica experiences replication lag (triggering alarms like ReplicaLag or RDSReadReplicaLag) because replica instance is underpowered, replication settings cause delays, primary instance write load is excessive, network latency between primary and replica is high, replication thread configuration is suboptimal, or read replica instance class is smaller than primary. Read replica data is stale, read queries return outdated results, and replication lag exceeds acceptable thresholds. This affects the database layer and impacts read consistency, typically caused by instance sizing issues, replication configuration problems, or write load increases; if using RDS Aurora, replication lag behavior differs and applications may experience read consistency issues.

## Impact

Read replica data is stale; read queries return outdated results; replication lag increases; ReplicaLag alarms fire; read scaling benefits are reduced; eventual consistency is delayed; read replica cannot keep up with primary writes; application reads from replica may see inconsistent data. RDSReadReplicaLag alarms may fire; if using RDS Aurora, replication lag behavior differs from standard RDS; applications may experience errors or performance degradation due to stale data; read workload distribution may be ineffective.

## Playbook

1. Verify RDS read replica `<replica-instance-id>` and primary instance `<primary-instance-id>` exist and are in "available" state, and AWS service health for RDS in region `<region>` is normal.
2. Retrieve CloudWatch metrics for RDS read replica `<replica-instance-id>` including ReplicaLag over the last 1 hour to identify lag patterns and spikes, analyzing lag trends.
3. Retrieve the RDS Read Replica `<replica-instance-id>` in region `<region>` and inspect its instance class, replication configuration, and replication status, comparing instance class with primary instance.
4. Retrieve CloudWatch metrics for RDS primary instance `<primary-instance-id>` including WriteIOPS and WriteThroughput over the last 1 hour to assess write load, analyzing write load patterns.
5. Query CloudWatch Logs for log groups containing RDS events and filter for replication error events or lag-related patterns for replica `<replica-instance-id>`, including replication error messages.
6. Retrieve CloudWatch alarms associated with RDS read replica `<replica-instance-id>` with metric ReplicaLag and check for alarms in ALARM state, verifying alarm threshold configurations.
7. Retrieve CloudWatch metrics for RDS read replica `<replica-instance-id>` including CPUUtilization and NetworkReceiveThroughput to verify resource utilization, checking if resource constraints affect replication.
8. Retrieve the RDS Read Replica `<replica-instance-id>` and primary instance `<primary-instance-id>` region configuration and verify if cross-region replication latency is contributing to lag, checking region locations.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for RDS replication configuration modification events related to replica `<replica-instance-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 6) to identify when ReplicaLag alarm first entered ALARM state. This timestamp establishes when replication lag exceeded acceptable thresholds.

2. If primary instance WriteIOPS and WriteThroughput metrics (from Playbook step 4) show spikes around the alarm time, high write load on the primary is overwhelming the replica's ability to keep up.

3. If replica instance class (from Playbook step 3) is smaller than primary instance class, the replica may be underpowered. Compare CPUUtilization and NetworkReceiveThroughput (from Playbook step 7) - high values indicate resource constraints on the replica.

4. If lag trend (from Playbook step 2) shows constant elevated lag rather than spikes, the replica is permanently undersized for the workload. If lag spikes correlate with write load spikes, the issue is transient write bursts.

5. If CloudTrail shows replication parameter changes (from Playbook step 9) around the lag increase, those parameter modifications may have affected replication thread performance or binary log processing.

6. If replica and primary are in different regions (from Playbook step 8), check network latency patterns. Cross-region replication inherently has higher latency; significant increases indicate network path issues.

7. If replication event logs (from Playbook step 5) show replication errors or interruptions around the alarm timestamp, replication thread failures or restarts may be causing lag accumulation.

If no correlation is found: extend analysis to 24 hours, review binary log replication progress, check for Aurora-specific replication lag patterns, verify Multi-AZ read replica configuration, and examine cross-region network connectivity.
