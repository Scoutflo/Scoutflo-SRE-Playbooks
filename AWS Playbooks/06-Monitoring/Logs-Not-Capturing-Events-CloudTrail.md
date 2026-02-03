# AWS CloudTrail Logs Not Capturing Events

## Meaning

CloudTrail logs fail to capture API events (triggering logging gaps or CloudTrailEventMissing alarms) because CloudTrail is not enabled, logging is turned off, S3 bucket policy blocks CloudTrail writes, IAM permissions are insufficient for CloudTrail operations, CloudTrail event selectors filter out events, CloudWatch Logs show gaps in event capture, or KMS key access prevents encrypted trail writes. API activity is not logged, audit trails are incomplete, and CloudTrail log files show gaps. This affects the security and compliance layer and compromises audit capabilities, typically caused by CloudTrail configuration issues, S3 permission problems, or KMS key access failures; if using AWS Organizations, organization trail configuration may affect event capture and Security Hub integration may show missing events.

## Impact

API activity is not logged; audit trails are incomplete; security monitoring fails; compliance requirements may be violated; CloudTrail log gaps occur; event history is missing; security investigations cannot proceed; API call tracking is lost; forensic analysis is impossible. CloudTrailEventMissing alarms fire; if using AWS Organizations, organization-wide audit trails are incomplete; Security Hub findings may be missing; applications may experience errors or performance degradation due to missing audit data for troubleshooting.

## Playbook

1. Verify CloudTrail trail `<trail-name>` exists and AWS service health for CloudTrail in region `<region>` is normal.
2. Retrieve the CloudTrail trail `<trail-name>` and verify CloudTrail is enabled and logging is turned on by checking trail status and IsLogging status, ensuring trail is in "ACTIVE" state.
4. Retrieve the S3 Bucket `<bucket-name>` bucket policy and check the policy allows CloudTrail to write logs, verifying bucket policy permissions.
5. Retrieve IAM permissions for CloudTrail service and validate IAM permissions include cloudtrail:PutEventSelectors and cloudtrail:UpdateTrail, checking service-linked role permissions.
6. Query CloudWatch Logs for log groups containing CloudTrail events from trail `<trail-name>` to identify potential gaps or issues with event capture, analyzing log delivery status.
7. Retrieve the CloudTrail trail `<trail-name>` event selectors and verify event selectors are not filtering out required events, checking selector configuration.
8. Retrieve the CloudTrail trail `<trail-name>` data events configuration and verify data events (S3, Lambda) are enabled if required, checking data event logging status.
9. Retrieve the CloudTrail trail `<trail-name>` KMS key configuration if trail is encrypted and verify KMS key policy allows CloudTrail to use the key, checking key access permissions.
10. Retrieve the CloudTrail trail `<trail-name>` organization trail configuration if using AWS Organizations and verify organization trail setup, checking member account event forwarding.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify CloudTrail service availability in the region. If service health indicates issues, event capture failures may be AWS-side requiring monitoring rather than configuration changes.

2. If trail status from Playbook step 2 shows IsLogging is false or trail is not in "ACTIVE" state, logging is disabled. The trail must be enabled for events to be captured. Check when logging was disabled.

3. If S3 bucket policy from Playbook step 4 does not allow CloudTrail to write logs (requires s3:PutObject permission for the CloudTrail service principal), log delivery fails silently. Verify the bucket policy explicitly allows CloudTrail writes.

4. If IAM permissions from Playbook step 5 show the CloudTrail service-linked role lacks required permissions, trail operations may fail. Verify cloudtrail:PutEventSelectors and cloudtrail:UpdateTrail permissions.

5. If CloudWatch Logs from Playbook step 6 show gaps in event delivery, identify the gap timestamps and correlate with configuration changes or S3 delivery failures.

6. If event selectors from Playbook step 7 filter out management events or exclude specific event sources, only matching events are captured. Verify event selectors include the required event types (ReadWriteType, Resources).

7. If data events from Playbook step 8 are not enabled for S3 or Lambda, data plane events are not captured. Data events require explicit configuration separate from management events.

8. If KMS key configuration from Playbook step 9 shows the trail uses encryption but the key policy does not allow CloudTrail to use the key, encrypted log delivery fails. Verify CloudTrail service principal in key policy.

9. If organization trail from Playbook step 10 is misconfigured, member accounts may not be forwarding events. Verify organization trail settings and member account enrollment.

If no correlation is found from the collected data: extend query timeframes to 24 hours, verify S3 bucket has sufficient capacity, check for S3 lifecycle policies that may delete or transition log files, and examine CloudWatch Logs integration configuration. Event capture failures may result from S3 bucket versioning issues, cross-region log delivery failures, or CloudTrail Insights configuration problems.

