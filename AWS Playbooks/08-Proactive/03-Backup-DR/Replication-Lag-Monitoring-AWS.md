# Replication Lag Monitoring

## Meaning

Replication lag monitoring indicates that data replication lag exceeds thresholds or replication synchronization issues are detected (triggering alarms like ReplicationLagHigh or ReplicationSyncFailed) because replication lag metrics exceed thresholds, replication lag monitoring fails, replication synchronization shows delays, replication health checks fail, or replication lag warnings are not generated. Replication lag metrics show high values, replication lag monitoring indicates failures, replication synchronization shows delays, and replication health checks indicate problems. This affects the data integrity layer and replication reliability, typically caused by replication service issues, network connectivity problems, replication lag threshold misconfigurations, or replication monitoring failures; if replication lag affects container workloads, container data replication may be delayed and applications may experience data synchronization issues.

## Impact

ReplicationLagHigh alarms fire; ReplicationSyncFailed alarms fire; data replication lag exceeds thresholds; replication synchronization is delayed; data consistency may be compromised; replication reliability is degraded. Replication lag monitoring shows high lag values; if replication lag affects container workloads, container data replication may be delayed, persistent volume replication may be slow, and container applications may experience data synchronization issues; applications may experience data inconsistency or replication delay failures.

## Playbook

1. Retrieve the RDS DB Instance `<db-instance-id>` read replica configuration and inspect replication lag metrics including ReplicaLag and ReplicationLag, verifying replication lag status.
2. Retrieve CloudWatch metrics for RDS read replica including ReplicaLag and ReplicationLag over the last 24 hours to identify replication lag patterns and threshold breaches.
3. Query CloudWatch Logs for log groups containing RDS replication events and filter for replication lag warnings or replication sync failure patterns within the last 24 hours.
4. Retrieve the RDS DB Instance `<db-instance-id>` primary instance configuration and verify primary instance health status, checking primary instance availability for replication.
5. Compare replication lag increase timestamps with network connectivity issue timestamps within 30 minutes and verify whether network issues cause replication lag increases, using CloudWatch Logs containing VPC Flow Logs as supporting evidence.
6. Retrieve CloudWatch metrics for RDS replication including ReplicationThroughput and ReplicationLatency over the last 24 hours to identify replication performance issues.
7. Compare replication lag threshold breach timestamps with replication lag monitoring alert timestamps within 5 minutes and verify whether alerts fire when thresholds are breached, using CloudWatch metrics as supporting evidence.
8. Retrieve the RDS DB Instance `<db-instance-id>` replication configuration and verify replication settings including replication instance class and replication parameter configuration, checking replication configuration.

## Diagnosis

1. **Analyze ReplicaLag metrics from Step 2**: If lag shows steady increase, replication throughput cannot keep pace with write load on primary. If lag shows spikes followed by recovery, intermittent issues are occurring. If lag is consistently high but stable, a configuration change may help.

2. **Evaluate primary instance health from Step 4**: If primary instance shows high CPU or IOPS utilization, it may be overloaded and slowing replication. If primary is healthy but lag is high, the replica or network is the bottleneck.

3. **Review replication throughput from Step 6**: If ReplicationThroughput is below expected levels, network bandwidth or replica I/O capacity is limiting. If ReplicationLatency is high, network latency between primary and replica is the cause.

4. **Cross-reference with network data from Step 5**: If VPC Flow Logs show packet loss or retransmissions between primary and replica, network quality is degraded. If network appears healthy, the issue is with database configuration.

5. **Assess replica configuration from Step 8**: If replica instance class is smaller than primary, upgrade the replica. If replication parameters are not optimized (e.g., parallel replication threads), tune the configuration.

If the above analysis is inconclusive: Check for long-running transactions on primary that delay replication. Review replica storage performance (IOPS, throughput). Consider replica in same AZ as primary to minimize latency. Evaluate whether read replica is overloaded with read traffic.
