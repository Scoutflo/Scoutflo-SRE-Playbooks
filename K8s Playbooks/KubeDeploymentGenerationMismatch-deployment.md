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

1. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and inspect its status to check observed generation versus desired generation and identify the mismatch.

2. Retrieve rollout history for the Deployment `<deployment-name>` in namespace `<namespace>` to identify recent updates or rollbacks that may have caused the mismatch.

3. Retrieve events for the Deployment `<deployment-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'ProgressDeadlineExceeded', 'ReplicaSetCreateError' to identify deployment issues.

4. Retrieve ReplicaSet resources belonging to the Deployment `<deployment-name>` in namespace `<namespace>` and check ReplicaSet status and replica counts to verify replica distribution.

5. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the Deployment `<deployment-name>` and check pod status to identify pods in failed or error states.

6. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and verify deployment update strategy and check if rollout is paused to identify update blockers.

## Diagnosis

Compare deployment generation mismatch detection timestamps with deployment update or rollback initiation times within 30 minutes and verify whether generation mismatch began when update or rollback started, using deployment events and rollout history as supporting evidence.

Correlate deployment generation mismatch with ReplicaSet creation failure timestamps within 30 minutes and verify whether ReplicaSet creation failures prevented generation update, using ReplicaSet events and deployment status as supporting evidence.

Compare deployment generation mismatch with pod scheduling failure timestamps within 30 minutes and verify whether pod scheduling failures prevented deployment from achieving desired generation, using pod events and deployment status as supporting evidence.

Analyze deployment generation mismatch patterns over the last 1 hour to determine if mismatch is persistent (reconciliation failure) or transient (update in progress), using deployment status history and ReplicaSet status as supporting evidence.

Correlate deployment generation mismatch with resource quota exhaustion timestamps within 30 minutes and verify whether quota limits prevented ReplicaSet or pod creation, using resource quota status and deployment events as supporting evidence.

Compare deployment generation mismatch with node capacity exhaustion timestamps within 30 minutes and verify whether insufficient cluster capacity prevented deployment from achieving desired generation, using node metrics and deployment scaling attempts as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for deployment operations, review deployment update strategy configuration, check for persistent resource constraints, verify deployment controller health, examine historical deployment generation patterns. Deployment generation mismatch may result from persistent resource constraints, deployment controller issues, or cluster capacity limitations rather than immediate changes.
