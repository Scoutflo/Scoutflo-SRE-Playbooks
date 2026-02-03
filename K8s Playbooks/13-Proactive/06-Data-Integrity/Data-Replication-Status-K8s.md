# Data Replication Status

## Meaning

Data replication status indicates that cross-cluster or cross-namespace data replication is not synchronized or replication operations fail (triggering alerts like ReplicationLagHigh or ReplicationFailed) because replication lag exceeds thresholds, replication jobs fail, replication status shows errors, replication metrics indicate failures, or replication health checks fail. Replication lag metrics exceed thresholds, replication jobs show failed status, replication status indicates errors, and replication health checks indicate unhealthy state. This affects the storage layer and data synchronization infrastructure, typically caused by replication service issues, network connectivity problems, replication job failures, or replication configuration errors; if replication protects container workloads, container data may be out of sync and applications may experience data consistency issues.

## Impact

ReplicationFailed alerts fire; ReplicationLagHigh alerts fire; data consistency cannot be guaranteed; cross-cluster data synchronization fails; replication jobs fail; replication lag exceeds acceptable thresholds. Replication jobs remain in failed or pending state; replication lag metrics show increasing delays; if replication protects container workloads, container data may be out of sync, persistent volume replication may fail, and container applications may experience data consistency issues; applications may experience data inconsistency or replication failures.

## Playbook

1. List persistent volume claims in namespace <namespace> to identify all persistent volume claims and their replication status.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent replication failures or lag issues.

3. Describe PVC <pvc-name> in namespace <namespace> to inspect its replication status, lag metrics, and health status.

4. Retrieve logs from replication pods with label app=replication in namespace <namespace> and filter for error patterns containing 'replication failed', 'replication lag high', or 'replication error'.

5. Retrieve Prometheus metrics for replication service including replication_lag and replication_lag_seconds over the last 1 hour to identify replication lag patterns.

6. Retrieve Prometheus metrics for replication service including replication_latency and replication_success_rate over the last 24 hours to identify replication failure patterns.

7. Describe PVC <source-pvc-name> in namespace <namespace> to verify source PVC health status and availability for replication.

8. List active Prometheus alerts with state 'firing' in source cluster and destination cluster related to replication to identify cluster replication health differences.

## Diagnosis

1. Review the PVC replication status from Step 3. If lag metrics are high, identify whether lag is consistent (suggesting capacity or performance issues) or spiking (suggesting intermittent connectivity problems).

2. Analyze the replication pod logs from Step 4. If logs show replication failure or error patterns, identify the failure cause (network, permissions, storage, or source availability).

3. If Step 5 replication lag metrics show increasing values, then replication is falling behind. If Step 6 shows low success rates, then replication jobs are failing rather than just lagging.

4. Review the source PVC health from Step 7. If source PVC shows issues, then replication lag may be due to source unavailability. If source is healthy, then replication infrastructure is the problem.

5. If Step 8 cluster alerts show differences between source and destination, identify which cluster has issues affecting replication.

If analysis is inconclusive: Examine events from Step 2 for replication failures or lag issues. Determine whether replication issues affect all replicated volumes (suggesting infrastructure problems) or specific volumes (suggesting volume-specific configuration issues). Verify network connectivity between source and destination clusters or namespaces.
