---
title: Service NodePort Not Accessible - Service
weight: 232
categories:
  - kubernetes
  - service
---

# ServiceNodePortNotAccessible-service

## Meaning

NodePort services are not accessible from outside the cluster (triggering service-related alerts) because firewall rules are blocking the NodePort, nodes are not reachable on the NodePort, kube-proxy is not functioning, or the service configuration is incorrect. NodePort connections are refused from external clients, kube-proxy pods may show failures in kube-system namespace, and firewall rules may block NodePort ports. This affects the network plane and prevents external access to services, typically caused by firewall restrictions, kube-proxy failures, or network configuration issues; applications are unreachable externally.

## Impact

NodePort services are unreachable from outside the cluster; external traffic cannot reach applications; NodePort connections are refused; firewall blocks NodePort access; KubeServiceNotReady alerts may fire; service status shows NodePort configured but not accessible; applications are unreachable externally; load balancing through NodePort fails. NodePort connections are refused indefinitely; kube-proxy pods may show failures; applications are unreachable externally and may show errors; external traffic cannot reach applications.

## Playbook

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its type, NodePort configuration, and port mappings to verify service setup.

2. List all nodes and retrieve their external IP addresses to identify which nodes should be accessible for NodePort connections.

3. From an external client or test pod, execute `curl` or `telnet` to test connectivity to `<node-ip>:<node-port>` to verify if the NodePort is reachable.

4. Check firewall rules on nodes or cloud provider security groups to verify if NodePort ports are open and accessible.

5. Check kube-proxy pod status in the kube-system namespace to verify if the service proxy is functioning correctly and forwarding NodePort traffic.

6. List events in namespace `<namespace>` and filter for service-related events, focusing on events with reasons such as `FailedToUpdateEndpoint` or messages indicating NodePort configuration issues.

## Diagnosis

1. Compare the NodePort accessibility failure timestamps with firewall rule modification timestamps, and check whether firewall rules were changed within 10 minutes before NodePort became inaccessible.

2. Compare the NodePort accessibility failure timestamps with kube-proxy restart or failure timestamps, and check whether proxy issues occurred within 5 minutes before NodePort failures.

3. Compare the NodePort accessibility failure timestamps with node network interface or IP address change timestamps, and check whether node networking changes occurred within 10 minutes before NodePort became inaccessible.

4. Compare the NodePort accessibility failure timestamps with service NodePort configuration modification timestamps, and check whether service port changes occurred within 30 minutes before accessibility failures.

5. Compare the NodePort accessibility failure timestamps with cloud provider security group or network ACL modification timestamps, and check whether network policy changes occurred within 10 minutes before NodePort failures.

6. Compare the NodePort accessibility failure timestamps with cluster network plugin restart or failure timestamps, and check whether network infrastructure issues occurred within 1 hour before NodePort accessibility failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes, 1 hour → 2 hours), review kube-proxy logs for gradual performance degradation, check for intermittent network connectivity issues, examine if firewall rules were gradually tightened, verify if node networking configurations drifted over time, and check for cloud provider network policy changes that may have accumulated. NodePort accessibility failures may result from gradual network infrastructure changes rather than immediate modifications.

