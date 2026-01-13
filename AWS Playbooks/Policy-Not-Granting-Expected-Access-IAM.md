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

1. Compare IAM policy modification timestamps with access denied event timestamps within 2 minutes and verify whether access failures began shortly after policy changes, using IAM policy configuration data as supporting evidence.
2. Correlate policy attachment change timestamps with permission error timestamps and verify whether access failures occurred after policy attachment or detachment, using IAM attachment events as supporting evidence.
3. Compare policy condition modification timestamps with access failure timestamps within 5 minutes and verify whether condition changes blocked access, using policy evaluation logs as supporting evidence.
4. Compare service control policy modification timestamps with access failure timestamps within 5 minutes and verify whether SCPs override IAM policy permissions, using IAM policy evaluation data as supporting evidence.
5. Analyze access denied event frequency over the last 15 minutes to determine if failures are constant (policy configuration issue) or intermittent (conditional policy evaluation).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including resource-based policies and session policies, check for gradual issues like policy evaluation order, verify external dependencies like cross-account trust relationships, examine historical patterns of IAM access, check for IAM policy tag-based access control, verify IAM role permissions boundary restrictions. Access failures may result from policy evaluation order, session policy restrictions, resource-based policy conflicts, AWS Organizations SCP overrides, or IAM policy size limits rather than immediate IAM policy changes.
