---
title: CoreDNS Latency High
weight: 11
categories: [kubernetes, dns]
---

# CoreDNSLatencyHigh

## Meaning

CoreDNS is experiencing high query latency (triggering CoreDNSLatencyHigh alerts) because DNS requests are taking longer than expected to resolve, typically due to upstream resolver delays, high query volume, resource constraints, or network issues. CoreDNS metrics show DNS request duration exceeding normal thresholds (usually > 1 second), application response times increase, and service-to-service communication slows down. This affects the cluster networking layer and indicates DNS performance degradation that impacts all applications depending on DNS resolution; database connections take longer to establish; API calls experience increased latency; overall application performance degrades.

## Impact

CoreDNSLatencyHigh alerts fire; application response times increase; service-to-service communication slows; database connection establishment takes longer; API calls to external services time out; health checks may fail due to DNS delays; pod startup times increase; user-facing latency increases; SLO violations may occur; timeout errors increase in application logs; connection pools may exhaust waiting for DNS; application throughput decreases.

## Playbook

1. Retrieve CoreDNS pods in namespace `kube-system` and verify CPU and memory utilization to check if DNS pods are resource-constrained.

2. Retrieve CoreDNS metrics (coredns_dns_request_duration_seconds) and identify which DNS query types (A, AAAA, SRV) and zones are experiencing high latency.

3. Retrieve logs from CoreDNS pods in namespace `kube-system` and filter for slow query patterns including 'duration', 'timeout', 'SERVFAIL' to identify specific domains or query patterns causing delays.

4. Retrieve the CoreDNS ConfigMap in namespace `kube-system` and verify the forward plugin configuration including upstream DNS servers and their health check settings.

5. Test DNS resolution latency from a running pod using time-based DNS queries to kube-dns service to measure actual resolution times for internal vs external domains.

6. Retrieve node network metrics for nodes hosting CoreDNS pods and verify network latency, packet loss, and interface errors that could affect DNS performance.

7. Check CoreDNS horizontal pod autoscaler (if configured) and verify if additional replicas are needed to handle query load.

## Diagnosis

Compare CoreDNS CPU utilization with query latency metrics and verify whether latency increases correlate with CPU saturation (> 80%), using pod resource metrics and DNS request rate as supporting evidence.

Correlate upstream DNS server response times with CoreDNS latency spikes and verify whether external DNS resolution is causing delays, using forward plugin metrics and upstream server health as supporting evidence.

Analyze DNS query patterns to identify if specific domains or query types (AAAA queries for IPv6, external domains) are causing disproportionate latency, using DNS query logs and response type breakdown as supporting evidence.

Compare CoreDNS pod count with DNS query rate and verify whether insufficient replicas are causing query queuing and latency, using HPA metrics and pod ready count as supporting evidence.

Check for NDOTS configuration issues in pods (default ndots:5 causes excessive search domain queries) that multiply DNS queries and increase overall latency, using pod DNS configuration and query patterns as supporting evidence.

If no correlation is found within the specified time windows: verify network connectivity to upstream DNS servers, check for firewall rules blocking or rate-limiting DNS traffic, examine CoreDNS cache hit rates, verify no DNS amplification or loop conditions exist, check for negative cache TTL issues causing repeated failed lookups.
