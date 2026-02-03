# Restore Testing

## Meaning

Restore testing indicates that backup restore procedures cannot be validated or restore operations fail during testing (triggering alerts like RestoreJobFailed or RestoreTestFailed) because restore jobs fail, restore time exceeds RTO targets, restored data integrity cannot be verified, restore operations timeout, or restore job metadata indicates incomplete restores. Restore jobs show failed status in cluster restore tools, restore operations remain in running state indefinitely, restore completion timestamps are missing, and restored data verification checks fail. This affects the storage layer and disaster recovery procedures, typically caused by restore service issues, data corruption, restore timeout problems, or restore job failures; if restores protect container workloads, container data recovery may fail and applications may experience data loss.

## Impact

RestoreTestFailed alerts fire; RestoreJobFailed alerts fire; disaster recovery procedures cannot be validated; RTO targets cannot be met; restore jobs fail; restored data integrity cannot be confirmed; restore operations timeout; restore completion cannot be verified. Restore jobs remain in running or failed state; restore metadata shows incomplete or corrupted restores; if restores protect container workloads, container data recovery may fail, persistent volume data may be corrupted, and container applications may experience data loss; applications may experience data loss or recovery failures.

## Playbook

1. List jobs in namespace <namespace> with label app=restore to identify restore jobs and their current status for restore testing validation.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to restore operations, failures, or data integrity issues.
3. Describe job <restore-job-name> in namespace <namespace> to inspect restore job details including status, completion timestamp, and error messages.
4. Retrieve logs from pod `<restore-pod-name>` in namespace `<namespace>` and filter for error patterns containing 'restore failed', 'restore timeout', or 'data integrity failed' within the last 24 hours.
5. Retrieve Prometheus metrics for restore service including restore_job_success_rate and restore_job_duration over the last 24 hours to identify restore job failure patterns.
6. Retrieve recovery point `<recovery-point-name>` details and inspect its creation timestamp, backup completion status, and data integrity checksums, verifying recovery point validity.
7. Compare restore job completion timestamps with RTO targets and verify whether restore operations complete within expected time windows, using restore job metadata as supporting evidence.
8. Retrieve restored resource `<resource-name>` configuration after restore completion and verify resource state matches expected restore state, checking restored resource integrity.

## Diagnosis

1. Review the restore job status from Steps 1 and 3. If jobs show failed status, examine error messages to identify the failure cause (recovery point issues, storage constraints, permissions, or timeouts).

2. Analyze the restore pod logs from Step 4. If logs show timeout patterns, then restore operations are taking too long. If logs show data integrity failures, then recovery points may be corrupted.

3. If Step 5 restore metrics show low success rates, then systematic restore issues exist. If success rates are high but specific restore tests fail, then those tests have configuration issues.

4. Review the recovery point details from Step 6. If recovery points show creation issues or invalid checksums, then source backups are the problem rather than restore procedures.

5. If Step 7 shows restore completions exceeding RTO targets, then restore performance optimization is needed even if restores eventually succeed. If completions are within RTO, then restore procedures meet targets.

If analysis is inconclusive: Examine events from Step 2 for restore-related failures. Review the restored resource integrity from Step 8 to verify restores produce valid resources. Determine whether failures affect all restore tests (suggesting infrastructure issues) or specific recovery points (suggesting point-specific corruption).
