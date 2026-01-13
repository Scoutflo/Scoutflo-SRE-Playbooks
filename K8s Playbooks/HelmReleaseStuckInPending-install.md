---
title: Helm Release Stuck in PENDING_INSTALL
weight: 244
categories:
  - kubernetes
  - workload
---

# HelmReleaseStuckInPending-install

## Meaning

A Helm release remains stuck in the PENDING_INSTALL state because one or more chart resources cannot be created, validated, or scheduled successfully by the cluster. This indicates Helm chart validation failures, resource creation errors, scheduling constraints, or RBAC permission issues preventing successful Helm installation.

## Impact

Helm releases cannot complete installation; applications fail to deploy; resources remain in pending state; deployments are incomplete; services cannot start; Helm installation hangs; chart resources fail to be created; installation progress stalls.

## Playbook

1. Check Helm release status for release `<release-name>` in namespace `<namespace>`.

2. Retrieve logs from failing pods in namespace `<namespace>` and filter for error patterns.

3. Check Helm release events for release `<release-name>` in namespace `<namespace>`.

4. Check Helm chart configuration to verify Helm chart values and templates.

5. Retrieve pods in namespace `<namespace>` to check for resource constraints.

6. Retrieve ResourceQuota and RBAC permissions in namespace `<namespace>`.

## Diagnosis

1. Compare the timestamps when Helm release entered PENDING_INSTALL state with Helm chart value change timestamps, and check whether pending state begins within 1 hour of chart value modifications.

2. Compare the Helm release pending timestamps with pod creation failure timestamps from failing pod logs and Helm release events, and verify whether pending state correlates with pod creation failures at the same time.

3. Compare the Helm release pending timestamps with resource constraint timestamps from pod resource usage, and check whether pending state correlates with resource constraints.

4. Compare the Helm release pending timestamps with deployment or configuration change timestamps, and verify whether pending state begins within 1 hour of deployment changes.

5. Compare the Helm release pending timestamps with Helm chart template error timestamps, and check whether pending state correlates with template validation failures.

6. Compare the Helm release pending timestamps with namespace or RBAC issue timestamps from resource quota and role binding changes, and verify whether pending state correlates with permission or quota problems at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours), review Helm chart templates for validation errors, check for resource name conflicts, examine namespace resource quotas for hidden constraints, verify if RBAC permissions are sufficient for all chart resources, check for admission webhook blocks, and review Helm release history for previous installation attempts. Pending installations may result from chart validation issues or resource conflicts not immediately visible in Helm events.
