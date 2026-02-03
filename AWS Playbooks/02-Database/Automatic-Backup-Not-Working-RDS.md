# RDS Automatic Backup Not Working

## Meaning

RDS automatic backups fail or are not created (triggering alarms like BackupFailure or RDSBackupFailure) because backup retention period is set to zero, backup window conflicts with maintenance windows, IAM permissions are insufficient for backup operations, storage is full preventing backup creation, backup service encounters errors, or RDS instance backup configuration is disabled. Database backups are not created, data protection is compromised, and point-in-time recovery is unavailable. This affects the database layer and compromises data protection, typically caused by configuration issues, storage problems, or permission failures; if using RDS Aurora, backup behavior differs and applications may be affected by missing backup data protection.

## Impact

Database backups are not created; data protection is compromised; point-in-time recovery is unavailable; backup retention policies fail; BackupFailure alarms fire; disaster recovery capabilities are lost; automated backup schedules are not executed; data loss risk increases. RDSBackupFailure alarms may fire; if using RDS Aurora, backup configuration differs from standard RDS; applications may be affected by missing backup protection; compliance requirements may be violated due to missing backups.

## Playbook

1. Verify RDS instance `<db-instance-id>` exists and is in "available" state, and AWS service health for RDS in region `<region>` is normal.
2. Retrieve the RDS Instance `<db-instance-id>` in region `<region>` and inspect its backup retention period, automated backup settings, backup window configuration, and latest backup status, verifying backup configuration is enabled.
3. Query CloudWatch Logs for log groups containing RDS events and filter for backup failure events or error patterns related to instance `<db-instance-id>`, including backup error messages.
4. Retrieve CloudWatch metrics for RDS instance `<db-instance-id>` including FreeStorageSpace over the last 24 hours to verify storage availability for backups, analyzing storage trends.
5. Retrieve CloudWatch alarms associated with RDS instance `<db-instance-id>` with metric BackupFailure and check for alarms in ALARM state, verifying alarm configurations.
6. Retrieve the RDS Instance `<db-instance-id>` maintenance window configuration and verify backup window does not conflict with maintenance window, checking window scheduling.
7. Retrieve the RDS Instance `<db-instance-id>` IAM role configuration and verify IAM permissions for backup operations, checking service-linked role permissions.
8. List RDS backup events for instance `<db-instance-id>` and check backup creation timestamps, backup status, and failure reasons, analyzing backup history.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for RDS backup configuration modification events related to instance `<db-instance-id>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when BackupFailure alarms first triggered. Cross-reference with RDS backup events (from Playbook step 8) to establish the exact timestamp when backups stopped completing.

2. If instance configuration (from Playbook step 2) shows backup retention period is zero, automated backups are disabled. This is the root cause - retention period must be 1-35 days to enable automated backups.

3. If retention period is configured but backups fail, check FreeStorageSpace metrics (from Playbook step 4). If storage is critically low around backup timestamps, insufficient storage prevented backup creation.

4. If storage is adequate, compare backup window with maintenance window (from Playbook step 6). Overlapping windows can cause conflicts where maintenance operations prevent backup completion.

5. If CloudTrail events (from Playbook step 9) show backup configuration changes around the failure timestamp, those modifications may have inadvertently disabled or misconfigured backup settings.

6. If backup event logs (from Playbook step 3 and step 8) show permission errors, verify IAM service-linked role permissions (from Playbook step 7). Missing or modified permissions prevent RDS from creating snapshots.

7. If backup failures are intermittent rather than constant (from backup history analysis), the issue may be transient service problems or periodic storage pressure during backup windows.

If no correlation is found: extend analysis to 14 days, review RDS event subscriptions for detailed error messages, check Aurora-specific backup configuration if applicable, verify cross-region snapshot copy permissions, and examine Multi-AZ backup replication status.
