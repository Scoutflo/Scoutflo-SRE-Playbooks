---
title: CoreDNS Pods CrashLooping - DNS
weight: 276
categories:
  - kubernetes
  - dns
---

# CoreDNSPodsCrashLooping-dns

## Meaning

CoreDNS pods are repeatedly crashing or restarting (triggering KubePodCrashLooping or KubeDNSDown alerts) because of invalid DNS configuration, missing upstream dependencies, insufficient compute resources, or Corefile syntax errors, which breaks in-cluster service name resolution and DNS query processing.

## Impact

DNS resolution fails across cluster; service discovery breaks; pods cannot resolve service names; applications fail to connect to services; cluster networking becomes unreliable; KubeDNSRequestsErrors alerts fire; CoreDNS pods in CrashLoopBackOff state; DNS query failures occur; service endpoints become unresolvable.

## Playbook

1. Describe CoreDNS pods in `kube-system` namespace using `kubectl describe pod -n kube-system -l k8s-app=kube-dns` to inspect pod details, conditions, restart counts, and recent events.

2. Retrieve events in `kube-system` namespace using `kubectl get events -n kube-system --field-selector involvedObject.name=coredns --sort-by='.metadata.creationTimestamp'` to identify recent CoreDNS-related events and issues.

3. Retrieve logs from CoreDNS pods in `kube-system` and look for configuration errors, upstream DNS lookup failures, or messages indicating resource exhaustion.

4. Retrieve the CoreDNS ConfigMap in `kube-system` and review the Corefile for syntax correctness, plugin configuration, and upstream DNS server definitions.

5. Retrieve the CoreDNS Deployment in `kube-system` and inspect resource requests and limits to ensure pods have adequate CPU and memory.

6. From a test pod, run `nslookup` or `dig` for internal and external domains to verify in-cluster DNS resolution behavior.

7. From a test pod, run `nslookup` or `dig` queries directly against the configured upstream DNS servers to confirm they are reachable and responding correctly.

## Diagnosis

Begin by analyzing the events collected in the Playbook section. The pod describe output and namespace events provide the primary diagnostic signals.

**If events show OOMKilled or memory-related termination reasons:**
- CoreDNS pods are being terminated due to memory exhaustion. Check resource limits in the Deployment and compare with actual memory usage from logs. Increase memory limits or reduce cache size in Corefile.

**If events show CrashLoopBackOff with Corefile parsing errors in logs:**
- The CoreDNS configuration contains syntax errors. Review the ConfigMap `coredns` for invalid plugin configurations, missing braces, or incorrect upstream server definitions. Validate Corefile syntax before applying.

**If events show connection refused or timeout errors to upstream DNS:**
- CoreDNS cannot reach upstream DNS servers. Verify upstream server IPs in the Corefile are correct and reachable. Check if NetworkPolicies in `kube-system` are blocking egress to upstream DNS ports.

**If events show plugin initialization failures:**
- A CoreDNS plugin failed to start. Check logs for the specific plugin name and error. Common causes include missing dependencies, invalid plugin configuration, or incompatible plugin versions after upgrades.

**If events show readiness probe failures without crash reasons:**
- CoreDNS is starting but failing health checks. Compare the probe configuration in the Deployment with CoreDNS startup time. Check if resource constraints are causing slow startup.

**If events are inconclusive, correlate timestamps:**
1. Check if CoreDNS crashes began shortly after ConfigMap modifications by comparing crash timestamps with ConfigMap `metadata.resourceVersion` changes.
2. Check if crashes correlate with Deployment rollouts by examining the Deployment revision history and rollout timestamps.
3. Check if crashes align with cluster-wide DNS query spikes by reviewing query rate patterns in CoreDNS logs.

**If no clear cause is identified:** Review CoreDNS logs for warnings that preceded the first crash, check for gradual memory growth patterns indicating leaks, and verify upstream DNS server health over the crash period.

