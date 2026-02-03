# Backup Integrity Verification

## Meaning

Backup integrity verification indicates that backup data integrity cannot be verified or backup corruption is detected (triggering alarms like BackupIntegrityFailed or BackupCorruptionDetected) because backup integrity checks fail, backup corruption is detected, backup checksum validation fails, backup restoration tests fail, or backup integrity monitoring indicates violations. Backup integrity checks show failures, backup corruption is detected, backup checksum validation fails, and backup integrity monitoring indicates problems. This affects the data integrity layer and backup reliability, typically caused by backup corruption, backup service issues, checksum validation failures, or backup integrity monitoring failures; if backup integrity affects container workloads, container backup data may be corrupted and applications may experience backup restoration failures.

## Impact

BackupIntegrityFailed alarms fire; BackupCorruptionDetected alarms fire; backup integrity cannot be verified; backup corruption is detected; backup restoration may fail; disaster recovery procedures may be compromised. Backup integrity verification shows failures; if backup integrity affects container workloads, container backup data may be corrupted, persistent volume backups may be invalid, and container applications may experience backup restoration failures; applications may experience data loss or backup restoration failures.

## Playbook

1. Retrieve the Backup Vault `<vault-name>` recovery point details and inspect recovery point integrity status, checksum validation results, and backup completion status, verifying backup integrity.
2. List backup jobs in Backup Vault `<vault-name>` in region `<region>` and retrieve backup job integrity check results to identify backups with integrity failures.
3. Query CloudWatch Logs for log groups containing AWS Backup events and filter for backup integrity errors or corruption detection patterns within the last 7 days.
4. Retrieve CloudWatch metrics for AWS Backup service including BackupJobSuccessRate and BackupIntegrityCheckResults over the last 30 days to identify backup integrity issues.
5. Retrieve the recovery point `<recovery-point-arn>` integrity check results and verify checksum validation and data integrity status, checking recovery point validity.
6. Compare backup integrity check failure timestamps with backup job completion timestamps within 1 hour and verify whether integrity failures occur after backup completion, using backup integrity check results as supporting evidence.
7. Retrieve S3 bucket `<bucket-name>` backup object integrity checks and verify backup object checksums and version consistency, checking S3 backup data integrity.
8. List EBS snapshot integrity check results for snapshot `<snapshot-id>` and verify snapshot data integrity status, checking EBS backup integrity.

## Diagnosis

1. **Analyze recovery point integrity from Step 1 and Step 5**: If integrity status shows failure, the recovery point is corrupted and cannot be reliably restored. If checksums are missing, integrity verification was not performed. If status is unknown, run manual verification.

2. **Evaluate backup job results from Step 2**: If backup jobs complete but integrity fails, corruption occurs during or after backup. If backup jobs fail before integrity check, address backup failures first. If specific resource types fail, investigate those resources.

3. **Review CloudWatch metrics from Step 4**: If BackupIntegrityCheckResults shows increasing failures, a systemic issue exists. If failures are sporadic, investigate affected recovery points individually. If no failures but concerns exist, run manual integrity tests.

4. **Cross-reference with timing from Step 6**: If integrity failures occur immediately after backup, the backup process is corrupting data. If failures occur later, storage degradation is the cause. If failures correlate with specific job types, those job configurations need review.

5. **Assess storage-level integrity from Step 7 and Step 8**: If S3 checksums fail, object storage corruption exists. If EBS snapshots show errors, snapshot integrity is compromised. If both storage types fail, investigate common infrastructure issues.

If the above analysis is inconclusive: Perform test restore to validate backup usability. Compare backup data with source data for verification. Review KMS key accessibility for encrypted backups. Consider implementing backup verification as regular process.
