# CloudFormation Drift Detection Not Detecting Changes

## Meaning

CloudFormation drift detection is not detecting changes (triggering drift detection failures or CloudFormationDriftDetectionFailed alarms) because drift detection is not enabled, stack resources are not in drift detection scope, drift detection execution fails, IAM permissions are insufficient for drift detection, CloudFormation service encounters errors during drift detection, or CloudFormation stack resource types do not support drift detection. CloudFormation drift detection fails, infrastructure drift is not detected, and stack configuration drift goes unnoticed. This affects the infrastructure compliance and tracking layer and compromises infrastructure state tracking, typically caused by drift detection configuration issues, permission problems, or resource type limitations; if using CloudFormation with nested stacks or stack sets, drift detection behavior may differ and applications may experience drift detection failures.

## Impact

CloudFormation drift detection fails; infrastructure drift is not detected; stack configuration drift goes unnoticed; drift detection automation is ineffective; infrastructure compliance tracking fails; stack resource changes are not identified; drift detection alarms do not fire; infrastructure state tracking is compromised. CloudFormationDriftDetectionFailed alarms may fire; if using CloudFormation with nested stacks or stack sets, drift detection behavior may differ; applications may experience infrastructure compliance issues; infrastructure state tracking may be ineffective.

## Playbook

1. Verify CloudFormation stack `<stack-name>` exists and AWS service health for CloudFormation in region `<region>` is normal.
2. Retrieve the CloudFormation Stack `<stack-name>` in region `<region>` and inspect its drift detection status, stack resource configurations, and drift detection execution history, verifying drift detection is enabled.
3. Query CloudWatch Logs for log groups containing CloudFormation events and filter for drift detection failure patterns or drift detection execution errors related to stack `<stack-name>`, including error message details.
4. Retrieve CloudFormation stack drift detection results for stack `<stack-name>` and check drift status, detected drift details, and drift detection timestamps, analyzing drift detection results.
5. Retrieve the IAM role `<role-name>` used by CloudFormation for drift detection and inspect its policy permissions for resource configuration access, verifying IAM permissions.
6. List CloudFormation stack resources for stack `<stack-name>` and check resource drift status, resource configuration, and drift detection scope, verifying resource drift detection support.
7. Retrieve the CloudFormation Stack `<stack-name>` nested stack configuration if applicable and verify nested stack drift detection, checking if nested stacks affect drift detection.
8. Retrieve CloudWatch metrics for CloudFormation including drift detection execution counts and verify drift detection execution patterns, checking if drift detection is being executed.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudFormation drift detection enablement or IAM role policy modification events related to stack `<stack-name>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs from Step 3**: Review CloudFormation event logs for drift detection failure patterns. If CloudWatch Logs indicate "AccessDenied" or permission-related errors during drift detection, then IAM permission issues are the cause (proceed to Step 5). If logs show "Resource type not supported" errors, then certain resources cannot be checked for drift. If logs are inconclusive, continue to step 2.

2. **Check IAM Permissions from Step 5**: If drift detection involves reading resource configurations, verify the IAM role from Step 5 has permissions to describe the resources being tracked (e.g., `ec2:DescribeInstances`, `s3:GetBucketConfiguration`). If IAM role lacks resource-specific read permissions, then permission gaps prevent drift detection. If permissions appear correct, continue to step 3.

3. **Review Drift Detection Results from Step 4**: If drift detection results from Step 4 show "DETECTION_COMPLETE" but no drift detected when changes exist, verify the specific resources that were checked. If drift detection results show "IN_SYNC" for resources that were manually modified, then either the modifications are not to properties CloudFormation tracks, or drift detection scope is limited. Continue to step 4.

4. **Evaluate Resource Support from Step 6**: If stack resources from Step 6 include resource types that do not support drift detection (check AWS documentation for supported types), then those resources cannot be monitored for drift. If resources show "NOT_CHECKED" drift status, then they are explicitly excluded from drift detection scope. If all resources support drift detection, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show drift detection configuration changes or IAM role modifications within 30 minutes of drift detection failures, then recent changes affected drift detection capability. Review the specific changes to identify issues.

**If no correlation is found**: Extend analysis to 30 days using drift detection execution patterns from Step 8. For nested stacks from Step 7, verify each nested stack is individually checked for drift. Check CloudFormation service health from Step 1 and verify the drift detection operation was actually triggered. Review resource type limitations in AWS documentation.
