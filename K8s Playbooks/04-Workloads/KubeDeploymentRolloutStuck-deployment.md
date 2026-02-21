---
title: Kube Deployment Rollout Stuck
weight: 48
categories: [kubernetes, deployment]
---

# KubeDeploymentRolloutStuck

## Meaning

Deployment rollout is stuck and not progressing (triggering KubeDeploymentRolloutStuck alerts) because new pods cannot become ready within the progress deadline, preventing the deployment from completing. Deployment shows progressing condition as False, old pods are not being replaced, and the new version is not fully deployed. This affects application updates; new version is not deployed; rollout is blocked; mixed version state may exist.

## Impact

KubeDeploymentRolloutStuck alerts fire; deployment cannot complete; new version is partially or not deployed; old pods continue running; potential version inconsistency; feature releases are blocked; bug fixes are not applied; CI/CD pipeline is stuck; manual intervention required.

## Playbook

1. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and check rollout status and conditions.

2. Identify the new ReplicaSet and check why its pods are not becoming ready.

3. Retrieve pods from the new ReplicaSet and check their status (Pending, CrashLoopBackOff, ImagePullBackOff).

4. Retrieve events for the failing pods to identify specific failure reasons.

5. Check if readiness probes are failing on new pods.

6. Verify resource requests can be satisfied by cluster capacity.

7. Check for PodDisruptionBudget blocking the rollout.

## Diagnosis

Analyze new pod failures to categorize: CrashLoopBackOff indicates application or configuration issues, Pending indicates resource or scheduling issues, ImagePullBackOff indicates image issues, using pod status as supporting evidence.

Check readiness probe configuration and verify probes are appropriate for the application startup time, using probe settings and application startup metrics as supporting evidence.

Verify the new image is correct, accessible, and functional by checking image tag and pull status, using image configuration and pull events as supporting evidence.

Compare new pod spec with old working pods to identify configuration changes that may cause failures, using deployment revision diff as supporting evidence.

Check for PDB violations that prevent old pods from being terminated before new pods are ready, using PDB status and eviction events as supporting evidence.

If no correlation is found within the specified time windows: rollback deployment to previous working version, fix the new version issues, redeploy with fixes, increase progress deadline if startup is legitimately slow, review deployment strategy (rolling vs recreate).
