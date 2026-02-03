# Restore Testing

## Meaning

Restore testing indicates that backup restore procedures cannot be validated or restore operations fail during testing (triggering alarms like RestoreJobFailed or RestoreTestFailed) because restore jobs fail, restore time exceeds RTO targets, restored data integrity cannot be verified, restore operations timeout, or restore job metadata indicates incomplete restores. Restore jobs show failed status in AWS Backup console, restore operations remain in running state indefinitely, restore completion timestamps are missing, and restored data verification checks fail. This affects the storage layer and disaster recovery procedures, typically caused by restore service issues, data corruption, restore timeout problems, or restore job failures; if restores protect container workloads, container data recovery may fail and applications may experience data loss.

## Impact

RestoreTestFailed alarms fire; disaster recovery procedures cannot be validated; RTO targets cannot be met; restore jobs fail; restored data integrity cannot be confirmed; restore operations timeout; restore completion cannot be verified. Restore jobs remain in running or failed state; restore metadata shows incomplete or corrupted restores; if restores protect container workloads, container data recovery may fail, persistent volume data may be corrupted, and container applications may experience data loss; applications may experience data loss or recovery failures.

## Playbook

1. Retrieve the Backup Vault `<vault-name>` in region `<region>` and inspect its recovery point availability and restore capabilities, verifying vault accessibility for restore operations.
2. List restore jobs in Backup Vault `<vault-name>` in region `<region>` and filter for jobs with status 'FAILED' or 'ABORTED' within the last 24 hours, checking restore job completion status.
3. Retrieve restore job `<restore-job-id>` details and inspect its status, completion timestamp, error messages, and restored resource configuration, checking restore job execution results.
4. Query CloudWatch Logs for log groups containing AWS Backup restore events and filter for error patterns containing 'restore failed', 'restore timeout', or 'data integrity failed' within the last 24 hours.
5. Retrieve CloudWatch metrics for AWS Backup service including RestoreJobSuccessRate and RestoreJobDuration over the last 24 hours to identify restore job failure patterns.
6. Retrieve the recovery point `<recovery-point-arn>` details and inspect its creation timestamp, backup completion status, and data integrity checksums, verifying recovery point validity.
7. Compare restore job completion timestamps with RTO targets and verify whether restore operations complete within expected time windows, using restore job metadata as supporting evidence.
8. Retrieve the restored resource `<resource-arn>` configuration after restore completion and verify resource state matches expected restore state, checking restored resource integrity.

## Diagnosis

1. **Analyze restore job status from Step 2**: If failed/aborted restore jobs are found, examine error messages from Step 3. If errors indicate "recovery point not found" or "corrupted", the source backup is the issue - verify recovery point validity from Step 6. If errors indicate "insufficient permissions", IAM role attached to restore job needs review.

2. **Evaluate recovery point health from Step 6**: If recovery point shows incomplete backup status or missing checksums, the backup itself is corrupted and cannot be restored. If recovery point is valid but restore fails, the issue is with restore configuration or target resources.

3. **Review CloudWatch metrics from Step 5**: If RestoreJobSuccessRate is below target, identify whether failures are consistent (configuration issue) or intermittent (resource availability issue). If RestoreJobDuration exceeds RTO targets from Step 7, storage performance or data volume is the bottleneck.

4. **Cross-reference with error logs from Step 4**: If logs show "timeout" errors, increase restore job timeout settings. If logs show "resource conflict" errors, the target resource already exists or is in use. If logs show "storage limit" errors, target storage capacity is insufficient.

5. **Verify restored resource state from Step 8**: If restore completes but resource state does not match expected configuration, data integrity verification failed. If resource configuration matches but application cannot use the data, application-level validation is needed.

If the above analysis is inconclusive: Attempt restore to a different target resource to isolate the issue. Verify KMS key accessibility for encrypted backups. Check IAM role trust relationships and policies. Review AWS Backup service quotas for concurrent restore jobs. Test with a smaller or different recovery point to confirm backup validity.
