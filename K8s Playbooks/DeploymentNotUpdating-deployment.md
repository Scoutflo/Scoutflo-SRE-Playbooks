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

1. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and inspect deployment status, conditions, and replica counts to identify update failures and mismatch between desired and updated replicas.

2. Verify ReplicaSet generation matches by comparing deployment generation with observed generation to check if deployment controller is reconciling.

3. List events in namespace `<namespace>` and filter for deployment-related events, focusing on events with reasons such as `FailedCreate`, `FailedUpdate`, or messages indicating pod creation or update failures.

4. Retrieve pods associated with the deployment and check their status to verify if new pods are being created, if they are failing to start, or if old pods are not being terminated.

5. Check the deployment's update strategy configuration (rolling update, recreate) and verify if strategy parameters are preventing updates.

6. List events in namespace `<namespace>` and filter for pod creation failures, image pull errors, or resource constraint errors that may prevent new pods from being created during updates.

7. Verify that the deployment controller is running and functioning by checking deployment controller pod status in the kube-system namespace and reviewing deployment controller logs.

## Diagnosis

1. Compare the deployment update failure timestamps with deployment controller reconciliation failure timestamps from deployment controller logs, and check whether controller reconciliation errors occurred within 5 minutes before deployment updates failed.

2. Compare the deployment update failure timestamps with ReplicaSet generation mismatch timestamps, and check whether ReplicaSet creation failures occurred within 5 minutes before deployment updates failed.

3. Compare the deployment update failure timestamps with pod creation failure event timestamps, and check whether pod creation errors occurred within 5 minutes before deployment updates failed.

4. Compare the deployment update failure timestamps with image pull failure event timestamps, and check whether image pull errors occurred within 5 minutes before deployment updates failed, preventing new pods from starting.

5. Compare the deployment update failure timestamps with deployment update strategy modification timestamps, and check whether strategy changes occurred within 30 minutes before update failures.

6. Compare the deployment update failure timestamps with resource quota or limit modification timestamps, and check whether resource constraints were introduced within 30 minutes before deployment updates failed.

7. Compare the deployment update failure timestamps with deployment controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before update failures.

8. Compare the deployment update failure timestamps with cluster scaling events or node capacity changes, and check whether resource availability decreased within 30 minutes before deployment updates failed.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review deployment controller logs for gradual performance degradation, check for intermittent resource constraint issues, examine if deployment update strategy was always restrictive but only recently enforced, verify if image registry connectivity issues developed over time, and check for cumulative resource pressure that may have prevented pod creation. Deployment update failures may result from gradual infrastructure issues rather than immediate configuration changes.

