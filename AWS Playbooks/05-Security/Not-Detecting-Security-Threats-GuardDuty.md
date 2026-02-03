# GuardDuty Not Detecting Security Threats

## Meaning

GuardDuty is not detecting security threats (triggering threat detection failures or GuardDutyThreatDetectionFailed alarms) because GuardDuty is not enabled, GuardDuty detector is disabled, data sources are not configured, IAM permissions are insufficient, GuardDuty service encounters errors during threat analysis, or GuardDuty threat intelligence feeds are not updated. GuardDuty threat detection fails, security threats are not identified, and threat-based alerts do not fire. This affects the security and threat detection layer and compromises security monitoring, typically caused by GuardDuty configuration issues, data source problems, or detector status issues; if using GuardDuty with multiple accounts or Regions, detection behavior may differ and applications may experience threat detection failures.

## Impact

GuardDuty threat detection fails; security threats are not identified; threat-based alerts do not fire; security monitoring is compromised; threat detection automation is ineffective; security incident detection is delayed; GuardDuty findings are not generated; security posture visibility is lost. GuardDutyThreatDetectionFailed alarms may fire; if using GuardDuty with multiple accounts or Regions, detection behavior may differ; applications may experience reduced security monitoring; security threat detection may be ineffective.

## Playbook

1. Verify GuardDuty detector `<detector-id>` exists and AWS service health for GuardDuty in region `<region>` is normal.
2. Retrieve the GuardDuty Detector `<detector-id>` in region `<region>` and inspect its detector status, enablement status, and data source configurations, verifying detector is enabled.
3. Query CloudWatch Logs for log groups containing GuardDuty events and filter for threat detection failure patterns or detector error messages, including detection error details.
4. Retrieve CloudWatch metrics for GuardDuty Detector `<detector-id>` including FindingsGenerated over the last 7 days to identify threat detection patterns, analyzing detection metrics.
5. List GuardDuty findings for detector `<detector-id>` and check finding generation patterns, threat severity, and detection timestamps, verifying finding generation.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for GuardDuty API call failures or detector configuration errors, checking for API errors.
7. Retrieve the GuardDuty Detector `<detector-id>` data source enablement status and verify data sources are enabled, checking if data source configuration affects detection.
8. Retrieve CloudWatch metrics for GuardDuty Detector `<detector-id>` including DataSourcesProcessed if available and verify data source processing patterns, checking if data sources are being processed.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for GuardDuty detector enablement or data source configuration modification events related to detector `<detector-id>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Metrics from Step 4**: Review GuardDuty metrics for detection activity. If CloudWatch metrics show FindingsGenerated at 0 over 7 days, then either no threats exist or detection is not working. Compare with expected threat activity based on environment risk profile. If metrics show some findings generated, detection may be working but missing specific threat types - continue to step 2.

2. **Verify Detector Enablement from Step 2**: If detector configuration from Step 2 shows detector status is "DISABLED" or detector is suspended, then threat detection is not running. Check if detector was recently disabled. If detector is enabled but status shows issues, continue to step 3.

3. **Check Data Source Configuration from Step 7**: If data sources from Step 7 show VPC Flow Logs, CloudTrail, or DNS logs are not enabled, then GuardDuty lacks visibility into network and API activity. Enable all relevant data sources for comprehensive threat detection. If data sources are enabled but metrics from Step 8 show no processing activity, then data source delivery is failing.

4. **Review CloudTrail Events from Step 6**: If CloudTrail events from Step 6 show GuardDuty API call failures or access denied errors, then permission issues are affecting detection. Verify GuardDuty service-linked role has proper permissions. If API calls are succeeding, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show detector enablement changes, data source modifications, or suppression rule additions within 5 minutes of detection stopping, then recent changes affected threat detection. Check for finding suppression rules that may be filtering legitimate threats.

**If no correlation is found**: Extend analysis to 90 days using finding patterns from Step 5. For multi-account setups, verify member accounts are properly linked to the administrator account. Review GuardDuty threat intelligence feed updates and service health from Step 1. Check for IP whitelisting or finding suppression rules that may be masking threats. Verify the account has actual network and API activity to analyze.
