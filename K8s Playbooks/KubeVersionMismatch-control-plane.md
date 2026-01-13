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

1. Retrieve the Node `<node-name>` for all nodes in the cluster and retrieve Kubernetes version information to compare versions and identify mismatches.

2. Retrieve the Pod `<pod-name>` in namespace `kube-system` with labels `component=kube-apiserver`, `component=kube-controller-manager`, and `component=kube-scheduler` and check control plane component versions including API server, controller manager, and scheduler to identify version differences.

3. Retrieve the Node `<node-name>` for worker nodes and check worker node versions and compare with control plane versions to identify version gaps.

4. Retrieve cluster upgrade status and verify if there is an ongoing Kubernetes upgrade process, especially in managed services, to determine if mismatches are expected during upgrades.

5. Check for version-specific API deprecations or changes that may affect compatibility by comparing component versions with Kubernetes compatibility matrices.

6. Retrieve events and logs for the Pod `<pod-name>` in namespace `<namespace>` running different versions and filter for version-related errors to identify compatibility issues.

## Diagnosis

Compare version mismatch detection timestamps with cluster upgrade initiation times within 1 hour and verify whether version mismatches began when upgrade process started, using upgrade logs and node version changes as supporting evidence.

Correlate version mismatches with node upgrade or replacement event timestamps within 1 hour and verify whether node upgrades created version inconsistencies, using node version history and upgrade events as supporting evidence.

Compare version mismatch patterns across nodes to determine if mismatches are systematic (upgrade in progress) or isolated (failed upgrade), using node versions and upgrade status as supporting evidence.

Analyze component version compatibility to identify which version differences may cause issues, using Kubernetes version compatibility matrices and component versions as supporting evidence.

Correlate version mismatches with API error or compatibility error timestamps within 1 hour and verify whether version mismatches caused API or component communication failures, using API error logs and component communication logs as supporting evidence.

Compare current version distribution with historical version patterns to verify whether version mismatches represent normal upgrade process or failed upgrade state, using version history and upgrade plans as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 24 hours for upgrade processes, review cluster upgrade procedures, check for failed upgrade operations, verify node pool version configurations, examine historical version consistency patterns. Version mismatches may result from incomplete upgrades, manual version changes, or upgrade process failures rather than immediate operational changes.
