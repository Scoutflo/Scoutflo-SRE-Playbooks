# SLO/SLI Monitoring

## Meaning

SLO/SLI monitoring indicates that Service Level Objective and Service Level Indicator monitoring cannot be performed or SLO/SLI violations are detected (triggering alerts like SLOViolation or SLIMonitoringFailed) because SLO/SLI metrics are unavailable, SLO/SLI monitoring tools fail, SLO/SLI violations are detected, SLO/SLI configuration is missing, or SLO/SLI monitoring indicates problems. SLO/SLI monitoring shows failures, SLO/SLI metrics are unavailable, SLO/SLI violations are detected, and SLO/SLI monitoring fails. This affects the performance monitoring layer and service level management, typically caused by SLO/SLI configuration failures, SLO/SLI monitoring tool failures, SLO/SLI metric collection issues, or SLO/SLI monitoring gaps; if SLO/SLI monitoring affects container workloads, container SLO/SLI may be unavailable and applications may experience service level management failures.

## Impact

SLOViolation alerts fire; SLIMonitoringFailed alerts fire; SLO/SLI monitoring cannot be performed; SLO/SLI violations are detected; service level management may be compromised; service level compliance may be at risk. SLO/SLI monitoring shows failures; if SLO/SLI monitoring affects container workloads, container SLO/SLI may be unavailable, pod service levels may be unmonitored, and container applications may experience service level management failures; applications may experience SLO/SLI monitoring gaps or service level compliance risks.

## Playbook

1. List pods in namespace <namespace> with label app=<service-name> and wide output to retrieve the service pods and verify their current status, readiness, and availability metrics.
2. List recent events in namespace <namespace> sorted by timestamp to identify service availability issues, pod failures, or latency-related warnings.
3. Describe deployment <service-name> in namespace <namespace> to inspect the deployment configuration including replica status, resource limits, and health check settings.
4. Retrieve Prometheus metrics for service `<service-name>` including SLI metrics such as availability, latency, and error_rate over the last 30 days to calculate SLO compliance.
5. Retrieve logs from SLO/SLI monitoring pods and filter for SLO violation patterns or SLI monitoring failures within the last 7 days.
6. Compare SLO violation detection timestamps with SLI metric threshold breach timestamps within 5 minutes and verify whether metric breaches cause SLO violations, using Prometheus metrics as supporting evidence.
7. Retrieve SLO/SLI monitoring tool execution results and verify tool availability and monitoring completion status, checking SLO/SLI monitoring tool health.
8. Retrieve SLO/SLI compliance history for service `<service-name>` and verify SLO compliance trends and SLI metric accuracy, checking SLO/SLI compliance data quality.
9. List Prometheus alerts for service `<service-name>` and verify alert SLO/SLI configuration to identify alerts without SLO/SLI monitoring, checking alert SLO/SLI coverage.

## Diagnosis

1. Review the SLI metrics from Step 4 (availability, latency, error_rate). If metrics show values below SLO thresholds, then genuine service performance issues are causing SLO violations. If metrics appear healthy but violations are reported, then SLO configuration may be incorrect.

2. Analyze the SLO/SLI monitoring tool status from Step 7. If tools show failures or incomplete status, then monitoring infrastructure issues may be causing false violations or missed violations. If tools are healthy, proceed to SLO configuration analysis.

3. If Step 5 logs show violation patterns, examine whether violations cluster around specific times (suggesting traffic patterns) or occur randomly (suggesting intermittent service issues).

4. Review the SLO compliance history from Step 8. If compliance is trending downward over 30 days, then systematic service degradation is occurring. If compliance oscillates, then specific incidents are causing temporary violations.

5. If Step 9 alert coverage shows services without SLO/SLI monitoring, then blind spots exist. Prioritize adding monitoring for critical services lacking SLO tracking.

If analysis is inconclusive: Examine events from Step 2 for pod failures or latency-related warnings. Determine whether SLO violations correlate with specific deployment events or traffic spikes. Verify that SLO targets are appropriately calibrated for realistic service performance expectations.
