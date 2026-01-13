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

1. Compare storage allocation modification timestamps with storage full error timestamps within 30 minutes and verify whether storage exhaustion occurred after allocation changes, using RDS storage events as supporting evidence.
2. Correlate database write operation timestamps with storage capacity timestamps and verify whether write operations caused storage to reach capacity limits, using RDS metrics as supporting evidence.
3. Compare log file retention modification timestamps with storage growth timestamps within 24 hours and verify whether log file accumulation caused storage exhaustion, using RDS log file configuration events as supporting evidence.
4. Compare automatic storage scaling configuration change timestamps with storage full error timestamps within 30 minutes and verify whether disabled automatic scaling prevented storage expansion, using RDS configuration events as supporting evidence.
5. Analyze storage growth rate over the last 7 days to determine if growth is constant (data accumulation) or sudden (bulk data operations).

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including database transaction logs and backup storage, check for gradual issues like log file accumulation, verify external dependencies like snapshot storage, examine historical patterns of storage growth, check for RDS Aurora storage model differences, verify RDS Multi-AZ storage duplication. Storage exhaustion may result from log file growth, snapshot accumulation, unoptimized data retention policies, RDS Aurora shared storage behavior, or storage I/O performance degradation rather than immediate storage allocation changes.
