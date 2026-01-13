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

1. Compare GuardDuty detector enablement change timestamps with missing threat detection timestamps within 1 hour and verify whether detection failures began when GuardDuty was disabled, using GuardDuty configuration events as supporting evidence.
2. Correlate threat intelligence feed configuration change timestamps with detection gap timestamps and verify whether feed disablement reduced threat detection, using GuardDuty configuration events as supporting evidence.
3. Compare data source configuration change timestamps with monitoring gap timestamps within 1 hour and verify whether data source changes prevented log monitoring, using GuardDuty data source events as supporting evidence.
4. Compare suppression rule creation timestamps with missing finding timestamps within 1 hour and verify whether suppression rules hid legitimate threats, using GuardDuty suppression rule events as supporting evidence.
5. Analyze threat detection gap frequency over the last 24 hours to determine if gaps are constant (configuration issue) or intermittent (log source availability).

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including CloudWatch Logs containing CloudTrail events and VPC Flow Log configuration, check for gradual issues like log source degradation, verify external dependencies like log source permissions, examine historical patterns of GuardDuty threat detection, check for AWS Organizations member account configuration issues, verify Security Hub integration problems. Detection failures may result from log source configuration issues, log delivery failures, threat intelligence feed connectivity problems, GuardDuty cost optimization settings affecting detection, or member account configuration in AWS Organizations rather than immediate GuardDuty configuration changes.
