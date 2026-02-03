# Error Budget Tracking

## Meaning

Error budget tracking indicates that error budget tracking cannot be performed or error budget exhaustion is detected (triggering alarms like ErrorBudgetExhausted or ErrorBudgetTrackingFailed) because error budget metrics are unavailable, error budget tracking tools fail, error budget exhaustion is detected, error budget configuration is missing, or error budget tracking monitoring indicates problems. Error budget tracking shows failures, error budget metrics are unavailable, error budget exhaustion is detected, and error budget tracking fails. This affects the performance monitoring layer and error budget management, typically caused by error budget configuration failures, error budget tracking tool failures, error budget metric collection issues, or error budget tracking monitoring gaps; if error budget tracking affects container workloads, container error budgets may be unavailable and applications may experience error budget management failures.

## Impact

ErrorBudgetExhausted alarms fire; ErrorBudgetTrackingFailed alarms fire; error budget tracking cannot be performed; error budget exhaustion is detected; error budget management may be compromised; service reliability may be at risk. Error budget tracking shows failures; if error budget tracking affects container workloads, container error budgets may be unavailable, pod error budgets may be unmonitored, and container applications may experience error budget management failures; applications may experience error budget tracking gaps or service reliability risks.

## Playbook

1. Retrieve error budget configuration for service `<service-name>` and verify error budget target definitions and error budget calculation settings, checking error budget configuration.
2. Retrieve CloudWatch metrics for service `<service-name>` including ErrorRate and Availability over the last 30 days to calculate error budget consumption and remaining budget.
3. Query CloudWatch Logs for log groups containing error budget tracking events and filter for error budget exhaustion patterns or error budget tracking failures within the last 7 days.
4. Compare error budget exhaustion detection timestamps with error rate increase timestamps within 1 hour and verify whether error rate increases cause budget exhaustion, using CloudWatch metrics as supporting evidence.
5. Retrieve error budget tracking tool execution results and verify tool availability and tracking completion status, checking error budget tracking tool health.
6. Compare error budget configuration change timestamps with error budget consumption change timestamps within 1 hour and verify whether configuration changes affect budget consumption, using error budget configuration data as supporting evidence.
7. Retrieve error budget consumption history for service `<service-name>` and verify error budget trends and consumption accuracy, checking error budget consumption data quality.
8. List CloudWatch alarms for service `<service-name>` and verify alarm error budget configuration to identify alarms without error budget tracking, checking alarm error budget coverage.

## Diagnosis

1. **Analyze error budget consumption from Step 2 and Step 7**: If error budget is nearly exhausted, throttle risky deployments. If budget consumption is accelerating, identify the source of increasing errors. If budget is healthy, reliability is maintained.

2. **Evaluate error rate trends from Step 4**: If error rate increases correlate with budget exhaustion, errors are consuming the budget as expected. If budget exhausts without error rate increase, SLO target may be too aggressive.

3. **Review error budget configuration from Step 1**: If SLO target is set too high (e.g., 99.99%), budget exhausts quickly. If target is appropriate, the issue is error rate. If configuration is missing, implement error budget tracking.

4. **Cross-reference with configuration changes from Step 6**: If budget consumption changed after configuration updates, verify the new configuration is correct. If no changes were made, error patterns changed.

5. **Assess tracking tool health from Step 5**: If tracking tools are failing, budget calculations may be inaccurate. If tools are healthy, budget calculations are reliable.

If the above analysis is inconclusive: Review incident correlation with error budget consumption. Implement error budget policies for deployment freezes. Consider burn rate alerts for early warning. Align error budget with business impact tolerance.
