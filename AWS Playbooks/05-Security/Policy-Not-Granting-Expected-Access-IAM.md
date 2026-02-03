# IAM Policy Not Granting Expected Access

## Meaning

IAM policies fail to grant expected permissions (triggering access denied errors or IAMPolicyAccessDenied alarms) because policy JSON contains syntax errors, policies are not attached to correct users or roles, policy conditions block access, conflicting deny statements exist in other policies, service control policies override permissions, resource-based policies conflict with identity-based policies, or policy evaluation order affects access. Users and roles cannot access required resources, applications fail with permission errors, and CloudWatch Logs show access denied events. This affects the security and access control layer and blocks resource access, typically caused by policy configuration issues, evaluation order problems, or SCP restrictions; if using AWS Organizations, service control policies may override IAM policies and applications may experience permission errors.

## Impact

Users and roles cannot access required resources; applications fail with permission errors; service operations are blocked; access denied errors appear in CloudWatch Logs containing CloudTrail events; IAM policy evaluation fails; expected permissions are not effective; security policies prevent legitimate access; operational tasks cannot complete. IAMPolicyAccessDenied alarms fire; if using AWS Organizations, service control policies may override IAM policies; applications may experience errors or performance degradation due to permission failures; service-to-service communication may be blocked.

## Playbook

1. Verify IAM policy `<policy-name>` and user `<user-name>` or role `<role-name>` exist, and AWS service health for IAM in region `<region>` is normal.
2. Retrieve the IAM Policy `<policy-name>` and review the policy JSON for syntax errors, validate policy structure, verify the policy is attached to the correct user `<user-name>` or role `<role-name>`, and inspect policy conditions to verify they are not blocking access unintentionally, checking JSON syntax, policy version, attachment status, and condition operators and values.
3. List all IAM policies attached to user `<user-name>` or role `<role-name>` and check for conflicting deny statements in other policies, verifying policy evaluation order and explicit deny wins over allow.
4. Retrieve the IAM Policy `<policy-name>` resource ARN format and verify resource ARNs match exactly, checking ARN format and wildcards.
5. Retrieve the AWS Organizations service control policies (SCPs) if using Organizations and verify SCPs are not overriding IAM policy permissions, checking SCP restrictions.
6. Retrieve the resource-based policies for resources being accessed and verify resource-based policies allow access, checking policy evaluation with identity-based policies.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for access denied events related to the policy `<policy-name>` within the last 1 hour, including policy evaluation details.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify IAM service availability. IAM is a global service, so check for any AWS-wide service health issues.

2. If policy JSON from Playbook step 2 contains syntax errors, the policy is invalid and permissions are not applied. Common errors include missing commas, incorrect quotation marks, or invalid ARN formats.

3. If policy attachment status from Playbook step 2 shows the policy is not attached to the intended user or role, permissions are not in effect. Verify the policy is attached directly or via group membership.

4. If policy conditions from Playbook step 2 include restrictions (aws:SourceIp, aws:MultiFactorAuthPresent, aws:PrincipalTag) that are not satisfied by the request, conditional access is denying the operation.

5. If conflicting policies from Playbook step 3 contain explicit Deny statements for the requested action, the Deny overrides any Allow. IAM policy evaluation follows: explicit Deny wins, then explicit Allow, then implicit Deny.

6. If resource ARN format from Playbook step 4 does not match the actual resource ARN (e.g., missing region, wrong account ID, incorrect resource name), the policy does not apply to the intended resource.

7. If SCPs from Playbook step 5 restrict the action at the organization level, IAM permissions are overridden. SCPs set maximum permissions; IAM policies cannot grant permissions beyond SCP boundaries.

8. If resource-based policies from Playbook step 6 explicitly Deny the principal, or if cross-account access requires both identity-based and resource-based Allow, missing permissions on either side block access.

9. If CloudTrail events from Playbook step 7 show specific authorization failure context, use the error details to identify which policy (identity-based, resource-based, SCP, or permissions boundary) caused the denial.

If no correlation is found from the collected data: extend CloudTrail query timeframes to 1 hour, verify IAM policy size limits (2 KB for users, 5 KB for roles, 10 KB for managed policies), check for permissions boundaries restricting effective permissions, and examine session policies for assumed roles. Access failures may result from policy version issues, AWS managed policy updates, or trust policy misconfigurations.

