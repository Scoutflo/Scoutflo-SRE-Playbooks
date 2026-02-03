# Cross-cluster Backup Sync

## Meaning

Cross-cluster backup sync indicates that backup synchronization between clusters is not completing or backup sync operations fail (triggering alerts like BackupSyncFailed or CrossClusterBackupSyncFailed) because backup sync jobs fail, backup sync lag exceeds thresholds, backup sync status shows errors, cross-cluster backup replication is not synchronized, or backup sync health checks fail. Backup sync jobs show failed status, backup sync lag metrics exceed thresholds, backup sync status indicates errors, and cross-cluster backup replication shows synchronization failures. This affects the storage layer and backup infrastructure, typically caused by backup sync service issues, cross-cluster network connectivity problems, backup sync job failures, or backup sync configuration errors; if backup sync protects container workloads, container backup data may be out of sync and applications may experience backup availability issues.

## Impact

CrossClusterBackupSyncFailed alerts fire; BackupSyncFailed alerts fire; cross-cluster backup synchronization fails; backup sync jobs fail; backup sync lag exceeds acceptable thresholds; disaster recovery procedures cannot rely on cross-cluster backups. Backup sync jobs remain in failed or pending state; backup sync lag metrics show increasing delays; if backup sync protects container workloads, container backup data may be out of sync, persistent volume backups may not be available in secondary cluster, and container applications may experience backup availability issues; applications may experience backup unavailability or cross-cluster backup sync failures.

## Playbook

1. List jobs in namespace <namespace> with label app=backup-sync to identify all cross-cluster backup sync jobs and their current status.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent backup copy failures or sync issues.

3. Describe job <copy-job-name> in namespace <namespace> to inspect its status, completion timestamp, and error messages.

4. Retrieve logs from backup sync pods with label app=backup-sync in namespace <namespace> and filter for error patterns containing 'copy failed', 'sync failed', or 'replication error'.

5. Retrieve Prometheus metrics for backup service including backup_copy_job_success_rate and backup_copy_job_duration over the last 24 hours to identify backup copy job failure patterns.

6. Compare backup copy job completion timestamps with backup creation timestamps in source cluster and verify whether backup copies complete within expected time windows, using backup copy job metadata as supporting evidence.

7. Retrieve configmap <backup-vault-configmap-name> in namespace <namespace> with YAML output and verify replication rule settings.

8. List volume snapshots in namespace <namespace> and verify recovery point creation timestamps match source cluster backup timestamps.

## Diagnosis

1. Review the backup sync job status from Steps 1 and 3. If jobs show failed status, examine error messages to identify the failure cause (network connectivity, permissions, storage capacity, or source backup issues).

2. Analyze the backup sync pod logs from Step 4. If logs show copy failure or replication error patterns, identify whether failures are due to network issues (suggesting connectivity problems) or data issues (suggesting source backup problems).

3. If Step 5 backup metrics show low success rates, then systematic sync issues exist. If success rates are high but specific jobs fail, then those jobs have configuration issues.

4. Review the backup completion comparison from Step 6. If backup copies are not completing within expected windows after source backup creation, then sync performance or capacity issues exist.

5. If Step 8 recovery point timestamps do not match source cluster backups, then sync lag exists and disaster recovery readiness is compromised.

If analysis is inconclusive: Examine events from Step 2 for backup copy failures or sync issues. Review the replication rule configuration from Step 7 to verify settings are correct. Determine whether sync failures affect all backups (suggesting infrastructure issues) or specific backup types (suggesting configuration problems for those backup types).
