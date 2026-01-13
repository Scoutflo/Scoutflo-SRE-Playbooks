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

1. List pods across all namespaces with status phase Unknown to identify pods stuck in Unknown state.

2. List all nodes and check node status.

3. Retrieve pod `<pod-name>` in namespace `<namespace>` to identify which node the pod is running on and verify pod's node allocation and status.

4. Retrieve node `<node-name>` and check node conditions to verify if node can communicate with API server.

5. Check kubelet service status and logs on affected node via Pod Exec tool or SSH for last 100 entries if node access is available.

6. From a pod on another reachable node, execute network connectivity tests such as `ping` to the unreachable node IP to test network connectivity.

7. From a pod on the affected node, execute `curl -k https://<api-server-ip>:6443` to verify API server connectivity from affected node.

8. List pods in namespace `kube-system` and filter for CNI plugin pods to check CNI status.

## Diagnosis

1. Compare the timestamps when pods entered Unknown state with node NotReady status change timestamps, and check whether Unknown state begins within 2 minutes of nodes becoming NotReady.

2. Compare the pod Unknown state timestamps with kubelet restart timestamps from affected node logs, and verify whether Unknown state correlates with kubelet restarts within 5 minutes.

3. Compare the pod Unknown state timestamps with API server connectivity issue timestamps from connectivity test results, and check whether Unknown state correlates with API server communication failures at the same time.

4. Compare the pod Unknown state timestamps with CNI plugin pod restart timestamps or network policy change timestamps, and verify whether Unknown state begins within 5 minutes of CNI issues or network policy changes.

5. Compare the pod Unknown state timestamps with node resource exhaustion timestamps from node conditions, and check whether Unknown state correlates with node resource problems.

6. Compare the pod Unknown state timestamps with cluster maintenance or upgrade activity timestamps, and verify whether Unknown state begins within 1 hour of infrastructure changes.

**If no correlation is found within the specified time windows**: Extend the search window (2 minutes → 5 minutes, 5 minutes → 10 minutes, 1 hour → 2 hours), review kubelet logs for earlier communication failures, check for network partition events, examine node condition history for gradual degradation, verify if API server endpoints changed, check for CNI plugin configuration issues, and review infrastructure change records for delayed effects. Unknown pod state may result from network partition or gradual node degradation not immediately visible in status transitions.
