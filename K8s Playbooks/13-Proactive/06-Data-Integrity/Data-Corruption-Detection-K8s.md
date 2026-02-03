# Data Corruption Detection

## Meaning

Data corruption detection indicates that data corruption is detected or data integrity violations are identified (triggering alerts like DataCorruptionDetected or DataIntegrityViolation) because data corruption checks detect corruption, data integrity violations are identified, data checksum validation fails, data corruption monitoring indicates problems, or data restoration tests reveal corruption. Data corruption checks show failures, data integrity violations are detected, data checksum validation fails, and data corruption monitoring indicates problems. This affects the data integrity layer and data reliability, typically caused by storage corruption, data transmission errors, checksum validation failures, or data corruption monitoring issues; if data corruption affects container workloads, container persistent volume data may be corrupted and applications may experience data integrity failures.

## Impact

DataCorruptionDetected alerts fire; DataIntegrityViolation alerts fire; data corruption is detected; data integrity violations are identified; data reliability is compromised; applications may experience data errors. Data corruption detection shows failures; if data corruption affects container workloads, container persistent volume data may be corrupted, pod data may be invalid, and container applications may experience data integrity failures; applications may experience data errors or data corruption failures.

## Playbook

1. List persistent volume claims in namespace <namespace> to identify all persistent volume claims and their current status for corruption analysis.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent data corruption errors or storage failures.

3. Describe PVC <pvc-name> in namespace <namespace> to inspect persistent volume corruption check status and last corruption check timestamp.

4. Retrieve logs from persistent volume controller pods with label app=csi-controller in namespace kube-system and filter for data corruption errors or integrity violation patterns.

5. Retrieve Prometheus metrics for persistent volumes including data_errors and data_corruption_errors over the last 24 hours to identify data corruption patterns.

6. List volume snapshots in namespace <namespace> and verify snapshot checksums and corruption detection results.

7. Describe statefulset <statefulset-name> in namespace <namespace> and verify data consistency and corruption detection status.

8. List persistent volume claim integrity check results and verify persistent volume data corruption status, checking PVC data integrity.

## Diagnosis

1. Review the PVC corruption status from Step 3. If corruption check status shows failures, assess the extent of corruption and determine whether data recovery from backup is needed.

2. Analyze the CSI controller logs from Step 4. If logs show corruption errors or integrity violation patterns, identify whether corruption is storage-level (suggesting disk or storage system issues) or application-level (suggesting application bugs).

3. If Step 5 persistent volume metrics show data_corruption_errors, identify the affected volumes and timestamps. If errors are increasing, then corruption is ongoing; if stable, then corruption may be from a past event.

4. Review the volume snapshot checksums from Step 6. If snapshots show corruption, then corruption existed at snapshot time and recovery requires older snapshots. If snapshots are clean, use them for recovery.

5. If Step 8 PVC integrity check results show failures, prioritize recovery for affected volumes based on data criticality.

If analysis is inconclusive: Examine events from Step 2 for storage failures or data-related errors. Review the statefulset data status from Step 7 to verify replication health. Determine whether corruption affects specific volumes (suggesting localized storage issues) or multiple volumes (suggesting systemic storage infrastructure problems).
