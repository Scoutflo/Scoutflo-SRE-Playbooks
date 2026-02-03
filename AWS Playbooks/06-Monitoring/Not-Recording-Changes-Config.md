# AWS Config Not Recording Changes

## Meaning

AWS Config is not recording changes (triggering configuration audit gaps or ConfigChangesNotRecorded alarms) because Config recorder is disabled, Config rules are not evaluating, delivery channel configuration is incorrect, IAM permissions are insufficient, Config service encounters errors during change detection, or Config recorder resource type recording scope excludes changed resources. AWS Config change detection fails, configuration change history is incomplete, and Config-based compliance fails. This affects the compliance and audit layer and compromises configuration tracking, typically caused by Config recorder issues, delivery channel problems, or permission failures; if using Config with multi-account or multi-region, recording behavior may differ and applications may experience configuration audit gaps.

## Impact

AWS Config change detection fails; configuration change history is incomplete; Config-based compliance fails; change tracking automation is ineffective; configuration audit trails are missing; Config rule evaluations fail; compliance requirements are not met; configuration change visibility is lost. ConfigChangesNotRecorded alarms may fire; if using Config with multi-account or multi-region, recording behavior may differ; applications may experience compliance issues; configuration audit trails may be incomplete.

## Playbook

1. Verify AWS Config recorder `<recorder-name>` exists and AWS service health for Config in region `<region>` is normal.
2. Retrieve the AWS Config Recorder `<recorder-name>` in region `<region>` and inspect its recording status, resource type recording configuration, and recorder enablement status, verifying recorder is recording.
3. Retrieve AWS Config Rules in region `<region>` and inspect rule evaluation status, rule compliance status, and rule configuration, verifying rules are configured.
4. Query CloudWatch Logs for log groups containing Config events and filter for change detection failure patterns or recording errors related to recorder `<recorder-name>`, including recording error details.
5. Retrieve the IAM role `<role-name>` used by AWS Config and inspect its policy permissions for Config operations and resource configuration access, verifying IAM permissions.
6. List AWS Config configuration items and check configuration item creation timestamps, change detection patterns, and resource recording status, analyzing configuration item creation.
7. Retrieve the AWS Config Delivery Channel `<delivery-channel-name>` configuration and verify delivery channel configuration, checking if delivery channel issues affect recording.
8. Retrieve CloudWatch metrics for AWS Config including ConfigurationItemsRecorded if available and verify configuration item recording patterns, checking if configuration items are being recorded.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for AWS Config recorder enablement or IAM role policy modification events related to recorder `<recorder-name>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs and Metrics from Steps 4 and 8**: Review Config event logs and recording metrics. If CloudWatch Logs from Step 4 show recorder errors or delivery failures, then configuration recording is encountering issues. If metrics from Step 8 show ConfigurationItemsRecorded at 0, then no changes are being captured. If some recording is occurring, continue to step 2.

2. **Check IAM Permissions from Step 5**: If Config recording requires reading resource configurations, verify the IAM role from Step 5 has `config:Put*` permissions and read permissions for all resource types being tracked. If CloudWatch Logs show "AccessDenied" errors, then permission issues prevent recording. If permissions appear correct, continue to step 3.

3. **Verify Recorder Status from Step 2**: If recorder status from Step 2 shows "Recording: false" or recorder is stopped, then recording was disabled. Check if resource type scope from Step 2 excludes the specific resource types that changed - if recording is limited to specific types, other changes will not be captured. If recorder is active, continue to step 4.

4. **Review Delivery Channel from Step 7**: If delivery channel from Step 7 shows S3 bucket is inaccessible or SNS topic delivery is failing, then configuration snapshots and change notifications are not being delivered. Verify S3 bucket exists and bucket policy allows Config service access. If delivery is working, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show recorder status changes or IAM role modifications within 5 minutes of recording stopping, then recent changes affected Config recording. Review the specific modifications to identify the issue.

**If no correlation is found**: Extend analysis to 30 days using configuration item data from Step 6. Verify the resources expected to be recorded are within the recorder's scope. For multi-account setups, verify aggregator configuration. Check Config service health from Step 1 and review whether resource types are supported by AWS Config.
