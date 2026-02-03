# RTO/RPO Validation

## Meaning

RTO/RPO validation indicates that Recovery Time Objective and Recovery Point Objective targets cannot be met or measured accurately (triggering alerts like RTOExceeded or RPOExceeded) because backup frequencies do not meet RPO targets, restore operations exceed RTO targets, backup completion times are not tracked, restore completion times are not measured, or RTO/RPO metrics indicate target violations. Backup completion times exceed RPO windows, restore operations exceed RTO targets, RTO/RPO metrics show target violations, and backup/restore timestamps indicate non-compliance with targets. This affects the disaster recovery layer and backup infrastructure, typically caused by backup schedule misalignment, restore operation delays, metric tracking failures, or RTO/RPO target misconfiguration; if RTO/RPO validation protects container workloads, container data recovery may not meet targets and applications may experience extended recovery times.

## Impact

RTOExceeded alerts fire; RPOExceeded alerts fire; disaster recovery targets cannot be met; backup frequencies violate RPO targets; restore operations exceed RTO targets; recovery procedures cannot be validated. Backup completion times exceed RPO windows; restore operations exceed RTO time limits; if RTO/RPO validation protects container workloads, container data recovery may not meet targets, persistent volume recovery may exceed RTO, and container applications may experience extended recovery times; applications may experience extended downtime or data loss beyond acceptable limits.

## Playbook

1. List cronjobs in namespace <namespace> with label app=backup to identify backup schedule jobs and their current configuration for RPO validation.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to backup or restore operations that may affect RTO/RPO compliance.
3. Describe cronjob <backup-cronjob-name> in namespace <namespace> to inspect backup schedule configuration, frequency, and last successful execution times.
4. List jobs in namespace <namespace> with label app=backup sorted by completion time to retrieve backup job completion timestamps and calculate actual backup frequency for RPO validation.
5. List jobs in namespace <namespace> with label app=restore sorted by completion time to retrieve restore job completion timestamps and calculate actual restore duration for RTO validation.
6. Retrieve Prometheus metrics for backup service including backup_job_duration and restore_job_duration over the last 30 days to identify RTO/RPO compliance patterns.
7. Compare backup job completion timestamps with backup schedule timestamps and verify whether backup frequencies meet RPO targets, using backup job metadata as supporting evidence.
8. Compare restore job completion timestamps with RTO targets and verify whether restore operations complete within RTO time limits, using restore job metadata as supporting evidence.

## Diagnosis

1. Review the backup cronjob configuration from Step 3 and job completion times from Step 4. If backup frequency does not match RPO requirements (e.g., RPO of 1 hour but backups every 4 hours), then backup schedules need adjustment.

2. Analyze the restore job durations from Step 5. If restore times consistently approach or exceed RTO targets, then restore optimization is needed. If restore times have comfortable margin, then RTO compliance is maintained.

3. If Step 6 backup/restore metrics show increasing durations over 30 days, then performance is degrading and may eventually cause RTO/RPO violations even if currently compliant.

4. Review the backup schedule comparison from Step 7. If actual backup completions do not match scheduled times, then backup jobs are failing or delayed. Investigate backup job failures.

5. If Step 8 restore completion analysis shows RTO being missed, identify the bottleneck (data transfer, compute resources, or storage I/O) and optimize accordingly.

If analysis is inconclusive: Examine events from Step 2 for backup or restore failures. Determine whether RTO/RPO violations are concentrated at specific times (suggesting resource contention) or random (suggesting infrastructure issues). Verify that RTO/RPO targets are realistic for the data volumes and infrastructure capabilities.
