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

1. List CoreDNS pods in the kube-system namespace and check their status, resource usage, and restart counts to verify if pods are experiencing issues.

2. Retrieve logs from CoreDNS pods in namespace kube-system and filter for timeout errors, query failures, or performance issues.

3. From test pods, execute repeated DNS queries using `nslookup` or `dig` via Pod Exec tool to test DNS resolution patterns and identify intermittent failures.

4. Check CoreDNS configuration by retrieving ConfigMap `coredns` in namespace kube-system and reviewing DNS server settings, cache configuration, and upstream server configuration.

5. Monitor CoreDNS pod resource usage metrics to verify if CPU or memory constraints are causing performance issues.

6. List events in namespace kube-system and filter for CoreDNS-related events over time to identify patterns in DNS issues.

## Diagnosis

1. Compare the DNS resolution failure timestamps with CoreDNS pod resource usage spike timestamps, and check whether high CPU or memory usage occurred within 5 minutes of DNS failures.

2. Compare the DNS resolution failure timestamps with CoreDNS configuration modification timestamps, and check whether configuration changes occurred within 30 minutes before intermittent failures.

3. Compare the DNS resolution failure timestamps with cluster workload increase or scaling event timestamps, and check whether DNS load increased within 30 minutes before failures.

4. Compare the DNS resolution failure timestamps with NetworkPolicy modification timestamps that may affect DNS traffic, and check whether policy changes occurred intermittently within 10 minutes before DNS failures.

5. Compare the DNS resolution failure timestamps with CoreDNS pod restart or crash timestamps, and check whether pod instability occurred within 5 minutes before DNS failures.

6. Compare the DNS resolution failure timestamps with upstream DNS server unavailability timestamps, and check whether external DNS issues occurred within 10 minutes before DNS failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes), review CoreDNS logs for gradual performance degradation patterns, check for intermittent network connectivity issues, examine if DNS query load gradually increased over time, verify if CoreDNS resource constraints developed gradually, and check for DNS cache or query limit issues that may occur intermittently. Intermittent DNS resolution failures may result from cumulative load or infrastructure instability rather than immediate changes.

