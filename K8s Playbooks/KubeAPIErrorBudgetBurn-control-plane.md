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

1. Retrieve API server metrics for current availability, remaining error budget, and which verbs (read/write) contribute to the burn to quantify error budget consumption.

2. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and filter for error patterns including high error rates, timeouts, and slow requests tied to namespaces, users, or admission webhooks to identify error sources.

3. Retrieve API server metrics for error spikes or latency issues to identify patterns and quantify degradation.

4. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=etcd` and validate etcd health, check aggregated API servers, and verify admission webhooks that may amplify burn rates.

5. Retrieve API server metrics for request rates, error rates, and latency patterns to identify performance degradation patterns.

6. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and verify API server resource usage and capacity constraints to identify resource limitations.

## Diagnosis

Compare API error budget burn detection timestamps with API server error rate spike times within 5 minutes and verify whether burn rate increased when error rates spiked, using API server error metrics and burn rate calculations as supporting evidence.

Correlate API error budget burn with etcd health degradation timestamps within 2 minutes and verify whether etcd issues caused API server errors or slow responses, using etcd health metrics and API server error logs as supporting evidence.

Compare API error budget burn with admission webhook timeout or error timestamps within 5 minutes and verify whether admission webhook issues contributed to error budget burn, using admission webhook metrics and API server logs as supporting evidence.

Analyze API server request latency patterns over the burn rate window to determine if burn is due to errors (high error rate) or latency (slow responses), using API server latency metrics and error rates as supporting evidence.

Correlate API error budget burn with aggregated API server failure timestamps within 5 minutes and verify whether aggregated API issues contributed to error budget consumption, using aggregated API status and API server error logs as supporting evidence.

Compare API error budget burn rate with historical burn rate patterns over the last 30 days and verify whether current burn rate represents a new issue or ongoing degradation, using error budget history and SLO metrics as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 24 hours for infrastructure changes, review API server capacity and limits, check for gradual performance degradation, verify external dependency health, examine historical error budget consumption patterns. API error budget burn may result from sustained high load, capacity limitations, or gradual performance degradation rather than immediate changes.
