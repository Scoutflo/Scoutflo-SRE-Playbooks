---
title: Pods Stuck In Unknown State - Pod
weight: 296
categories:
  - kubernetes
  - pod
---

# PodsStuckInUnknownState-pod

## Meaning

Pods are reported in the Unknown phase (potentially triggering KubePodNotReady alerts) because the control plane has lost contact with the kubelet on the node hosting them, so their real runtime state cannot be accurately determined. Pods show Unknown phase in kubectl, nodes show NotReady condition, and kubelet logs may show connection timeout errors or API server communication failures. This indicates node communication failures, kubelet issues, or network partition problems preventing status updates; applications running on affected nodes may experience errors or become unreachable.

## Impact

Pod status cannot be determined; pods may be running but appear unavailable; services may lose endpoints; applications may be inaccessible; cluster state becomes inconsistent; KubePodNotReady alerts fire; pods remain in Unknown state; kubelet communication failures occur; node status becomes unreliable. Pods show Unknown phase indefinitely; nodes show NotReady condition; kubelet logs show connection timeout errors; applications running on affected nodes may experience errors or become unreachable.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to identify which node the pod is running on and verify pod's node allocation and status.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify pod-related events that may indicate communication or node issues.

3. List pods across all namespaces with status phase Unknown to identify pods stuck in Unknown state.

4. List all nodes and check node status.

5. Retrieve node <node-name> and check node conditions to verify if node can communicate with API server.

6. Check kubelet service status and logs on affected node via Pod Exec tool or SSH for last 100 entries if node access is available.

7. From a pod on another reachable node, execute network connectivity tests to the unreachable node IP to test network connectivity.

8. From a pod on the affected node, verify API server connectivity to <api-server-ip> on port 6443.

9. List pods in namespace kube-system and filter for CNI plugin pods to check CNI status.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify when and why communication with the pod was lost. Events may show the last known state before the pod became Unknown.

2. If node status shows NotReady condition (from Playbook steps 4-5), the kubelet on the node has lost communication with the API server. This is the primary cause of Unknown pod state. The pod may still be running on the node but its status cannot be reported.

3. If kubelet service is not running or shows errors (from Playbook step 6), restart the kubelet service on the affected node. Check kubelet logs for certificate expiration, API server connectivity issues, or resource exhaustion.

4. If network connectivity tests fail (from Playbook steps 7-8), there is a network partition between the node and control plane. Common causes include:
   - Network infrastructure failures (switches, routers)
   - Firewall rules blocking API server port 6443
   - Cloud provider network issues
   - Node network interface problems

5. If CNI plugin pods are failing (from Playbook step 9), pod networking on the node is broken. This can prevent kubelet from communicating with the API server if it routes through the pod network.

6. If all checks pass but pods remain Unknown, the issue may be intermittent connectivity. Check for packet loss or high latency between the node and API server.

**If the node is confirmed unreachable**: Consider draining the node and investigating physical/virtual machine health. If the node cannot be recovered, delete it from the cluster. Pods on the Unknown node will be rescheduled to healthy nodes after the node is removed or the pod-eviction-timeout is exceeded.
