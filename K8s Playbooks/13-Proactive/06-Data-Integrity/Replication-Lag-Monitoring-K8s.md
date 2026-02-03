# Replication Lag Monitoring

## Meaning

Replication lag monitoring indicates that persistent volume replication lag exceeds thresholds or replication synchronization issues are detected (triggering alerts like ReplicationLagHigh or ReplicationSyncFailed) because replication lag metrics exceed thresholds, replication lag monitoring fails, replication synchronization shows delays, replication health checks fail, or replication lag warnings are not generated. Replication lag metrics show high values, replication lag monitoring indicates failures, replication synchronization shows delays, and replication health checks indicate problems. This affects the data integrity layer and replication reliability, typically caused by replication service issues, network connectivity problems, replication lag threshold misconfigurations, or replication monitoring failures; if replication lag affects container workloads, container data replication may be delayed and applications may experience data synchronization issues.

## Impact

ReplicationLagHigh alerts fire; ReplicationSyncFailed alerts fire; data replication lag exceeds thresholds; replication synchronization is delayed; data consistency may be compromised; replication reliability is degraded. Replication lag monitoring shows high lag values; if replication lag affects container workloads, container data replication may be delayed, persistent volume replication may be slow, and container applications may experience data synchronization issues; applications may experience data inconsistency or replication delay failures.

## Playbook

1. Describe PVC <pvc-name> in namespace <namespace> to inspect the PersistentVolumeClaim replication configuration, status, and any replication-related annotations.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to replication lag issues, sync failures, or storage events.
3. Retrieve Prometheus metrics for persistent volume replication including replication_lag and replication_lag_seconds over the last 24 hours to identify replication lag patterns and threshold breaches.
4. Retrieve logs from replication controller pods and filter for replication lag warnings or replication sync failure patterns within the last 24 hours.
5. Describe PVC <source-pvc-name> in namespace <namespace> to verify source PVC health status, checking source PVC availability for replication.
6. Compare replication lag increase timestamps with network connectivity issue timestamps within 30 minutes and verify whether network issues cause replication lag increases, using network policy logs as supporting evidence.
7. Retrieve Prometheus metrics for persistent volume replication including replication_throughput and replication_latency over the last 24 hours to identify replication performance issues.
8. Compare replication lag threshold breach timestamps with replication lag monitoring alert timestamps within 5 minutes and verify whether alerts fire when thresholds are breached, using Prometheus metrics as supporting evidence.

## Diagnosis

1. Review the replication lag metrics from Step 3. If lag exceeds configured thresholds, identify whether lag is consistent (suggesting capacity issues) or spiking (suggesting intermittent issues like network problems).

2. Analyze the replication controller logs from Step 4. If logs show sync failure patterns, identify the failure cause (network, permissions, storage capacity). If logs show warnings without failures, then lag is occurring without complete sync failure.

3. If Step 5 source PVC health shows issues, then replication lag may be caused by source unavailability rather than replication infrastructure problems. Focus on restoring source health.

4. Review the replication performance metrics from Step 7. If throughput is low or latency is high, then replication infrastructure may be under-resourced or experiencing network issues.

5. If Step 8 shows alerts not firing when thresholds are breached, then alerting configuration needs adjustment. If alerts are firing correctly, then monitoring is functioning and focus should be on remediation.

If analysis is inconclusive: Examine events from Step 2 for replication-related issues or storage events. Review the network connectivity from Step 6 to verify cross-cluster or cross-namespace network health. Determine whether lag affects all replicated resources (suggesting infrastructure issues) or specific resources (suggesting resource-specific problems).
