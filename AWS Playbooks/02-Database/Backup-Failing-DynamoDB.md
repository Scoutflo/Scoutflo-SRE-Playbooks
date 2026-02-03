# DynamoDB Backup Failing

## Meaning

DynamoDB backup is failing (triggering backup failures or DynamoDBBackupFailed alarms) because backup permissions are insufficient, backup request limits are exceeded, table is in invalid state for backup, backup name conflicts exist, backup service encounters errors during backup creation, or DynamoDB table backup settings prevent backup creation. DynamoDB backups are not created, point-in-time recovery is unavailable, and backup retention policies fail. This affects the database backup and data protection layer and compromises disaster recovery, typically caused by permission issues, limit constraints, or table state problems; if using DynamoDB Global Tables, backup behavior may differ and applications may be affected by missing backup protection.

## Impact

DynamoDB backups are not created; point-in-time recovery is unavailable; backup retention policies fail; data protection is compromised; backup automation is ineffective; disaster recovery capabilities are lost; backup failure alarms fire; backup schedules are not executed. DynamoDBBackupFailed alarms may fire; if using DynamoDB Global Tables, backup behavior may differ; applications may be affected by missing backup protection; compliance requirements may be violated due to missing backups.

## Playbook

1. Verify DynamoDB table `<table-name>` exists and AWS service health for DynamoDB in region `<region>` is normal.
2. Retrieve the DynamoDB Table `<table-name>` in region `<region>` and inspect its backup configuration, backup status, and recent backup creation attempts, verifying table state is valid for backup.
3. Query CloudWatch Logs for log groups containing DynamoDB events and filter for backup failure events or error patterns related to table `<table-name>`, including failure reason details.
4. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including UserErrors over the last 24 hours to identify backup-related error patterns, analyzing error frequency.
5. List DynamoDB backup requests for table `<table-name>` and check backup status, failure reasons, and backup creation timestamps, analyzing backup history.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB backup API call failures related to table `<table-name>`, checking API error details.
7. Retrieve the DynamoDB Table `<table-name>` point-in-time recovery (PITR) status and verify PITR is enabled if required, checking PITR configuration.
8. Retrieve CloudWatch metrics for DynamoDB including backup request counts and verify if backup request limits are reached, checking for limit constraints.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM policy modification events related to DynamoDB backup operations within the last 24 hours, checking for permission changes.

## Diagnosis

1. Analyze CloudWatch Logs containing DynamoDB events and CloudTrail API call failures (from Playbook steps 3 and 6) to identify specific backup failure error messages. If errors indicate "AccessDenied", proceed immediately to IAM permission verification. If errors indicate "LimitExceededException", backup request limits are the cause. If errors indicate "ResourceInUseException", table state is preventing backup.

2. For access-denied errors, review IAM policy permissions (from Playbook step 9) associated with the backup operation. If recent IAM policy modifications removed DynamoDB backup permissions, restore the required permissions. If no recent changes, verify the IAM role or user has dynamodb:CreateBackup, dynamodb:DescribeBackup, and related permissions.

3. Review CloudWatch metrics for DynamoDB table UserErrors (from Playbook step 4) to identify backup-related error patterns over the last 24 hours. If error frequency is constant, this suggests a persistent configuration issue. If errors are intermittent, the issue may be related to service limits or transient table states.

4. Verify DynamoDB table configuration (from Playbook step 2) to check table state and backup eligibility. If table is in CREATING, UPDATING, or DELETING state, backups cannot be created until the table returns to ACTIVE state. If point-in-time recovery (PITR) is required but not enabled (from Playbook step 7), enable it for continuous backup capability.

5. Examine backup history and request patterns (from Playbook step 5) to determine if backup request limits are being exceeded. If multiple backup requests are made concurrently or backup names conflict with existing backups, the service rejects new requests.

6. Compare backup failure patterns across different tables within 24 hours. If failures are table-specific, the issue is related to that table's state or configuration. If failures are account-wide affecting multiple tables, the issue is likely IAM permissions or service limits.

7. Correlate backup failure timestamps with CloudTrail events (from Playbook step 9) within 30 minutes to identify any configuration or permission changes that coincide with when backups started failing.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including backup name conflicts and table backup settings, check for gradual issues like backup request limit exhaustion or table state transitions, verify external dependencies like DynamoDB backup service availability, examine historical patterns of backup failures, check for DynamoDB Global Tables backup configuration differences, verify DynamoDB table encryption affecting backup. Backup failures may result from backup name conflicts, table state constraints, backup service issues, DynamoDB Global Tables backup configuration, or DynamoDB table encryption configuration rather than immediate backup configuration changes.
