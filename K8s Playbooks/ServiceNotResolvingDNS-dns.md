---
title: Service Not Resolving DNS - DNS
weight: 216
categories:
  - kubernetes
  - dns
---

# ServiceNotResolvingDNS-dns

## Meaning

Kubernetes service DNS resolution is failing (triggering KubeDNSDown or KubeDNSRequestsErrors alerts) because CoreDNS pods are not running, the kube-dns service is unavailable, DNS configuration is incorrect, or network policies are blocking DNS traffic. CoreDNS pods show CrashLoopBackOff or Failed state in kube-system namespace, DNS queries return errors, and CoreDNS logs show connection failures or configuration errors. This affects the DNS plane and prevents cluster-internal service discovery, typically caused by CoreDNS pod failures, NetworkPolicy restrictions, or DNS configuration issues; applications cannot connect to services by name.

## Impact

Service DNS names cannot be resolved; cluster-internal service discovery fails; applications cannot connect to services by name; DNS queries return errors; CoreDNS pods are not running; KubeDNSDown alerts fire; KubeDNSRequestsErrors alerts fire; service-to-service communication fails; applications cannot resolve service endpoints. CoreDNS pods show CrashLoopBackOff or Failed state indefinitely; DNS queries return errors; applications cannot connect to services by name and may show errors; service-to-service communication fails.

## Playbook

1. List pods in the kube-system namespace and check CoreDNS pod status to verify if DNS pods are running and ready.

2. Retrieve the kube-dns Service in the kube-system namespace and verify it exists and has endpoints to ensure DNS service is accessible.

3. Retrieve CoreDNS pod `<coredns-pod-name>` in namespace kube-system and inspect its status, logs, and events to identify why DNS is not functioning.

4. Check CoreDNS plugin status by executing `coredns -plugins` using Pod Exec tool in CoreDNS pod to verify if plugins are functioning correctly.

5. Check upstream DNS server availability by reviewing CoreDNS logs for upstream DNS connection failures or timeouts.

6. From a test pod, execute `nslookup <service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries using Pod Exec tool to test DNS resolution and verify if queries are working.

7. Check CoreDNS configuration by retrieving ConfigMap `coredns` in namespace kube-system and reviewing DNS server configuration and upstream server settings.

8. List NetworkPolicy objects in namespace kube-system and check if policies are blocking DNS traffic to or from CoreDNS pods.

## Diagnosis

1. Compare the DNS resolution failure timestamps with CoreDNS pod restart or crash timestamps, and check whether DNS pod failures occurred within 5 minutes before DNS resolution failures.

2. Compare the DNS resolution failure timestamps with upstream DNS server unavailability timestamps from CoreDNS logs, and check whether upstream DNS issues occurred within 5 minutes before DNS resolution failures.

3. Compare the DNS resolution failure timestamps with CoreDNS plugin failure timestamps, and check whether plugin failures occurred within 5 minutes before DNS resolution failures.

4. Compare the DNS resolution failure timestamps with CoreDNS configuration modification timestamps, and check whether DNS configuration changes occurred within 30 minutes before resolution failures.

5. Compare the DNS resolution failure timestamps with kube-dns service or endpoint modification timestamps, and check whether DNS service changes occurred within 10 minutes before resolution failures.

6. Compare the DNS resolution failure timestamps with NetworkPolicy creation or modification timestamps that may affect DNS traffic, and check whether policy changes occurred within 10 minutes before DNS failures.

7. Compare the DNS resolution failure timestamps with CoreDNS resource constraint or OOM kill timestamps, and check whether resource issues occurred within 5 minutes before DNS pod failures.

8. Compare the DNS resolution failure timestamps with cluster upgrade or CoreDNS deployment update timestamps, and check whether infrastructure changes occurred within 1 hour before DNS resolution failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review CoreDNS logs for gradual performance degradation, check for intermittent DNS query processing issues, examine if DNS configuration accumulated problems over time, verify if network path issues developed gradually, and check for DNS cache or query limit issues that may have accumulated. DNS resolution failures may result from gradual CoreDNS or infrastructure degradation rather than immediate changes.

