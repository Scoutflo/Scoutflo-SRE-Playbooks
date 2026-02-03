# AWS Organizations SCP Preventing Service Access

## Meaning

AWS Organizations Service Control Policy (SCP) is preventing service access (triggering access denied errors or OrganizationsSCPAccessDenied alarms) because SCP policy denies required service actions, SCP policy conditions are too restrictive, SCP policy is attached to incorrect organizational unit, SCP policy evaluation blocks legitimate access, or SCP policy syntax has errors. AWS Organizations SCP blocks service access, service operations are denied, and access denied errors occur. This affects the governance and access control layer and blocks service operations, typically caused by SCP policy misconfiguration, condition threshold issues, or OU attachment problems; if using Organizations with multiple OUs, SCP hierarchy may affect access and applications may experience service access failures.

## Impact

AWS Organizations SCP blocks service access; service operations are denied; SCP policy restrictions prevent legitimate access; access denied errors occur; service automation is blocked; organizational policy enforcement is too aggressive; service access is incorrectly restricted. OrganizationsSCPAccessDenied alarms may fire; if using Organizations with multiple OUs, SCP hierarchy may affect access; applications may experience errors or performance degradation due to blocked service access; service operations may be completely blocked.

## Playbook

1. Verify AWS Organizations SCP `<scp-id>` exists and AWS service health for Organizations in region `<region>` is normal.
2. Retrieve the AWS Organizations Service Control Policy `<scp-id>` and inspect its policy document, policy attachments, organizational unit associations, and policy conditions, verifying policy syntax.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for access denied events, SCP policy evaluation patterns, or service access failures related to SCP `<scp-id>`, including access denied details.
4. Retrieve the AWS Organizations Organizational Unit `<ou-id>` where SCP `<scp-id>` is attached and inspect OU structure, account associations, and SCP policy hierarchy, verifying SCP attachment configuration.
5. List AWS service API calls that were denied by SCP `<scp-id>` and check denied action patterns, service patterns, and account patterns, analyzing denial patterns.
6. Retrieve the AWS Organizations SCP `<scp-id>` policy evaluation order and verify policy evaluation hierarchy, checking if multiple SCPs affect evaluation.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for SCP policy modification events or policy attachment changes related to SCP `<scp-id>` within the last 24 hours, checking for configuration changes.
8. Retrieve CloudWatch metrics for AWS Organizations if available and verify Organizations service health, checking if service issues affect SCP evaluation.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for organizational unit structure modification events related to OU `<ou-id>` within the last 24 hours, checking for OU changes.

## Diagnosis

1. **Analyze CloudTrail Events from Step 3**: Review CloudTrail logs for access denied events and SCP policy evaluation patterns. If CloudTrail shows "AccessDenied" with "Organizations" or "SCP" in the error context, then SCP is actively blocking the action. Identify the specific denied action and resource from the logs. If access denied patterns are unclear, continue to step 2.

2. **Evaluate SCP Policy Document from Step 2**: If the SCP policy from Step 2 contains explicit "Deny" statements matching the blocked service actions identified in Step 3, then the policy configuration is causing the restriction. Check policy conditions - if conditions like `aws:RequestedRegion`, `aws:PrincipalOrgID`, or IP restrictions are present, verify if the request context matches the condition requirements. If policy appears correct, continue to step 3.

3. **Check SCP Attachment and OU Hierarchy from Step 4**: If the SCP is attached to an OU that should not have this restriction, then incorrect attachment is the issue. Review OU structure from Step 4 - if the affected account is in an OU with restrictive SCPs inherited from parent OUs, then policy hierarchy is causing cumulative restrictions. Compare with CloudTrail events from Step 9 - if OU structure modifications occurred within 1 hour of access denials, then recent OU changes affected policy application.

4. **Correlate with Policy Modification Events from Step 7**: If CloudTrail events from Step 7 show SCP policy modifications within 5 minutes of access denial onset, then recent policy changes introduced the restriction. Review the policy version before and after modification to identify the specific change that caused the denial.

5. **Analyze Policy Evaluation Order from Step 6**: If multiple SCPs are attached at different levels (root, OU, account), evaluate the combined effective permissions. If the effective policy evaluation results in denial due to missing explicit "Allow" in any SCP in the hierarchy, then the policy inheritance model is causing the restriction.

**If no correlation is found**: Extend analysis to 30 days using CloudTrail patterns from Step 3. Check for SCP policy condition evaluation issues where conditions are too restrictive. Verify Organizations service health from Step 8 and examine whether policy syntax errors in Step 2 are preventing proper evaluation. Review SCP policy hierarchy conflicts where multiple overlapping SCPs create unintended restrictions.
