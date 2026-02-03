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

1. Describe node <node-name> (if the node appears in the cluster) to see:
   - Conditions section showing registration status
   - Events section showing join or registration failures
   - System Info and kubelet version details

2. Retrieve node events sorted by timestamp to see the sequence of node registration events and any join failures.

3. List join tokens and verify token expiration times and whether the token is still valid for cluster joining.

4. Verify network connectivity between the new node and control plane nodes by testing connectivity to API server endpoint and required ports.

5. On the new node, check kubelet configuration and verify if kubelet is configured with correct cluster endpoint and authentication credentials.

6. Check kubelet logs on the new node using Pod Exec tool or SSH if node access is available and filter for join errors, authentication failures, or connectivity issues.

7. Verify certificate authority (CA) certificate availability and validity on the new node for kubelet authentication.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 (if node appears in cluster) to identify registration failures. Events showing "RegisteredNode" failures, authentication errors, or TLS handshake failures indicate specific join issues. Note event timestamps and error messages.

2. If node events or kubelet logs indicate token-related errors ("token expired", "invalid token"), check join token validity from Playbook step 3. Bootstrap tokens have expiration times and may have expired before the join attempt.

3. If kubelet logs from Playbook step 6 show network connectivity errors ("connection refused", "no route to host", "timeout"), verify network connectivity from Playbook step 4. The node must reach the API server on port 6443 and other required control plane ports.

4. If network connectivity tests fail, check firewall rules and network policies. Required ports (6443 for API server, 10250 for kubelet, 2379-2380 for etcd if applicable) must be open between the new node and control plane.

5. If kubelet logs show authentication or certificate errors, verify CA certificate availability from Playbook step 7. The new node must trust the cluster CA certificate to establish TLS connections.

6. If kubelet configuration from Playbook step 5 shows incorrect API server endpoint or cluster settings, correct the configuration. Misconfigured cluster endpoint prevents kubelet from finding the control plane.

7. If kubelet logs show API server unreachable errors, verify API server availability and health. Control plane issues prevent new nodes from joining even with correct configuration.

**If no root cause is identified from events**: Verify the join command syntax and parameters are correct, check if the cluster uses custom admission controllers that may reject node registration, review control plane logs for node registration errors, and verify node meets cluster requirements (Kubernetes version compatibility, required labels, etc.).

