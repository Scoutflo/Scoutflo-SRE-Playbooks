---
title: Pod Cannot Connect to External Services - Network
weight: 234
categories:
  - kubernetes
  - network
---

# PodCannotConnecttoExternalServices-network

## Meaning

Pods cannot connect to external services (triggering KubePodNotReady alerts when pods become unresponsive due to external connectivity failures) because network policies are blocking egress traffic, the cluster's egress gateway is misconfigured, DNS cannot resolve external domains, or firewall rules are blocking outbound connections. Pods show connection timeout or refused errors in logs, NetworkPolicy resources may show egress blocking rules, and DNS resolution tests for external domains may fail. This affects the network plane and prevents pods from reaching external services, typically caused by NetworkPolicy restrictions or DNS issues; applications may show errors when accessing external services.

## Impact

Pods cannot reach external APIs or services; outbound internet connectivity fails; external service integrations break; egress traffic is blocked; network policies prevent external access; KubePodNotReady alerts fire when pods become unresponsive due to external connectivity failures; applications cannot fetch external resources; external database or API connections fail; pod logs show connection timeout or refused errors; applications fail to start or function correctly. Pods show connection timeout or refused errors in logs indefinitely; NetworkPolicy resources may show egress blocking rules; applications may show errors when accessing external services; external service integrations break.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its network configuration and DNS settings to verify pod networking setup.

2. List NetworkPolicy objects in namespace `<namespace>` and review their egress rules to verify if policies are blocking external traffic.

3. From the pod `<pod-name>`, execute `curl` or `wget` to external service URLs using Pod Exec tool to test outbound connectivity and verify if external connections are blocked.

4. From the pod `<pod-name>`, execute `nslookup` or `dig` for external domains using Pod Exec tool to test DNS resolution for external services.

5. Check cluster egress gateway or network plugin configuration to verify if egress traffic routing is correctly configured.

6. List events in namespace `<namespace>` and filter for network-related events, focusing on events with reasons such as `NetworkPolicyDenied` or messages indicating egress blocking.

## Diagnosis

1. Compare the pod external connectivity failure timestamps with NetworkPolicy creation or modification timestamps, and check whether egress-blocking policies were added or modified within 10 minutes before external connectivity failures.

2. Compare the pod external connectivity failure timestamps with pod DNS configuration modification timestamps, and check whether DNS policy changes occurred within 30 minutes before external connectivity failures.

3. Compare the pod external connectivity failure timestamps with cluster egress gateway or network plugin configuration modification timestamps, and check whether egress routing changes occurred within 30 minutes before connectivity failures.

4. Compare the pod external connectivity failure timestamps with firewall rule modification timestamps, and check whether firewall rules were changed within 10 minutes before external connectivity failures.

5. Compare the pod external connectivity failure timestamps with external DNS resolution failure timestamps, and check whether DNS issues occurred within 5 minutes before external connectivity failures.

6. Compare the pod external connectivity failure timestamps with cluster network plugin restart or failure timestamps, and check whether network infrastructure issues occurred within 1 hour before external connectivity failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review network plugin logs for gradual egress routing issues, check for intermittent firewall rule enforcement, examine if network policies accumulated egress restrictions over time, verify if DNS resolution for external domains degraded gradually, and check for external service availability issues that may have developed. External connectivity failures may result from gradual network policy or infrastructure changes rather than immediate modifications.

