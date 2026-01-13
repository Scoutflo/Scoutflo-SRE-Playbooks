---
title: Kube StatefulSet Replicas Mismatch
weight: 20
---

# KubeStatefulSetReplicasMismatch

## Meaning

StatefulSet has not matched the expected number of replicas (triggering KubeStatefulSetReplicasMismatch alerts) because the current number of ready replicas does not match the desired replica count, indicating that pods cannot be created, scheduled, or become ready. StatefulSets show replica count mismatches in kubectl, pods remain in Pending, CrashLoopBackOff, or NotReady state, and StatefulSet events show FailedCreate, FailedScheduling, or FailedAttachVolume errors. This affects the workload plane and indicates scheduling constraints, resource limitations, pod health issues, or persistent volume problems preventing StatefulSet from achieving desired state, typically caused by cluster capacity limitations, volume zone constraints, or persistent scheduling issues; PersistentVolumeClaim binding failures may block pod creation.

## Impact

KubeStatefulSetReplicasMismatch alerts fire; service degradation or unavailability; StatefulSet cannot achieve desired replica count; current replicas mismatch desired replicas; applications run with insufficient capacity; stateful workloads may lose quorum; data consistency may be affected; persistent volume problems block StatefulSet scaling. StatefulSets show replica count mismatches indefinitely; pods remain in Pending, CrashLoopBackOff, or NotReady state; PersistentVolumeClaim binding failures may prevent pod creation; applications run with insufficient capacity and may experience errors or performance degradation.

## Playbook

1. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and inspect its status to check current replicas versus desired replicas and identify the mismatch.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the StatefulSet `<statefulset-name>` and check pod status to identify pods in Pending, CrashLoopBackOff, or NotReady states.

3. Retrieve events for the StatefulSet `<statefulset-name>` in namespace `<namespace>` and filter for error patterns including 'FailedCreate', 'FailedScheduling', 'FailedAttachVolume' to identify StatefulSet issues.

4. Retrieve PersistentVolumeClaim resources belonging to StatefulSet pods and check PersistentVolumeClaim status to verify volume binding and availability.

5. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and check pod template parameters including resource requests, node selectors, tolerations, and affinity rules to verify configuration issues.

6. Retrieve the Node `<node-name>` resources and verify node capacity and availability across the cluster for scheduling additional pods.

## Diagnosis

Compare StatefulSet replica mismatch detection timestamps with StatefulSet scaling event timestamps within 30 minutes and verify whether mismatch began when StatefulSet attempted to scale, using StatefulSet events and scaling history as supporting evidence.

Correlate StatefulSet replica mismatch with PersistentVolume binding failure timestamps within 10 minutes and verify whether volume binding failures prevented pod creation, using PVC events and StatefulSet pod status as supporting evidence.

Compare StatefulSet replica mismatch with pod scheduling failure timestamps within 30 minutes and verify whether pod scheduling failures prevented achieving desired replica count, using pod events and StatefulSet status as supporting evidence.

Analyze pod status patterns over the last 15 minutes to determine if replica mismatch is due to scheduling failures, pod crashes, volume issues, or readiness probe failures, using pod status and events as supporting evidence.

Correlate StatefulSet replica mismatch with node capacity exhaustion or zone unavailability timestamps within 30 minutes and verify whether insufficient cluster capacity or zone constraints prevented scaling, using node metrics and StatefulSet scaling attempts as supporting evidence.

Compare StatefulSet replica mismatch with PersistentVolume zone or availability issues and verify whether volume zone mismatches prevented pod scheduling, using PVC zone information and node zones as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for StatefulSet operations, review StatefulSet resource requests, check for persistent resource constraints, verify PersistentVolume availability and zone configurations, examine historical StatefulSet scaling patterns. StatefulSet replica mismatch may result from cluster capacity limitations, volume zone constraints, or persistent scheduling issues rather than immediate changes.
