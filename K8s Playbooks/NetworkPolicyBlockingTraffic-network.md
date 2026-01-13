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

1. List NetworkPolicy objects in namespace `<namespace>` and review their rules, selectors, and policy types to identify which policies may be blocking traffic.

2. Retrieve the NetworkPolicy `<policy-name>` in namespace `<namespace>` and inspect its ingress and egress rules, pod selectors, and namespace selectors to verify policy configuration.

3. Retrieve the pod `<pod-name>` that is experiencing blocked traffic and verify its labels match or do not match NetworkPolicy selectors.

4. List events in namespace `<namespace>` and filter for network-related events, focusing on events with reasons such as `NetworkPolicyDenied` or messages indicating policy blocking.

5. From a test pod, execute connectivity tests to verify which traffic is being blocked and which policies are enforcing the blocks.

6. Check if default deny policies exist in the namespace that may be blocking all traffic unless explicitly allowed.

## Diagnosis

1. Compare the network traffic blocking timestamps with NetworkPolicy creation timestamps, and check whether new policies were added within 10 minutes before traffic was blocked.

2. Compare the network traffic blocking timestamps with NetworkPolicy rule modification timestamps, and check whether policy rules were changed within 10 minutes before traffic blocking.

3. Compare the network traffic blocking timestamps with pod label modification timestamps, and check whether pod labels were changed within 30 minutes before traffic blocking, causing selector mismatches.

4. Compare the network traffic blocking timestamps with default deny NetworkPolicy creation timestamps, and check whether default deny policies were added within 10 minutes before traffic blocking.

5. Compare the network traffic blocking timestamps with NetworkPolicy namespace selector modification timestamps, and check whether namespace selectors were changed within 10 minutes before traffic blocking.

6. Compare the network traffic blocking timestamps with network plugin restart or configuration modification timestamps, and check whether network infrastructure changes occurred within 1 hour before traffic blocking, affecting policy enforcement.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review network plugin logs for gradual policy enforcement issues, check for intermittent policy rule processing problems, examine if network policies accumulated restrictive rules over time, verify if pod labels drifted gradually causing selector mismatches, and check for network plugin updates that may have changed policy enforcement behavior. Network policy blocking may result from cumulative policy restrictions rather than immediate changes.

