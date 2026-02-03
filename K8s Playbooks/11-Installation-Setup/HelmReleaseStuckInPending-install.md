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

1. Retrieve the Helm release status for release `<release-name>` in namespace `<namespace>` to inspect installation state.

2. Get events in the namespace `<namespace>` sorted by timestamp to identify Helm release failures and resource creation errors.

3. Retrieve logs from failing pods in namespace `<namespace>` and filter for error patterns.

4. Check Helm chart configuration to verify Helm chart values and templates.

5. Retrieve pods in namespace `<namespace>` to check for resource constraints.

6. Retrieve ResourceQuota and RBAC permissions in namespace `<namespace>`.

## Diagnosis

Begin by analyzing the Helm release status, namespace events, and pod states collected in the Playbook section. The release status message, resource creation events, and pod scheduling status provide the primary diagnostic signals.

**If events show FailedCreate with RBAC or permission errors:**
- Helm cannot create resources due to insufficient permissions. Check if the service account or user running Helm has ClusterRole or Role bindings for all resource types in the chart. Grant necessary RBAC permissions.

**If events show FailedScheduling for pods created by the chart:**
- Pods cannot be scheduled due to resource constraints or node selectors. Check pod pending reasons. If `Insufficient cpu` or `Insufficient memory`, add cluster capacity or reduce resource requests.

**If events show admission webhook denied or validation errors:**
- An admission controller is blocking resource creation. Check the event message for which webhook denied the request. Review the chart values against the webhook's validation policies.

**If events show ResourceQuota exceeded:**
- The namespace quota blocks resource creation. Check `kubectl get resourcequota -n <namespace>`. Either increase quota limits or reduce chart resource requirements.

**If Helm status shows "another operation in progress":**
- A previous Helm operation did not complete cleanly. Run `helm history <release> -n <namespace>` to check for stuck releases. Use `helm rollback` to a previous revision or `helm uninstall` if appropriate.

**If chart resources are created but Deployment pods fail to start:**
- The chart installed but application pods have issues. Check pod describe output for container startup errors. This is an application issue rather than a Helm issue.

**If events are inconclusive, correlate timestamps:**
1. Check if PENDING_INSTALL began after a failed upgrade attempt by reviewing Helm history.
2. Check if resource quota changes occurred that blocked the installation.
3. Check if admission webhooks were added or modified.

**If no clear cause is identified:** Run `helm install --dry-run --debug` to validate the chart templates without applying. Check for template rendering errors or invalid resource specifications.
