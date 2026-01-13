---
title: DaemonSet Not Deploying Pods on All Nodes - DaemonSet
weight: 220
categories:
  - kubernetes
  - daemonset
---

# DaemonSetNotDeployingPodsonAllNodes-daemonset

## Meaning

DaemonSet pods are not being deployed on all nodes (triggering DaemonSet-related alerts) because node selectors or affinity rules restrict which nodes can run the pods, node taints prevent scheduling without matching tolerations, insufficient resources on nodes prevent pod creation, or nodes are unschedulable. DaemonSets show number scheduled mismatch in kubectl, pods remain in Pending state on some nodes, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created on all nodes, typically caused by node selector/toleration mismatches or resource constraints; node-level functionality is unavailable on affected nodes.

## Impact

DaemonSet pods are missing on some nodes; node-level functionality is unavailable on affected nodes; monitoring, logging, or networking components may be missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; node-specific services are not running; cluster functionality is inconsistent across nodes. DaemonSets show number scheduled mismatch indefinitely; pods remain in Pending state on some nodes; node-level functionality is unavailable on affected nodes and may cause errors; cluster functionality is inconsistent across nodes.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status, desired number of nodes, ready number of nodes, and status conditions to identify missing pods and deployment issues.

2. List all nodes and compare with DaemonSet pod distribution to identify which nodes are missing DaemonSet pods.

3. Verify that the DaemonSet controller is running and functioning by checking DaemonSet controller pod status in the kube-system namespace.

4. Retrieve the DaemonSet `<daemonset-name>` and inspect pod template node selector, affinity rules, and tolerations to verify scheduling constraints.

5. For nodes missing DaemonSet pods, check node labels, taints, and scheduling status to verify if they match DaemonSet requirements.

6. List events in namespace `<namespace>` and filter for DaemonSet-related events, focusing on events with reasons such as `FailedCreate` or messages indicating scheduling failures.

7. Check nodes missing DaemonSet pods for resource availability and verify if insufficient resources are preventing pod creation.

8. Check for PodDisruptionBudget conflicts that may prevent DaemonSet pod creation on nodes.

## Diagnosis

1. Compare the DaemonSet pod missing timestamps with DaemonSet controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before DaemonSet pods became missing.

2. Compare the DaemonSet pod missing timestamps with node label modification timestamps, and check whether required node labels were removed or changed within 30 minutes before DaemonSet pods became missing.

3. Compare the DaemonSet pod missing timestamps with node taint addition timestamps, and check whether new taints were applied within 30 minutes before DaemonSet pods stopped being scheduled.

4. Compare the DaemonSet pod missing timestamps with DaemonSet node selector or affinity rule modification timestamps, and check whether scheduling constraints were added or made more restrictive within 30 minutes before pods became missing.

5. Compare the DaemonSet pod missing timestamps with PodDisruptionBudget creation or modification timestamps, and check whether PDB conflicts occurred within 30 minutes before DaemonSet pods could not be created.

6. Compare the DaemonSet pod missing timestamps with node resource exhaustion timestamps, and check whether nodes ran out of resources within 30 minutes before DaemonSet pods could not be created.

7. Compare the DaemonSet pod missing timestamps with node cordoning or unschedulable status change timestamps, and check whether nodes became unschedulable within 30 minutes before DaemonSet pods became missing.

8. Compare the DaemonSet pod missing timestamps with DaemonSet toleration modification timestamps, and check whether tolerations were removed or modified within 30 minutes before pods stopped matching node taints.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review DaemonSet controller logs for gradual scheduling issues, check for intermittent node availability problems, examine if node selectors or affinity rules were always restrictive but only recently enforced, verify if node resource constraints developed over time, and check for cumulative scheduling restrictions from multiple constraints. DaemonSet pod missing issues may result from gradual cluster state changes rather than immediate configuration modifications.

