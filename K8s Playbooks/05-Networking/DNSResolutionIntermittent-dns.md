---
title: DNS Resolution Intermittent - DNS
weight: 259
categories:
  - kubernetes
  - dns
---

# DNSResolutionIntermittent-dns

## Meaning

DNS resolution is intermittently failing (triggering KubeDNSRequestsErrors alerts) because CoreDNS pods are experiencing high load, CoreDNS configuration is suboptimal, DNS query timeouts occur, or network policies intermittently block DNS traffic. DNS queries work sometimes but fail at other times, CoreDNS pods may show high resource usage, and DNS query timeouts occur intermittently. This affects the DNS plane and causes unreliable service discovery, typically caused by CoreDNS performance issues or NetworkPolicy restrictions; applications experience sporadic DNS errors.

## Impact

DNS resolution fails intermittently; service discovery is unreliable; applications experience sporadic DNS errors; KubeDNSRequestsErrors alerts fire intermittently; service-to-service communication fails randomly; DNS query timeouts occur; CoreDNS pods may be overloaded; cluster DNS performance is degraded. DNS queries fail intermittently; CoreDNS pods may show high resource usage; applications experience sporadic DNS errors and may show errors; service-to-service communication fails randomly.

## Playbook

1. Describe CoreDNS pods in `kube-system` namespace using `kubectl describe pod -n kube-system -l k8s-app=kube-dns` to inspect pod details, conditions, resource usage, and restart counts.

2. Retrieve events in `kube-system` namespace using `kubectl get events -n kube-system --field-selector involvedObject.name=coredns --sort-by='.metadata.creationTimestamp'` to identify CoreDNS-related events and patterns over time.

3. Retrieve logs from CoreDNS pods in namespace kube-system and filter for timeout errors, query failures, or performance issues.

4. From test pods, execute repeated DNS queries using `nslookup` or `dig` via Pod Exec tool to test DNS resolution patterns and identify intermittent failures.

5. Check CoreDNS configuration by retrieving ConfigMap `coredns` in namespace kube-system and reviewing DNS server settings, cache configuration, and upstream server configuration.

6. Monitor CoreDNS pod resource usage metrics to verify if CPU or memory constraints are causing performance issues.

## Diagnosis

Begin by analyzing the events and pod status collected in the Playbook section. CoreDNS pod conditions, resource usage, and repeated DNS query test results provide the primary diagnostic signals.

**If pod describe shows high restart counts or recent restarts:**
- CoreDNS pod instability is causing intermittent failures. Examine the termination reason from the previous container state. If OOMKilled, increase memory limits. If Error, check logs for the specific failure cause.

**If CoreDNS logs show timeout errors to upstream DNS servers:**
- Upstream DNS connectivity is unreliable. Test upstream DNS servers directly from a debug pod. Check for intermittent network issues or upstream server overload. Consider adding multiple upstream servers for redundancy.

**If CoreDNS logs show high query latency or queue overflow messages:**
- CoreDNS is overloaded. Check CPU usage from pod metrics. If near limits, increase CPU requests/limits or scale CoreDNS replicas horizontally.

**If DNS test queries fail only for specific domains:**
- The issue is domain-specific, not a general CoreDNS problem. Check if the domain exists in cluster DNS, verify the service and endpoints exist, and confirm the service is in a Ready state.

**If DNS queries succeed from CoreDNS pod but fail from application pods:**
- Network path between application pods and CoreDNS is affected. Check for NetworkPolicies that intermittently block DNS traffic (port 53 UDP/TCP). Verify kube-dns service endpoints are populated.

**If events are inconclusive, correlate timestamps:**
1. Check if intermittent failures align with CoreDNS pod restarts by matching failure timestamps with pod restart times from describe output.
2. Check if failures correlate with cluster scaling events that increased DNS query load.
3. Check if failures occur during specific time windows that might indicate scheduled jobs or cron workloads.

**If no clear cause is identified:** Increase CoreDNS replicas to improve availability, review DNS cache configuration for optimization opportunities, and monitor DNS query latency over an extended period to identify patterns.

