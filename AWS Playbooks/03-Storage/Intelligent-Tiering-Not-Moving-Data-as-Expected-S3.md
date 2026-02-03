# S3 Intelligent-Tiering Not Moving Data as Expected

## Meaning

S3 Intelligent-Tiering is not moving data as expected (triggering storage optimization failures or S3IntelligentTieringNotWorking alarms) because Intelligent-Tiering is not enabled, data access patterns do not trigger tier transitions, tier transition rules are misconfigured, data access frequency thresholds are not met, Intelligent-Tiering service encounters errors during tier analysis, or Intelligent-Tiering monitoring period has not completed. S3 Intelligent-Tiering tier transitions do not occur, storage cost optimization fails, and data remains in expensive tiers. This affects the storage and cost optimization layer and increases storage costs, typically caused by Intelligent-Tiering configuration issues, access pattern problems, or monitoring period constraints; if using S3 Intelligent-Tiering with different access tiers, transition behavior may differ and applications may experience suboptimal storage costs.

## Impact

S3 Intelligent-Tiering tier transitions do not occur; storage cost optimization fails; data remains in expensive tiers; tier transition automation is ineffective; storage costs are higher than expected; Intelligent-Tiering benefits are not realized; cost management objectives are not met. S3IntelligentTieringNotWorking alarms may fire; if using S3 Intelligent-Tiering with different access tiers, transition behavior may differ; applications may experience higher storage costs; cost optimization benefits may not be realized.

## Playbook

1. Verify S3 bucket `<bucket-name>` exists and AWS service health for S3 in region `<region>` is normal.
2. Retrieve the S3 Bucket `<bucket-name>` in region `<region>` and inspect its Intelligent-Tiering configuration, tier transition settings, and Intelligent-Tiering status, verifying Intelligent-Tiering is enabled.
3. Query CloudWatch Logs for log groups containing S3 server access logs and filter for object access patterns, access frequency, and tier transition events related to bucket `<bucket-name>`, including access pattern details.
4. Retrieve CloudWatch metrics for S3 Bucket `<bucket-name>` including BucketSizeBytes by storage class over the last 30 days to identify tier distribution patterns, analyzing tier distribution.
5. List S3 objects in bucket `<bucket-name>` with Intelligent-Tiering enabled and check object access timestamps, tier assignments, and tier transition eligibility, analyzing object tier status.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 Intelligent-Tiering configuration or tier transition events related to bucket `<bucket-name>`, checking for configuration changes.
7. Retrieve the S3 Bucket `<bucket-name>` Intelligent-Tiering monitoring configuration and verify monitoring period settings, checking if monitoring period affects tier transitions.
8. Retrieve CloudWatch metrics for S3 Intelligent-Tiering including TierTransitionCount if available and verify tier transition activity, checking if transitions are occurring.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 object access pattern changes or Intelligent-Tiering configuration modification events related to bucket `<bucket-name>` within the last 30 days, checking for access or configuration changes.

## Diagnosis

1. **Analyze CloudWatch Metrics and Storage Class Distribution from Step 4**: Review S3 storage metrics for tier distribution patterns. If CloudWatch metrics show BucketSizeBytes remaining static in the Frequent Access tier with no movement to Infrequent Access or Archive tiers, then transitions are not occurring. Compare metrics over 30 days - Intelligent-Tiering requires 30 consecutive days without access before transitioning to Infrequent Access tier. If objects are being accessed within the monitoring period, continue to step 2.

2. **Review S3 Access Logs from Step 3**: If server access logs from Step 3 show objects being accessed regularly (GET requests), then access patterns are resetting the transition timer. Objects must not be accessed for 30 days to move to Infrequent Access, 90 days for Archive Instant Access, and 180 days for Deep Archive. If access patterns meet thresholds but transitions still do not occur, continue to step 3.

3. **Verify Intelligent-Tiering Configuration from Step 2**: If Intelligent-Tiering configuration from Step 2 is not enabled on the bucket or specific objects, then data is not eligible for tier transitions. Check if objects have the INTELLIGENT_TIERING storage class - objects in STANDARD or other storage classes do not automatically transition. Verify archive access tier configurations from Step 7 are enabled if expecting Archive transitions. If configuration appears correct, continue to step 4.

4. **Check Object Tier Status from Step 5**: If object metadata from Step 5 shows objects in INTELLIGENT_TIERING but tier transitions are not occurring as expected, verify the object upload date. Objects must complete the monitoring period from their upload date, not from Intelligent-Tiering enablement date. If objects were recently transitioned to INTELLIGENT_TIERING storage class, they need to complete the full monitoring period.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show Intelligent-Tiering configuration modifications or access pattern changes within the monitoring period, then recent changes may have reset transition timers or altered eligibility.

**If no correlation is found**: Extend analysis to 180 days using object metadata from Step 5. Verify Archive Instant Access and Deep Archive Access tiers are enabled in the Intelligent-Tiering configuration from Step 7. Note that Intelligent-Tiering has minimum 30-day wait periods by design - if expecting faster transitions, consider lifecycle policies instead. Check object sizes - objects smaller than 128KB are not transitioned between access tiers.
