---
title: Nginx Ingress 5xx Errors High
weight: 51
categories: [kubernetes, ingress]
---

# NginxIngress5xxErrorsHigh

## Meaning

Nginx Ingress is returning high rate of 5xx server errors (triggering NginxIngress5xxErrorsHigh, NginxIngressHighErrorRate alerts) because backend services are failing, unavailable, or timing out. Ingress metrics show elevated 5xx responses, users experience server errors, and backend service health is degraded. This affects user experience and service reliability; requests are failing; SLO violations occur; customer impact is significant.

## Impact

NginxIngress5xxErrorsHigh alerts fire; users see 500, 502, 503, or 504 errors; API calls fail; application functionality is broken; mobile apps fail; integrations break; customer complaints increase; revenue is affected; SLA violations may occur; error rate SLOs are breached.

## Playbook

1. Retrieve ingress controller metrics and identify which backend services are generating 5xx errors.

2. Analyze error breakdown by HTTP status code (500=server error, 502=bad gateway, 503=service unavailable, 504=gateway timeout).

3. Check backend service pod health and readiness for services returning errors.

4. Retrieve ingress controller logs filtered by the affected ingress and look for upstream connection failures.

5. Verify backend service endpoints exist and pods are in Ready state.

6. Check backend pod logs for application errors causing 500 responses.

7. Verify ingress annotations for timeout settings and proxy behavior.

## Diagnosis

Analyze error code distribution: 502 indicates backend connection failures, 503 indicates no healthy backends, 504 indicates timeout, 500 indicates application errors, using error code metrics as supporting evidence.

For 502 errors, verify backend pods are running and network connectivity exists between ingress and backend, using pod status and network tests as supporting evidence.

For 503 errors, check service endpoints and verify pods are Ready (passing readiness probes), using endpoint status and pod readiness as supporting evidence.

For 504 errors, verify backend response times and check if ingress timeout settings are appropriate, using latency metrics and ingress annotations as supporting evidence.

For 500 errors, investigate backend application logs for exceptions and errors, using application logs and error patterns as supporting evidence.

If no correlation is found within the specified time windows: check for deployment rollout issues, verify configuration changes to backends, check database or dependency availability, review application releases, consider rolling back recent changes.
