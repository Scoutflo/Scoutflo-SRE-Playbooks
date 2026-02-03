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

1. Describe the pod `<pod-name>` in namespace `<namespace>` using `kubectl describe pod <pod-name> -n <namespace>` to inspect its DNS configuration in `spec.dnsPolicy` and `spec.dnsConfig`, and review pod conditions and events.

2. Retrieve events for the pod using `kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name> --sort-by='.metadata.creationTimestamp'` to identify recent events related to DNS access issues.

3. List pods in the kube-system namespace and check CoreDNS pod status to verify if DNS pods are running and ready.

4. Retrieve the kube-dns Service in the kube-system namespace and verify it exists and has endpoints to ensure DNS service is accessible.

5. From the pod `<pod-name>`, execute `nslookup <service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries using Pod Exec tool to test DNS resolution.

6. List NetworkPolicy objects in namespace `<namespace>` and namespace kube-system and check if policies are blocking DNS traffic to or from CoreDNS pods.

7. Retrieve CoreDNS pod logs in namespace kube-system and inspect for errors to identify why DNS is not functioning.

## Diagnosis

Begin by analyzing the pod describe output and events collected in the Playbook section. The pod's DNS configuration, CoreDNS pod status, and kube-dns service state provide the primary diagnostic signals.

**If pod describe shows dnsPolicy: None or custom dnsConfig:**
- The pod has custom DNS settings that may be misconfigured. Verify that `dnsConfig.nameservers` includes the kube-dns service IP (typically 10.96.0.10). If dnsPolicy is None, all DNS settings must be explicitly provided.

**If CoreDNS pods in kube-system are not Running or Ready:**
- Cluster DNS service is unavailable. This is the root cause. Investigate CoreDNS pod failures separately using the CoreDNSPodsCrashLooping playbook before continuing.

**If kube-dns service has no endpoints:**
- The DNS service exists but has no backend pods. Check if CoreDNS pods exist and are labeled correctly with `k8s-app=kube-dns`. Verify CoreDNS Deployment replicas are not scaled to zero.

**If NetworkPolicies exist in the pod's namespace or kube-system:**
- Network policies may block DNS traffic. Check if policies allow egress to kube-dns service on port 53 (UDP and TCP). Check if kube-system policies allow ingress from the pod's namespace.

**If DNS queries from the pod time out but CoreDNS is healthy:**
- Network connectivity between the pod and CoreDNS is blocked. Verify the pod's node has network connectivity to CoreDNS pod nodes. Check CNI plugin status on both nodes.

**If events are inconclusive, correlate timestamps:**
1. Check if DNS failures began after the pod was created with a specific DNS policy by examining pod creation time and DNS configuration.
2. Check if failures correlate with NetworkPolicy changes by comparing failure onset with policy creation timestamps.
3. Check if the kube-dns service or endpoints were modified by examining service resource version changes.

**If no clear cause is identified:** Create a debug pod in the same namespace with default DNS settings to isolate whether the issue is pod-specific or namespace-wide. Test DNS resolution to both cluster services and external domains.

