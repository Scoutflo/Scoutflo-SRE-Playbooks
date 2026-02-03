# Data Consistency Checks

## Meaning

Data consistency checks indicate that data consistency cannot be verified or data integrity issues are detected (triggering alarms like DataConsistencyFailed or DataIntegrityViolation) because data consistency verification fails, data integrity checks detect corruption, data replication shows inconsistencies, data checksum validation fails, or data consistency monitoring indicates violations. Data consistency checks show failures, data integrity violations are detected, data replication inconsistencies are identified, and data consistency monitoring indicates problems. This affects the data integrity layer and database reliability, typically caused by data corruption, replication lag issues, checksum validation failures, or data consistency monitoring issues; if data consistency affects container workloads, container persistent volume data may be inconsistent and applications may experience data integrity issues.

## Impact

DataConsistencyFailed alarms fire; DataIntegrityViolation alarms fire; data consistency cannot be verified; data integrity issues are detected; data corruption may occur; database reliability is compromised. Data consistency checks show failures; if data consistency affects container workloads, container persistent volume data may be inconsistent, pod data may be corrupted, and container applications may experience data integrity issues; applications may experience data corruption or data consistency failures.

## Playbook

1. Retrieve the RDS DB Instance `<db-instance-id>` configuration and verify database consistency check status and last consistency check timestamp, checking data consistency monitoring.
2. Retrieve RDS read replica lag metrics for DB instance `<db-instance-id>` and verify replication lag does not exceed thresholds, checking data replication consistency.
3. Query CloudWatch Logs for log groups containing RDS database events and filter for data consistency errors or integrity violation patterns within the last 7 days.
4. Retrieve CloudWatch metrics for RDS database including ReplicaLag and DatabaseConnections over the last 24 hours to identify data consistency issues.
5. Retrieve DynamoDB table `<table-name>` consistency metrics and verify read consistency and write consistency settings, checking DynamoDB data consistency.
6. Compare data consistency check timestamps with data modification timestamps within 1 hour and verify whether consistency checks detect issues after modifications, using database consistency check results as supporting evidence.
7. Retrieve S3 bucket `<bucket-name>` object integrity checks and verify object checksums and version consistency, checking S3 data integrity.
8. List EBS volume integrity check results for volume `<volume-id>` and verify volume data integrity status, checking EBS data consistency.

## Diagnosis

1. **Analyze replication lag from Step 2 and Step 4**: If ReplicaLag is consistently high, replicas are falling behind and may have stale data. If lag spikes during specific operations, those operations need optimization. If lag is zero but consistency issues exist, the problem is elsewhere.

2. **Evaluate database logs from Step 3**: If logs show checksum errors, data corruption exists. If logs show replication errors, investigate the replication stream. If logs show constraint violations, application logic may be flawed.

3. **Review DynamoDB consistency from Step 5**: If using eventual consistency where strong is needed, switch to strong consistency. If write conflicts occur, implement conditional writes. If global table lag exists, check cross-region replication.

4. **Cross-reference with S3 integrity from Step 7**: If object checksums fail, data was corrupted during transfer or storage. If version conflicts exist, concurrent writes may be causing issues. If objects are missing, lifecycle policies may have deleted them.

5. **Assess EBS integrity from Step 8**: If EBS volume checks show errors, the underlying storage has issues. If errors correlate with I/O patterns, high load may be causing problems. If errors are isolated, specific files may be corrupted.

If the above analysis is inconclusive: Run database consistency check tools (DBCC, pg_checksums). Review application transaction handling for race conditions. Check for network issues affecting data transfer. Consider point-in-time recovery to restore consistent state.
