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

1. Describe pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, error rates, and any server-side issues affecting client connections.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for client errors, authentication failures, or rate limiting events.

3. Retrieve API client error metrics and identify which clients are experiencing high error rates exceeding 1% to determine the scope of the issue.

4. Retrieve the Pod `<pod-name>` in namespace `<namespace>` for client pods and check network connectivity between client pods and API server endpoints to verify connectivity issues.

5. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` experiencing errors and filter for API error patterns including 'connection refused', 'timeout', 'rate limited', 'authentication failed', 'authorization failed' to identify error causes.

6. Retrieve Secret resources containing client certificates and ServiceAccount resources for clients experiencing errors and verify client certificate and service account token validity to identify authentication issues.

7. Retrieve API server metrics for error rates and latency to determine if errors are client-side or server-side and identify root cause location.

8. Retrieve ResourceQuota resources in namespace `<namespace>` and FlowSchema resources and verify resource quota and rate limiting configurations that may affect client API access.

## Diagnosis

1. Analyze client error events from Playbook to identify error patterns and affected clients. If events show connection refused, timeout, or authentication errors, use event timestamps to determine when errors began and which clients are affected.

2. If events indicate API server issues (errors, latency), verify API server status from Playbook step 1. If API server events show problems at timestamps correlating with client errors, server-side issues are the root cause.

3. If events indicate authentication or certificate failures, verify client certificate and service account token validity from Playbook step 6. If certificate-related events show expiration or validation failures, authentication issues are causing client errors.

4. If events indicate rate limiting or flow control rejections, examine API server flow control metrics from Playbook step 8. If flow control events show rejections at client error timestamps, rate limiting is causing failures.

5. If events indicate network connectivity issues, verify network path from client to API server from Playbook step 4. If network events show failures or policy changes at error timestamps, network issues are the root cause.

6. If events show consistent error patterns (not intermittent), the issue is likely a configuration problem. If errors occur continuously at same rate, investigate client configuration, credentials, or API server capacity.

7. If events show intermittent error patterns, focus on transient causes. If errors correlate with specific time periods or operations, network instability, API server load, or resource contention may be the cause.

**If no correlation is found**: Extend timeframes to 1 hour for network changes, review client API usage patterns, check for API server capacity issues, verify client library versions, examine historical client error patterns. Client errors may result from network instability, API server capacity limitations, or client misconfigurations rather than immediate changes.
