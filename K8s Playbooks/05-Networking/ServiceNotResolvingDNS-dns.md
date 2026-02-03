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

1. Describe CoreDNS pods in `kube-system` namespace using `kubectl describe pod -n kube-system -l k8s-app=kube-dns` to inspect pod details, conditions, status, and recent events.

2. Retrieve events in `kube-system` namespace using `kubectl get events -n kube-system --field-selector involvedObject.name=coredns --sort-by='.metadata.creationTimestamp'` to identify recent CoreDNS-related events and issues.

3. Retrieve the kube-dns Service in the kube-system namespace and verify it exists and has endpoints to ensure DNS service is accessible.

4. Retrieve CoreDNS pod logs in namespace kube-system and inspect for errors to identify why DNS is not functioning.

5. Check CoreDNS plugin status by executing `coredns -plugins` using Pod Exec tool in CoreDNS pod to verify if plugins are functioning correctly.

6. Check upstream DNS server availability by reviewing CoreDNS logs for upstream DNS connection failures or timeouts.

7. From a test pod, execute `nslookup <service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries using Pod Exec tool to test DNS resolution and verify if queries are working.

8. Check CoreDNS configuration by retrieving ConfigMap `coredns` in namespace kube-system and reviewing DNS server configuration and upstream server settings.

9. List NetworkPolicy objects in namespace kube-system and check if policies are blocking DNS traffic to or from CoreDNS pods.

## Diagnosis

Begin by analyzing the events and CoreDNS status collected in the Playbook section. CoreDNS pod state, kube-dns service endpoints, and DNS query test results provide the primary diagnostic signals.

**If CoreDNS pods show CrashLoopBackOff or are not Ready:**
- The DNS service is down. Check the pod termination reason from describe output. If OOMKilled, increase memory limits. If configuration errors appear in logs, review the Corefile in ConfigMap `coredns`.

**If kube-dns service exists but shows no endpoints:**
- CoreDNS pods are not registered with the service. Verify pods have the label `k8s-app=kube-dns` and are in Ready state. Check if the service selector matches the pod labels.

**If CoreDNS logs show SERVFAIL or NXDOMAIN for cluster domains:**
- CoreDNS cannot resolve the requested service. Verify the service exists in the specified namespace. Check that the service has a valid ClusterIP and is not headless without endpoints.

**If CoreDNS logs show upstream connection failures:**
- External DNS resolution fails, which may affect cluster DNS if plugins are chained. Verify upstream DNS servers in the Corefile are reachable. This typically affects external domain resolution, not cluster-internal services.

**If DNS queries work from CoreDNS pod but fail from other pods:**
- Network path to CoreDNS is blocked. Check NetworkPolicies in kube-system that might restrict ingress. Verify the CNI plugin is functioning on nodes where failing pods run.

**If the service exists but nslookup returns the wrong IP or no result:**
- DNS cache may contain stale entries, or the service was recently modified. Check if service ClusterIP changed recently. CoreDNS caches may take time to update.

**If events are inconclusive, correlate timestamps:**
1. Check if resolution failures began after CoreDNS pod restarts by matching failure times with pod restart timestamps.
2. Check if the CoreDNS ConfigMap was recently modified by examining the ConfigMap resource version.
3. Check if cluster upgrades occurred that might have affected CoreDNS by reviewing cluster events.

**If no clear cause is identified:** Test DNS resolution for multiple services to determine if the issue is service-specific or cluster-wide. Check CoreDNS metrics for query success/failure rates if metrics are available.

