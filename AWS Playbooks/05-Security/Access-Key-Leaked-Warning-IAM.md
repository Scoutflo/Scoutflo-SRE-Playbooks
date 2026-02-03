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

1. Analyze GuardDuty findings and Security Hub alerts from Playbook steps 5-6 to identify when credential compromise was first detected. The finding timestamp provides the baseline for correlation with all other events.

2. If GuardDuty shows IAMAccessKeyExposed or UnauthorizedAccess findings, examine the CloudTrail events from Playbook step 2 for the specific API calls made using the compromised key. The event timestamps and source IP addresses indicate the scope of unauthorized access.

3. If CloudTrail events from Playbook step 2 show API calls from unexpected geographic locations or IP addresses, correlate these with the access key last used information from Playbook step 1 to confirm unauthorized usage patterns.

4. If MFA configuration from Playbook step 3 shows MFA is not enforced for the affected user, check CloudTrail events for credential-based access that bypassed MFA requirements. This indicates whether MFA gaps enabled the compromise.

5. If IAM policies from Playbook step 4 show excessive permissions, examine CloudTrail events for resource modifications that exploited overly permissive access. Events showing cross-service access or administrative actions indicate privilege escalation.

6. If Secrets Manager or Parameter Store logs from Playbook step 9 show access key retrieval, verify whether stored credentials were accessed by unauthorized principals before the key was used maliciously.

7. Analyze the frequency and pattern of suspicious API calls to determine if activity is constant (ongoing automated compromise) or intermittent (targeted manual attacks requiring immediate containment).

If no correlation is found from the collected data: extend CloudTrail query timeframes to 7 days, review IAM Access Analyzer findings from Playbook step 7 for external access attempts, check for keys exposed in CI/CD pipeline configurations or environment variables, and examine cross-account access patterns from Playbook step 8. Security breaches may result from credential sharing, third-party service compromises, social engineering, or keys stored insecurely rather than direct key exposure.
