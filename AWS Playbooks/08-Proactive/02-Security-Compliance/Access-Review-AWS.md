# Access Review

## Meaning

Access review indicates that access permissions cannot be reviewed or excessive access permissions are detected (triggering alarms like ExcessiveAccessDetected or AccessReviewFailed) because access review tools fail, access permissions are not reviewed, excessive access permissions are detected, access review monitoring indicates problems, or access review configuration is missing. Access reviews show failures, access permissions are not reviewed, excessive access permissions are detected, and access review fails. This affects the compliance layer and access management, typically caused by access review configuration failures, access review tool failures, access permission analysis issues, or access review monitoring gaps; if access review affects container workloads, container access permissions may be excessive and applications may experience access management risks.

## Impact

ExcessiveAccessDetected alarms fire; AccessReviewFailed alarms fire; access permissions cannot be reviewed; excessive access permissions are detected; access management may be compromised; security risks may exist. Access reviews show failures; if access review affects container workloads, container access permissions may be excessive, pod access controls may be misconfigured, and container applications may experience access management risks; applications may experience access review gaps or security risks.

## Playbook

1. List IAM users in account `<account-id>` and retrieve IAM user policy configurations to identify users with excessive permissions or unused access.
2. List IAM roles in account `<account-id>` and retrieve IAM role policy configurations to identify roles with overly permissive policies or unused access.
3. Retrieve IAM access analyzer findings for account `<account-id>` and filter for findings indicating excessive access or unused permissions, checking access analyzer coverage.
4. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM policy modification events within the last 30 days to identify access permission changes.
5. Compare access review failure timestamps with IAM policy modification timestamps within 1 hour and verify whether policy modifications introduce excessive access, using IAM access analyzer findings as supporting evidence.
6. Retrieve IAM role last used timestamps and verify role usage patterns to identify unused roles with excessive permissions, checking role access usage.
7. List IAM policies in account `<account-id>` and verify policy compliance with least privilege principles and access review requirements, checking IAM policy access review coverage.
8. Compare access review analysis timestamps with IAM access analyzer finding timestamps within 1 hour and verify whether access reviews identify excessive access correctly, using IAM access analyzer findings as supporting evidence.

## Diagnosis

1. **Analyze IAM Access Analyzer findings from Step 3**: If findings indicate external access, prioritize remediation as resources are accessible outside the account. If findings indicate unused permissions, these can be removed safely. If findings indicate overly broad access, narrow to specific resources.

2. **Evaluate role usage from Step 2 and Step 6**: If roles have not been used in 90+ days, they are candidates for removal or privilege reduction. If roles are actively used but have excessive permissions, analyze actual API calls via CloudTrail to right-size permissions.

3. **Review user permissions from Step 1**: If users have direct policy attachments, consider using groups instead. If users have admin-level access, verify business justification. If users have unused permissions (no corresponding CloudTrail activity), remove those permissions.

4. **Cross-reference with recent changes from Step 4 and Step 5**: If excessive access was recently granted, identify who made the change and why. If access review findings correlate with policy changes, those changes introduced the issue.

5. **Assess policy compliance from Step 7**: If policies use wildcards for actions or resources, they violate least privilege. If policies lack conditions (MFA, IP restrictions), they may be overly permissive. If policies are overly complex, simplify for maintainability.

If the above analysis is inconclusive: Use IAM Access Analyzer policy generation to create right-sized policies based on CloudTrail activity. Review service control policies (SCPs) that may provide compensating controls. Check for cross-account access that may be intentional. Consider implementing just-in-time access for elevated privileges.
