# Data Corruption Detection

## Meaning

Data corruption detection indicates that data corruption is detected or data integrity violations are identified (triggering alarms like DataCorruptionDetected or DataIntegrityViolation) because data corruption checks detect corruption, data integrity violations are identified, data checksum validation fails, data corruption monitoring indicates problems, or data restoration tests reveal corruption. Data corruption checks show failures, data integrity violations are detected, data checksum validation fails, and data corruption monitoring indicates problems. This affects the data integrity layer and data reliability, typically caused by storage corruption, data transmission errors, checksum validation failures, or data corruption monitoring issues; if data corruption affects container workloads, container persistent volume data may be corrupted and applications may experience data integrity failures.

## Impact

DataCorruptionDetected alarms fire; DataIntegrityViolation alarms fire; data corruption is detected; data integrity violations are identified; data reliability is compromised; applications may experience data errors. Data corruption detection shows failures; if data corruption affects container workloads, container persistent volume data may be corrupted, pod data may be invalid, and container applications may experience data integrity failures; applications may experience data errors or data corruption failures.

## Playbook

1. Retrieve the RDS DB Instance `<db-instance-id>` configuration and verify database corruption check status and last corruption check timestamp, checking data corruption monitoring.
2. Query CloudWatch Logs for log groups containing RDS database events and filter for data corruption errors or integrity violation patterns within the last 7 days.
3. Retrieve CloudWatch metrics for RDS database including DatabaseErrors and DatabaseCorruptionErrors over the last 24 hours to identify data corruption patterns.
4. Retrieve EBS volume `<volume-id>` integrity check results and verify volume data corruption status, checking EBS data integrity.
5. Retrieve S3 bucket `<bucket-name>` object integrity checks and verify object checksums and corruption detection results, checking S3 data integrity.
6. Compare data corruption detection timestamps with data write operation timestamps within 1 hour and verify whether corruption is detected after write operations, using data corruption check results as supporting evidence.
7. Retrieve DynamoDB table `<table-name>` consistency metrics and verify data consistency and corruption detection status, checking DynamoDB data integrity.
8. List EBS snapshot integrity check results for snapshot `<snapshot-id>` and verify snapshot data corruption status, checking EBS backup data integrity.

## Diagnosis

1. **Analyze database error logs from Step 2 and Step 3**: If logs show checksum failures or page corruption errors, database-level corruption exists. If DatabaseErrors metric is elevated, identify the specific error types. If corruption patterns are recent, identify when corruption was first detected.

2. **Evaluate EBS volume integrity from Step 4**: If EBS status checks show I/O errors or impaired status, storage-level corruption is likely. If volume performance metrics show degradation before corruption, hardware issues may be the root cause. If volume is healthy but corruption exists, logical corruption is more likely.

3. **Review S3 object integrity from Step 5**: If S3 checksum validation fails, objects were corrupted during upload or storage. If specific prefixes show corruption, the source of those objects needs investigation. If corruption is widespread, network or storage issues exist.

4. **Cross-reference with write operations from Step 6**: If corruption is detected immediately after write operations, the write process is introducing corruption. If corruption is detected without recent writes, storage degradation is occurring over time.

5. **Assess recovery options from Step 8**: If clean EBS snapshots exist before corruption, recovery is possible. If all snapshots are corrupted, data recovery is limited. If DynamoDB shows corruption from Step 7, check point-in-time recovery availability.

If the above analysis is inconclusive: Restore from backup to a parallel environment for data comparison. Check application logic for data handling bugs. Review network path for transmission issues. Consider AWS Support engagement for infrastructure-level investigation.
