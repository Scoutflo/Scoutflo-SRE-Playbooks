# CloudWatch Alarm Not Triggering as Expected

## Meaning

CloudWatch alarm is not triggering as expected (triggering alerting failures or CloudWatchAlarmNotTriggering alarms) because alarm threshold is incorrect, alarm evaluation period is too long, alarm metric is not available, alarm state transition conditions are not met, alarm is disabled or in INSUFFICIENT_DATA state, or alarm action configuration prevents notifications. CloudWatch alarms do not trigger, alerting fails, and threshold breaches are not detected. This affects the monitoring and alerting layer and compromises incident detection, typically caused by alarm configuration issues, metric data problems, or action configuration failures; if using CloudWatch composite alarms, evaluation logic may differ and applications may experience alerting failures.

## Impact

CloudWatch alarms do not trigger; alerting fails; monitoring automation is ineffective; alarm state transitions do not occur; threshold breaches are not detected; alarm notifications are not sent; alerting reliability is compromised; incident detection is delayed. CloudWatchAlarmNotTriggering alarms may fire; if using CloudWatch composite alarms, evaluation logic may differ; applications may experience errors or performance degradation due to delayed incident detection; monitoring automation may be ineffective.

## Playbook

1. Verify CloudWatch alarm `<alarm-name>` exists and AWS service health for CloudWatch in region `<region>` is normal.
2. Retrieve the CloudWatch Alarm `<alarm-name>` in region `<region>` and inspect its alarm configuration, threshold settings, evaluation period, metric configuration, and alarm state, verifying alarm is enabled.
3. Retrieve CloudWatch metrics for alarm `<alarm-name>` including the metric used by the alarm over the last 24 hours to verify metric data availability and values, analyzing metric data gaps.
4. Retrieve CloudWatch alarm history for alarm `<alarm-name>` over the last 7 days to identify alarm state transitions and evaluation patterns, analyzing evaluation history.
5. Query CloudWatch Logs for log groups containing CloudWatch alarm events and filter for alarm evaluation patterns or state transition events related to alarm `<alarm-name>`, including evaluation logs.
6. List CloudWatch alarm actions for alarm `<alarm-name>` and check SNS topic configurations, action enablement, and notification settings, verifying action configuration.
7. Retrieve the CloudWatch Alarm `<alarm-name>` metric math or composite alarm configuration if applicable and verify alarm evaluation logic, checking if composite alarm logic prevents triggering.
8. Retrieve CloudWatch alarm history for alarm `<alarm-name>` including state change history and verify alarm state transitions, checking if alarm transitions occurred but actions failed.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudWatch alarm configuration modification events related to alarm `<alarm-name>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics collected for alarm `<alarm-name>` (from Playbook step 3) to verify metric data availability and identify data gaps. If metric data shows consistent gaps or INSUFFICIENT_DATA patterns, the alarm cannot evaluate properly. If metric data appears complete, proceed to threshold analysis.

2. Review CloudWatch alarm history (from Playbook step 4) to examine alarm state transitions and evaluation patterns over the last 7 days. If alarm history shows the alarm remained in INSUFFICIENT_DATA state, correlate with metric availability timestamps. If alarm history shows OK state despite expected threshold breaches, the threshold configuration is likely incorrect.

3. Examine alarm configuration details (from Playbook step 2) including threshold settings, evaluation period, and comparison operator. If threshold values do not match expected metric ranges based on the metric data analysis, threshold misconfiguration is the root cause. If thresholds appear correct, check if evaluation period is too long for the metric publishing frequency.

4. If alarm configuration appears correct but alarm still does not trigger, check alarm action configuration (from Playbook step 6) to verify SNS topics are correctly configured and actions are enabled. If actions are disabled or SNS topic configurations are incorrect, alarm state changes may occur but notifications are not sent.

5. For composite alarms, analyze the metric math or composite alarm configuration (from Playbook step 7) to verify evaluation logic. If composite alarm logic combines multiple conditions incorrectly, the overall alarm may not trigger even when individual metrics breach thresholds.

6. Correlate CloudTrail events (from Playbook step 9) with alarm non-triggering timestamps within 30 minutes to identify any recent configuration changes that may have affected alarm behavior. If configuration modifications coincide with when the alarm stopped triggering, those changes are the likely cause.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including alarm action configurations and SNS topic delivery status, check for gradual issues like metric data pattern changes or threshold drift, verify external dependencies like metric namespace availability or alarm evaluation service health, examine historical patterns of alarm triggering, check for CloudWatch composite alarm evaluation logic issues, verify CloudWatch alarm action delivery failures. Non-triggering may result from alarm action configuration issues, SNS topic delivery failures, alarm evaluation service problems, CloudWatch composite alarm evaluation logic, or alarm action delivery failures rather than immediate alarm configuration changes.
