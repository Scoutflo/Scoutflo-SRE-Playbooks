---
title: Network Policy Blocking Traffic - Network
weight: 295
categories:
  - kubernetes
  - network
---

# NetworkPolicyBlockingTraffic-network

## Meaning

NetworkPolicy resources are unintentionally blocking traffic (triggering KubePodNotReady or KubeServiceNotReady alerts) because policy rules are too restrictive, ingress or egress rules do not allow required traffic, policy pod selectors do not match intended pods, or default deny policies are blocking legitimate traffic. Pods show connection failures, NetworkPolicy resources show restrictive rules, and pod events may show NetworkPolicyDenied errors. This affects the network plane and prevents pods from communicating when they should be allowed, typically caused by overly restrictive NetworkPolicy rules or selector mismatches; applications cannot access dependencies and may show errors.

## Impact

Legitimate traffic is blocked; pods cannot communicate as required; applications fail due to network restrictions; service-to-service communication is blocked; ingress or egress traffic is denied; KubePodNotReady alerts fire when pods cannot communicate and become unready; KubeServiceNotReady alerts fire when services cannot route traffic due to network policy blocks; network policies prevent required connectivity; applications cannot access dependencies; pod-to-pod communication fails; service endpoints are unreachable. Pods show connection failures indefinitely; NetworkPolicy resources show restrictive rules; applications cannot access dependencies and may experience errors or performance degradation; service-to-service communication is blocked.

## Playbook

1. Describe NetworkPolicy `<policy-name>` in namespace `<namespace>` to retrieve detailed information including ingress and egress rules, pod selectors, and namespace selectors.

2. Retrieve events in namespace `<namespace>` sorted by timestamp and filter for NetworkPolicyDenied reason to identify network-related issues and policy blocking events.

3. List NetworkPolicy resources in namespace `<namespace>` and review their rules, selectors, and policy types to identify which policies may be blocking traffic.

4. Describe pod `<pod-name>` in namespace `<namespace>` and retrieve its labels to verify whether labels match or do not match NetworkPolicy selectors.

5. Execute connectivity tests from a test pod using Pod Exec tool to verify which traffic is being blocked and which policies are enforcing the blocks.

6. List NetworkPolicy resources in namespace `<namespace>` and check for default deny policies (policyTypes containing Ingress or Egress with empty rules) that may be blocking all traffic unless explicitly allowed.

## Diagnosis

1. Analyze NetworkPolicy events and pod events from Playbook to identify NetworkPolicyDenied errors or connection failures. If events show explicit policy denial messages, the blocking policy is identified in the event details.

2. If events indicate policy blocking, check the NetworkPolicy pod selectors against pod labels from Playbook data. If pod labels do not match policy selectors, the pod is subject to default deny behavior without explicit allow rules.

3. If pod labels match policy selectors, review ingress and egress rules in the NetworkPolicy from Playbook. If rules do not include the required ports, protocols, or source/destination selectors, traffic is blocked by overly restrictive rules.

4. If ingress/egress rules appear correct, check for default deny policies (policyTypes with Ingress or Egress but empty rules) from Playbook data. If default deny exists without corresponding allow policies, all traffic is blocked.

5. If no default deny is blocking, check namespace selectors in NetworkPolicy rules from Playbook. If namespace selectors do not match the source/destination namespace labels, cross-namespace traffic is blocked.

6. If NetworkPolicy configuration appears correct, verify network plugin pod status in kube-system from Playbook data. If network plugin pods show failures or restarts, policy enforcement may be inconsistent or delayed.

**If no policy misconfiguration is found**: Review network plugin logs for policy synchronization issues, check if multiple overlapping policies create unintended restrictions, verify if namespace labels changed affecting namespace selectors, and examine if network plugin version or configuration changes affected policy enforcement behavior.

