# AWS STS Token Expired Error

## Meaning

AWS STS token expiration errors occur (triggering authentication failures or STSTokenExpired errors) because temporary credentials expire, IAM role session duration limits are reached, MFA token validation fails, role trust policy restricts session duration, token refresh mechanisms fail to renew credentials, or STS session policy limits reduce token validity. Temporary credentials expire, API calls fail with token expired errors, and applications lose access to AWS services. This affects the authentication and authorization layer and blocks service access, typically caused by session duration limits, token refresh failures, or trust policy restrictions; if using cross-account role assumption, session duration may be further restricted and applications may experience authentication failures.

## Impact

Temporary credentials expire; API calls fail with token expired errors; applications lose access to AWS services; role assumption fails; session-based access is denied; authentication errors occur; service-to-service communication fails; automated processes cannot authenticate. STSTokenExpired errors may fire; if using cross-account role assumption, session duration restrictions may be more strict; applications may experience errors or performance degradation due to authentication failures; automated workflows may break due to credential expiration.

## Playbook

1. Verify IAM role `<role-name>` exists and AWS service health for STS and IAM in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for STS AssumeRole or GetSessionToken events with error patterns indicating token expiration, including expiration error details.
3. Retrieve the IAM role `<role-name>` used for STS token generation and inspect its trust policy, session duration settings, and maximum session duration configuration, verifying session duration limits.
4. Retrieve CloudWatch metrics for STS API calls including AssumeRole and GetSessionToken error rates over the last 1 hour to identify token expiration patterns, analyzing expiration frequency.
5. List IAM role sessions for role `<role-name>` and check session expiration timestamps and active session counts, verifying session duration.
6. Query CloudWatch Logs for log groups containing application logs and filter for STS token expiration error messages or authentication failure patterns, including expiration timestamps.
7. Retrieve the IAM role `<role-name>` trust policy and verify cross-account role assumption configuration if applicable, checking if cross-account restrictions affect session duration.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM role trust policy modification events related to role `<role-name>` within the last 24 hours, checking for session duration changes.
9. Retrieve CloudWatch metrics for STS API calls including AssumeRoleWithSAML or AssumeRoleWithWebIdentity if using SAML or OIDC, verifying token expiration patterns for different token types.

## Diagnosis

1. Analyze CloudTrail events (from Playbook step 2) to identify when STS token expiration errors first appeared. Compare AssumeRole or GetSessionToken error timestamps to establish the correlation baseline.

2. If IAM role configuration (from Playbook step 3) shows MaxSessionDuration, compare with application usage patterns. If applications hold sessions longer than configured duration, tokens expire as expected behavior requiring refresh.

3. If CloudTrail shows trust policy modifications (from Playbook step 8) around the error timestamp, verify whether trust policy changes restricted the session duration or added conditions preventing token issuance.

4. If STS API call metrics (from Playbook step 4) show errors across multiple roles, the issue may be account-wide (STS service issue) or application-wide (refresh logic failure). If errors are role-specific, the issue is role configuration.

5. If expiration patterns (from Playbook step 6) show consistent timing aligned with session duration limits, the application is not refreshing tokens before expiration. If patterns are irregular, refresh mechanism failures are the cause.

6. If cross-account role assumption is involved (from Playbook step 7), verify trust policy allows the assuming principal and check for session duration restrictions in cross-account scenarios.

7. If SAML or OIDC authentication metrics (from Playbook step 9) show errors around token expiration, identity provider token validity may be shorter than STS session duration.

If no correlation is found: extend analysis to 48 hours, review application token refresh logic implementation, check MFA device availability for MFA-protected sessions, verify STS session policy restrictions, and examine cross-account role assumption duration limits.
