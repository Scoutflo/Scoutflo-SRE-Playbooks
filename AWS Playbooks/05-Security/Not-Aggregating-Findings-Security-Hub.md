# AWS Security Hub Not Aggregating Findings

## Meaning

AWS Security Hub is not aggregating findings (triggering security aggregation failures or SecurityHubFindingsNotAggregating alarms) because Security Hub is not enabled, security standards are not subscribed, finding aggregation configuration is incorrect, IAM permissions are insufficient, Security Hub service encounters errors during aggregation, or Security Hub finding source integrations are not configured. Security Hub findings are not aggregated, security posture visibility is lost, and finding-based analysis fails. This affects the security and compliance layer and compromises security visibility, typically caused by Security Hub configuration issues, integration problems, or permission failures; if using Security Hub with multiple accounts or Regions, aggregation behavior may differ and applications may experience security visibility gaps.

## Impact

Security Hub findings are not aggregated; security posture visibility is lost; finding-based analysis fails; security standards compliance tracking fails; finding aggregation automation is ineffective; security insights are unavailable; compliance requirements are not met; security monitoring is compromised. SecurityHubFindingsNotAggregating alarms may fire; if using Security Hub with multiple accounts or Regions, aggregation behavior may differ; applications may experience reduced security visibility; security compliance tracking may be ineffective.

## Playbook

1. Verify AWS Security Hub configuration exists and AWS service health for Security Hub in region `<region>` is normal.
2. Retrieve the AWS Security Hub configuration in region `<region>` and inspect its enablement status, security standards subscriptions, and finding aggregation settings, verifying Security Hub is enabled.
3. Query CloudWatch Logs for log groups containing Security Hub events and filter for aggregation failure patterns or finding processing errors, including aggregation error details.
4. Retrieve CloudWatch metrics for Security Hub including FindingsImported and FindingsUpdated over the last 24 hours to identify finding aggregation patterns, analyzing aggregation metrics.
5. List Security Hub findings and check finding aggregation status, finding sources, and finding update timestamps, verifying finding aggregation.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Security Hub API call failures or aggregation errors, checking for API errors.
7. Retrieve the AWS Security Hub finding source integrations and verify integration configurations, checking if finding sources are integrated.
8. Retrieve the AWS Security Hub security standards subscriptions and verify standards are subscribed, checking if standards affect aggregation.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Security Hub enablement or security standards subscription modification events within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Metrics from Step 4**: Review Security Hub metrics for finding aggregation patterns. If CloudWatch metrics show FindingsImported at 0, then no findings are being received from integrated sources. If FindingsUpdated is at 0 but FindingsImported shows activity, then finding processing is failing. Compare with expected finding volume from security tools. If metrics show some activity, continue to step 2.

2. **Verify Security Hub Enablement from Step 2**: If Security Hub configuration from Step 2 shows Security Hub is not enabled or was recently disabled, then lack of enablement is the root cause. Check security standards subscriptions from Step 8 - if no standards are enabled, then compliance findings will not be generated. If Security Hub is enabled, continue to step 3.

3. **Check Finding Source Integrations from Step 7**: If finding source integrations from Step 7 show GuardDuty, Inspector, or third-party tools are not integrated, then those finding sources are not sending data. Verify each expected integration is enabled and properly configured. If integrations appear correct, continue to step 4.

4. **Review CloudTrail Events from Step 6**: If CloudTrail events from Step 6 show Security Hub API call failures or access denied errors, then permission issues are affecting aggregation. Check for `securityhub:BatchImportFindings` permission issues if custom integrations are used. If API calls are succeeding, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show Security Hub enablement changes, security standards modifications, or integration configuration changes within 5 minutes of aggregation failures, then recent changes caused the issue. Review the specific modifications to identify the breaking change.

**If no correlation is found**: Extend analysis to 30 days using finding patterns from Step 5. For multi-account setups, verify the aggregation region is correctly configured. Check that member accounts are properly linked to the administrator account. Review Security Hub service health from Step 1 and verify finding source services (GuardDuty, Inspector) are properly enabled and generating findings.
