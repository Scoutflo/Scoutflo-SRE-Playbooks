# AWS Config Not Recording Resource Changes

## Meaning

AWS Config is not recording resource changes (triggering configuration tracking gaps or ConfigResourceChangesNotRecorded alarms) because Config recorder is stopped, Config delivery channel is misconfigured, IAM permissions are insufficient for Config operations, resource types are not recorded, Config service encounters errors during change recording, or Config recorder resource type scope excludes resources. AWS Config resource changes are not recorded, configuration history is incomplete, and compliance tracking fails. This affects the compliance and audit layer and compromises resource change tracking, typically caused by Config recorder issues, delivery channel problems, or resource type scope limitations; if using Config with different resource types or delivery channels, recording behavior may differ and applications may experience configuration tracking gaps.

## Impact

AWS Config resource changes are not recorded; configuration history is incomplete; compliance tracking fails; Config-based analysis is unavailable; resource change visibility is lost; Config recording automation is ineffective; configuration audit trails are incomplete; compliance requirements are not met. ConfigResourceChangesNotRecorded alarms may fire; if using Config with different resource types or delivery channels, recording behavior may differ; applications may experience compliance issues; resource change tracking may be ineffective.

## Playbook

1. Verify AWS Config recorder `<recorder-name>` exists and AWS service health for Config in region `<region>` is normal.
2. Retrieve the AWS Config Recorder `<recorder-name>` in region `<region>` and inspect its recorder status, recording status, resource types recorded, and recording configuration, verifying recorder is recording.
3. Retrieve the AWS Config Delivery Channel `<delivery-channel-name>` in region `<region>` and inspect its delivery channel configuration, S3 bucket settings, and SNS topic settings, verifying delivery channel configuration.
4. Query CloudWatch Logs for log groups containing Config events and filter for recording failure patterns or delivery errors related to recorder `<recorder-name>`, including recording error details.
5. Retrieve the IAM role `<role-name>` used by AWS Config and inspect its policy permissions for Config operations and resource access, verifying IAM permissions.
6. List AWS Config configuration snapshots and check snapshot creation timestamps, snapshot completeness, and resource change recording patterns, analyzing snapshot creation.
7. Retrieve the AWS Config Recorder `<recorder-name>` resource type recording scope and verify resource types are included, checking if resource type scope excludes resources.
8. Retrieve CloudWatch metrics for AWS Config including ConfigurationItemsRecorded if available and verify configuration item recording patterns, checking if configuration items are being recorded.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for AWS Config recorder status or delivery channel modification events related to recorder `<recorder-name>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs and Metrics from Steps 4 and 8**: Review Config event logs and recording metrics for patterns. If CloudWatch Logs from Step 4 show delivery errors to S3 or SNS, then delivery channel issues are preventing recording. If metrics from Step 8 show ConfigurationItemsRecorded at 0, then no changes are being captured. If some recording is occurring, continue to step 2.

2. **Check IAM Permissions from Step 5**: If Config requires permissions to read resource configurations and write to delivery destinations, verify the IAM role from Step 5 has `config:Put*`, `s3:PutObject`, and resource-specific read permissions. If CloudWatch Logs show "AccessDenied" errors, then permission issues prevent recording. If permissions appear correct, continue to step 3.

3. **Verify Recorder and Recording Scope from Steps 2 and 7**: If recorder status from Step 2 shows "Recording: false", then the recorder is stopped. If resource type scope from Step 7 is limited to specific types and the changed resources are not included, then scope limitations prevent recording. Verify recording scope includes all resource types you need to track. If recorder is active, continue to step 4.

4. **Review Delivery Channel Configuration from Step 3**: If delivery channel from Step 3 shows S3 bucket is missing, bucket policy blocks access, or SNS topic is misconfigured, then configuration items cannot be delivered. Verify the S3 bucket exists and allows Config service access. If delivery is configured correctly, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show recorder status changes, delivery channel modifications, or IAM role changes within 5 minutes of recording stopping, then recent changes caused the issue. Review the specific modifications to identify the breaking change.

**If no correlation is found**: Extend analysis to 30 days using snapshot data from Step 6. Verify the resources you expect to be recorded are supported by AWS Config (check AWS documentation for supported resource types). For multi-region tracking, verify Config is enabled in all required regions. Check Config service health from Step 1.
