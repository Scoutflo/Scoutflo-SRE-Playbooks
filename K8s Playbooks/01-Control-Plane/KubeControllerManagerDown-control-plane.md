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

1. Describe pods in namespace kube-system with label component=kube-controller-manager to retrieve detailed controller manager pod information including status, restart count, container states, and any error conditions.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for controller manager failures, CrashLoopBackOff, or connection errors.

3. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

4. Verify network connectivity between monitoring system and controller manager endpoints to confirm if connectivity issues are preventing monitoring.

5. Retrieve the Pod `<pod-name>` in namespace `kube-system` and check controller manager resource usage and verify if resource constraints are affecting operation.

6. Verify etcd connectivity from controller manager perspective by checking etcd endpoint accessibility as controllers depend on etcd.

## Diagnosis

1. Analyze controller manager pod events from Playbook to identify the failure mode. If events show CrashLoopBackOff, Failed, or pod termination, use event timestamps and error messages to determine when failures began and the root cause category.

2. If events indicate controller manager crashes or panics, examine logs from Playbook step 3. If logs show panic messages, fatal errors, or startup failures at event timestamps, application-level issues or configuration problems caused the crash.

3. If events indicate etcd connectivity failures, verify etcd pod status and health from Playbook step 6. If etcd events show unavailability, leader election issues, or connection errors at timestamps preceding controller manager failures, etcd is the root cause.

4. If events indicate certificate errors or authentication failures, verify certificate expiration and validity. If certificate-related errors appear at event timestamps, expired or invalid certificates caused controller manager failures.

5. If events indicate resource pressure (OOMKilled, CPU throttling), verify pod resource usage at event timestamps. If resource usage exceeded limits when failures began, resource constraints caused the failure.

6. If events indicate control plane node issues, analyze node condition transitions from Playbook. If node events show NotReady, MemoryPressure, or DiskPressure at timestamps preceding controller manager failures, node-level problems are the root cause.

7. If events indicate monitoring connectivity issues (Prometheus cannot discover targets), verify network connectivity between monitoring system and controller manager endpoints from Playbook step 4. If network issues are present at failure timestamps, monitoring-specific connectivity problems may exist.

**If no correlation is found**: Extend timeframes to 1 hour for infrastructure changes, review controller manager configuration, check for etcd connectivity issues, verify control plane node health, examine historical controller manager stability patterns. Controller manager failures may result from control plane node issues, etcd problems, or resource constraints rather than immediate configuration changes.
