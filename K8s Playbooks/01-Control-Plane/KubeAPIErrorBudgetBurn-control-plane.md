---
title: Kube API Error Budget Burn
weight: 20
---

# KubeAPIErrorBudgetBurn

## Meaning

KubeAPIErrorBudgetBurn fires when the API server consumes its allowed error budget too quickly because of excessive errors or slow responses (triggering KubeAPIErrorBudgetBurn alerts). API server metrics show high error rates or slow response times, API server logs show timeout errors or admission webhook failures, and error budget consumption exceeds acceptable thresholds. This affects the control plane and indicates that API server availability or performance is degrading beyond acceptable SLO thresholds, typically caused by high error rates, slow response times, etcd issues, admission webhook problems, or capacity constraints; applications using Kubernetes API may show errors in application monitoring.

## Impact

KubeAPIErrorBudgetBurn alerts fire; overall availability of Kubernetes cluster is no longer guaranteed; there may be too many errors returned by the API server and/or responses take too long to guarantee proper reconciliation; API server error budget is being consumed; cluster SLO targets may be at risk; API operations may become unreliable; controller reconciliation may be affected; read/write verb operations contribute to error budget burn; cluster operations degrade beyond acceptable thresholds. API server metrics show sustained high error rates or slow response times; API server logs show timeout errors or admission webhook failures; applications using Kubernetes API may experience errors or performance degradation; etcd connectivity issues or admission webhook problems may contribute to error budget consumption.

## Playbook

1. Describe pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, resource usage, and any error conditions contributing to error budget burn.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for API server errors, timeouts, or admission webhook failures.

3. Retrieve API server metrics for current availability, remaining error budget, and which verbs (read/write) contribute to the burn to quantify error budget consumption.

4. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and filter for error patterns including high error rates, timeouts, and slow requests tied to namespaces, users, or admission webhooks to identify error sources.

5. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=etcd` and validate etcd health, check aggregated API servers, and verify admission webhooks that may amplify burn rates.

6. Retrieve API server metrics for request rates, error rates, and latency patterns to identify performance degradation patterns.

7. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and verify API server resource usage and capacity constraints to identify resource limitations.

## Diagnosis

1. Analyze API server events from Playbook to identify error patterns and timing. If events show timeout errors, admission webhook failures, or connection issues, use event timestamps to determine when error budget burn accelerated.

2. If events indicate high error rates or failed requests, examine API server logs for specific error types at event timestamps. If logs show 5xx errors, timeouts, or rejection patterns, identify which request types are contributing to error budget burn.

3. If events indicate etcd connectivity or performance issues, analyze etcd pod events and health from Playbook step 5. If etcd events show latency spikes, leader elections, or failures at timestamps correlating with error budget burn, etcd is the primary contributor.

4. If events indicate admission webhook timeouts or failures, review admission webhook metrics and logs. If webhook events show slow responses or errors at timestamps during burn periods, webhook latency is consuming error budget.

5. If events indicate aggregated API server issues, verify aggregated API status from Playbook step 5. If aggregated API events show failures at timestamps correlating with burn, aggregated API problems are contributing to error budget consumption.

6. If events show API server resource pressure, verify pod resource usage at event timestamps. If CPU or memory approached limits during burn periods, resource constraints caused slow responses contributing to budget burn.

7. If events are inconclusive, analyze whether burn is due to errors (high 5xx rate) or latency (slow responses) by examining API server request duration metrics at event timestamps. If latency patterns dominate, focus on performance optimization; if errors dominate, focus on reliability issues.

**If no correlation is found**: Extend timeframes to 24 hours for infrastructure changes, review API server capacity and limits, check for gradual performance degradation, verify external dependency health, examine historical error budget consumption patterns. API error budget burn may result from sustained high load, capacity limitations, or gradual performance degradation rather than immediate changes.
