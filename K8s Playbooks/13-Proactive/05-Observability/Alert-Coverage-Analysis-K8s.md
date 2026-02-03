# Alert Coverage Analysis

## Meaning

Alert coverage analysis indicates that Prometheus alert rule coverage is incomplete or alert coverage gaps are detected (triggering alerts like AlertCoverageIncomplete or AlertRuleGapDetected) because Prometheus alerts are not configured for services, alert rules are missing, alert coverage analysis tools fail, alert coverage monitoring indicates gaps, or alert rule coverage is insufficient. Alert coverage gaps are detected, Prometheus alerts are not configured, alert rules are missing, and alert coverage analysis fails. This affects the observability layer and alerting coverage, typically caused by alert configuration failures, alert rule deployment issues, alert coverage analysis tool failures, or alert coverage monitoring gaps; if alert coverage affects container workloads, container alerts may not be configured and applications may experience alert monitoring blind spots.

## Impact

AlertCoverageIncomplete alerts fire; AlertRuleGapDetected alerts fire; alert rule coverage is incomplete; alert coverage gaps are detected; alert monitoring may be insufficient; incident detection may be delayed. Alert coverage gaps are detected; if alert coverage affects container workloads, container alerts may not be configured, pod alerts may be missing, and container applications may experience alert monitoring blind spots; applications may experience alert coverage gaps or alert configuration failures.

## Playbook

1. List prometheusrules and alertmanagers in namespace <namespace> to identify configured alert rules and alerting infrastructure.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent changes or issues with alert configurations.

3. Describe prometheusrules in namespace <namespace> to verify alert rule coverage for critical metrics.

4. List Prometheus alert groups and verify alert group coverage for service dependencies to identify missing alert groups, checking alert group coverage.

5. Retrieve logs from Prometheus pods with label app=prometheus in namespace <namespace> and filter for alert configuration events.

6. Compare alert coverage analysis results with pod deployment timestamps and verify whether new pods have alerts configured upon deployment, using pod configuration data as supporting evidence.

7. List Prometheus metric alarms and verify metric alarm coverage for service metrics to identify metrics without alerts, checking metric alert coverage gaps.

8. Retrieve Prometheus alert evaluation results and verify alert evaluation coverage for services to identify services without alert evaluations, checking alert evaluation coverage.

## Diagnosis

1. Review the PrometheusRule configurations from Step 3. If critical services lack alerting rules for key metrics (availability, error rate, latency), these are the primary coverage gaps requiring immediate attention.

2. Analyze the alert group coverage from Step 4. If alert groups are missing for service dependencies, then dependency failures may go undetected. Prioritize adding alerts for critical dependencies.

3. If Step 5 Prometheus logs show alert configuration events or rule evaluation errors, then alerting infrastructure issues exist. If logs are clean, then the issue is missing rule configuration rather than infrastructure problems.

4. Review the metric alarm coverage from Step 7. If metrics exist without corresponding alerts, identify which metrics are critical for operational visibility and add alerting rules.

5. If Step 6 shows new pods without alerts upon deployment, then deployment automation needs to include alert configuration. Integrate alert creation into CI/CD pipelines.

If analysis is inconclusive: Examine events from Step 2 for recent changes affecting alert configurations. Review the alert evaluation coverage from Step 8 to identify services lacking alert evaluations. Determine whether coverage gaps are concentrated in specific namespaces or service types (suggesting deployment pipeline issues) or distributed (suggesting ad-hoc practices).
