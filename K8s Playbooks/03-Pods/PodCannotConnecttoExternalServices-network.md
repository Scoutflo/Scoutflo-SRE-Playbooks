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

1. Describe the pod `<pod-name>` in namespace `<namespace>` to retrieve detailed information including network configuration and DNS settings.

2. Retrieve events for the pod `<pod-name>` in namespace `<namespace>` sorted by timestamp to identify network-related issues and egress blocking events.

3. List NetworkPolicy objects in namespace `<namespace>` and review their egress rules to verify if policies are blocking external traffic.

4. From the pod `<pod-name>`, execute curl or wget to external service URLs to test outbound connectivity and verify if external connections are blocked.

5. From the pod `<pod-name>`, execute nslookup or dig for external domains to test DNS resolution for external services.

6. Check cluster egress gateway or network plugin configuration to verify if egress traffic routing is correctly configured.

## Diagnosis

1. Analyze pod events from Playbook to identify network-related errors or egress blocking events. If events show connection timeout or refused errors to external services, note the specific external endpoints failing.

2. If events indicate connectivity failures, check DNS resolution test results from Playbook. If nslookup or dig for external domains fails, the issue is DNS resolution rather than network connectivity.

3. If DNS resolution works, check NetworkPolicy egress rules from Playbook data. If egress policies exist without rules allowing external traffic (0.0.0.0/0 or specific external CIDRs), egress traffic is blocked by policy.

4. If NetworkPolicy allows egress, review connectivity test results (curl/wget) from Playbook. If connections timeout rather than refuse, check firewall rules or security groups blocking outbound traffic.

5. If firewall rules are not blocking, verify pod network configuration and DNS settings from Playbook. If dnsPolicy is incorrect or nameserver configuration is missing, DNS-based external service resolution fails.

6. If pod network configuration is correct, check network plugin and egress gateway status from Playbook data. If egress routing is misconfigured or NAT is not functioning, pods cannot reach external networks.

**If no egress configuration issue is found**: Verify external service availability independently, check if proxy or egress gateway is required for external access, review cloud provider NAT gateway or internet gateway configuration, and examine if specific external IPs or domains are blocked by organizational firewall policies.

