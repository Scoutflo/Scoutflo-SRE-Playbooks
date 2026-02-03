# AWS Secrets Manager Not Rotating Credentials

## Meaning

AWS Secrets Manager is not rotating credentials (triggering rotation failures or SecretsManagerRotationFailed alarms) because rotation is not enabled, rotation Lambda function has errors, IAM permissions are insufficient for rotation, rotation schedule is misconfigured, rotation Lambda function cannot access the secret, or Secrets Manager rotation Lambda function encounters runtime errors. Secrets Manager credentials are not rotated automatically, credential rotation fails, and secret rotation automation is ineffective. This affects the security and credential management layer and compromises credential security, typically caused by rotation configuration issues, Lambda function problems, or permission failures; if using Secrets Manager with RDS, rotation behavior may differ and applications may experience credential rotation failures.

## Impact

Secrets Manager credentials are not rotated automatically; credential rotation fails; rotation schedules are not executed; secret rotation automation is ineffective; credential security is compromised; rotation Lambda function errors occur; rotation alarms fire; credential management fails. SecretsManagerRotationFailed alarms may fire; if using Secrets Manager with RDS, rotation behavior may differ; applications may experience errors or performance degradation due to expired credentials; credential security may be compromised.

## Playbook

1. Verify Secrets Manager secret `<secret-name>` exists and AWS service health for Secrets Manager and Lambda in region `<region>` is normal.
2. Retrieve the Secrets Manager Secret `<secret-name>` in region `<region>` and inspect its rotation configuration, rotation enabled status, rotation schedule, and rotation Lambda function ARN, verifying rotation is enabled.
3. Retrieve the Lambda Function `<function-name>` used for secret rotation and inspect its function code, execution role, and error logs, verifying function is configured.
4. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for rotation error patterns, permission errors, or rotation failure messages, including error details.
5. Retrieve the IAM role `<role-name>` attached to Lambda function `<function-name>` and inspect its policy permissions for Secrets Manager rotation operations, verifying IAM permissions.
6. List Secrets Manager rotation events for secret `<secret-name>` and check rotation status, failure reasons, and rotation attempt timestamps, analyzing rotation history.
7. Retrieve the Lambda Function `<function-name>` CloudWatch metrics including Errors and Invocations and verify function execution patterns, checking if function is being invoked.
8. Retrieve the Secrets Manager Secret `<secret-name>` rotation Lambda function configuration and verify Lambda function can access the secret, checking secret access permissions.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Secrets Manager rotation configuration or Lambda function modification events related to secret `<secret-name>` within the last 30 days, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs for the rotation Lambda function (from Playbook step 4) to identify specific rotation error messages. If errors indicate "AccessDenied", proceed immediately to IAM permission verification. If errors indicate database connection failures, check external connectivity. If errors indicate Lambda function code errors, review the function code.

2. For access-denied errors, verify IAM role permissions (from Playbook step 5) attached to the rotation Lambda function. The role must have permissions to call Secrets Manager APIs (secretsmanager:GetSecretValue, secretsmanager:PutSecretValue, secretsmanager:UpdateSecretVersionStage) and any service-specific permissions needed to rotate credentials (e.g., rds:ModifyDBInstance for RDS).

3. Review Lambda function metrics (from Playbook step 7) including Errors and Invocations to determine if the function is being invoked. If Invocations is zero, the rotation schedule may not be triggering. If Errors matches Invocations, every rotation attempt is failing.

4. Examine Secrets Manager rotation configuration (from Playbook step 2) to verify rotation is enabled, the rotation schedule is correct, and the Lambda function ARN is properly specified. If rotation is disabled or schedule is misconfigured, rotations will not occur.

5. Review rotation event history (from Playbook step 6) to identify rotation attempt patterns and failure reasons. If rotation attempts are occurring but failing consistently, focus on the specific failure reason. If no rotation attempts are recorded, the rotation schedule configuration is the issue.

6. Verify Lambda function can access the secret (from Playbook step 8) by checking if the function's IAM role has the required Secrets Manager permissions and if any resource policies on the secret restrict access.

7. Correlate CloudTrail events (from Playbook step 9) with rotation failure timestamps within 30 minutes to identify any rotation configuration or IAM policy modifications. If permission changes coincide with when rotations started failing, those changes are the likely cause.

8. Compare rotation failure patterns across different secrets within 24 hours. If failures are secret-specific, the issue is with that secret's rotation Lambda function or configuration. If failures affect all secrets using the same Lambda function, examine the Lambda function code or IAM permissions.

9. For database credential rotations, verify the Lambda function can connect to the database. If network connectivity (VPC configuration, security groups) prevents the Lambda function from reaching the database, rotation cannot complete.

If no correlation is found within the specified time windows: extend timeframes to 90 days, review alternative evidence sources including rotation Lambda function code and secret access patterns, check for gradual issues like Lambda function code errors or secret access permission changes, verify external dependencies like database connectivity for credential updates or external service availability, examine historical patterns of rotation failures, check for Secrets Manager rotation schedule configuration issues, verify Secrets Manager rotation Lambda function timeout settings. Rotation failures may result from Lambda function code errors, secret access permission issues, external service connectivity problems, Secrets Manager rotation schedule misconfiguration, or Secrets Manager rotation Lambda function timeout settings rather than immediate rotation configuration changes.
