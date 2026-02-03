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

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Number scheduled, ready, and mis-scheduled counts
   - Node selector, tolerations, and affinity rule configurations
   - Conditions showing scheduling mismatches
   - Events showing scheduling-related issues

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of mis-scheduling issues.

3. List pods belonging to DaemonSet in namespace <namespace> with label app=<daemonset-label> and describe pods to identify pods running on incorrect nodes.

4. Describe node <node-name> where DaemonSet pods are mis-scheduled and check node taints and labels to verify node configuration mismatches.

5. Check node-feature-discovery pods in kube-system namespace to verify tools that may affect node labels used by DaemonSet selectors.

## Diagnosis

1. Analyze DaemonSet events and pod distribution from Playbook to understand the mis-scheduling pattern. Identify which nodes have DaemonSet pods running that should not, based on the DaemonSet's nodeSelector and node affinity rules.

2. If mis-scheduled pods are running on nodes that should be excluded by nodeSelector, compare node labels with DaemonSet nodeSelector requirements. Labels may have changed on nodes after pods were scheduled. Pods scheduled before label changes continue running even if they no longer match selectors.

3. If mis-scheduled pods are running on tainted nodes, verify whether DaemonSet tolerations are overly permissive. Tolerations with operator "Exists" and no key match all taints. Check if tolerations were added that allow scheduling on unintended nodes.

4. If node-feature-discovery or similar tools are in use, check if automatic label updates caused nodes to match or unmatch the DaemonSet's selectors. Dynamic label changes can cause pods to become mis-scheduled relative to current node state.

5. If mis-scheduling is systematic across many nodes, the DaemonSet's scheduling constraints may be misconfigured. Verify that nodeSelector, nodeAffinity, and tolerations together correctly express the intended node targeting. Missing nodeSelector with broad tolerations schedules to all nodes.

6. If mis-scheduling is isolated to specific nodes, check if those nodes recently had taints removed or labels added that now match the DaemonSet's requirements. Compare current node configuration with intended node pool membership.

7. If DaemonSet pods exist on nodes where they cause resource contention or policy violations, the resolution may require either updating DaemonSet scheduling constraints or deleting the mis-scheduled pods manually. Note that pods scheduled to nodes before constraint changes are not automatically evicted.
