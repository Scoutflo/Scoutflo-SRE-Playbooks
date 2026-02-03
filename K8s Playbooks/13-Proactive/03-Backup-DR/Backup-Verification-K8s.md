# Backup Verification

## Meaning

Backup verification indicates that etcd backups or cluster state backups may not be completing successfully or backup integrity cannot be confirmed (triggering alerts like KubeBackupFailed or BackupVerificationFailed) because backup jobs fail, backup retention policies are not met, backup encryption verification fails, backup completion status cannot be verified, or backup metadata indicates incomplete backups. Backups show failed status in cluster backup tools, backup jobs remain in running state indefinitely, backup completion timestamps are missing or outdated, and backup verification checks fail. This affects the storage layer and backup infrastructure, typically caused by backup service issues, retention policy violations, encryption key problems, or backup job failures; if backups protect container workloads, container data recovery may be impossible and applications may experience data loss risks.

## Impact

KubeBackupFailed alerts fire; BackupVerificationFailed alerts fire; data recovery may be impossible; RTO and RPO targets cannot be met; backup jobs fail; backup retention policies are violated; backup encryption verification fails; backup completion cannot be confirmed; disaster recovery procedures cannot be executed. Backup jobs remain in running or failed state; backup metadata shows incomplete or corrupted backups; if backups protect container workloads, container data recovery may fail, persistent volume data may be lost, and container applications may experience data loss risks; applications may experience data loss or recovery failures.

## Playbook

1. List jobs in namespace <namespace> with label app=etcd-backup to identify all backup jobs and their completion status.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent backup failures or issues.

3. Describe job <backup-job-name> in namespace <namespace> to inspect its status, completion timestamp, and error messages.

4. Retrieve logs from backup pod <backup-pod-name> in namespace <namespace> and filter for error patterns containing 'backup failed', 'verification failed', or 'retention policy violation'.

5. Retrieve Prometheus metrics for backup service including backup_job_success_rate and backup_job_duration over the last 24 hours to identify backup job failure patterns.

6. List volume snapshots in namespace <namespace> and verify recovery point creation timestamps match backup schedule.

7. Retrieve secret <backup-secret-name> in namespace <namespace> with YAML output to verify encryption key accessibility.

8. Compare backup job completion timestamps with backup schedule timestamps and verify whether backup jobs complete within expected time windows, using backup job metadata as supporting evidence.

## Diagnosis

1. Review the backup job status from Steps 1 and 3. If jobs show failed status or incomplete completion, examine error messages to identify the failure cause (permissions, storage, encryption, or resource constraints).

2. Analyze the backup pod logs from Step 4. If logs show encryption or verification failure patterns, then encryption key accessibility from Step 7 needs investigation. If logs show retention policy violations, then backup cleanup automation is failing.

3. If Step 5 backup metrics show low success rates over 24 hours, then systematic backup issues exist. If success rates are high but specific jobs fail, then those jobs have configuration issues.

4. Review the volume snapshot timestamps from Step 6. If recovery points are missing or outdated relative to the backup schedule, then backup completion is failing or snapshots are not being created.

5. If Step 8 backup job completion analysis shows jobs not completing within expected windows, then backup performance issues or resource constraints may be causing timeouts.

If analysis is inconclusive: Examine events from Step 2 for backup-related failures. Determine whether failures affect all backup jobs (suggesting infrastructure issues) or specific jobs (suggesting job-specific configuration problems). Verify backup storage capacity and backup job service account permissions.
