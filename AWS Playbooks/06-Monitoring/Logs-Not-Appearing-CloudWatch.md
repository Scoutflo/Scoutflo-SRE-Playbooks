# CloudWatch Logs Not Appearing

## Meaning

CloudWatch Logs are not appearing (triggering log visibility gaps or CloudWatchLogsMissing alarms) because log group does not exist, IAM permissions are insufficient for log creation, log retention period expires, log stream creation fails, CloudWatch Logs service encounters errors during log ingestion, or CloudWatch Logs log group quota limits are reached. CloudWatch Logs are missing, log-based debugging fails, and log visibility is compromised. This affects the monitoring and observability layer and reduces troubleshooting capabilities, typically caused by permission issues, log group configuration problems, or service constraints; if using CloudWatch Logs with log insights or subscriptions, log behavior may differ and applications may experience log visibility issues.

## Impact

CloudWatch Logs are missing; log-based debugging fails; log visibility is compromised; log streams are not created; application logs are not collected; log-based monitoring is ineffective; troubleshooting capabilities are reduced; log retention policies cannot be applied. CloudWatchLogsMissing alarms may fire; if using CloudWatch Logs with log insights or subscriptions, log behavior may differ; applications may experience reduced observability; troubleshooting may be significantly impaired.

## Playbook

1. Verify CloudWatch Logs access and AWS service health for CloudWatch Logs in region `<region>` is normal.
2. Query CloudWatch Logs for log groups matching expected log group patterns and check if log groups exist and are accessible, verifying log group existence.
3. Retrieve the IAM role `<role-name>` or IAM user `<user-name>` used for log publishing and inspect its policy permissions for CloudWatch Logs operations including CreateLogGroup, CreateLogStream, and PutLogEvents, verifying IAM permissions.
4. Query CloudWatch Logs for log groups containing application logs and filter for log publishing errors or PutLogEvents API call failures, including publishing error details.
5. Retrieve CloudWatch metrics for CloudWatch Logs including IncomingLogEvents and IncomingBytes over the last 24 hours to identify log ingestion patterns, analyzing log ingestion.
6. List CloudWatch log groups and check log group configurations, retention settings, and log stream creation patterns, verifying log group configuration.
7. Retrieve CloudWatch Logs log group quota limits and verify quota usage, checking if quota limits prevent log ingestion.
8. Retrieve CloudWatch metrics for CloudWatch Logs including ThrottledLogEvents if available and verify log throttling patterns, checking if throttling affects log ingestion.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudWatch Logs log group or IAM policy modification events within the last 24 hours, checking for configuration changes.

## Diagnosis

1. **Check IAM Permissions from Step 3 First**: If log publishing requires IAM permissions, verify the IAM role or user from Step 3 has `logs:CreateLogGroup`, `logs:CreateLogStream`, and `logs:PutLogEvents` permissions. If CloudTrail events show "AccessDenied" for CloudWatch Logs API calls, then permission issues are blocking log delivery. If permissions appear correct, continue to step 2.

2. **Analyze CloudWatch Metrics from Step 5**: Review log ingestion metrics for delivery patterns. If CloudWatch metrics show IncomingLogEvents at 0 for the expected log group, then no logs are being received. If metrics show throttling from Step 8, then quota limits are affecting ingestion. Compare with expected log volume to identify gaps. If metrics show some logs arriving, continue to step 3.

3. **Verify Log Group Existence from Steps 2 and 6**: If log groups from Step 2 do not exist, then log group creation failed or log group was deleted. Check if application is configured to create log groups automatically or if IAM permissions include CreateLogGroup. If log group exists but shows no recent streams, then log stream creation is failing. Continue to step 4.

4. **Check Quota Limits from Step 7**: If quota limits from Step 7 show log group count or PutLogEvents rate limits are reached, then quota exhaustion is preventing new logs. Check if account has requested quota increases for high-volume logging. If quotas are not the issue, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show log group deletion, IAM policy modifications, or retention policy changes within 1 hour of logs disappearing, then recent changes caused the issue. If retention policy was set to a short period, logs may have been automatically deleted.

**If no correlation is found**: Extend analysis to 30 days using log ingestion patterns. Verify the application is correctly configured to send logs to CloudWatch (agent configuration, SDK setup). Check for network connectivity issues if applications run in VPCs without CloudWatch Logs VPC endpoints. Review log group subscription filters that might be consuming logs.
