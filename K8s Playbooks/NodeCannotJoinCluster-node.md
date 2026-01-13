---
title: Node Cannot Join Cluster - Node
weight: 262
categories:
  - kubernetes
  - node
---

# NodeCannotJoinCluster-node

## Meaning

Nodes cannot join the Kubernetes cluster (triggering node-related alerts) because join tokens are expired or invalid, network connectivity to the control plane is blocked, required ports are not open, or kubelet configuration is incorrect. New nodes show unjoined status, kubelet logs show join errors or authentication failures, and network connectivity tests to API server endpoints may fail. This affects the data plane and prevents cluster scaling and capacity expansion; applications may be unable to scale due to insufficient node capacity.

## Impact

Nodes cannot join the cluster; cluster scaling fails; new nodes remain unjoined; cluster capacity cannot be increased; KubeNodeNotReady alerts fire; node registration fails; kubelet cannot authenticate; cluster expansion is blocked; manual intervention required for node addition. New nodes show unjoined status indefinitely; kubelet logs show join errors or authentication failures; cluster capacity cannot be increased; applications may be unable to scale due to insufficient node capacity.

## Playbook

1. Check the join token validity by verifying token expiration times and whether the token is still valid for cluster joining.

2. Verify network connectivity between the new node and control plane nodes by testing connectivity to API server endpoint and required ports.

3. On the new node, check kubelet configuration and verify if kubelet is configured with correct cluster endpoint and authentication credentials.

4. Verify that required ports (e.g., 6443 for API server) are open and accessible between the new node and control plane.

5. Check kubelet logs on the new node using Pod Exec tool or SSH if node access is available and filter for join errors, authentication failures, or connectivity issues.

6. Verify certificate authority (CA) certificate availability and validity on the new node for kubelet authentication.

## Diagnosis

1. Compare the node join failure timestamps with join token expiration timestamps, and check whether tokens expired within 1 hour before join failures.

2. Compare the node join failure timestamps with network connectivity failure timestamps, and check whether network issues occurred within 10 minutes before join failures.

3. Compare the node join failure timestamps with firewall rule modification timestamps, and check whether firewall rules were changed within 10 minutes before join failures.

4. Compare the node join failure timestamps with kubelet configuration modification timestamps on the new node, and check whether configuration changes occurred within 30 minutes before join failures.

5. Compare the node join failure timestamps with control plane API server unavailability timestamps, and check whether API server issues occurred within 5 minutes before join failures.

6. Compare the node join failure timestamps with cluster upgrade or certificate rotation timestamps, and check whether infrastructure changes occurred within 1 hour before join failures, affecting node registration.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes, 1 hour → 24 hours for token expiration), review kubelet logs for gradual join issues, check for intermittent network connectivity problems, examine if join token management drifted over time, verify if firewall rules gradually became restrictive, and check for control plane API server performance degradation that may have developed. Node join failures may result from gradual infrastructure or configuration issues rather than immediate changes.

