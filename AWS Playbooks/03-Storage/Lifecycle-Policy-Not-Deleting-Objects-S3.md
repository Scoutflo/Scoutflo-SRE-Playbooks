# S3 Lifecycle Policy Not Deleting Objects

## Meaning

S3 lifecycle policy is not deleting objects as expected (triggering storage cost issues or S3LifecyclePolicyNotWorking alarms) because lifecycle policy rules are not configured, transition rules are incorrect, expiration rules are not met, policy status is disabled, object tags do not match lifecycle rule filters, or S3 bucket versioning prevents deletion of current versions. S3 objects are not deleted automatically, storage costs increase, and lifecycle transitions do not occur. This affects the storage and cost management layer and increases storage costs, typically caused by policy configuration issues, rule filter problems, or versioning conflicts; if using S3 lifecycle with Intelligent-Tiering, policy behavior may differ and applications may experience storage cost issues.

## Impact

S3 objects are not deleted automatically; storage costs increase; lifecycle transitions do not occur; expiration rules are not applied; storage optimization fails; old objects accumulate; lifecycle policy automation is ineffective; cost management objectives are not met. S3LifecyclePolicyNotWorking alarms may fire; if using S3 lifecycle with Intelligent-Tiering, policy behavior may differ; applications may experience increased storage costs; storage optimization objectives may not be met.

## Playbook

1. Verify S3 bucket `<bucket-name>` exists and AWS service health for S3 in region `<region>` is normal.
2. Retrieve the S3 Bucket `<bucket-name>` in region `<region>` and inspect its lifecycle policy configuration, rule definitions, expiration settings, and transition rules, verifying lifecycle policy is enabled.
3. Query CloudWatch Logs for log groups containing S3 server access logs and filter for lifecycle transition events or deletion patterns related to bucket `<bucket-name>`, including lifecycle action details.
4. Retrieve CloudWatch metrics for S3 Bucket `<bucket-name>` including BucketSizeBytes and NumberOfObjects over the last 30 days to identify object accumulation patterns, analyzing storage trends.
5. List S3 objects in bucket `<bucket-name>` with creation dates older than lifecycle expiration rules and check if objects should have been deleted, analyzing object age.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 lifecycle policy modification events related to bucket `<bucket-name>`, checking for policy changes.
7. Retrieve the S3 Bucket `<bucket-name>` versioning configuration and verify versioning status, checking if versioning prevents deletion of current versions.
8. Retrieve the S3 Bucket `<bucket-name>` lifecycle policy rule filters and verify object tag matching, checking if tag filters prevent deletion.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 object tagging or lifecycle policy rule modification events related to bucket `<bucket-name>` within the last 30 days, checking for tag or rule changes.

## Diagnosis

1. Analyze CloudWatch metrics for S3 bucket (from Playbook step 4) including BucketSizeBytes and NumberOfObjects over the last 30 days to identify object accumulation patterns. If object count and size are increasing when they should be decreasing, lifecycle policies are not executing as expected.

2. Review S3 lifecycle policy configuration (from Playbook step 2) to verify expiration rules are correctly defined and enabled. If rule status is "Disabled", objects will not be deleted. If expiration days are set higher than expected, objects may not yet have reached expiration age.

3. Examine S3 server access logs (from Playbook step 3) to identify lifecycle transition or deletion events. If logs show no lifecycle actions for objects that should have expired, verify rule filters and expiration settings. If logs show some deletions but not all, rule filters may be excluding certain objects.

4. Verify bucket versioning configuration (from Playbook step 7) to determine if versioning affects deletion behavior. If versioning is enabled, lifecycle rules must explicitly define actions for both current and previous versions. Deleting current versions creates delete markers but does not remove previous versions.

5. Check lifecycle policy rule filters (from Playbook step 8) including prefix and tag filters. If objects do not match rule filters (wrong prefix or missing required tags), they will not be processed by the lifecycle rule.

6. Analyze objects that should have been deleted (from Playbook step 5) to verify their creation dates exceed expiration thresholds. If objects are newer than the expiration period, they are not yet eligible for deletion.

7. Correlate CloudTrail events (from Playbook step 6 and 9) with object accumulation timestamps to identify any lifecycle policy modifications that may have disabled or changed expiration rules.

8. Compare deletion patterns across different object prefixes within 30 days. If deletions occur for some prefixes but not others, the lifecycle rules may have incorrect prefix filters or some prefixes may be excluded from rules.

9. Note that lifecycle policy execution is not immediate; S3 may take up to 24-48 hours to execute lifecycle rules after objects become eligible. If objects recently became eligible for expiration, allow sufficient time for lifecycle execution.

If no correlation is found within the specified time windows: extend timeframes to 90 days, review alternative evidence sources including lifecycle policy rule status and object versioning configuration, check for gradual issues like policy rule evaluation delays or object version accumulation, verify external dependencies like lifecycle policy service availability, examine historical patterns of object retention, check for S3 bucket versioning preventing deletion, verify S3 lifecycle policy rule filter tag matching. Lifecycle policy issues may result from object versioning preventing deletion, lifecycle policy rule evaluation delays, object tag mismatches, S3 bucket versioning configuration, or S3 lifecycle policy rule filter tag matching issues rather than immediate policy configuration changes.
