# Data Consistency Checks

## Meaning

Data consistency checks indicate that data consistency cannot be verified or data integrity issues are detected (triggering alerts like DataConsistencyFailed or DataIntegrityViolation) because data consistency verification fails, data integrity checks detect corruption, data replication shows inconsistencies, data checksum validation fails, or data consistency monitoring indicates violations. Data consistency checks show failures, data integrity violations are detected, data replication inconsistencies are identified, and data consistency monitoring indicates problems. This affects the data integrity layer and persistent volume reliability, typically caused by data corruption, replication lag issues, checksum validation failures, or data consistency monitoring issues; if data consistency affects container workloads, container persistent volume data may be inconsistent and applications may experience data integrity issues.

## Impact

DataConsistencyFailed alerts fire; DataIntegrityViolation alerts fire; data consistency cannot be verified; data integrity issues are detected; data corruption may occur; persistent volume reliability is compromised. Data consistency checks show failures; if data consistency affects container workloads, container persistent volume data may be inconsistent, pod data may be corrupted, and container applications may experience data integrity issues; applications may experience data corruption or data consistency failures.

## Playbook

1. List persistent volume claims in namespace <namespace> to identify all persistent volume claims and their current status.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent data consistency issues or storage errors.

3. Describe PVC <pvc-name> in namespace <namespace> to inspect persistent volume consistency check status and last consistency check timestamp.

4. Describe statefulset <statefulset-name> in namespace <namespace> to verify stateful set data consistency and replication status.

5. Retrieve logs from persistent volume controller pods with label app=csi-controller in namespace kube-system and filter for data consistency errors.

6. Retrieve Prometheus metrics for persistent volumes including replication_lag and data_consistency_status over the last 24 hours to identify data consistency issues.

7. Retrieve persistent volume integrity check results for volume `<volume-name>` and verify volume data integrity status, checking persistent volume data consistency.

8. List all PVCs in namespace <namespace> with wide output and verify volume data integrity status, checking PVC data consistency.

## Diagnosis

1. Review the PVC status from Steps 1 and 3. If consistency check status shows failures, identify the affected volumes and examine consistency check timestamps to determine when inconsistencies were introduced.

2. Analyze the statefulset data consistency from Step 4. If replication status shows errors, then data may be inconsistent across replicas. If replication is healthy, then single-replica data corruption may be the issue.

3. If Step 5 CSI controller logs show data consistency errors, identify whether errors are storage-level (suggesting storage infrastructure issues) or application-level (suggesting application data corruption).

4. Review the replication metrics from Step 6. If replication_lag is high, then consistency violations may be due to lag rather than corruption. If lag is low, then actual data corruption exists.

5. If Step 7 volume integrity check results show failures, then persistent volume data is corrupted and recovery from backup may be needed.

If analysis is inconclusive: Examine events from Step 2 for storage errors or data-related issues. Review the PVC data consistency from Step 8 to verify volume-level integrity. Determine whether consistency issues affect all replicas (suggesting application-level corruption) or specific replicas (suggesting storage-level issues on those replicas).
