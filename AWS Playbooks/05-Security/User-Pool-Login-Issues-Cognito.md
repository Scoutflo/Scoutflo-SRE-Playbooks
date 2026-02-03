# AWS Cognito User Pool Login Issues

## Meaning

AWS Cognito User Pool login is failing (triggering authentication failures or CognitoLoginFailure alarms) because user credentials are incorrect, user account is disabled, MFA is required but not completed, user pool configuration is incorrect, Cognito service encounters errors during authentication, or Cognito user pool password policy prevents login. Cognito user pool login fails, user authentication is denied, and application access is blocked. This affects the authentication and identity management layer and blocks user access, typically caused by credential issues, MFA problems, or user pool configuration errors; if using Cognito with external identity providers, authentication flow may differ and applications may experience login failures.

## Impact

Cognito user pool login fails; user authentication is denied; application access is blocked; user login errors occur; MFA authentication fails; user pool authentication automation is ineffective; user experience is degraded; application authentication is compromised. CognitoLoginFailure alarms may fire; if using Cognito with external identity providers, authentication flow may differ; applications may experience errors or performance degradation due to blocked user access; user-facing authentication may fail.

## Playbook

1. Verify Cognito user pool `<user-pool-id>` exists and AWS service health for Cognito in region `<region>` is normal.
2. Retrieve the Cognito User Pool `<user-pool-id>` in region `<region>` and inspect its user pool configuration, authentication settings, MFA configuration, and user pool policies, verifying user pool is enabled.
3. Query CloudWatch Logs for log groups containing Cognito events and filter for authentication failure patterns, login errors, or user pool authentication errors, including error message details.
4. Retrieve CloudWatch metrics for Cognito User Pool `<user-pool-id>` including SignInSuccesses and SignInFailures over the last 24 hours to identify authentication patterns, analyzing authentication failure frequency.
5. List Cognito user pool users and check user status, account enablement, and authentication attempt patterns, verifying user account status.
6. Query CloudWatch Logs for log groups containing application logs and filter for Cognito authentication error messages or login failure patterns, including application error details.
7. Retrieve the Cognito User Pool `<user-pool-id>` password policy configuration and verify password policy settings, checking if password policy affects login.
8. Retrieve the Cognito User Pool `<user-pool-id>` MFA configuration and verify MFA settings, checking if MFA requirements affect authentication.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Cognito user pool configuration modification events related to pool `<user-pool-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs and Metrics from Steps 3 and 4**: Review Cognito authentication logs for specific error patterns. If CloudWatch Logs from Step 3 show "NotAuthorizedException" with "Incorrect username or password", then credential issues are the cause. If logs show "UserNotConfirmedException", then user verification is pending. If CloudWatch metrics from Step 4 show SignInFailures spiking across all users, then pool-wide configuration issues exist. If failures are user-specific, continue to step 2.

2. **Check User Account Status from Step 5**: If the user account from Step 5 shows status as "DISABLED", "FORCE_CHANGE_PASSWORD", or "RESET_REQUIRED", then account state is blocking login. Verify user confirmation status - if users are unconfirmed, then email/phone verification is incomplete. If account status is normal, continue to step 3.

3. **Evaluate MFA Configuration from Step 8**: If MFA is required per Step 8 but CloudWatch Logs show MFA-related errors like "CodeMismatchException" or "ExpiredCodeException", then MFA is causing failures. If users have not enrolled MFA devices but MFA is mandatory, then MFA enrollment gaps exist. If MFA is not the issue, continue to step 4.

4. **Review Password Policy from Step 7**: If password policy from Step 7 requires specific complexity and CloudWatch Logs show "InvalidPasswordException", then password requirements are not met. If password policy includes expiration and users have not updated passwords, then expired credentials are blocking access. If password policy is not the issue, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show user pool configuration modifications (authentication settings, app client settings, or Lambda triggers) within 5 minutes of login failures beginning, then recent changes caused the issue. Review specific modifications to identify the breaking change.

**If no correlation is found**: Extend analysis to 7 days using login failure patterns. If using external identity providers, verify SAML/OIDC configuration and identity provider availability. Check application logs from Step 6 for client-side authentication errors. Verify Cognito service health from Step 1 and review whether app client settings (OAuth scopes, callback URLs) are correctly configured.
