# CloudTrail Events Not Showing in Logs

## Meaning

CloudTrail events are not showing in logs (triggering audit trail gaps or CloudTrailEventsMissing alarms) because CloudTrail logging is stopped, log delivery to S3 or CloudWatch Logs fails, IAM permissions are insufficient for log delivery, log file delivery errors occur, CloudTrail trail configuration is incorrect, or CloudTrail log file integrity validation fails. CloudTrail events are missing from logs, audit trail is incomplete, and compliance requirements are not met. This affects the security and audit layer and compromises audit trail completeness, typically caused by CloudTrail configuration issues, delivery failures, or permission problems; if using CloudTrail with multiple trails or Organizations trails, log delivery behavior may differ and applications may experience audit trail gaps.

## Impact

CloudTrail events are missing from logs; audit trail is incomplete; compliance requirements are not met; security event visibility is lost; log-based analysis fails; CloudTrail log delivery fails; audit trail gaps occur; security monitoring is compromised. CloudTrailEventsMissing alarms may fire; if using CloudTrail with multiple trails or Organizations trails, log delivery behavior may differ; applications may experience compliance issues; security audit capabilities may be compromised.

## Playbook

1. Verify CloudTrail trail `<trail-name>` exists and AWS service health for CloudTrail in region `<region>` is normal.
2. Retrieve the CloudTrail Trail `<trail-name>` in region `<region>` and inspect its trail status, logging status, S3 bucket configuration, and CloudWatch Logs log group configuration, verifying trail is logging.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for log delivery failure patterns or missing event patterns related to trail `<trail-name>`, including delivery error details.
4. Retrieve the S3 Bucket `<bucket-name>` configured for CloudTrail trail `<trail-name>` and inspect bucket policy, log file delivery status, and bucket access permissions, verifying S3 bucket configuration.
5. Retrieve the IAM role `<role-name>` used by CloudTrail for log delivery and inspect its policy permissions for S3 and CloudWatch Logs operations, verifying IAM permissions.
6. List CloudTrail log files in S3 bucket `<bucket-name>` and check log file delivery timestamps, file sizes, and delivery patterns, analyzing log delivery.
7. Retrieve the CloudTrail Trail `<trail-name>` CloudWatch Logs log group configuration and verify log group configuration, checking if CloudWatch Logs delivery is configured correctly.
8. Retrieve CloudWatch metrics for CloudTrail including log file delivery if available and verify log delivery patterns, checking if log files are being delivered.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudTrail trail configuration or S3 bucket policy modification events related to trail `<trail-name>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs and Trail Status from Steps 3 and 2**: Review CloudTrail event delivery patterns. If CloudWatch Logs from Step 3 show no recent events, verify trail status from Step 2. If trail status shows "Logging: false" or trail is stopped, then logging was disabled. If trail shows delivery errors, then delivery configuration is the issue. If trail appears active, continue to step 2.

2. **Check IAM Permissions from Step 5**: If log delivery involves S3 or CloudWatch Logs, verify the IAM role from Step 5 has `s3:PutObject` permission on the destination bucket and `logs:PutLogEvents` for CloudWatch Logs integration. If CloudTrail logs show "AccessDenied" errors, then permission issues are blocking delivery. If permissions appear correct, continue to step 3.

3. **Verify S3 Bucket Configuration from Step 4**: If S3 bucket policy from Step 4 does not allow CloudTrail service (`cloudtrail.amazonaws.com`) to write objects, then bucket policy is blocking delivery. Verify the bucket exists and is accessible. If bucket policy blocks delivery or bucket was deleted, then S3 configuration is the root cause. If S3 is properly configured, continue to step 4.

4. **Review Log File Delivery from Step 6**: If log files in S3 from Step 6 show gaps in delivery timestamps, then intermittent delivery failures occurred. Check the most recent log file timestamp - if significantly older than expected (CloudTrail delivers approximately every 5 minutes for active trails), then delivery has stopped. Compare with CloudWatch metrics from Step 8 if available.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show trail configuration modifications, S3 bucket policy changes, or IAM role modifications within 5 minutes of log delivery stopping, then recent changes broke delivery. Review the specific modifications to identify the breaking change.

**If no correlation is found**: Extend analysis to 30 days using S3 access logs and CloudWatch Logs patterns. Verify CloudWatch Logs log group from Step 7 is correctly configured with proper retention. For Organizations trails, verify the organization trail is properly configured for member accounts. Check for CloudTrail log file integrity validation failures that might indicate tampering or corruption.
