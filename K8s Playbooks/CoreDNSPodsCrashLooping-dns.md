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

1. Retrieve logs from CoreDNS pods in `kube-system` and look for configuration errors, upstream DNS lookup failures, or messages indicating resource exhaustion.

2. List pods in `kube-system` and filter for CoreDNS pods to check their current phase, readiness, and restart counts across the cluster.

3. Retrieve the CoreDNS ConfigMap in `kube-system` and review the Corefile for syntax correctness, plugin configuration, and upstream DNS server definitions.

4. Retrieve the CoreDNS Deployment in `kube-system` and inspect resource requests and limits to ensure pods have adequate CPU and memory.

5. From a test pod, run `nslookup` or `dig` for internal and external domains to verify in-cluster DNS resolution behavior.

6. From a test pod, run `nslookup` or `dig` queries directly against the configured upstream DNS servers to confirm they are reachable and responding correctly.

## Diagnosis

1. Compare the CoreDNS crash timestamps from pod status with CoreDNS ConfigMap modification timestamps, and check whether ConfigMap updates occurred within 30 minutes before the crashes.

2. Compare the CoreDNS crash timestamps with CoreDNS pod resource usage metrics and configured resource limits, and check whether CPU or memory usage was near or above limits at the time of crashes.

3. Compare the CoreDNS crash timestamps with CoreDNS Deployment modification timestamps, and check whether new deployments or rollouts occurred within 1 hour before crashes began.

4. Compare the CoreDNS crash timestamps with DNS query rate metrics (for example, QPS to CoreDNS) and check whether spikes in query volume align with periods of increased crashes.

5. Compare the CoreDNS crash timestamps with cluster upgrade or maintenance window timestamps, and check whether crashes started within 1 hour of upgrade or maintenance activities.

6. Compare the CoreDNS crash timestamps with NetworkPolicy modification timestamps affecting `kube-system` and upstream DNS connectivity test results, and check whether new policies or upstream DNS failures coincide within 10 minutes of the observed crash periods.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review CoreDNS logs for earlier configuration errors or warnings, check for gradual resource exhaustion patterns, examine DNS query rate trends for spikes that may have triggered crashes, verify if ConfigMap changes were applied gradually, and check upstream DNS server health over a longer period. DNS issues may have cascading effects that manifest after initial problems.

