# MFA Authentication Failing for IAM User

## Meaning

MFA authentication fails for IAM users (triggering authentication errors or IAMMFAFailure alarms) because MFA device is not configured, MFA token is invalid or expired, MFA device is lost or unregistered, IAM policy requires MFA but device is missing, MFA token validation service encounters errors, or device time synchronization issues cause token mismatches. IAM users cannot authenticate, access to AWS services is denied, and MFA-required operations fail. This affects the authentication and authorization layer and blocks user access, typically caused by MFA device configuration issues, token validation problems, or policy misconfiguration; if using hardware MFA devices, device issues may affect authentication and applications may experience user access failures.

## Impact

IAM users cannot authenticate; access to AWS services is denied; MFA-required operations fail; user login attempts are blocked; authentication errors occur; IAM user sessions cannot be established; MFA-protected resources are inaccessible; user access is completely blocked. IAMMFAFailure alarms may fire; if using hardware MFA devices, device battery or time sync issues may cause failures; applications may experience errors or performance degradation due to blocked user access; user-facing services may become inaccessible.

## Playbook

1. Verify IAM user `<user-name>` exists and AWS service health for IAM in region `<region>` is normal.
2. Retrieve the IAM User `<user-name>` and inspect its MFA device configuration, MFA device status, and MFA-enabled status, verifying MFA device is active.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for MFA authentication failure events related to user `<user-name>`, including authentication attempt patterns.
4. Retrieve IAM user login attempts for user `<user-name>` and check for MFA authentication failure patterns or error messages, analyzing failure reasons.
5. List IAM policies attached to user `<user-name>` and check for MFA requirement conditions in policy statements, verifying policy condition syntax.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for MFA device registration or deletion events for user `<user-name>`, checking device lifecycle events.
7. Retrieve the IAM User `<user-name>` MFA device serial number or virtual MFA device ARN and verify device status, checking if device is synchronized.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM policy modification events related to user `<user-name>` within the last 24 hours, checking for MFA requirement changes.
9. Retrieve CloudWatch metrics for IAM authentication attempts including MFA failure rates over the last 1 hour to identify authentication failure patterns.

## Diagnosis

1. Analyze CloudTrail events (from Playbook step 3 and step 4) to identify when MFA authentication failures first appeared. This timestamp establishes the correlation baseline for root cause analysis.

2. If CloudTrail shows MFA device deletion events (from Playbook step 6) around the failure timestamp, the device was removed while IAM policies still require MFA, causing authentication failures.

3. If IAM policies (from Playbook step 5) show MFA condition requirements but user MFA configuration (from Playbook step 2) shows no active device, the policy requires MFA but no device is configured or enabled.

4. If MFA device is configured and active (from Playbook step 2) but failures persist, check device serial number and sync status (from Playbook step 7). Time synchronization issues between device and AWS cause token validation failures.

5. If failures affect multiple users (from CloudTrail analysis in Playbook step 3), check for account-wide patterns. If only specific users are affected, the issue is user-specific (device or policy). If widespread, MFA service availability may be the cause.

6. If IAM policy modification events in CloudTrail (from Playbook step 8) show recent MFA requirement additions, verify users have properly configured MFA devices before policy enforcement.

7. If failure frequency shows intermittent patterns rather than constant failures (from Playbook step 9), token timing issues or temporary service availability problems are likely causes.

If no correlation is found: extend analysis to 48 hours, review hardware MFA device battery status, check virtual MFA application time synchronization, verify MFA service health status, and examine IAM policy condition evaluation logic for edge cases.
