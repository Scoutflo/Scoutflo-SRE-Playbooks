---
title: Kube DaemonSet MisScheduled
weight: 20
---

# KubeDaemonSetMisScheduled

## Meaning

DaemonSet pods are running on nodes where they should not be scheduled (triggering alerts related to DaemonSet scheduling issues) because node selectors, tolerations, or affinity rules are misconfigured, or node taints and labels have changed without updating the DaemonSet configuration. DaemonSets show number mis-scheduled in kubectl, pods run on incorrect nodes, and node taints/labels may show mismatches with DaemonSet selector requirements. This affects the workload plane and indicates configuration mismatches between DaemonSet requirements and node configurations, typically caused by configuration drift, node pool changes, or feature discovery label updates; node feature discovery label changes may cause selector mismatches.

## Impact

DaemonSet mis-scheduling alerts fire; service degradation or unavailability; excessive resource usage on unintended nodes; DaemonSet pods running on wrong nodes; DaemonSet desired state mismatch; pods may be evicted or fail to run correctly; system components may be misconfigured; resource waste on inappropriate nodes. DaemonSets show number mis-scheduled; pods run on incorrect nodes; node taint/label mismatches with DaemonSet selectors may cause mis-scheduling; system components may be misconfigured on inappropriate nodes.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status to check number scheduled, number ready, and number mis-scheduled to verify mis-scheduling.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the DaemonSet `<daemonset-name>` and check pod status to identify pods running on incorrect nodes.

3. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and verify node selector, tolerations, and affinity rule configurations in the pod template to identify configuration issues.

4. Retrieve the Node `<node-name>` where DaemonSet pods are mis-scheduled and check node taints and labels to verify node configuration mismatches.

5. Retrieve events for the DaemonSet `<daemonset-name>` in namespace `<namespace>` and filter for scheduling-related patterns to identify scheduling issues.

6. Verify node feature discovery or similar tools that may affect node labels used by DaemonSet selectors by checking node label sources and feature discovery configurations.

## Diagnosis

Compare DaemonSet mis-scheduling detection timestamps with node taint or label change timestamps within 10 minutes and verify whether mis-scheduling began after node configuration changes, using node taint/label history and DaemonSet pod scheduling events as supporting evidence.

Correlate DaemonSet mis-scheduling with DaemonSet configuration change timestamps within 30 minutes and verify whether mis-scheduling began after DaemonSet template updates, using DaemonSet modification history and pod scheduling events as supporting evidence.

Analyze DaemonSet pod distribution patterns across nodes to determine if mis-scheduling is systematic (configuration issue) or isolated (node-specific issue), using pod node assignments and DaemonSet selector configurations as supporting evidence.

Compare DaemonSet node selector requirements with actual node labels and taints at mis-scheduling times and verify whether selector mismatches caused mis-scheduling, using DaemonSet configurations and node metadata as supporting evidence.

Correlate DaemonSet mis-scheduling with node feature discovery update timestamps within 10 minutes and verify whether node label changes from feature discovery caused selector mismatches, using node feature discovery logs and node label changes as supporting evidence.

Compare DaemonSet toleration configurations with node taint configurations and verify whether missing or incorrect tolerations caused pods to run on tainted nodes, using DaemonSet tolerations and node taints as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for configuration changes, review DaemonSet selector and toleration configurations, check for node pool changes, verify node feature discovery configurations, examine historical DaemonSet scheduling patterns. DaemonSet mis-scheduling may result from configuration drift, node pool changes, or feature discovery label updates rather than immediate changes.
