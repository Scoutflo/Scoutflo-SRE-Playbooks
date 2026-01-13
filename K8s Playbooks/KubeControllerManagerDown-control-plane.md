---
title: Kube Controller Manager Down
weight: 20
---

# KubeControllerManagerDown

## Meaning

Kube Controller Manager has disappeared from Prometheus target discovery or is unreachable (triggering KubeControllerManagerDown alerts) because the controller manager process has failed, lost network connectivity, or cannot be monitored. Controller manager pods show CrashLoopBackOff or Failed state in kubectl, controller manager logs show fatal errors, panic messages, or connection timeout errors, and Prometheus cannot discover controller manager targets. This affects the control plane and prevents Kubernetes controllers from reconciling resource states, managing deployments, and maintaining cluster state, typically caused by pod failures, etcd connectivity issues, certificate problems, or resource constraints; applications may experience deployment failures and show errors in application monitoring.

## Impact

KubeControllerManagerDown alerts fire; cluster is not fully functional; Kubernetes resources cannot be reconciled; controllers stop managing deployments, ReplicaSets, and other resources; desired state cannot be achieved; deployments and other workloads may not update; cluster state drifts from desired configuration; Prometheus cannot discover controller manager targets; deployment, ReplicaSet, and other resource reconciliation stops; cluster operations are severely degraded. Controller manager pods remain in CrashLoopBackOff or Failed state; controller manager endpoints return connection refused or timeout errors; deployments cannot scale or update; applications may experience deployment failures and show errors or performance degradation.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-controller-manager` or check static pod status if running as static pod and inspect its status, restart count, and container states to verify if the controller manager is running.

2. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

3. Retrieve events for the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff' to identify pod lifecycle issues.

4. Verify network connectivity between monitoring system and controller manager endpoints to confirm if connectivity issues are preventing monitoring.

5. Retrieve the Pod `<pod-name>` in namespace `kube-system` and check controller manager resource usage and verify if resource constraints are affecting operation.

6. Verify etcd connectivity from controller manager perspective by checking etcd endpoint accessibility as controllers depend on etcd.

## Diagnosis

Compare controller manager unavailability timestamps with controller manager pod restart or failure timestamps within 5 minutes and verify whether unavailability coincides with pod failures, using pod events and controller manager status as supporting evidence.

Correlate controller manager failures with etcd connectivity failure timestamps within 2 minutes and verify whether controller manager failures align with etcd unavailability, using etcd health status and controller manager logs as supporting evidence.

Compare controller manager log error timestamps with certificate expiration times within 2 minutes and verify whether controller manager failures began after certificate expiration, using controller manager logs and certificate metadata as supporting evidence.

Analyze controller manager error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using controller manager logs and pod resource usage metrics as supporting evidence.

Correlate controller manager unavailability with control plane node condition transitions within 5 minutes and verify whether node failures caused controller manager unavailability, using node conditions and controller manager pod status as supporting evidence.

Compare controller manager pod resource usage metrics with resource limits at failure times and verify whether resource constraints caused controller manager failures, using pod metrics and resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review controller manager configuration, check for etcd connectivity issues, verify control plane node health, examine historical controller manager stability patterns. Controller manager failures may result from control plane node issues, etcd problems, or resource constraints rather than immediate configuration changes.
