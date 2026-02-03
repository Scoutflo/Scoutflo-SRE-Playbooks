# RDS Storage Full Error

## Meaning

RDS database storage is full or approaching capacity limits (triggering alarms like FreeStorageSpace) because allocated storage is insufficient, large tables consume excessive space, old or unnecessary data accumulates, automatic storage scaling is disabled, storage metrics indicate capacity exhaustion, or RDS log files consume excessive space. Database write operations fail, storage full errors occur, and CloudWatch metrics show FreeStorageSpace approaching zero. This affects the database layer and blocks data writes, typically caused by storage allocation issues, data growth, or log file accumulation; if using RDS Aurora, shared storage model may behave differently and storage I/O performance may degrade as storage fills.

## Impact

Database write operations fail; storage full errors occur; FreeStorageSpace alarms fire; database becomes read-only; new data cannot be inserted; database backups may fail; storage capacity is exhausted; database performance degrades; automatic scaling may trigger; application write operations error. Database queries timeout; transaction failures occur; if using RDS Aurora, storage I/O performance degrades as shared storage fills; applications may experience errors or performance degradation due to storage exhaustion; connection pool limits may be reached preventing new connections.

## Playbook

1. Verify RDS instance `<rds-instance-id>` exists and is in "available" state, and AWS service health for RDS in region `<region>` is normal.
2. Retrieve CloudWatch metrics for RDS instance `<rds-instance-id>` including FreeStorageSpace to check current storage utilization, analyzing storage trends over the last 7 days.
3. Retrieve the RDS Instance `<rds-instance-id>` storage configuration and verify allocated storage settings and automatic storage scaling configuration, checking maximum storage limit.
4. Query CloudWatch Logs for log groups containing RDS instance logs and filter for storage-related messages indicating capacity issues or storage errors, including log file size information.
5. Retrieve the RDS Instance `<rds-instance-id>` log file retention settings and verify log file retention period, checking if log files are consuming excessive storage.
6. Retrieve the RDS Instance `<rds-instance-id>` automatic storage scaling settings and verify if automatic scaling is enabled to prevent future issues, checking scaling trigger thresholds.
7. Retrieve the RDS Instance `<rds-instance-id>` backup retention and Performance Insights data retention settings and verify automated backup retention period and Performance Insights data retention period, checking if backups or Performance Insights data are consuming storage.
8. Verify if using RDS Aurora and check Aurora storage model (shared storage), and retrieve CloudWatch metrics for RDS instance `<rds-instance-id>` including ReadIOPS and WriteIOPS, verifying storage behavior differences from standard RDS and checking for storage I/O performance degradation as storage fills.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify RDS service availability in the region. If service health indicates issues, storage errors may be AWS-side requiring monitoring rather than configuration changes.

2. If FreeStorageSpace metric from Playbook step 2 shows storage approaching or at zero, storage exhaustion is confirmed. Analyze the 7-day trend to determine if growth was gradual (data accumulation) or sudden (bulk operations, log explosion).

3. If storage configuration from Playbook step 3 shows allocated storage is insufficient and automatic storage scaling is disabled, storage cannot expand automatically. Enable autoscaling with appropriate maximum limit to prevent future exhaustion.

4. If RDS logs from Playbook step 4 show storage-related error messages, identify when storage errors first appeared. This timestamp marks when storage became critically low.

5. If log file retention from Playbook step 5 shows extended retention periods, log files may be consuming significant storage. Check if log files represent a large portion of total storage usage.

6. If automatic scaling settings from Playbook step 6 show autoscaling is enabled but maximum storage threshold has been reached, the configured maximum is insufficient. Increase maximum storage allocation.

7. If backup retention from Playbook step 7 is set to many days, automated backups consume additional storage. If Performance Insights retention is extended, that data also consumes storage.

8. If using RDS Aurora (Playbook step 8), storage is shared across the cluster and scales automatically. Storage I/O performance may degrade as the cluster grows. Check ReadIOPS and WriteIOPS metrics for I/O bottlenecks that may indicate storage pressure.

If no correlation is found from the collected data: extend FreeStorageSpace metric analysis to 30 days, examine database table sizes to identify large tables, check for orphaned or temporary tables consuming space, and review binary log retention settings. Storage exhaustion may result from unoptimized queries creating temporary tables, large transaction logs, or schema changes requiring table rebuilds.

