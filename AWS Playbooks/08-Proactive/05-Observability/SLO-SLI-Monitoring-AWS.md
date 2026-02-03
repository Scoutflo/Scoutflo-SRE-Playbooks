# SLO/SLI Monitoring

## Meaning

SLO/SLI monitoring indicates that Service Level Objective and Service Level Indicator monitoring cannot be performed or SLO/SLI violations are detected (triggering alarms like SLOViolation or SLIMonitoringFailed) because SLO/SLI metrics are unavailable, SLO/SLI monitoring tools fail, SLO/SLI violations are detected, SLO/SLI configuration is missing, or SLO/SLI monitoring indicates problems. SLO/SLI monitoring shows failures, SLO/SLI metrics are unavailable, SLO/SLI violations are detected, and SLO/SLI monitoring fails. This affects the performance monitoring layer and service level management, typically caused by SLO/SLI configuration failures, SLO/SLI monitoring tool failures, SLO/SLI metric collection issues, or SLO/SLI monitoring gaps; if SLO/SLI monitoring affects container workloads, container SLO/SLI may be unavailable and applications may experience service level management failures.

## Impact

SLOViolation alarms fire; SLIMonitoringFailed alarms fire; SLO/SLI monitoring cannot be performed; SLO/SLI violations are detected; service level management may be compromised; service level compliance may be at risk. SLO/SLI monitoring shows failures; if SLO/SLI monitoring affects container workloads, container SLO/SLI may be unavailable, pod service levels may be unmonitored, and container applications may experience service level management failures; applications may experience SLO/SLI monitoring gaps or service level compliance risks.

## Playbook

1. Retrieve SLO/SLI configuration for service `<service-name>` and verify SLO/SLI target definitions and SLI metric configurations, checking SLO/SLI configuration.
2. Retrieve CloudWatch metrics for service `<service-name>` including SLI metrics such as Availability, Latency, and ErrorRate over the last 30 days to calculate SLO compliance.
3. Query CloudWatch Logs for log groups containing SLO/SLI monitoring events and filter for SLO violation patterns or SLI monitoring failures within the last 7 days.
4. Compare SLO violation detection timestamps with SLI metric threshold breach timestamps within 5 minutes and verify whether metric breaches cause SLO violations, using CloudWatch metrics as supporting evidence.
5. Retrieve SLO/SLI monitoring tool execution results and verify tool availability and monitoring completion status, checking SLO/SLI monitoring tool health.
6. Compare SLO/SLI configuration change timestamps with SLO violation detection timestamps within 1 hour and verify whether configuration changes affect SLO compliance, using SLO/SLI configuration data as supporting evidence.
7. Retrieve SLO/SLI compliance history for service `<service-name>` and verify SLO compliance trends and SLI metric accuracy, checking SLO/SLI compliance data quality.
8. List CloudWatch alarms for service `<service-name>` and verify alarm SLO/SLI configuration to identify alarms without SLO/SLI monitoring, checking alarm SLO/SLI coverage.

## Diagnosis

1. **Analyze SLI metrics from Step 2**: If Availability is below SLO target, identify the periods of unavailability. If Latency exceeds SLO target, identify slow transactions or endpoints. If ErrorRate exceeds SLO target, investigate error causes. Calculate error budget consumption from compliance history.

2. **Evaluate SLO configuration from Step 1**: If SLO targets are unrealistic (e.g., 100% availability), adjust to achievable targets. If SLI metrics do not accurately represent user experience, refine the metrics. If SLO calculation methodology is incorrect, fix the formula.

3. **Review SLO compliance history from Step 7**: If compliance is degrading over time, service reliability is decreasing. If compliance varies significantly, identify patterns (time of day, day of week). If recent violations exist, correlate with incidents or changes.

4. **Cross-reference with monitoring tools from Step 5**: If monitoring tools are failing, SLI data may be incomplete or inaccurate. If tools show intermittent failures, SLI calculations may be based on partial data. If tools are healthy but violations detected, violations are real.

5. **Assess alarm coverage from Step 8**: If alarms do not trigger before SLO violations, thresholds are too lenient. If alarms trigger frequently without SLO impact, thresholds are too strict. If critical SLIs have no alarms, monitoring coverage is incomplete.

If the above analysis is inconclusive: Review SLI data sources for accuracy. Compare SLO calculations with actual user-reported experience. Evaluate whether composite SLOs accurately reflect service health. Consider synthetic monitoring to supplement real user metrics.
