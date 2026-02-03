# RTO/RPO Validation

## Meaning

RTO/RPO validation indicates that Recovery Time Objective and Recovery Point Objective targets cannot be met or measured accurately (triggering alarms like RTOExceeded or RPOExceeded) because backup frequencies do not meet RPO targets, restore operations exceed RTO targets, backup completion times are not tracked, restore completion times are not measured, or RTO/RPO metrics indicate target violations. Backup completion times exceed RPO windows, restore operations exceed RTO targets, RTO/RPO metrics show target violations, and backup/restore timestamps indicate non-compliance with targets. This affects the disaster recovery layer and backup infrastructure, typically caused by backup schedule misalignment, restore operation delays, metric tracking failures, or RTO/RPO target misconfiguration; if RTO/RPO validation protects container workloads, container data recovery may not meet targets and applications may experience extended recovery times.

## Impact

RTOExceeded alarms fire; RPOExceeded alarms fire; disaster recovery targets cannot be met; backup frequencies violate RPO targets; restore operations exceed RTO targets; recovery procedures cannot be validated. Backup completion times exceed RPO windows; restore operations exceed RTO time limits; if RTO/RPO validation protects container workloads, container data recovery may not meet targets, persistent volume recovery may exceed RTO, and container applications may experience extended recovery times; applications may experience extended downtime or data loss beyond acceptable limits.

## Playbook

1. Retrieve the Backup Plan `<plan-name>` in region `<region>` and inspect its backup schedule frequency and RPO target configuration, verifying backup schedule alignment with RPO targets.
2. List backup jobs in Backup Vault `<vault-name>` in region `<region>` and retrieve backup job completion timestamps to calculate actual backup frequency and compare with RPO targets.
3. List restore jobs in Backup Vault `<vault-name>` in region `<region>` and retrieve restore job completion timestamps to calculate actual restore duration and compare with RTO targets.
4. Retrieve CloudWatch metrics for AWS Backup service including BackupJobDuration and RestoreJobDuration over the last 30 days to identify RTO/RPO compliance patterns.
5. Query CloudWatch Logs for log groups containing AWS Backup events and filter for backup or restore job completion timestamps within the last 30 days to verify RTO/RPO measurement accuracy.
6. Compare backup job completion timestamps with backup schedule timestamps and verify whether backup frequencies meet RPO targets, using backup job metadata as supporting evidence.
7. Compare restore job completion timestamps with RTO targets and verify whether restore operations complete within RTO time limits, using restore job metadata as supporting evidence.
8. Retrieve the Backup Plan `<plan-name>` RTO and RPO target configuration and verify target values are correctly configured, checking RTO/RPO target settings.

## Diagnosis

1. **Analyze backup frequency from Step 2 and Step 6**: If time between backup completions exceeds RPO target, backup schedule frequency is insufficient. If backups complete on schedule but RPO is still violated, the RPO target may be more aggressive than the configured schedule. Cross-reference with backup plan from Step 1 to identify misalignment.

2. **Evaluate restore duration from Step 3 and Step 7**: If restore jobs consistently exceed RTO targets, identify the bottleneck. If RestoreJobDuration from Step 4 shows increasing trends, data volume growth is outpacing restore capacity. If durations are inconsistent, resource availability varies.

3. **Review CloudWatch metrics from Step 4**: If BackupJobDuration shows delays, backup jobs are taking longer than scheduled intervals, causing RPO violations. If both backup and restore durations exceed targets, infrastructure capacity is insufficient for current data volumes.

4. **Cross-reference with configuration from Step 8**: If RTO/RPO targets in configuration do not match business requirements, update the configuration. If targets are correct but consistently violated, backup/restore infrastructure needs scaling or optimization.

5. **Assess compliance trend from Step 5**: If RTO/RPO violations are increasing over time, data growth or infrastructure degradation is the cause. If violations are sporadic, specific job failures or resource contention are likely.

If the above analysis is inconclusive: Benchmark restore times with test restores to establish realistic RTO. Review backup job parallelism settings. Evaluate whether RPO targets are achievable with current backup technology. Consider incremental backup strategies to reduce backup duration. Assess storage tier performance for restore operations.
