---
title: Kube API Terminated Requests
weight: 20
---

# KubeAPITerminatedRequests

## Meaning

The API server has terminated over 20% of its incoming requests (triggering KubeAPITerminatedRequests alerts) because API server flow control is rejecting requests due to rate limiting, priority and fairness constraints, or capacity limits. API server flow control metrics show high termination rates, FlowSchema resources show throttling configurations, and API server logs show flow control rejection errors. This affects the control plane and indicates that API server capacity is being exceeded or flow control configuration is too restrictive, typically caused by excessive client request rates, misconfigured flow schemas, or insufficient API server resources; applications using Kubernetes API may show errors.

## Impact

KubeAPITerminatedRequests alerts fire; clients cannot interact with the cluster reliably; in-cluster services may degrade or become unavailable; API requests are terminated; flow control rejects requests; API operations fail intermittently; controllers may fail to reconcile; applications using Kubernetes API experience failures; cluster operations are throttled; user-facing services may become unresponsive; workload scaling operations may be blocked. API server flow control metrics show sustained high termination rates; FlowSchema resources show throttling configurations; API server logs show flow control rejection errors; applications using Kubernetes API may experience errors or performance degradation.

## Playbook

1. Retrieve API server flow control metrics and identify which flow schemas are throttling traffic to determine which request types are being terminated.

2. Retrieve FlowSchema resources and inspect flow schema configurations and priority levels to understand request prioritization and identify misconfigurations.

3. Retrieve API server metrics for request rates, terminated request rates, and flow control rejections to quantify the termination rate and identify patterns.

4. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and check API server resource usage and capacity to verify if resource constraints are causing terminations.

5. Retrieve API server configuration and verify API server flow control configuration including priority and fairness settings to identify restrictive configurations.

6. Retrieve metrics for client API request rates and identify clients or controllers making excessive API requests that may trigger flow control.

## Diagnosis

Compare API terminated request spike timestamps with API server flow control rejection timestamps within 5 minutes and verify whether terminations coincide with flow control activations, using flow control metrics and terminated request rates as supporting evidence.

Correlate API terminated requests with client API request rate spike timestamps within 5 minutes and verify whether high client request rates triggered flow control, using client API usage metrics and flow control rejections as supporting evidence.

Compare API terminated request patterns with flow schema priority configurations to determine if terminations are due to low-priority requests being throttled, using flow schema configurations and terminated request patterns as supporting evidence.

Analyze API terminated request patterns over the last 15 minutes to determine if terminations are consistent (capacity issue) or intermittent (burst traffic), using terminated request metrics and API server load as supporting evidence.

Correlate API terminated requests with API server resource usage spikes within 5 minutes and verify whether resource constraints caused flow control to activate, using API server resource metrics and flow control activation times as supporting evidence.

Compare API terminated request rates with historical patterns over the last 7 days and verify whether current terminations represent a new issue or ongoing capacity problems, using terminated request history and API server capacity data as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for traffic analysis, review API server flow control configuration, check for client misconfigurations causing excessive requests, verify API server capacity settings, examine historical flow control patterns. API terminated requests may result from API server capacity limitations, misconfigured flow control, or client request patterns rather than immediate changes.
