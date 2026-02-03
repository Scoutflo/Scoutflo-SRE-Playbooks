# Backup Verification

## Meaning

Backup verification indicates that automated or manual backups may not be completing successfully or backup integrity cannot be confirmed (triggering alarms like BackupJobFailed or BackupVerificationFailed) because backup jobs fail, backup retention policies are not met, backup encryption verification fails, backup completion status cannot be verified, or backup metadata indicates incomplete backups. Backups show failed status in AWS Backup console, backup jobs remain in running state indefinitely, backup completion timestamps are missing or outdated, and backup verification checks fail. This affects the storage layer and backup infrastructure, typically caused by backup service issues, retention policy violations, encryption key problems, or backup job failures; if backups protect container workloads, container data recovery may be impossible and applications may experience data loss risks.

## Impact

BackupVerificationFailed alarms fire; data recovery may be impossible; RTO and RPO targets cannot be met; backup jobs fail; backup retention policies are violated; backup encryption verification fails; backup completion cannot be confirmed; disaster recovery procedures cannot be executed. Backup jobs remain in running or failed state; backup metadata shows incomplete or corrupted backups; if backups protect container workloads, container data recovery may fail, persistent volume data may be lost, and container applications may experience data loss risks; applications may experience data loss or recovery failures.

## Playbook

1. Retrieve the Backup Vault `<vault-name>` in region `<region>` and inspect its configuration, backup retention policies, and encryption settings, verifying vault accessibility.
2. List backup jobs in Backup Vault `<vault-name>` in region `<region>` and filter for jobs with status 'FAILED' or 'ABORTED' within the last 24 hours, checking backup job completion status.
3. Retrieve the Backup Plan `<plan-name>` in region `<region>` and inspect its backup rules, schedule configuration, and retention policies, verifying backup plan configuration.
4. Retrieve backup job `<backup-job-id>` details and inspect its status, completion timestamp, and error messages, checking backup job execution results.
5. Query CloudWatch Logs for log groups containing AWS Backup events and filter for error patterns containing 'backup failed', 'verification failed', or 'retention policy violation' within the last 24 hours.
6. Retrieve CloudWatch metrics for AWS Backup service including BackupJobSuccessRate and BackupJobDuration over the last 24 hours to identify backup job failure patterns.
7. List recovery points in Backup Vault `<vault-name>` for resource `<resource-arn>` and verify recovery point creation timestamps match backup schedule, checking recovery point availability.
8. Retrieve the Backup Vault `<vault-name>` encryption configuration and verify encryption key accessibility, checking KMS key permissions for backup encryption.
9. Compare backup job completion timestamps with backup schedule timestamps and verify whether backup jobs complete within expected time windows, using backup job metadata as supporting evidence.

## Diagnosis

1. **Analyze backup job status from Step 2**: If failed/aborted backup jobs are found, examine error messages from Step 4. If errors indicate "access denied", verify KMS key permissions from Step 8. If errors indicate "resource not found", the backup target resource was deleted or modified. If errors indicate "snapshot limit exceeded", resource snapshot quotas need increase.

2. **Evaluate recovery point creation from Step 7**: If recovery points are missing for scheduled backup times, backup jobs are not running. If recovery points exist but are older than expected, backup schedule from Step 3 may be misconfigured or jobs are failing silently.

3. **Review CloudWatch metrics from Step 6**: If BackupJobSuccessRate is below 99%, identify the pattern. If failures occur at specific times, resource contention during backup windows is likely. If failures are random, KMS key or network issues are probable.

4. **Cross-reference with encryption status from Step 8**: If KMS key is not accessible or has been deleted, encrypted backups will fail. If key policy restricts AWS Backup service principal, update the key policy to allow backup operations.

5. **Assess retention compliance from Step 5**: If logs show "retention policy violation", recovery points are being deleted before retention period expires. If retention settings from Step 1 and Step 3 conflict, the more restrictive policy applies.

If the above analysis is inconclusive: Test backup with a manual job to isolate automated scheduling issues. Verify resource snapshot capabilities are enabled. Check AWS Backup service quotas. Review CloudTrail for KMS key access denials. Validate backup plan rule precedence if multiple rules apply.
