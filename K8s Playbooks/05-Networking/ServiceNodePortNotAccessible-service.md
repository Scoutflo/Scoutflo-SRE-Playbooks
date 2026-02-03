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

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its type, NodePort configuration, and port mappings.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify NodePort configuration issues.

3. List all nodes and retrieve their external IP addresses to identify which nodes should be accessible for NodePort connections.

4. From an external client or test pod, execute curl or telnet to test connectivity to `<node-ip>:<node-port>` to verify if the NodePort is reachable.

5. Check firewall rules on nodes or cloud provider security groups to verify if NodePort ports are open and accessible.

6. Check kube-proxy pod status in the `kube-system` namespace to verify if the service proxy is functioning correctly and forwarding NodePort traffic.

## Diagnosis

1. Analyze service events and configuration from Playbook to verify NodePort is correctly assigned. If service type is not NodePort or nodePort field is not set, external access via NodePort is not configured.

2. If NodePort is configured, check service endpoints from Playbook. If endpoints list is empty, no backend pods are available to receive traffic (selector mismatch or pods not Ready).

3. If endpoints exist, verify kube-proxy status from Playbook. If kube-proxy is not running or shows failures on nodes, NodePort iptables/ipvs rules are not programmed and traffic is not forwarded.

4. If kube-proxy is healthy, check connectivity test results from Playbook (curl to node-ip:node-port). If connections are refused, verify the NodePort is within the allowed range (default 30000-32767) and not conflicting with existing ports.

5. If NodePort is valid, check firewall rules and security group configuration. If NodePort is blocked by node firewall (iptables rules), cloud security groups, or network ACLs, external traffic cannot reach the node.

6. If firewall allows traffic, verify node external IP addresses from Playbook and confirm nodes are reachable on the network. If nodes have only internal IPs or are behind NAT without proper port forwarding, NodePort is not accessible externally.

**If no configuration issue is found**: Check externalTrafficPolicy setting (Local vs Cluster) for traffic routing behavior, verify if nodes are in a private subnet requiring bastion or VPN access, and examine if load balancer or ingress controller should be used instead of direct NodePort access.

