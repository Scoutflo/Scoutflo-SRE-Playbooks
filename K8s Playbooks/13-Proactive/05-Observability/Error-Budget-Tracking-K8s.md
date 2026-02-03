# Error Budget Tracking

## Meaning

Error budget tracking indicates that error budget tracking cannot be performed or error budget exhaustion is detected (triggering alerts like ErrorBudgetExhausted or ErrorBudgetTrackingFailed) because error budget metrics are unavailable, error budget tracking tools fail, error budget exhaustion is detected, error budget configuration is missing, or error budget tracking monitoring indicates problems. Error budget tracking shows failures, error budget metrics are unavailable, error budget exhaustion is detected, and error budget tracking fails. This affects the performance monitoring layer and error budget management, typically caused by error budget configuration failures, error budget tracking tool failures, error budget metric collection issues, or error budget tracking monitoring gaps; if error budget tracking affects container workloads, container error budgets may be unavailable and applications may experience error budget management failures.

## Impact

ErrorBudgetExhausted alerts fire; ErrorBudgetTrackingFailed alerts fire; error budget tracking cannot be performed; error budget exhaustion is detected; error budget management may be compromised; service reliability may be at risk. Error budget tracking shows failures; if error budget tracking affects container workloads, container error budgets may be unavailable, pod error budgets may be unmonitored, and container applications may experience error budget management failures; applications may experience error budget tracking gaps or service reliability risks.

## Playbook

1. Retrieve deployment <deployment-name> in namespace <namespace> with full YAML output and describe service <service-name> in namespace <namespace> to verify service configuration and SLO definitions.

2. List recent events in namespace <namespace> sorted by timestamp and filtered by involved object name <deployment-name> to identify any recent issues affecting error budget.

3. Retrieve error budget configuration for service `<service-name>` and verify error budget target definitions and error budget calculation settings, checking error budget configuration.

4. Retrieve Prometheus metrics for service `<service-name>` including error_rate and availability over the last 30 days to calculate error budget consumption and remaining budget.

5. Retrieve logs from error budget tracking pods and filter for error budget exhaustion patterns or error budget tracking failures within the last 7 days.

6. Compare error budget exhaustion detection timestamps with error rate increase timestamps within 1 hour and verify whether error rate increases cause budget exhaustion, using Prometheus metrics as supporting evidence.

7. Retrieve error budget tracking tool execution results and verify tool availability and tracking completion status, checking error budget tracking tool health.

8. Compare error budget configuration change timestamps with error budget consumption change timestamps within 1 hour and verify whether configuration changes affect budget consumption, using error budget configuration data as supporting evidence.

9. Retrieve error budget consumption history for service `<service-name>` and verify error budget trends and consumption accuracy, checking error budget consumption data quality.

10. List Prometheus alerts for service `<service-name>` and verify alert error budget configuration to identify alerts without error budget tracking, checking alert error budget coverage.

## Diagnosis

1. Review the error budget configuration from Step 3 and Prometheus metrics from Step 4. If the remaining error budget shows less than 10% remaining, this confirms error budget exhaustion is the primary issue requiring immediate attention.

2. If Step 4 metrics show error rate or availability degradation correlating with budget consumption, then recent service reliability issues are depleting the budget. If error rates appear stable but budget is still consumed, then the SLO target may be misconfigured relative to baseline performance.

3. Analyze the error budget tracking tool results from Step 7. If tool execution shows failures or incomplete status, then tracking infrastructure issues are preventing accurate budget monitoring. If tools are healthy, proceed to configuration analysis.

4. If Step 8 configuration changes correlate with consumption changes, then recent configuration modifications may have affected budget calculation. If no recent changes exist, then organic service degradation is the likely cause.

5. Review alert coverage from Step 10. If services lack error budget tracking alerts, then monitoring gaps exist that need addressing. If alerts are configured but not firing during budget exhaustion, then alert thresholds require adjustment.

If analysis is inconclusive: Examine the 30-day consumption history from Step 9 to identify whether budget exhaustion follows predictable patterns (suggesting systematic issues) or occurs randomly (suggesting incident-driven consumption). Check for error budget configuration misalignments with actual service behavior and verify that error rate metric collection is functioning correctly.
