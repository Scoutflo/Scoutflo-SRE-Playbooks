---
title: CoreDNS Down
weight: 10
categories: [kubernetes, dns]
---

# CoreDNSDown

## Meaning

CoreDNS pods are not running or not responding (triggering alerts like CoreDNSDown or KubeDNSDown) because the DNS service is experiencing failures due to pod crashes, resource exhaustion, configuration errors, or node issues. CoreDNS deployment shows zero or insufficient ready replicas in kubectl, DNS resolution fails cluster-wide, pods across all namespaces show 'connection refused' or 'no such host' errors in logs, and application logs show DNS lookup failures. This affects the cluster DNS layer and indicates critical infrastructure failure typically caused by resource constraints, configuration errors, node failures, or network issues; applications cannot resolve service names or external domains; new pods may fail to start if they depend on DNS resolution during initialization.

## Impact

CoreDNSDown alerts fire; all DNS resolution fails cluster-wide; pods cannot resolve service names; applications show 'no such host' errors in logs; external domain resolution fails; kubectl exec and logs may fail if they rely on DNS; new pod deployments may hang in ContainerCreating state; service mesh communication breaks; health checks depending on DNS fail; database connections fail with hostname resolution errors; API calls to external services timeout with DNS errors. Application errors increase dramatically; cascading failures occur across all namespaces; service endpoints become unreachable; ingress controllers cannot resolve backend services; entire application stack may become unavailable.

## Playbook

1. Retrieve the CoreDNS Deployment in namespace `kube-system` and verify the number of ready replicas, checking if replicas are 0 or below desired count to confirm DNS service is down.

2. Retrieve all CoreDNS pods in namespace `kube-system` and inspect their status, restart counts, and node placement to identify which pods are failing and where, filtering for status patterns including 'CrashLoopBackOff', 'Pending', 'Error', 'OOMKilled'.

3. Retrieve events for CoreDNS pods in namespace `kube-system` and filter for error patterns including 'Failed', 'Error', 'OOMKilled', 'Evicted', 'FailedScheduling', 'BackOff' to identify pod lifecycle issues.

4. Retrieve logs from CoreDNS pods in namespace `kube-system` and filter for error patterns including 'SERVFAIL', 'NXDOMAIN', 'connection refused', 'plugin/errors', 'context deadline exceeded', 'i/o timeout' to identify DNS-specific errors.

5. Retrieve the CoreDNS ConfigMap (coredns or kube-dns) in namespace `kube-system` and verify the Corefile configuration for syntax errors, missing plugins, or misconfigured upstream resolvers.

6. Retrieve the nodes where CoreDNS pods are scheduled and verify node conditions including Ready, MemoryPressure, DiskPressure, NetworkUnavailable to identify node-level issues affecting DNS pods.

7. Execute 'nslookup kubernetes.default.svc.cluster.local' using Pod Exec tool in a running pod to test DNS resolution against the kube-dns service IP and verify if DNS is completely down or partially degraded.

## Diagnosis

Analyze CoreDNS pod events from Playbook step 3 to identify the primary failure reason. If events indicate 'OOMKilled' with exit code 137, correlate pod termination timestamps with memory usage metrics within 5 minutes and verify whether pods are being killed due to memory limits being too low, using container memory metrics and pod resource specifications as supporting evidence.

If events indicate 'FailedScheduling' with messages like 'node(s) had taints' or 'Insufficient cpu/memory', compare pod scheduling timestamps with node available resources and verify whether scheduling constraints or resource exhaustion prevent CoreDNS pods from running, using node allocatable resources and pod tolerations as supporting evidence.

Compare CoreDNS pod termination timestamps with node condition transition times within 5 minutes and verify whether DNS failures coincide with node failures or network unavailable conditions, using node events and pod scheduling history as supporting evidence.

Correlate CoreDNS configuration changes (ConfigMap modification timestamps) with DNS failure timestamps within 5 minutes and verify whether a Corefile syntax error or misconfigured upstream resolver caused the outage, using ConfigMap revision history and controller logs as supporting evidence.

If CoreDNS pods show 'Pending' state, analyze pod events for affinity, toleration, or resource constraint violations and verify whether node selector or anti-affinity rules prevent scheduling, using pod spec and node labels as supporting evidence.

If no correlation is found within the specified time windows: verify cluster networking (CNI) is functioning correctly by checking CNI pod status, check if kube-proxy is running on all nodes, verify ServiceAccount and RBAC permissions for CoreDNS, examine underlying node networking for interface errors, check for NetworkPolicy rules blocking DNS traffic on port 53 UDP/TCP.
