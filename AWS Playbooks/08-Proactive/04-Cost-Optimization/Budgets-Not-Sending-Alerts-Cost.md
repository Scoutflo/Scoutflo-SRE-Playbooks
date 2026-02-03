# AWS Budgets Not Sending Alerts

## Meaning

AWS Budgets are not sending alerts (triggering budget alerting failures or BudgetsAlertNotSending alarms) because budget alert thresholds are not configured, SNS topic for alerts is not configured, IAM permissions are insufficient for alert delivery, budget alert actions are disabled, SNS topic delivery fails, or budget alert threshold evaluation does not trigger. AWS Budget alerts are not sent, budget threshold breaches are not notified, and budget monitoring automation is ineffective. This affects the cost management and monitoring layer and compromises budget monitoring, typically caused by alert configuration issues, SNS delivery problems, or threshold evaluation failures; if using Budgets with multiple alert actions, alert behavior may differ and applications may experience missing budget notifications.

## Impact

AWS Budget alerts are not sent; budget threshold breaches are not notified; budget monitoring automation is ineffective; cost overruns are not detected; budget alert delivery fails; financial monitoring is compromised; budget-based cost management fails; alert notifications are not received. BudgetsAlertNotSending alarms may fire; if using Budgets with multiple alert actions, alert behavior may differ; applications may experience unexpected costs; cost monitoring may be ineffective.

## Playbook

1. Verify AWS Budget `<budget-name>` exists and AWS service health for Budgets and SNS in region `<region>` is normal.
2. Retrieve the AWS Budget `<budget-name>` and inspect its budget configuration, alert thresholds, alert actions, and SNS topic configurations, verifying alert actions are configured.
3. Retrieve the SNS Topic `<topic-arn>` configured for budget alerts and inspect topic policy, subscription status, and message delivery settings, verifying SNS topic is configured correctly.
4. Query CloudWatch Logs for log groups containing SNS events and filter for budget alert delivery failure patterns or SNS delivery errors, including delivery error details.
5. Retrieve CloudWatch metrics for AWS Budgets including BudgetAlertCount over the last 30 days to identify alert delivery patterns, analyzing alert delivery frequency.
6. List AWS Budget alert history for budget `<budget-name>` and check alert generation timestamps, alert delivery status, and alert threshold breaches, analyzing alert history.
7. Retrieve the AWS Budget `<budget-name>` alert action configurations and verify alert action enablement, checking if alert actions are enabled.
8. Retrieve CloudWatch metrics for SNS Topic `<topic-arn>` including NumberOfMessagesPublished and verify message publishing patterns, checking if messages are being published.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for AWS Budget alert configuration or SNS topic modification events related to budget `<budget-name>` within the last 30 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Metrics and SNS Delivery from Steps 5 and 8**: Review budget alert and SNS metrics for delivery patterns. If CloudWatch metrics from Step 5 show BudgetAlertCount at 0 when thresholds were exceeded, then alerts are not being generated. If SNS metrics from Step 8 show NumberOfMessagesPublished at 0 for the budget topic, then messages are not being sent. If metrics show alerts generated but not delivered, continue to step 2.

2. **Check SNS Topic Configuration from Step 3**: If SNS topic from Step 3 has incorrect access policy blocking budget service (`budgets.amazonaws.com`), then permission issues prevent alert publishing. Verify subscription status - if subscriptions are pending confirmation or endpoint is invalid (unverified email, unreachable HTTP endpoint), then delivery fails at subscription level. If SNS is properly configured, continue to step 3.

3. **Review Budget Alert Configuration from Steps 2 and 7**: If budget from Step 2 has no alert thresholds configured or alert actions from Step 7 are disabled, then alerts cannot be generated. Verify threshold types (actual vs forecasted) and threshold percentages - if thresholds are set too high to trigger, then alert configuration is the issue. Check alert action SNS topic ARN is correctly specified. If configuration appears correct, continue to step 4.

4. **Verify Alert History from Step 6**: If alert history from Step 6 shows alerts were generated but status indicates delivery failure, then SNS delivery issues exist. Check failure reasons in alert history. If no alerts appear in history despite budget exceeding thresholds, then budget evaluation is not triggering alerts - verify budget amount and actual spend align with threshold calculations.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show budget alert, SNS topic, or IAM policy modifications within 5 minutes of alert delivery failures, then recent changes caused the issue. Review specific modifications to identify whether threshold changes, SNS policy updates, or permission changes broke alert delivery.

**If no correlation is found**: Extend analysis to 90 days using alert history from Step 6. Verify SNS topic subscriptions are confirmed and endpoints are reachable. Check SNS delivery status logs for specific error messages. Verify budget service health from Step 1 and ensure the budget is using the correct notification type (SNS vs email direct).
