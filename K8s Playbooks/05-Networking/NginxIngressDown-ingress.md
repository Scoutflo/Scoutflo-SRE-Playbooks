---
title: Nginx Ingress Down
weight: 50
categories: [kubernetes, ingress]
---

# NginxIngressDown

## Meaning

Nginx Ingress Controller is not running or not responding (triggering NginxIngressDown, NginxIngressControllerDown alerts) because the ingress controller pods are crashing, not scheduled, or not healthy. Ingress controller deployment shows zero ready replicas, no ingress traffic is being routed, and all HTTP/HTTPS endpoints are unreachable. This affects all ingress-routed traffic; external access to services is blocked; the cluster is effectively offline to external users.

## Impact

NginxIngressDown alerts fire; all ingress traffic stops; external users cannot access any service; HTTP and HTTPS endpoints return connection refused or timeout; load balancer health checks fail; DNS-based failover may trigger; complete service outage for ingress-routed applications; revenue loss for customer-facing services.

## Playbook

1. Retrieve the ingress-nginx deployment in the ingress-nginx namespace and verify replica status.

2. Check ingress controller pod status, restart count, and events for failure reasons.

3. Retrieve ingress controller logs for configuration errors or runtime failures.

4. Verify ConfigMap configuration for nginx is valid and not corrupted.

5. Check for resource constraints (CPU, memory) preventing pod operation.

6. Verify the LoadBalancer or NodePort service is correctly exposing the controller.

7. Check if admission webhook failures are preventing controller operation.

## Diagnosis

Analyze controller pod status and identify if pods are CrashLooping (configuration error), Pending (scheduling issue), or terminated (resource issue), using pod status and events as supporting evidence.

Check nginx configuration validity by looking for configuration reload errors in logs, using controller logs and nginx error messages as supporting evidence.

Verify ingress resources don't have invalid configurations that cause controller to fail on reload, using recent ingress changes and configuration validation as supporting evidence.

Check for OOMKilled events if controller memory is insufficient for the number of ingress routes, using container status and memory metrics as supporting evidence.

Verify admission webhook is healthy as webhook failures can block ingress updates and potentially controller operation, using webhook pod status and API server logs as supporting evidence.

If no correlation is found within the specified time windows: roll back recent ingress configuration changes, restart controller pods, increase resource limits, check for conflicting ingress resources, verify LoadBalancer service is provisioned correctly.
