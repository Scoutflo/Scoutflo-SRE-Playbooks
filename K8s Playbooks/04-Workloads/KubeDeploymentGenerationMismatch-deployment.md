---
title: Kube Deployment Generation Mismatch
weight: 20
---

# KubeDeploymentGenerationMismatch

## Meaning

Deployment generation mismatch due to possible rollback or failed update (triggering alerts related to deployment generation issues) because the observed generation does not match the desired generation, indicating that a deployment update or rollback operation has not completed successfully. Deployments show generation mismatches in kubectl, deployment events show Failed, ProgressDeadlineExceeded, or ReplicaSetCreateError errors, and ReplicaSet resources may show creation failures. This affects the workload plane and indicates deployment reconciliation failures or update problems, typically caused by persistent resource constraints, deployment controller issues, or cluster capacity limitations; applications run with outdated configurations and may show errors.

## Impact

KubeDeploymentGenerationMismatch alerts fire; service degradation or unavailability; deployment cannot achieve desired state; generation mismatch prevents proper reconciliation; deployment update or rollback is stuck; deployment status shows generation mismatch; controllers cannot reconcile deployment state; deployment reconciliation operations fail. Deployments show generation mismatches indefinitely; deployment events show Failed or ProgressDeadlineExceeded errors; ReplicaSet creation failures prevent generation updates; applications run with outdated configurations and may experience errors or performance degradation.

## Playbook

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Observed generation versus desired generation
   - Replicas status (desired/updated/ready/available)
   - Conditions showing why rollout is stuck
   - Events showing Failed, ProgressDeadlineExceeded, or ReplicaSetCreateError errors

2. List events in namespace <namespace> filtered by involved object name <deployment-name> and sorted by last timestamp to see the sequence of generation mismatch issues.

3. Retrieve rollout history for deployment <deployment-name> in namespace <namespace> to identify recent updates or rollbacks that may have caused the mismatch.

4. List ReplicaSet resources in namespace <namespace> with label app=<app-label> and check ReplicaSet status and replica counts to verify replica distribution.

5. List pods in namespace <namespace> with label app=<app-label> and describe pod <pod-name> to identify pods in failed or error states.

6. Retrieve deployment <deployment-name> in namespace <namespace> and check the update strategy configuration and whether rollout is paused to identify update blockers.

## Diagnosis

1. Analyze deployment events from Playbook steps 1-2 to identify the primary failure reason. Events showing "ProgressDeadlineExceeded" indicate rollout timeout. Events showing "ReplicaSetCreateError" indicate ReplicaSet creation failures. Events showing "FailedCreate" indicate pod creation issues. Events showing "Paused" indicate intentionally paused rollout.

2. If events indicate ProgressDeadlineExceeded, check deployment conditions from Playbook step 1 to identify the specific reason rollout did not complete. Correlate with rollout history from Playbook step 3 to determine if this is a new update or a stuck previous update.

3. If events indicate ReplicaSet creation failures, analyze ReplicaSet status from Playbook step 4 to identify which generation's ReplicaSet failed. Check for resource quota constraints or admission webhook rejections in the event messages.

4. If events indicate scheduling failures (FailedScheduling), correlate pod pending status from Playbook step 5 with the new ReplicaSet to confirm new pods cannot be scheduled. Verify resource constraints from node capacity data.

5. If events indicate image pull failures (ErrImagePull, ImagePullBackOff), verify the new image reference from the deployment spec and check if the new image exists and is accessible.

6. If events indicate pod crashes (CrashLoopBackOff, Error) for new pods, analyze pod describe output from Playbook step 5 to identify why new version pods are failing. This indicates application-level issues with the new deployment version.

7. If deployment shows "Paused: true" from Playbook step 6, the generation mismatch is expected behavior during a paused rollout. Verify if pause was intentional or requires manual intervention to resume.

8. If events are inconclusive, compare observed generation versus desired generation from Playbook step 1 and correlate with rollout history from Playbook step 3 to determine if mismatch is due to a recent update, a rollback attempt, or a stuck reconciliation.

**If no clear failure reason is identified from events**: Review deployment controller logs for reconciliation errors, check for persistent resource constraints across the cluster, verify deployment controller pod health in kube-system namespace, and examine if the deployment has been modified multiple times in quick succession causing controller backlog.
