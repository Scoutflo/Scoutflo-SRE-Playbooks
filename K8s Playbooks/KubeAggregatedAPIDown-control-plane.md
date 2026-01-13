---
title: Kube Aggregated API Down
weight: 20
---

# KubeAggregatedAPIDown

## Meaning

Kubernetes aggregated API server is unavailable (triggering KubeAggregatedAPIDown alerts) because the aggregated API server has failed, lost network connectivity, or cannot be reached by the API server aggregation layer. Aggregated API server pods show CrashLoopBackOff or Failed state in kubectl, aggregated API server logs show fatal errors, panic messages, or connection timeout errors, and aggregated API endpoints return connection refused or timeout errors. This affects the control plane and prevents custom resources, metrics APIs, or other aggregated API functionality from working, typically caused by pod failures, network issues, configuration problems, or resource constraints; applications using custom resources may show errors.

## Impact

KubeAggregatedAPIDown alerts fire; aggregated API endpoints return errors; custom resources may be unavailable; HPA may fail if using custom metrics; cluster functionality dependent on aggregated APIs is degraded; inability to see cluster metrics; unable to use custom metrics to scale; cluster operations may be severely limited; custom resource definitions cannot be accessed; metrics-based autoscaling fails. Aggregated API server pods remain in CrashLoopBackOff or Failed state; aggregated API endpoints return connection refused or timeout errors; applications using custom resources may experience errors or performance degradation; APIService registration issues may prevent aggregated API connectivity.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` for aggregated API server deployments and inspect its status, restart count, and container states to verify if the aggregated API server is running.

2. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'timeout', 'certificate' to identify startup or runtime failures.

3. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff' to identify pod lifecycle issues.

4. Retrieve the Service `<service-name>` for aggregated API server endpoints in namespace `<namespace>` and verify network connectivity between API server and aggregated API server endpoints.

5. Retrieve NetworkPolicy resources in namespace `<namespace>` and check if network policies block communication between API server and aggregated API servers.

6. Retrieve the Service `<service-name>` and Endpoints for aggregated API server in namespace `<namespace>` and verify aggregated API server configuration and service endpoints.

7. Retrieve APIService resources and check API server aggregation layer configuration and aggregated API server registrations.

## Diagnosis

Compare aggregated API unavailability timestamps with aggregated API server pod restart or failure timestamps within 5 minutes and verify whether unavailability coincides with pod failures, using pod events and aggregated API server status as supporting evidence.

Correlate aggregated API failures with network policy or firewall rule change timestamps within 10 minutes and verify whether network configuration changes blocked API server to aggregated API communication, using network policy events and connection logs as supporting evidence.

Compare aggregated API log error timestamps with configuration change times within 10 minutes and verify whether aggregated API failures began after configuration updates, using aggregated API logs and configuration modification times as supporting evidence.

Analyze aggregated API error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using aggregated API logs and pod resource usage metrics as supporting evidence.

Correlate aggregated API unavailability with API server aggregation layer configuration change timestamps within 10 minutes and verify whether aggregation layer changes affected aggregated API connectivity, using API server logs and aggregation configuration as supporting evidence.

Compare aggregated API server pod resource usage metrics with resource limits at failure times and verify whether resource constraints caused aggregated API failures, using pod metrics and resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review aggregated API server configuration, check for API server aggregation layer issues, verify network connectivity, examine historical aggregated API stability patterns. Aggregated API failures may result from network issues, configuration problems, or resource constraints rather than immediate changes.
