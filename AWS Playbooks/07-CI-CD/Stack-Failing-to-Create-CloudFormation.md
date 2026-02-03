# CloudFormation Stack Failing to Create

## Meaning

A CloudFormation stack fails to create (triggering stack creation failures or CloudFormationStackCreationFailed alarms) because template syntax errors exist, IAM role permissions are insufficient, resource limits are exceeded, resource dependencies cannot be resolved, template validation fails during stack creation, or CloudFormation service quotas are reached. CloudFormation stacks cannot be created, infrastructure deployment fails, and stack creation is blocked. This affects the infrastructure as code layer and blocks deployments, typically caused by template errors, permission issues, or resource constraints; if using CloudFormation nested stacks or stack sets, configuration may differ and applications may experience deployment failures.

## Impact

CloudFormation stacks cannot be created; infrastructure deployment fails; stack creation is blocked; template validation errors occur; resource provisioning fails; infrastructure automation is interrupted; stack rollback occurs; deployment processes cannot complete. CloudFormationStackCreationFailed alarms may fire; if using CloudFormation nested stacks or stack sets, configuration may differ; applications may experience errors or performance degradation due to failed infrastructure deployments; infrastructure may remain undeployed.

## Playbook

1. Verify CloudFormation stack `<stack-name>` exists and AWS service health for CloudFormation in region `<region>` is normal.
2. Retrieve the CloudFormation Stack `<stack-name>` in region `<region>` and inspect its stack status, stack events, and failure reasons, analyzing failure details.
3. Query CloudWatch Logs for log groups containing CloudFormation events and filter for stack creation failure events, validation errors, or resource creation errors related to stack `<stack-name>`, including error messages.
4. Retrieve CloudFormation stack events for stack `<stack-name>` and check for resource creation failures, dependency resolution errors, or validation errors, analyzing event chronology.
5. Retrieve the IAM role `<role-name>` used by CloudFormation stack `<stack-name>` and inspect its policy permissions for resource creation operations, verifying IAM permissions.
6. Retrieve CloudFormation stack resources for stack `<stack-name>` and check resource creation status and failure reasons, verifying which resources failed.
7. Retrieve the CloudFormation Stack `<stack-name>` template and verify template syntax, checking for template validation errors.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudFormation stack template or parameter modification events related to stack `<stack-name>` within the last 24 hours, checking for template changes.
9. Retrieve CloudWatch metrics for CloudFormation including StackCreationFailures over the last 24 hours to identify stack creation failure patterns.

## Diagnosis

1. Analyze CloudFormation stack events (from Playbook step 2 and step 4) to identify which resource failed first and the exact failure reason. The first resource failure timestamp and error message establish the root cause.

2. If stack events show CREATE_FAILED with "Resource handler returned message" errors, examine the specific resource (from Playbook step 6). Resource-level failures indicate invalid resource properties or service-specific constraints.

3. If template inspection (from Playbook step 7) or CloudFormation events (from Playbook step 3) show validation errors, template syntax issues are preventing stack creation before resource provisioning begins.

4. If IAM role permissions (from Playbook step 5) were modified around the failure timestamp (check CloudTrail from Playbook step 8), missing permissions for creating specific resource types are the cause.

5. If stack events show dependency resolution failures, examine resource dependency chains in the template. Circular dependencies or missing DependsOn declarations cause ordering failures.

6. If CloudFormation metrics (from Playbook step 9) or stack events show resource limit errors, verify service quotas for the failing resource types. Account limits may be preventing resource creation.

7. If failures are intermittent rather than constant (from Playbook step 4 pattern analysis), transient issues like resource name conflicts or regional capacity constraints may be the cause.

If no correlation is found: extend analysis to 48 hours, review template parameter validation, check for nested stack configuration issues, verify stack set deployment conflicts, examine resource name uniqueness requirements, and review service quota limits.
