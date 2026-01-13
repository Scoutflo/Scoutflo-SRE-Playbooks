# AWS Access Key Leaked Warning

## Meaning

AWS access keys are potentially leaked or compromised (triggering security alerts like IAMAccessKeyExposed or GuardDuty findings) because access keys are exposed in public repositories, keys are used from unauthorized locations, CloudWatch Logs containing CloudTrail events show suspicious API calls, MFA is not enforced, or security policies allow excessive permissions. CloudTrail logs show API calls from unexpected geographic locations or IP addresses, access key usage patterns indicate unauthorized access, and Security Hub or GuardDuty findings identify compromised credentials. This affects the security layer and indicates credential compromise, typically caused by key exposure, unauthorized access, or insufficient security controls; compromised keys may be used in CI/CD pipelines, exposed in environment variables, or stored insecurely in AWS Secrets Manager or Parameter Store.

## Impact

Security breach risk increases; unauthorized access may occur; compromised credentials can be used maliciously; IAMAccessKeyExposed or GuardDuty findings fire; account security is compromised; sensitive data may be accessed; resource modifications may occur; compliance violations may result; immediate credential rotation is required. CloudTrail logs show suspicious API calls from unexpected locations; unauthorized resource access occurs; data exfiltration may happen; service modifications are made without authorization; if keys are used in CI/CD pipelines, automated deployments may be compromised; applications may experience errors or performance degradation due to unauthorized changes.

## Playbook

1. Verify access key `<access-key-id>` exists and retrieve the IAM Access Key `<access-key-id>` status and last used information, checking last used timestamp and location.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for suspicious API calls associated with access key `<access-key-id>` within the last 24 hours, including geographic location analysis.
3. Retrieve IAM user `<user-name>` MFA configuration and verify MFA enforcement status for all users.
4. Retrieve IAM policies attached to user `<user-name>` and review security policies for excessive permissions.
5. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Security Hub or GuardDuty findings related to access key `<access-key-id>` or user `<user-name>`, checking security service integration logs.
6. Query CloudWatch Logs for log groups containing GuardDuty logs if available and filter for credential compromise findings related to access key `<access-key-id>`, checking GuardDuty detection logs.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM Access Analyzer findings or external access attempts related to user `<user-name>` or access key `<access-key-id>`, checking access analysis logs.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for cross-account access attempts using access key `<access-key-id>`.
9. Query CloudWatch Logs for log groups containing Secrets Manager or Systems Manager Parameter Store logs and filter for access key usage related to user `<user-name>`, checking for stored credentials that may need rotation.

## Diagnosis

1. Compare access key creation or exposure timestamps with suspicious API call timestamps within 24 hours and verify whether suspicious activity began after key exposure, using CloudWatch Logs containing CloudTrail events as supporting evidence.
2. Correlate access key usage location timestamps with unauthorized access attempt timestamps and verify whether access occurred from unexpected geographic locations, using CloudWatch Logs containing CloudTrail event source IP addresses as supporting evidence.
3. Compare MFA enforcement change timestamps with unauthorized access timestamps within 1 hour and verify whether lack of MFA enabled unauthorized access, using IAM configuration data as supporting evidence.
4. Compare permission policy modification timestamps with unauthorized resource access timestamps within 1 hour and verify whether excessive permissions enabled broader unauthorized access, using CloudWatch Logs containing CloudTrail resource modification events as supporting evidence.
5. Analyze suspicious API call frequency over the last 24 hours to determine if activity is constant (ongoing compromise) or intermittent (targeted attacks).

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including GuardDuty findings and Security Hub alerts, check for gradual issues like credential sharing, verify external dependencies like third-party service access, examine historical patterns of access key usage, check for keys exposed in environment variables or CI/CD pipeline configurations. Security breaches may result from credential sharing, third-party service compromises, social engineering, or keys stored insecurely in Secrets Manager or Parameter Store rather than immediate access key exposure.
