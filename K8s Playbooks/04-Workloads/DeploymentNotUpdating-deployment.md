---
title: Deployment Not Updating - Deployment
weight: 226
categories:
  - kubernetes
  - deployment
---

# DeploymentNotUpdating-deployment

## Meaning

Deployments are not updating or rolling out new replicas (triggering KubeDeploymentReplicasMismatch alerts) because the deployment controller is not reconciling, pods cannot be created due to resource constraints, image pull failures prevent new pods from starting, or deployment update strategy is blocking updates. Deployments show generation mismatches in kubectl, deployment events show FailedCreate or FailedUpdate errors, and ReplicaSet resources may show creation failures. This affects the workload plane and prevents application updates from being applied, typically caused by resource constraints, image pull failures, or deployment controller issues; applications cannot be upgraded and may show errors.

## Impact

Deployment updates are not applied; new application versions cannot be deployed; rolling updates fail; pods remain at old image versions; desired replica count is not achieved; KubeDeploymentReplicasMismatch alerts fire; deployment status shows update failures; applications cannot be upgraded; service disruptions may occur during failed updates. Deployments show generation mismatches indefinitely; deployment events show FailedCreate or FailedUpdate errors; applications cannot be upgraded and may experience errors or performance degradation; rolling updates fail.

## Playbook

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Replicas status (desired/updated/ready/available)
   - Conditions showing why rollout is stuck
   - Events showing FailedCreate, FailedScheduling, or other errors

2. List events in namespace <namespace> filtered by involved object name <deployment-name> and sorted by last timestamp to see the sequence of update failures.

3. Check rollout status for deployment <deployment-name> in namespace <namespace> to see if rollout is progressing or stuck.

4. List ReplicaSets in namespace <namespace> with label app=<app-label> to see old vs new and check which ReplicaSet has the new pods vs old pods.

5. List pods in namespace <namespace> with label app=<app-label> and describe pod <new-pod-name> to see why new pods are failing.

6. Check for resource constraints:
   - Describe ResourceQuota objects in namespace <namespace>
   - Describe nodes to check allocated resources and capacity

7. Retrieve deployment <deployment-name> in namespace <namespace> and check the update strategy to see if maxUnavailable/maxSurge settings are blocking the rollout.

8. Retrieve logs from kube-controller-manager pods in namespace kube-system and filter for deployment <deployment-name> related controller errors.

## Diagnosis

1. Analyze deployment events from Playbook steps 1-2 to identify the primary update failure reason. Events showing "FailedCreate" indicate pod creation issues. Events showing "ProgressDeadlineExceeded" indicate rollout timeout. Events showing "FailedScheduling" indicate scheduling constraints. Events showing "ImagePullBackOff" or "ErrImagePull" indicate image pull failures.

2. If events indicate image pull failures (ErrImagePull, ImagePullBackOff), this is the most common cause of update failures. Verify the new image reference from deployment spec, check if the image exists in the registry, verify registry credentials if using a private registry, and check for network connectivity to the image registry.

3. If events indicate scheduling failures (FailedScheduling), correlate with node capacity data from Playbook step 6 to confirm resource exhaustion. Check if the new pod spec has increased resource requests compared to the old version that cannot be satisfied.

4. If events indicate resource quota issues (messages containing "exceeded quota"), verify quota status from Playbook step 6 and compare with new pod resource requests. Determine if quota needs to be increased or if new deployment resource requests are excessive.

5. If events indicate pod crashes for new pods (CrashLoopBackOff, Error, OOMKilled), analyze new pod describe output from Playbook step 5 to identify application-level issues with the new version. Check container logs for startup errors or configuration problems in the new version.

6. If rollout status from Playbook step 3 shows rollout is stuck but no failure events, check deployment update strategy from Playbook step 7. Verify maxUnavailable and maxSurge settings are not blocking the rollout (e.g., maxUnavailable=0 with pods unable to become ready).

7. If ReplicaSet analysis from Playbook step 4 shows new ReplicaSet has 0 ready pods while old ReplicaSet still has all pods, the update is stuck at the first new pod creation. Focus diagnosis on why the first new pod cannot start.

8. If deployment controller logs from Playbook step 8 show reconciliation errors or the controller is not processing the deployment, this indicates control plane issues rather than workload issues.

**If no clear failure reason is identified from events**: Review if deployment is paused (check deployment spec for paused: true), verify webhook configurations are not rejecting pod creation, check for pod security policy or admission controller blocks, examine if the new container has incompatible security context requirements, and verify service account permissions if the new version requires different RBAC access.

