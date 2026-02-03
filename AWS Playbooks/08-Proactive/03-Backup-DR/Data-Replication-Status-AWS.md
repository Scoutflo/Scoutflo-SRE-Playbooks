# Data Replication Status

## Meaning

Data replication status indicates that cross-region or cross-account data replication is not synchronized or replication operations fail (triggering alarms like ReplicationLagHigh or ReplicationFailed) because replication lag exceeds thresholds, replication jobs fail, replication status shows errors, replication metrics indicate failures, or replication health checks fail. Replication lag metrics exceed thresholds, replication jobs show failed status, replication status indicates errors, and replication health checks indicate unhealthy state. This affects the storage layer and data synchronization infrastructure, typically caused by replication service issues, network connectivity problems, replication job failures, or replication configuration errors; if replication protects container workloads, container data may be out of sync and applications may experience data consistency issues.

## Impact

ReplicationFailed alarms fire; ReplicationLagHigh alarms fire; data consistency cannot be guaranteed; cross-region data synchronization fails; replication jobs fail; replication lag exceeds acceptable thresholds. Replication jobs remain in failed or pending state; replication lag metrics show increasing delays; if replication protects container workloads, container data may be out of sync, persistent volume replication may fail, and container applications may experience data consistency issues; applications may experience data inconsistency or replication failures.

## Playbook

1. Retrieve the RDS DB Instance `<db-instance-id>` read replica configuration in region `<region>` and inspect its replication status, lag metrics, and health status, verifying read replica accessibility.
2. List S3 bucket replication configurations for bucket `<bucket-name>` in region `<region>` and verify replication rule status and replication job completion status, checking S3 replication status.
3. Retrieve CloudWatch metrics for RDS read replica including ReplicaLag and ReplicationLag over the last 1 hour to identify replication lag patterns.
4. Query CloudWatch Logs for log groups containing RDS replication events and filter for error patterns containing 'replication failed', 'replication lag high', or 'replication error' within the last 1 hour.
5. Retrieve CloudWatch metrics for S3 replication including ReplicationLatency and ReplicationSuccessRate over the last 24 hours to identify S3 replication failure patterns.
6. Compare replication lag timestamps with replication job completion timestamps and verify whether replication lag increases after replication job failures, using replication status data as supporting evidence.
7. Retrieve the RDS DB Instance `<db-instance-id>` primary instance configuration and verify primary instance health status, checking primary instance availability for replication.
8. List active alarms in region `<source-region>` and region `<destination-region>` with state 'ALARM' related to replication to identify regional replication health differences.

## Diagnosis

1. **Analyze RDS replica status from Step 1**: If ReplicaLag metric from Step 3 exceeds thresholds, examine primary instance health from Step 7. If primary instance shows high CPU or connection counts, the primary is overloaded and causing replication delays. If primary is healthy, proceed to network analysis.

2. **Evaluate S3 replication metrics from Step 5**: If ReplicationLatency is elevated or ReplicationSuccessRate is below 99.9%, check S3 bucket replication rule configuration from Step 2. If rules show correct status but replication fails, verify destination bucket permissions and existence.

3. **Cross-reference with error logs from Step 4**: If logs show "replication failed" errors, identify the specific error type. If errors indicate I/O limits, the source or destination storage is throttled. If errors indicate authentication failures, IAM role trust policies need review.

4. **Compare regional alarm states from Step 8**: If source region shows healthy alarms but destination region shows ALARM state, the issue is destination-specific. If both regions show ALARM states, a broader infrastructure issue exists.

5. **Assess replication lag trend from Step 3**: If ReplicaLag is increasing over time, the replication is falling behind due to write load exceeding replication throughput. If lag is stable but high, a configuration adjustment is needed. If lag fluctuates, network latency variations are the cause.

If the above analysis is inconclusive: Review VPC Flow Logs for cross-region connectivity issues. Check for recent configuration changes to replication settings. Verify IAM role permissions for cross-account replication. Examine storage quotas and limits. Consider whether data volume has increased beyond replication capacity.
