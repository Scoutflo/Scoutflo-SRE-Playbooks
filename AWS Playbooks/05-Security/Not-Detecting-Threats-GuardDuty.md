# AWS GuardDuty Not Detecting Threats

## Meaning

GuardDuty fails to detect security threats (triggering security monitoring gaps or GuardDutyFindingMissing alerts) because GuardDuty is not enabled, threat intelligence feeds are disabled, CloudTrail, VPC Flow Logs, or DNS logs are not being monitored, GuardDuty findings are filtered out, IAM permissions prevent GuardDuty from accessing necessary logs, or GuardDuty suppression rules hide findings. GuardDuty findings are missing or suppressed, security monitoring shows gaps, and CloudWatch Logs indicate GuardDuty data source issues. This affects the security monitoring layer and compromises threat detection, typically caused by configuration issues, data source problems, or finding suppression; if using AWS Organizations, member account configuration may affect detection and Security Hub integration may show missing findings.

## Impact

Security threats go undetected; security monitoring is ineffective; GuardDuty findings are missing; security alerts do not fire; threat detection gaps occur; security investigations cannot identify threats; compliance monitoring fails; malicious activity may go unnoticed; security posture is compromised. GuardDutyFindingMissing alerts fire; Security Hub findings are incomplete; if using AWS Organizations, organization-wide threat detection is compromised; security compliance requirements may be violated; applications may experience security-related errors or performance issues due to undetected threats.

## Playbook

1. Verify GuardDuty detector `<detector-id>` exists and AWS service health for GuardDuty in region `<region>` is normal.
2. Retrieve the GuardDuty Detector `<detector-id>` configuration and verify GuardDuty is enabled by checking detector status, ensuring detector is in "ENABLED" state.
3. Retrieve the GuardDuty Detector `<detector-id>` settings and check if threat intelligence feeds are enabled, verifying threat intelligence feed status.
4. Retrieve the GuardDuty Detector `<detector-id>` data source configuration and verify CloudTrail, VPC Flow Logs, and DNS logs are being monitored, checking data source status for each source.
5. Retrieve the GuardDuty Detector `<detector-id>` suppression rules and verify suppression rules are not hiding legitimate threat findings, checking rule criteria and scope.
6. Retrieve the IAM role `<role-name>` for GuardDuty service and check IAM permissions for GuardDuty to access necessary logs, verifying service-linked role permissions.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for GuardDuty API call failures, Security Hub integration errors, or configuration errors related to detector `<detector-id>`.
8. Retrieve the GuardDuty Detector `<detector-id>` feature enablement status and verify S3 Protection, EKS Protection, RDS Protection, and Malware Protection features are enabled if applicable.
9. Verify if using AWS Organizations and check GuardDuty member account configuration, verifying organization-wide GuardDuty setup.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify GuardDuty service availability in the region. If service health indicates issues, detection gaps may be AWS-side requiring monitoring rather than configuration changes.

2. If detector status from Playbook step 2 shows GuardDuty is not in "ENABLED" state, the detector was disabled and threat detection stopped at the state change timestamp. Re-enable immediately.

3. If threat intelligence feed status from Playbook step 3 shows feeds are disabled, correlate the disablement timestamp with when detection gaps began. Disabled feeds reduce detection coverage for known malicious indicators.

4. If data source configuration from Playbook step 4 shows CloudTrail, VPC Flow Logs, or DNS logs are not being monitored, examine CloudTrail events from Playbook step 7 for the data source configuration change. Missing data sources create blind spots in specific detection categories.

5. If suppression rules from Playbook step 5 contain overly broad criteria, review rule creation timestamps to determine if legitimate findings are being suppressed. Rules matching large IP ranges or common event types may hide real threats.

6. If IAM permissions from Playbook step 6 show the GuardDuty service-linked role lacks required permissions, correlate permission changes with detection failures. Missing log access permissions prevent GuardDuty from analyzing security data.

7. If feature enablement from Playbook step 8 shows S3 Protection, EKS Protection, RDS Protection, or Malware Protection are disabled, detection is limited to enabled features only.

8. If using AWS Organizations (Playbook step 9), verify member account GuardDuty configuration. Misconfigured member accounts will not forward findings to the administrator account.

If no correlation is found from the collected data: extend CloudTrail query timeframes to 7 days, review Security Hub integration status, check for log delivery failures in data sources, and examine GuardDuty cost optimization settings that may affect detection frequency. Detection failures may result from log source delivery issues, threat intelligence connectivity problems, or organization-wide configuration inconsistencies.

