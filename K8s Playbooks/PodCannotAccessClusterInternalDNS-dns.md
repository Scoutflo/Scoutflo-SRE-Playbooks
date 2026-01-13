---
title: Pod Cannot Access Cluster Internal DNS - DNS
weight: 284
categories:
  - kubernetes
  - dns
---

# PodCannotAccessClusterInternalDNS-dns

## Meaning

Pods cannot access cluster internal DNS (triggering KubeDNSDown or KubeDNSRequestsErrors alerts) because CoreDNS pods are not running, the kube-dns service is unavailable, DNS configuration is incorrect, network policies are blocking DNS traffic, or the pod's DNS configuration is misconfigured. Pods show DNS query failures, CoreDNS pods show CrashLoopBackOff or Failed state in kube-system namespace, and DNS queries return errors. This affects the DNS plane and prevents cluster-internal service discovery, typically caused by CoreDNS pod failures, NetworkPolicy restrictions, or DNS configuration issues; applications cannot connect to services by name.

## Impact

Pods cannot resolve service DNS names; cluster-internal service discovery fails; applications cannot connect to services by name; DNS queries fail; CoreDNS pods are not running or accessible; KubeDNSDown alerts fire; KubeDNSRequestsErrors alerts fire; service-to-service communication fails; applications cannot resolve service endpoints. Pods show DNS query failures indefinitely; CoreDNS pods show CrashLoopBackOff or Failed state; applications cannot connect to services by name and may show errors; service-to-service communication fails.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its DNS configuration in `spec.dnsPolicy` and `spec.dnsConfig` to verify DNS settings.

2. List pods in the kube-system namespace and check CoreDNS pod status to verify if DNS pods are running and ready.

3. Retrieve the kube-dns Service in the kube-system namespace and verify it exists and has endpoints to ensure DNS service is accessible.

4. From the pod `<pod-name>`, execute `nslookup <service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries using Pod Exec tool to test DNS resolution.

5. List NetworkPolicy objects in namespace `<namespace>` and namespace kube-system and check if policies are blocking DNS traffic to or from CoreDNS pods.

6. Retrieve CoreDNS pod `<coredns-pod-name>` in namespace kube-system and inspect its status, logs, and events to identify why DNS is not functioning.

## Diagnosis

1. Compare the pod DNS access failure timestamps with CoreDNS pod restart or crash timestamps, and check whether DNS pod failures occurred within 5 minutes before DNS access failures.

2. Compare the pod DNS access failure timestamps with pod DNS configuration modification timestamps, and check whether DNS policy or config changes occurred within 30 minutes before DNS access failures.

3. Compare the pod DNS access failure timestamps with NetworkPolicy creation or modification timestamps that may affect DNS traffic, and check whether policy changes occurred within 10 minutes before DNS access failures.

4. Compare the pod DNS access failure timestamps with kube-dns service or endpoint modification timestamps, and check whether DNS service changes occurred within 10 minutes before DNS access failures.

5. Compare the pod DNS access failure timestamps with CoreDNS configuration modification timestamps, and check whether DNS configuration changes occurred within 30 minutes before DNS access failures.

6. Compare the pod DNS access failure timestamps with cluster network plugin restart or failure timestamps, and check whether network infrastructure issues occurred within 1 hour before DNS access failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review CoreDNS logs for gradual performance degradation, check for intermittent DNS query processing issues, examine if DNS configuration accumulated problems over time, verify if network policies gradually restricted DNS access, and check for DNS cache or query limit issues that may have accumulated. DNS access failures may result from gradual CoreDNS or network infrastructure degradation rather than immediate changes.

