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

1. Describe StatefulSet <statefulset-name> in namespace <namespace> to see:
   - Replicas status (desired/current/ready)
   - Pod template configuration including resource requests
   - Conditions showing why replicas mismatch
   - Events showing FailedCreate, FailedScheduling, or FailedAttachVolume errors

2. Retrieve events for StatefulSet <statefulset-name> in namespace <namespace> sorted by timestamp to see the sequence of replica mismatch issues.

3. List pods belonging to StatefulSet in namespace <namespace> with label app=<statefulset-label> and describe pods to identify pods in Pending, CrashLoopBackOff, or NotReady states.

4. List PersistentVolumeClaim resources in namespace <namespace> with label app=<statefulset-label> and describe PVCs to verify volume binding and availability.

5. Retrieve StatefulSet <statefulset-name> configuration in namespace <namespace> and verify resource requests, node selectors, tolerations, and affinity rules.

6. Analyse node capacity by describing nodes and checking allocated resources to verify availability across the cluster for scheduling additional pods.

## Diagnosis

1. Analyze StatefulSet events from Playbook to identify the replica creation blocker. Events showing "FailedCreate" indicate PVC or pod creation issues. Events showing "FailedScheduling" indicate resource or placement constraints. Events showing "FailedAttachVolume" indicate storage problems preventing pod startup.

2. If events indicate PVC binding issues (Pending PVCs, ProvisioningFailed), verify PVC status for each pod ordinal. StatefulSets create pods sequentially, so a single PVC binding failure blocks creation of that pod and all subsequent pods. Check StorageClass provisioner availability and zone constraints.

3. If events indicate scheduling failures (InsufficientCPU, InsufficientMemory, NodeAffinity), compare pod resource requests with available node capacity from Playbook. Verify if node selectors or anti-affinity rules are too restrictive for the current cluster state.

4. If pods exist but are not Ready (CrashLoopBackOff, Error, or failing readiness probes), the replica count shows current pods but ready count is lower. Analyze pod logs and container exit codes to identify the application-level failure preventing readiness.

5. If events indicate volume attachment failures, verify that StatefulSet's volumeClaimTemplates specify a StorageClass that can provision volumes in zones where schedulable nodes exist. Zone mismatches between PV and nodes cause permanent scheduling failures.

6. If some replicas are running but fewer than desired, identify which pod ordinal is missing or failing. StatefulSets create pods in order (0, 1, 2...), so the lowest missing ordinal indicates where the failure occurred. Check events and status for that specific pod.

7. If no clear event pattern exists, verify the StatefulSet's podManagementPolicy. With OrderedReady policy (default), any unhealthy pod blocks creation of higher-ordinal pods. With Parallel policy, all pods are created simultaneously but each still requires its PVC to be bound first.
