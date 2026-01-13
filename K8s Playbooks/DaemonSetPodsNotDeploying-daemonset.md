---
title: DaemonSet Pods Not Deploying - DaemonSet
weight: 239
categories:
  - kubernetes
  - daemonset
---

# DaemonSetPodsNotDeploying-daemonset

## Meaning

DaemonSet pods are not being deployed to nodes (triggering DaemonSet-related alerts) because node selectors do not match available nodes, tolerations do not match node taints, resource constraints prevent pod creation, or the DaemonSet controller is not functioning. DaemonSets show number scheduled mismatch in kubectl, pods remain in Pending state, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created, typically caused by node selector/toleration mismatches, resource constraints, or DaemonSet controller issues; node-level functionality is unavailable.

## Impact

DaemonSet pods are not created; node-level functionality is unavailable; monitoring, logging, or networking components are missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; cluster functionality is impaired; node-specific services are not running. DaemonSets show number scheduled mismatch indefinitely; pods remain in Pending state; node-level functionality is unavailable and may cause errors; cluster functionality is impaired.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status, desired number of nodes, current number of nodes, and status conditions to identify deployment issues.

2. Verify that the DaemonSet controller is running and functioning by checking DaemonSet controller pod status in the kube-system namespace and reviewing controller logs.

3. List all nodes and check their labels, taints, and scheduling status to verify if any nodes match the DaemonSet's node selector and toleration requirements.

4. Retrieve the DaemonSet `<daemonset-name>` and inspect pod template node selector, tolerations, and affinity rules to verify scheduling configuration.

5. List events in namespace `<namespace>` and filter for DaemonSet-related events, focusing on events with reasons such as `FailedCreate` or messages indicating why pods cannot be created.

6. Check nodes for resource availability and verify if insufficient CPU, memory, or other resources are preventing DaemonSet pod creation.

7. Check for PodDisruptionBudget conflicts that may prevent DaemonSet pod creation.

## Diagnosis

1. Compare the DaemonSet pod deployment failure timestamps with DaemonSet controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before pod deployment failures.

2. Compare the DaemonSet pod deployment failure timestamps with DaemonSet node selector modification timestamps, and check whether node selector changes occurred within 30 minutes before pods stopped deploying.

3. Compare the DaemonSet pod deployment failure timestamps with node taint addition timestamps, and check whether new taints were applied within 30 minutes before DaemonSet pods could not be scheduled.

4. Compare the DaemonSet pod deployment failure timestamps with DaemonSet toleration modification timestamps, and check whether tolerations were removed or modified within 30 minutes before pods stopped matching node taints.

5. Compare the DaemonSet pod deployment failure timestamps with PodDisruptionBudget creation or modification timestamps, and check whether PDB conflicts occurred within 30 minutes before DaemonSet pods could not be created.

6. Compare the DaemonSet pod deployment failure timestamps with node resource exhaustion timestamps, and check whether nodes ran out of resources within 30 minutes before DaemonSet pods could not be created.

7. Compare the DaemonSet pod deployment failure timestamps with node removal or cluster scaling events, and check whether eligible nodes were removed within 30 minutes before DaemonSet pods became unavailable.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review DaemonSet controller logs for gradual scheduling issues, check for intermittent node availability problems, examine if node selectors or tolerations were always incompatible but only recently enforced, verify if node resource constraints developed over time, and check for cumulative scheduling restrictions. DaemonSet pod deployment failures may result from gradual cluster state changes rather than immediate configuration modifications.

