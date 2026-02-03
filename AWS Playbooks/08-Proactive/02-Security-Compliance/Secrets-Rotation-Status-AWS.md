# Secrets Rotation Status

## Meaning

Secrets rotation status indicates that secrets rotation has not occurred according to schedule or rotation operations fail (triggering alarms like SecretsRotationFailed or SecretsRotationOverdue) because secrets rotation schedules are not met, rotation operations fail, rotation status shows overdue, rotation automation does not trigger, or rotation completion cannot be verified. Secrets show rotation overdue status, rotation operations show failed status, rotation schedules are not met, and rotation automation triggers do not activate. This affects the security layer and secrets management, typically caused by rotation automation failures, rotation schedule misconfigurations, rotation IAM permission issues, or rotation service unavailability; if secrets protect container workloads, container secret rotation may fail and applications may experience authentication failures.

## Impact

SecretsRotationFailed alarms fire; SecretsRotationOverdue alarms fire; secrets may become compromised; rotation schedules are not met; rotation automation fails; security policies are violated. Secrets rotation status shows overdue or failed; if secrets protect container workloads, container secret rotation may fail, pod secret updates may not occur, and container applications may experience authentication failures; applications may experience authentication failures or security risks from stale secrets.

## Playbook

1. List secrets in Secrets Manager in region `<region>` and retrieve secret rotation configuration and last rotation timestamp to identify secrets with overdue rotations.
2. Retrieve the Secrets Manager Secret `<secret-arn>` details and inspect its rotation configuration, last rotation timestamp, and rotation status, verifying rotation schedule compliance.
3. List RDS DB instances in region `<region>` with automatic password rotation enabled and verify rotation status and last rotation timestamp.
4. Query CloudWatch Logs for log groups containing Secrets Manager rotation events and filter for rotation failure patterns or rotation overdue warnings within the last 7 days.
5. Retrieve CloudWatch metrics for Secrets Manager service including RotationSuccessRate and RotationDuration over the last 30 days to identify rotation failure patterns.
6. Verify Secrets Manager rotation IAM role permissions by retrieving the IAM role `<role-name>` attached to secret rotation and checking its policy permissions, verifying rotation role access.
7. Compare secret rotation schedule timestamps with actual rotation completion timestamps and verify whether rotations occur according to schedule, using Secrets Manager secret data as supporting evidence.
8. Retrieve the Secrets Manager Secret `<secret-arn>` rotation Lambda function configuration and verify whether rotation automation is correctly configured, checking rotation function accessibility.

## Diagnosis

1. **Analyze rotation status from Step 1 and Step 2**: If secrets show "Rotation overdue" status, check last rotation timestamp. If rotation has never occurred, rotation may not be enabled. If rotation occurred previously but stopped, investigate Lambda function or IAM changes.

2. **Evaluate rotation Lambda function from Step 8**: If Lambda function does not exist or is misconfigured, rotation cannot occur. If function exists but is not invoked, the rotation schedule trigger is failing. If function is invoked but fails, examine CloudWatch Logs from Step 4 for specific errors.

3. **Review rotation logs from Step 4**: If logs show "access denied" errors, verify IAM role permissions from Step 6. If logs show "connection failed" errors, the Lambda function cannot reach the target database/service. If logs show "validation failed", the new secret value does not work.

4. **Cross-reference IAM permissions from Step 6**: If rotation role lacks permissions to Secrets Manager, rotation will fail. If rotation role lacks permissions to the target service (RDS, Redshift, etc.), secret update works but validation fails. If rotation role has no trust policy for Lambda, the function cannot assume the role.

5. **Assess CloudWatch metrics from Step 5**: If RotationSuccessRate is low, systemic issues exist. If RotationDuration is increasing, rotation Lambda function performance is degrading. If no metrics exist, rotation is not being attempted.

If the above analysis is inconclusive: Manually trigger rotation to test the process. Verify network connectivity from Lambda function to target service. Check for VPC configuration issues if Lambda is in a VPC. Review secret version stages to understand rotation state.
