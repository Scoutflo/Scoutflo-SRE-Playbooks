# Log Coverage Analysis

## Meaning

Log coverage analysis indicates that log collection coverage is incomplete or log coverage gaps are detected (triggering alerts like LogCoverageIncomplete or LogCollectionGapDetected) because pod logs are not configured, log collection agents are not installed, log coverage analysis tools fail, log coverage monitoring indicates gaps, or log collection coverage is insufficient. Log coverage gaps are detected, pod logs are not configured, log collection agents are missing, and log coverage analysis fails. This affects the observability layer and log monitoring coverage, typically caused by log configuration failures, log collection agent installation issues, log coverage analysis tool failures, or log coverage monitoring gaps; if log coverage affects container workloads, container logs may not be collected and applications may experience log monitoring blind spots.

## Impact

LogCoverageIncomplete alerts fire; LogCollectionGapDetected alerts fire; log collection coverage is incomplete; log coverage gaps are detected; log monitoring may be insufficient; troubleshooting may be difficult. Log coverage gaps are detected; if log coverage affects container workloads, container logs may not be collected, pod logs may be missing, and container applications may experience log monitoring blind spots; applications may experience log coverage gaps or log collection failures.

## Playbook

1. List pods, deployments, and daemonsets in namespace <namespace> with wide output and describe daemonset <log-collector-daemonset> in namespace <logging-namespace> to understand the log collection infrastructure and pod logging status.

2. List recent events in namespace <namespace> and <logging-namespace> sorted by timestamp to identify any log collection failures or issues.

3. List pods in namespace `<namespace>` and verify pod log configuration and log collection agent installation status, checking pod-level log coverage.

4. List deployments in namespace `<namespace>` and verify deployment log configuration and log collection settings, checking deployment log coverage.

5. List services in namespace `<namespace>` and verify service log configuration and log collection settings, checking service log coverage.

6. Retrieve logs from log collection pods and verify log stream activity over the last 7 days to identify inactive log streams or log collection failures, checking log collection health.

7. Compare log coverage analysis results with pod deployment timestamps and verify whether new pods have log collection configured upon deployment, using pod configuration data as supporting evidence.

8. Retrieve log collection agent status for pods in namespace `<namespace>` and verify agent health and log collection status, checking log agent coverage.

9. List log collection configuration and verify log collection coverage for pods to identify pods without log collection, checking log collection coverage gaps.

10. Retrieve Prometheus metrics for log collection including log_collection_success_rate and log_collection_latency over the last 7 days to identify log collection issues.

## Diagnosis

1. Review the pod log configuration status from Step 3. If pods lack log collection configuration, this is the primary coverage gap. Check whether the issue is missing agent sidecars, incorrect log paths, or missing annotations.

2. Analyze the log collection agent status from Step 8. If agents show unhealthy status or missing deployments, then infrastructure-level issues are preventing log collection. If agents are healthy, then pod-level configuration is the issue.

3. If Step 6 log stream activity shows inactive streams, then log collection is configured but not functioning. If streams are active but Step 10 metrics show high collection latency or low success rate, then collection performance issues exist.

4. Review the daemonset status from Step 1. If the log collector daemonset has pods not running on all nodes, then some workloads will have no log coverage. If all daemonset pods are running, proceed to configuration analysis.

5. If Step 7 shows new pods without log collection configured upon deployment, then deployment templates or admission webhooks need updating to include log collection configuration automatically.

If analysis is inconclusive: Examine events from Step 2 for log collection failures or configuration issues. Determine whether coverage gaps are clustered in specific namespaces (suggesting namespace-level configuration issues) or distributed across the cluster (suggesting systemic issues). Verify that log collection automation is integrated into deployment pipelines.
