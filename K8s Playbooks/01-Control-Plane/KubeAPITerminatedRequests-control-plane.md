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

1. Describe pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, resource usage, and flow control configuration.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for flow control rejections, rate limiting, or terminated request errors.

3. Retrieve API server flow control metrics and identify which flow schemas are throttling traffic to determine which request types are being terminated.

4. Retrieve FlowSchema resources and inspect flow schema configurations and priority levels to understand request prioritization and identify misconfigurations.

5. Retrieve API server metrics for request rates, terminated request rates, and flow control rejections to quantify the termination rate and identify patterns.

6. Retrieve API server configuration and verify API server flow control configuration including priority and fairness settings to identify restrictive configurations.

7. Retrieve metrics for client API request rates and identify clients or controllers making excessive API requests that may trigger flow control.

## Diagnosis

1. Analyze flow control and rate limiting events from Playbook to identify when request terminations began and which flow schemas are active. If events show flow control rejections or throttling, use event timestamps to determine the onset of terminations.

2. If events indicate specific flow schema activations, examine FlowSchema configurations from Playbook step 4. If events show particular priority levels being throttled, identify which request types or clients are affected and whether flow schema configuration is appropriate.

3. If events indicate high client request rates, identify which clients or controllers are generating excessive API requests from Playbook step 7. If events show specific clients with high request volumes at termination timestamps, client behavior is triggering flow control.

4. If events indicate API server resource pressure, verify pod resource usage at event timestamps. If CPU or memory usage spiked when terminations increased, resource constraints forced flow control activation.

5. If events show terminations affecting specific request types (read vs write verbs), analyze which operations are being terminated. If write operations are prioritized over reads in flow schemas, adjust priority configurations accordingly.

6. If events indicate consistent terminations (not intermittent), analyze API server capacity configuration. If terminations are steady rather than bursty, API server capacity may be insufficient for baseline load.

7. If events indicate intermittent terminations, identify burst traffic patterns at event timestamps. If terminations correlate with specific time periods or operations, targeted traffic management can resolve the issue.

**If no correlation is found**: Extend timeframes to 1 hour for traffic analysis, review API server flow control configuration, check for client misconfigurations causing excessive requests, verify API server capacity settings, examine historical flow control patterns. API terminated requests may result from API server capacity limitations, misconfigured flow control, or client request patterns rather than immediate changes.
