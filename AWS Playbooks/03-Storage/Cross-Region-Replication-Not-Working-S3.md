# S3 Cross-Region Replication Not Working

## Meaning

S3 cross-region replication is not working (triggering replication failures or S3ReplicationFailed alarms) because replication configuration is missing or incorrect, IAM role permissions are insufficient, source and destination buckets are misconfigured, replication status shows failures, replication rules do not match object filters, or S3 bucket versioning is disabled preventing replication. S3 objects are not replicated to destination region, data redundancy is lost, and cross-region backup fails. This affects the storage and data protection layer and compromises disaster recovery, typically caused by replication configuration issues, permission problems, or bucket configuration errors; if using S3 replication with encryption, KMS key configuration may affect replication and applications may be affected by missing cross-region redundancy.

## Impact

S3 objects are not replicated to destination region; data redundancy is lost; cross-region backup fails; replication lag increases; replication status shows errors; disaster recovery capabilities are compromised; data synchronization fails; replication automation is ineffective. S3ReplicationFailed alarms may fire; if using S3 replication with encryption, KMS key configuration may affect replication; applications may be affected by missing cross-region redundancy; disaster recovery capabilities may be compromised.

## Playbook

1. Verify S3 source bucket `<source-bucket-name>` exists and AWS service health for S3 in region `<region>` is normal.
2. Retrieve the S3 Bucket `<source-bucket-name>` in region `<region>` and inspect its replication configuration, replication rules, destination bucket settings, and replication status, verifying replication is enabled.
3. Retrieve the IAM role `<role-name>` used for S3 replication and inspect its policy permissions for replication operations on source and destination buckets, verifying IAM permissions.
4. Query CloudWatch Logs for log groups containing S3 server access logs and filter for replication failure events or error patterns related to bucket `<source-bucket-name>`, including replication error details.
5. Retrieve CloudWatch metrics for S3 Bucket `<source-bucket-name>` including ReplicationLatency and ReplicationBytes over the last 24 hours to identify replication patterns, analyzing replication metrics.
6. List S3 objects in source bucket `<source-bucket-name>` that should be replicated and check replication status and failure reasons, analyzing object replication status.
7. Retrieve the S3 Bucket `<source-bucket-name>` versioning configuration and verify versioning is enabled, checking if versioning affects replication.
8. Retrieve the S3 Bucket `<destination-bucket-name>` in destination region and verify bucket exists and replication permissions, checking destination bucket configuration.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 replication configuration or IAM role policy modification events related to source bucket `<source-bucket-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for S3 replication (from Playbook step 5) including ReplicationLatency and ReplicationBytes to identify replication patterns. If metrics show zero ReplicationBytes, replication is not occurring at all. If ReplicationLatency is increasing, there may be a backlog of objects waiting to replicate.

2. Review CloudWatch Logs containing S3 server access logs and CloudTrail events (from Playbook steps 4 and 6) to identify specific replication failure errors. If errors indicate "AccessDenied", proceed immediately to IAM permission verification. If errors indicate destination bucket issues, check destination bucket configuration.

3. For access-denied errors, verify IAM role permissions (from Playbook step 3) used for S3 replication. The replication role must have s3:GetObjectVersionForReplication, s3:ReplicateObject, and s3:ReplicateDelete permissions on both source and destination buckets. If using KMS encryption, the role also needs kms:Decrypt on source and kms:Encrypt on destination.

4. Verify source bucket versioning configuration (from Playbook step 7) to confirm versioning is enabled. S3 cross-region replication requires versioning to be enabled on both source and destination buckets. If versioning is disabled or suspended, replication cannot function.

5. Examine replication configuration (from Playbook step 2) to verify replication rules are correctly defined including destination bucket, rule status, and filter criteria. If rules use prefix or tag filters, verify objects match the filter criteria.

6. Verify destination bucket exists and is accessible (from Playbook step 8) by checking destination bucket configuration. If the destination bucket does not exist, was deleted, or the replication role lacks write permissions, replication fails.

7. Review object replication status (from Playbook step 6) for specific objects that should have been replicated. If replication status shows "FAILED", examine the failure reason. If status shows "PENDING", there may be a backlog or temporary delay.

8. Correlate CloudTrail events (from Playbook step 9) with replication failure timestamps within 30 minutes to identify any IAM role policy or replication configuration modifications. If permission changes coincide with when replication stopped working, those changes are the likely cause.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including replication rule status and destination bucket configuration, check for gradual issues like destination bucket access issues or replication role permission drift, verify external dependencies like cross-region network connectivity or destination bucket permissions, examine historical patterns of replication failures, check for S3 bucket versioning requirements, verify S3 replication with KMS encryption key configuration. Replication failures may result from destination bucket configuration issues, replication role permission problems, cross-region connectivity issues, S3 bucket versioning not enabled, or S3 replication with KMS encryption key configuration rather than immediate replication configuration changes.
