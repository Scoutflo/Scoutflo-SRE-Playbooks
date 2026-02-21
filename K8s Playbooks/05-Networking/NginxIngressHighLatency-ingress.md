---
title: Nginx Ingress High Latency
weight: 52
categories: [kubernetes, ingress]
---

# NginxIngressHighLatency

## Meaning

Nginx Ingress is experiencing high request latency (triggering NginxIngressHighLatency, IngressHighLatency alerts) because requests are taking longer than expected to complete, indicating backend slowness, ingress resource constraints, or network issues. Ingress metrics show elevated response times, users experience slow page loads, and SLO latency thresholds are breached. This affects user experience; application feels slow; timeout errors may increase; customer satisfaction decreases.

## Impact

NginxIngressHighLatency alerts fire; user-facing response times increase; page load times are slow; API responses are delayed; timeout errors may occur; user experience degrades; bounce rates increase; SLO violations occur; downstream systems may timeout waiting for responses; cascading delays across service mesh.

## Playbook

1. Retrieve ingress controller latency metrics and identify which backend services have highest latency.

2. Analyze latency breakdown: time spent in ingress vs time spent in backend (upstream_response_time).

3. Check backend service pod performance and resource utilization.

4. Verify ingress controller pod CPU and memory utilization for resource constraints.

5. Check for connection queuing at ingress level indicating capacity issues.

6. Verify backend service horizontal scaling is adequate for load.

7. Check network latency between ingress pods and backend services.

## Diagnosis

Compare ingress processing time with upstream response time to determine if latency is in ingress or backend, using nginx timing metrics as supporting evidence.

If upstream latency is high, investigate backend service performance (CPU, memory, dependencies), using backend metrics and application profiling as supporting evidence.

If ingress processing time is high, check ingress controller resource utilization and connection handling capacity, using controller metrics and pod resources as supporting evidence.

Correlate latency with traffic volume and verify whether latency increases with load indicating capacity issues, using traffic metrics and latency correlation as supporting evidence.

Check for slow-responding backends holding connections and affecting other requests due to connection pool exhaustion, using connection metrics and timeout configurations as supporting evidence.

If no correlation is found within the specified time windows: scale backend services, increase ingress controller resources, optimize backend application performance, add caching layers, review database query performance, consider CDN for static content.
