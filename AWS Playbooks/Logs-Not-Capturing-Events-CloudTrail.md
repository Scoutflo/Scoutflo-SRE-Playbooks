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

1. Compare CloudTrail trail status change timestamps with missing event timestamps within 5 minutes and verify whether event capture failures began when trail was disabled, using CloudTrail trail configuration data as supporting evidence.
2. Correlate logging configuration change timestamps with missing log timestamps and verify whether logging disablement caused events to stop being captured, using CloudTrail trail configuration data as supporting evidence.
3. Compare S3 bucket policy modification timestamps with CloudTrail write failure timestamps within 5 minutes and verify whether bucket policy changes blocked log writes, using S3 access events as supporting evidence.
4. Compare CloudTrail event selector modification timestamps with missing event timestamps within 5 minutes and verify whether event selector changes filtered out required events, using CloudTrail event selector configuration events as supporting evidence.
5. Analyze missing event frequency over the last 1 hour to determine if gaps are constant (configuration issue) or intermittent (permission or service issues).

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including S3 bucket access logs and CloudTrail delivery status, check for gradual issues like S3 bucket capacity, verify external dependencies like KMS key access for encrypted trails, examine historical patterns of CloudTrail event capture, check for AWS Organizations organization trail configuration issues, verify CloudTrail log file CloudWatch Logs integration problems. Event capture failures may result from S3 bucket capacity issues, KMS key access problems, CloudTrail service limitations, S3 lifecycle policy conflicts, or AWS Organizations member account configuration rather than immediate configuration changes.

