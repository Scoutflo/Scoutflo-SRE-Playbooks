---
title: Nginx Ingress 4xx Errors High
weight: 53
categories: [kubernetes, ingress]
---

# NginxIngress4xxErrorsHigh

## Meaning

Nginx Ingress is returning high rate of 4xx client errors (triggering NginxIngress4xxErrorsHigh alerts) because clients are making invalid requests, authentication is failing, or resources are not found. Ingress metrics show elevated 4xx responses, which may indicate configuration issues, broken client integrations, or attack traffic. This affects client success rate and may indicate security scanning, misconfigured clients, or routing issues.

## Impact

NginxIngress4xxErrorsHigh alerts fire; client requests are failing; API integrations may be broken; mobile apps may malfunction; authentication failures affect user access; 404 errors indicate missing routes; 403 errors indicate authorization issues; potential security scanning activity; client-side debugging needed; customer complaints may increase.

## Playbook

1. Retrieve ingress controller metrics and identify the breakdown of 4xx status codes (400, 401, 403, 404, 429).

2. Identify which ingress resources or backend paths are generating the most 4xx errors.

3. Retrieve ingress controller access logs filtered by 4xx status codes to see request patterns.

4. For 401/403 errors: verify authentication and authorization configuration in ingress annotations.

5. For 404 errors: verify ingress routing rules match expected paths and backend services exist.

6. For 429 errors: check rate limiting configuration and identify clients being throttled.

7. Check for unusual client IP patterns that may indicate scanning or attack traffic.

## Diagnosis

Analyze 4xx error breakdown: 400=bad request, 401=unauthorized, 403=forbidden, 404=not found, 429=rate limited, using status code distribution as supporting evidence.

For 404 spikes, correlate with recent ingress or deployment changes that may have changed routing, using ingress modification timestamps and path analysis as supporting evidence.

For 401/403 increases, check authentication service health and configuration changes, using auth service logs and ingress auth annotations as supporting evidence.

Check client IP distribution to identify if errors come from specific clients (misconfigured integration) or many clients (ingress issue), using access logs and IP analysis as supporting evidence.

Compare with normal 4xx baseline to distinguish between normal invalid requests and anomalous increase, using historical error rates as supporting evidence.

If no correlation is found within the specified time windows: review API documentation for client-side errors, check for bot or scanner traffic, verify DNS changes haven't redirected traffic incorrectly, review authentication provider configuration, consider implementing request validation.
