---
title: Kube Client Errors
weight: 20
---

# KubeClientErrors

## Meaning

Kubernetes API server client is experiencing over 1% error rate in the last 15 minutes (triggering KubeClientErrors alerts) because API client requests are failing due to network issues, authentication problems, rate limiting, or API server errors. Client logs show connection refused, timeout, rate limited, or authentication failed errors, API client metrics show error rates exceeding 1%, and API operations fail intermittently. This affects the workload and control plane and indicates client-side or server-side issues preventing reliable API communication, typically caused by network connectivity problems, certificate expiration, rate limiting, or API server capacity issues; applications using Kubernetes API may show errors.

## Impact

KubeClientErrors alerts fire; specific Kubernetes client may malfunction; service degradation; API operations fail intermittently; controllers may fail to reconcile; applications using Kubernetes API experience errors; client-side retries may exhaust; API request failures occur; client error rates exceed 1% threshold; cluster operations become unreliable for affected clients. Client logs show connection refused, timeout, or authentication failed errors; API operations fail intermittently; applications using Kubernetes API may experience errors or performance degradation.

## Playbook

1. Retrieve API client error metrics and identify which clients are experiencing high error rates exceeding 1% to determine the scope of the issue.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` for client pods and check network connectivity between client pods and API server endpoints to verify connectivity issues.

3. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` experiencing errors and filter for API error patterns including 'connection refused', 'timeout', 'rate limited', 'authentication failed', 'authorization failed' to identify error causes.

4. Retrieve Secret resources containing client certificates and ServiceAccount resources for clients experiencing errors and verify client certificate and service account token validity to identify authentication issues.

5. Retrieve API server metrics for error rates and latency to determine if errors are client-side or server-side and identify root cause location.

6. Retrieve ResourceQuota resources in namespace `<namespace>` and FlowSchema resources and verify resource quota and rate limiting configurations that may affect client API access.

## Diagnosis

Compare client error rate increase timestamps with API server error or latency spike times within 5 minutes and verify whether client errors coincide with API server issues, using API server metrics and client error logs as supporting evidence.

Correlate client error timestamps with network policy or firewall rule change times within 10 minutes and verify whether network configuration changes caused connectivity issues, using network policy events and client connection logs as supporting evidence.

Compare client error patterns with certificate expiration or authentication failure times within 2 minutes and verify whether authentication issues caused client errors, using certificate metadata and authentication logs as supporting evidence.

Analyze client error patterns over the last 15 minutes to determine if errors are consistent (configuration issue) or intermittent (network issues), using client error logs and API server metrics as supporting evidence.

Correlate client errors with API server rate limiting or flow control rejection timestamps within 5 minutes and verify whether rate limiting caused client errors, using API server flow control metrics and client error logs as supporting evidence.

Compare client resource requests with actual resource usage at error times and verify whether resource constraints caused client failures, using pod metrics and client resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for network changes, review client API usage patterns, check for API server capacity issues, verify client library versions, examine historical client error patterns. Client errors may result from network instability, API server capacity limitations, or client misconfigurations rather than immediate changes.
