---
title: Kube Version Mismatch
weight: 20
---

# KubeVersionMismatch

## Meaning

Different semantic versions of Kubernetes components are running across the cluster (triggering KubeVersionMismatch alerts) because control plane nodes, worker nodes, or components are running different Kubernetes versions, typically during cluster upgrade processes. Nodes show different Kubernetes versions in cluster dashboards, control plane components show version mismatches, and API version compatibility errors may appear in logs. This affects the control plane and data plane and indicates version incompatibilities that may cause API version mismatches, feature availability issues, or component communication problems, typically caused by incomplete upgrades, failed upgrade processes, or manual version changes; applications may experience API version compatibility errors.

## Impact

KubeVersionMismatch alerts fire; incompatible API versions between Kubernetes components may cause issues; single containers, applications, or cluster stability may be affected; API version mismatches occur; feature availability varies across components; component communication may fail; cluster operations may be inconsistent; ongoing Kubernetes upgrade process may be incomplete or failed; version-specific API deprecations or changes cause compatibility issues. Nodes show different Kubernetes versions indefinitely; control plane components show version mismatches; API version compatibility errors may appear in logs; applications may experience API version compatibility errors or feature availability issues.

## Playbook

1. List all nodes with wide output to retrieve all nodes with their Kubernetes versions and identify version mismatches across the cluster.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for version-related errors, API compatibility issues, or upgrade failures.

3. Describe pods in namespace kube-system with label tier=control-plane to retrieve detailed control plane component information and check component versions including API server, controller manager, and scheduler.

4. Retrieve cluster upgrade status and verify if there is an ongoing Kubernetes upgrade process, especially in managed services, to determine if mismatches are expected during upgrades.

5. Check for version-specific API deprecations or changes that may affect compatibility by comparing component versions with Kubernetes compatibility matrices.

6. Retrieve events and logs for the Pod `<pod-name>` in namespace `<namespace>` running different versions and filter for version-related errors to identify compatibility issues.

## Diagnosis

1. Analyze cluster and node events from Playbook to identify if an upgrade is in progress or has recently occurred. If events show upgrade-related activity, version mismatches may be expected during the upgrade window.

2. If events indicate an active upgrade process, verify upgrade status from Playbook step 4. If upgrade is still in progress at event timestamps, version mismatches are expected and will resolve upon completion.

3. If events indicate upgrade failures or rollback activity, examine upgrade logs for errors. If events show failed upgrade attempts or incomplete node upgrades, the upgrade process needs remediation.

4. If events show node upgrade or replacement activity, correlate node version changes with event timestamps from Playbook step 1. If specific nodes show different versions after upgrade events, those nodes may have failed to upgrade.

5. If events indicate API compatibility errors, identify which component versions are incompatible. If events show API version errors between components at specific timestamps, version skew is causing operational issues requiring immediate attention.

6. If events show systematic version patterns across nodes (control plane vs workers), the version skew follows expected upgrade order. If version mismatches are isolated to specific nodes, those nodes require individual investigation.

7. If no upgrade activity is indicated in events, verify if version mismatches are due to manual interventions or configuration drift. If versions differ without upgrade events, manual changes or misconfigurations are the cause.

**If no correlation is found**: Extend timeframes to 24 hours for upgrade processes, review cluster upgrade procedures, check for failed upgrade operations, verify node pool version configurations, examine historical version consistency patterns. Version mismatches may result from incomplete upgrades, manual version changes, or upgrade process failures rather than immediate operational changes.
