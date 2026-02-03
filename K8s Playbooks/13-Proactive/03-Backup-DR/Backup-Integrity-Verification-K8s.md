# Backup Integrity Verification

## Meaning

Backup integrity verification indicates that etcd backup data integrity cannot be verified or backup corruption is detected (triggering alerts like BackupIntegrityFailed or BackupCorruptionDetected) because backup integrity checks fail, backup corruption is detected, backup checksum validation fails, backup restoration tests fail, or backup integrity monitoring indicates violations. Backup integrity checks show failures, backup corruption is detected, backup checksum validation fails, and backup integrity monitoring indicates problems. This affects the data integrity layer and backup reliability, typically caused by backup corruption, backup service issues, checksum validation failures, or backup integrity monitoring failures; if backup integrity affects container workloads, container backup data may be corrupted and applications may experience backup restoration failures.

## Impact

BackupIntegrityFailed alerts fire; BackupCorruptionDetected alerts fire; backup integrity cannot be verified; backup corruption is detected; backup restoration may fail; disaster recovery procedures may be compromised. Backup integrity verification shows failures; if backup integrity affects container workloads, container backup data may be corrupted, persistent volume backups may be invalid, and container applications may experience backup restoration failures; applications may experience data loss or backup restoration failures.

## Playbook

1. List jobs in namespace <namespace> with label app=backup to identify all backup jobs and their current status.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent backup integrity issues or failures.

3. Describe job <backup-job-name> in namespace <namespace> to inspect job completion status, error messages, and integrity check results.

4. Retrieve logs from backup pods with label app=backup in namespace <namespace> and filter for backup integrity errors or corruption detection patterns.

5. Retrieve Prometheus metrics for backup service including backup_job_success_rate and backup_integrity_check_results over the last 30 days to identify backup integrity issues.

6. List volume snapshots in namespace <namespace> to verify snapshot data integrity status and completion.

7. Compare backup integrity check failure timestamps with backup job completion timestamps within 1 hour and verify whether integrity failures occur after backup completion, using backup integrity check results as supporting evidence.

8. List etcd backup integrity check results and verify backup data integrity status, checking etcd backup integrity.

## Diagnosis

1. Review the backup job status from Steps 1 and 3. If jobs show failed status or integrity check failures, examine error messages to identify the corruption cause (storage issues, network transmission errors, or service failures).

2. Analyze the backup pod logs from Step 4. If logs show integrity errors or corruption detection patterns, identify whether corruption occurred during backup creation or afterward during storage.

3. If Step 5 backup metrics show integrity check failures, assess whether failures are increasing (suggesting ongoing corruption issues) or stable (suggesting past event).

4. Review the volume snapshot status from Step 6. If snapshots show integrity issues, then snapshot data is corrupted and recovery requires alternative backup sources.

5. If Step 7 integrity check comparison shows failures occurring after backup completion, then storage or post-backup processes are causing corruption. If failures occur during backup, then backup creation is the issue.

If analysis is inconclusive: Examine events from Step 2 for backup-related failures. Review the etcd backup integrity from Step 8 to verify cluster state backup integrity. Determine whether corruption affects all backups (suggesting systemic issues) or specific backups (suggesting targeted corruption or job-specific problems).
