---
title: Kube Deployment Replicas Mismatch
weight: 20
---

# KubeDeploymentReplicasMismatch

## Meaning

Deployment has not matched the expected number of replicas (triggering KubeDeploymentReplicasMismatch alerts) because the current number of ready replicas does not match the desired replica count, indicating that pods cannot be created, scheduled, or become ready. Deployments show replica count mismatches in kubectl, pods remain in Pending or NotReady state, and deployment events show FailedCreate or FailedScheduling errors. This affects the workload plane and indicates scheduling constraints, resource limitations, or pod health issues preventing deployment from achieving desired state, typically caused by cluster capacity limitations, resource quota constraints, or persistent scheduling issues; applications run with insufficient capacity and may show errors.

## Impact

KubeDeploymentReplicasMismatch alerts fire; service degradation or unavailability; deployment cannot achieve desired replica count; current replicas mismatch desired replicas; applications run with insufficient capacity; rolling updates may be blocked; replica counts do not match desired state. Deployments show replica count mismatches indefinitely; pods remain in Pending or NotReady state; applications run with insufficient capacity and may experience errors or performance degradation.

## Playbook

1. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and inspect its status to check current replicas versus desired replicas and identify the mismatch.

2. Retrieve ReplicaSet resources belonging to the Deployment `<deployment-name>` in namespace `<namespace>` and check ReplicaSet status and replica counts to verify replica distribution.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the Deployment `<deployment-name>` and check pod status to identify pods in Pending, CrashLoopBackOff, or NotReady states.

4. Retrieve events for the Deployment `<deployment-name>` in namespace `<namespace>` and filter for error patterns including 'FailedCreate', 'FailedScheduling', 'ReplicaSetCreateError' to identify deployment issues.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and check pod template parameters including resource requests, node selectors, tolerations, and affinity rules to verify configuration issues.

6. Retrieve the Node `<node-name>` resources and verify node capacity and availability across the cluster for scheduling additional pods.

## Diagnosis

Compare deployment replica mismatch detection timestamps with deployment scaling event timestamps within 30 minutes and verify whether mismatch began when deployment attempted to scale, using deployment events and scaling history as supporting evidence.

Correlate deployment replica mismatch with pod scheduling failure timestamps within 30 minutes and verify whether pod scheduling failures prevented achieving desired replica count, using pod events and deployment status as supporting evidence.

Compare deployment replica mismatch with resource quota exhaustion timestamps within 30 minutes and verify whether resource quotas prevented pod creation, using resource quota status and deployment events as supporting evidence.

Analyze pod status patterns over the last 15 minutes to determine if replica mismatch is due to scheduling failures, pod crashes, or readiness probe failures, using pod status and events as supporting evidence.

Correlate deployment replica mismatch with node capacity exhaustion timestamps within 30 minutes and verify whether insufficient cluster capacity prevented scaling, using node metrics and deployment scaling attempts as supporting evidence.

Compare deployment replica mismatch with HPA scaling event timestamps within 30 minutes and verify whether HPA scaling conflicts or resource constraints caused mismatch, using HPA events and deployment status as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for deployment operations, review deployment resource requests, check for persistent resource constraints, verify pod disruption budgets, examine historical deployment scaling patterns. Deployment replica mismatch may result from cluster capacity limitations, resource quota constraints, or persistent scheduling issues rather than immediate changes.
