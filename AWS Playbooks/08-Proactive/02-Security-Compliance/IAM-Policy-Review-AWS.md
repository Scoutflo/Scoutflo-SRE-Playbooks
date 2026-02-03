# IAM Policy Review

## Meaning

IAM policy review indicates that IAM policies may be overly permissive, misconfigured, or violate least privilege principles (triggering alarms like OverlyPermissiveIAMPolicy or IAMPolicyAuditFailed) because IAM policies grant excessive permissions, unused IAM roles exist, IAM policies violate least privilege principles, IAM policy statements allow wildcard actions, or IAM policy conditions are missing or misconfigured. IAM policies show overly permissive statements, IAM policy audit findings indicate violations, unused IAM roles are detected, and IAM policy configurations violate security policies. This affects the security layer and access control, typically caused by misconfigured IAM policies, lack of IAM role lifecycle management, or security policy violations; if IAM policies protect container workloads, container service account permissions may be overly permissive and applications may experience security risks.

## Impact

IAMPolicyAuditFailed alarms fire; OverlyPermissiveIAMPolicy alarms fire; access permissions are overly permissive; security policies are violated; unused IAM roles consume resources; IAM policies violate least privilege principles. IAM policy configurations show overly permissive statements; if IAM policies protect container workloads, container service account permissions may be overly permissive, pod IAM role permissions may be misconfigured, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized access risks.

## Playbook

1. List IAM roles in account `<account-id>` and retrieve IAM role policy configurations to identify roles with overly permissive policies.
2. Retrieve the IAM Role `<role-name>` policy configuration and inspect its policy statements for wildcard actions or overly broad resource permissions, verifying policy restrictiveness.
3. List IAM users in account `<account-id>` and retrieve IAM user policy configurations to identify users with excessive permissions.
4. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM policy modification events within the last 7 days to identify policy changes.
5. Retrieve Security Hub findings for IAM compliance checks and filter for findings with severity 'HIGH' or 'CRITICAL' related to IAM policy misconfigurations.
6. List IAM roles in account `<account-id>` and verify role usage by checking CloudTrail events for role assumption activity over the last 90 days to identify unused roles.
7. Compare IAM policy modification timestamps with security policy violation timestamps within 24 hours and verify whether IAM policy changes violate security policies, using CloudWatch Logs containing CloudTrail events as supporting evidence.
8. Retrieve the IAM Role `<role-name>` last used timestamp and verify whether role has been used recently, checking role activity patterns.

## Diagnosis

1. **Analyze Security Hub findings from Step 5**: If HIGH/CRITICAL findings identify specific IAM policies, those policies require immediate remediation. If findings indicate wildcard actions ("*"), narrow permissions to specific actions. If findings indicate broad resource scope ("*"), restrict to specific resource ARNs.

2. **Evaluate unused roles from Step 6 and Step 8**: If roles have not been used in 90+ days, they are candidates for removal. If roles show recent creation but no usage, they may be unused or awaiting deployment. Cross-reference with role trust policies to understand intended use.

3. **Review recent policy changes from Step 4**: If overly permissive policies were recently modified, identify who made the change and why. If policy changes correlate with security violations from Step 7, the change introduced the vulnerability.

4. **Cross-reference role policies from Step 1 and Step 2**: If roles have inline policies with wildcards AND attached managed policies, permission scope is likely excessive. If roles are attached to many resources, impact of permission changes is broader.

5. **Assess user permissions from Step 3**: If users have admin-level policies, verify this is business-justified. If users have multiple policies with overlapping permissions, consolidate and simplify.

If the above analysis is inconclusive: Use IAM Access Analyzer to identify external access. Run IAM policy simulations to verify actual permission scope. Review service control policies (SCPs) that may constrain permissions. Check for permission boundaries that limit effective permissions.
