# Metric Coverage Gaps

## Meaning

Metric coverage gaps indicate that Prometheus metric collection coverage is incomplete or metric coverage gaps are detected (triggering alerts like MetricCoverageIncomplete or MetricCollectionGapDetected) because Prometheus metrics are not collected for pods, custom metrics are missing, metric exporters are not installed, metric coverage analysis tools fail, or metric coverage monitoring indicates gaps. Metric coverage gaps are detected, Prometheus metrics are not collected, custom metrics are missing, and metric coverage analysis fails. This affects the observability layer and metric monitoring coverage, typically caused by metric configuration failures, metric exporter installation issues, metric coverage analysis tool failures, or metric coverage monitoring gaps; if metric coverage affects container workloads, container metrics may not be collected and applications may experience metric monitoring blind spots.

## Impact

MetricCoverageIncomplete alerts fire; MetricCollectionGapDetected alerts fire; metric collection coverage is incomplete; metric coverage gaps are detected; metric monitoring may be insufficient; performance analysis may be difficult. Metric coverage gaps are detected; if metric coverage affects container workloads, container metrics may not be collected, pod metrics may be missing, and container applications may experience metric monitoring blind spots; applications may experience metric coverage gaps or metric collection failures.

## Playbook

1. List pods, services, and servicemonitors in namespace <namespace> with wide output and describe servicemonitor <servicemonitor-name> in namespace <namespace> to understand the metric collection configuration and coverage.

2. List recent events in namespace <namespace> and <monitoring-namespace> sorted by timestamp to identify any metric collection failures or configuration issues.

3. Retrieve Prometheus metrics namespace coverage for services in namespace `<namespace>` and verify metric collection coverage to identify services without metrics, checking metric coverage gaps.

4. List pods in namespace `<namespace>` and verify Prometheus metrics exporter installation status and metric collection configuration, checking pod-level metric coverage.

5. List deployments in namespace `<namespace>` and verify deployment metrics configuration and metric exporter association, checking deployment metric coverage.

6. List services in namespace `<namespace>` and verify Prometheus service monitor configuration and service metric collection settings, checking service metric coverage.

7. Retrieve Prometheus metrics for service namespaces and verify metric availability over the last 7 days to identify missing metrics or metric collection failures, checking metric collection health.

8. Compare metric coverage analysis results with pod deployment timestamps and verify whether new pods have metrics configured upon deployment, using pod configuration data as supporting evidence.

9. Retrieve Prometheus metrics exporter status for pods in namespace `<namespace>` and verify exporter health and metric collection status, checking metric exporter coverage.

10. List Prometheus custom metrics and verify custom metric coverage for services to identify services without custom metrics, checking custom metric coverage gaps.

## Diagnosis

1. Review the metric namespace coverage from Step 3. If services show no metrics in Prometheus, this is the primary coverage gap. Identify whether the issue is missing ServiceMonitors, incorrect label selectors, or missing metric endpoints.

2. Analyze the pod-level metric exporter status from Step 4. If exporters are not installed or misconfigured, then pods cannot expose metrics for collection. If exporters are present but Step 9 shows unhealthy status, then exporter maintenance is needed.

3. If Step 6 ServiceMonitor configurations exist but Step 7 metric availability shows gaps, then label matching or port configuration may be incorrect. If ServiceMonitors are missing entirely, then metric collection infrastructure needs to be deployed.

4. Review the custom metric coverage from Step 10. If services lack custom metrics beyond default resource metrics, then application-specific observability may be insufficient for business monitoring needs.

5. If Step 8 shows new pods without metrics upon deployment, then deployment automation needs to include metric configuration. If existing pods lose metrics over time, then configuration drift or exporter failures are occurring.

If analysis is inconclusive: Examine events from Step 2 for metric collection failures or Prometheus scrape errors. Determine whether coverage gaps are concentrated in specific service types (suggesting template issues) or distributed randomly (suggesting ad-hoc deployments without standards). Verify that Prometheus service availability and capacity are sufficient for the workload.
