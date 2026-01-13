---
title: DaemonSet Pods Not Running on Specific Node - DaemonSet
weight: 264
categories:
  - kubernetes
  - daemonset
---

# DaemonSetPodsNotRunningonSpecificNode-daemonset

## Meaning

DaemonSet pods are not running on a specific node (triggering DaemonSet-related alerts) because the node has taints without matching tolerations in the DaemonSet, the node selector does not match the node's labels, insufficient resources prevent pod creation, or the node is unschedulable. DaemonSets show number scheduled mismatch for the specific node, pods remain in Pending state, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created on the specific node, typically caused by node taint/toleration mismatches or resource constraints; node-level functionality is unavailable on that node.

## Impact

DaemonSet pod is missing on the specific node; node-level functionality is unavailable on that node; monitoring, logging, or networking components are missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; node-specific services are not running on the affected node; cluster functionality is inconsistent. DaemonSets show number scheduled mismatch for the specific node indefinitely; pods remain in Pending state; node-level functionality is unavailable on that node and may cause errors; cluster functionality is inconsistent.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status and status conditions to verify which nodes are missing pods.

2. Verify that the DaemonSet controller is running and functioning by checking DaemonSet controller pod status in the kube-system namespace.

3. Retrieve the node `<node-name>` and inspect its labels, taints, and scheduling status to verify if it matches DaemonSet requirements.

4. Retrieve the DaemonSet `<daemonset-name>` and inspect pod template tolerations to verify if they match the node's taints.

5. Retrieve the DaemonSet `<daemonset-name>` and inspect pod template node selector and affinity rules to verify if they match the node's labels.

6. List events on node `<node-name>` and filter for DaemonSet-related events, focusing on events with reasons such as `FailedCreate` or messages indicating why the pod cannot be created.

7. Check the node `<node-name>` for resource availability and verify if insufficient CPU, memory, or other resources are preventing DaemonSet pod creation.

8. Check for PodDisruptionBudget conflicts that may prevent DaemonSet pod creation on the specific node.

## Diagnosis

1. Compare the DaemonSet pod missing timestamps on the specific node with DaemonSet controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before the DaemonSet pod became missing.

2. Compare the DaemonSet pod missing timestamps on the specific node with node taint addition timestamps, and check whether new taints were applied within 30 minutes before the DaemonSet pod became missing.

3. Compare the DaemonSet pod missing timestamps with DaemonSet toleration modification timestamps, and check whether tolerations were removed or modified within 30 minutes before the pod stopped matching node taints.

4. Compare the DaemonSet pod missing timestamps with node label modification timestamps, and check whether required labels were removed or changed within 30 minutes before the DaemonSet pod became missing.

5. Compare the DaemonSet pod missing timestamps with PodDisruptionBudget creation or modification timestamps, and check whether PDB conflicts occurred within 30 minutes before the DaemonSet pod could not be created on the specific node.

6. Compare the DaemonSet pod missing timestamps with node resource exhaustion timestamps, and check whether the node ran out of resources within 30 minutes before the DaemonSet pod could not be created.

7. Compare the DaemonSet pod missing timestamps with node cordoning or unschedulable status change timestamps, and check whether the node became unschedulable within 30 minutes before the DaemonSet pod became missing.

8. Compare the DaemonSet pod missing timestamps with DaemonSet node selector or affinity rule modification timestamps, and check whether scheduling constraints were added or made more restrictive within 30 minutes before the pod became missing.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review DaemonSet controller logs for gradual scheduling issues on the specific node, check for intermittent node availability problems, examine if node taints or labels were always incompatible but only recently enforced, verify if node resource constraints developed over time, and check for cumulative scheduling restrictions. DaemonSet pod missing on a specific node may result from gradual node state changes rather than immediate configuration modifications.

