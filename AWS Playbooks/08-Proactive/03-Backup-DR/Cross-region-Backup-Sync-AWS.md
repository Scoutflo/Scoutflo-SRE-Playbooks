# Cross-region Backup Sync

## Meaning

Cross-region backup sync indicates that backup synchronization between regions is not completing or backup sync operations fail (triggering alarms like BackupSyncFailed or CrossRegionBackupSyncFailed) because backup sync jobs fail, backup sync lag exceeds thresholds, backup sync status shows errors, cross-region backup replication is not synchronized, or backup sync health checks fail. Backup sync jobs show failed status, backup sync lag metrics exceed thresholds, backup sync status indicates errors, and cross-region backup replication shows synchronization failures. This affects the storage layer and backup infrastructure, typically caused by backup sync service issues, cross-region network connectivity problems, backup sync job failures, or backup sync configuration errors; if backup sync protects container workloads, container backup data may be out of sync and applications may experience backup availability issues.

## Impact

CrossRegionBackupSyncFailed alarms fire; BackupSyncFailed alarms fire; cross-region backup synchronization fails; backup sync jobs fail; backup sync lag exceeds acceptable thresholds; disaster recovery procedures cannot rely on cross-region backups. Backup sync jobs remain in failed or pending state; backup sync lag metrics show increasing delays; if backup sync protects container workloads, container backup data may be out of sync, persistent volume backups may not be available in secondary region, and container applications may experience backup availability issues; applications may experience backup unavailability or cross-region backup sync failures.

## Playbook

1. Retrieve the Backup Vault `<vault-name>` in source region `<source-region>` and destination region `<destination-region>` and inspect their cross-region replication configuration, verifying backup vault accessibility in both regions.
2. List backup copy jobs in Backup Vault `<vault-name>` in destination region `<destination-region>` and filter for jobs with status 'FAILED' or 'ABORTED' within the last 24 hours, checking backup copy job completion status.
3. Retrieve backup copy job `<copy-job-id>` details and inspect its status, completion timestamp, error messages, and source region backup availability, checking backup copy job execution results.
4. Query CloudWatch Logs for log groups containing AWS Backup copy events and filter for error patterns containing 'copy failed', 'sync failed', or 'replication error' within the last 24 hours.
5. Retrieve CloudWatch metrics for AWS Backup service including CopyJobSuccessRate and CopyJobDuration over the last 24 hours to identify backup copy job failure patterns.
6. Compare backup copy job completion timestamps with backup creation timestamps in source region and verify whether backup copies complete within expected time windows, using backup copy job metadata as supporting evidence.
7. Retrieve the Backup Vault `<vault-name>` cross-region replication rule configuration and verify replication rule is correctly configured, checking backup replication rule settings.
8. List recovery points in Backup Vault `<vault-name>` in destination region `<destination-region>` and verify recovery point creation timestamps match source region backup timestamps, checking cross-region backup availability.

## Diagnosis

1. **Analyze copy job status from Step 2**: If failed/aborted copy jobs are identified, examine the error messages from Step 3. If errors indicate "access denied" or "permission denied", the issue is IAM-related. If errors indicate "vault not found" or "replication rule error", proceed to Step 7 to verify replication configuration. If errors indicate network timeouts, proceed to network analysis.

2. **Evaluate CloudWatch metrics from Step 5**: If CopyJobSuccessRate is below 95%, this indicates a systemic issue. If CopyJobDuration has increased significantly compared to baseline, cross-region network latency may be the root cause. If metrics show intermittent failures, network connectivity issues are likely.

3. **Cross-reference with replication configuration from Step 7**: If replication rules are correctly configured but copy jobs fail, check backup vault accessibility in both regions from Step 1. If destination vault shows access errors, verify IAM cross-account/cross-region permissions.

4. **Compare recovery point timestamps from Step 8**: If recovery points in destination region are significantly older than source region backups, backup sync lag is confirmed. If recovery points match expected timestamps, the sync is operational and the alert may be a false positive.

5. **Determine failure pattern**: If copy job failures occur at consistent times, check for scheduled maintenance windows or resource contention. If failures are random, network instability or service throttling is more likely.

If the above analysis is inconclusive: Review CloudWatch Logs from Step 4 for specific error patterns. Check for backup vault capacity constraints in destination region. Verify KMS key accessibility for encrypted backups. Examine cross-region VPC peering or Transit Gateway connectivity if applicable. Consider AWS Backup service health dashboard for regional service issues.
