---
title: Kube Scheduler Down
weight: 20
---

# KubeSchedulerDown

## Meaning

Kube Scheduler has disappeared from Prometheus target discovery or is unreachable (triggering KubeSchedulerDown alerts) because the scheduler process has failed, lost network connectivity, or cannot be monitored. Scheduler pods show CrashLoopBackOff or Failed state in kubectl, scheduler logs show fatal errors, panic messages, or connection timeout errors, and pods remain in Pending state waiting for scheduling. This affects the control plane and prevents the scheduler from assigning pods to nodes, causing new pods to remain in Pending state, typically caused by pod failures, API server connectivity issues, certificate problems, or resource constraints; applications cannot start new pods and may show errors in application monitoring.

## Impact

KubeSchedulerDown alerts fire; cluster may be partially or fully non-functional; new pods cannot be scheduled; pods remain in Pending state; scheduler cannot assign pods to nodes; deployments and other workloads cannot scale; cluster scheduling operations are blocked; Prometheus cannot discover scheduler targets; pod scheduling operations are completely blocked. Scheduler pods remain in CrashLoopBackOff or Failed state; scheduler endpoints return connection refused or timeout errors; pods remain in Pending state indefinitely; applications cannot start new pods and may experience errors or performance degradation.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-scheduler` or check static pod status if running as static pod and inspect its status, restart count, and container states to verify if the scheduler is running.

2. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

3. Retrieve events for the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff' to identify pod lifecycle issues.

4. Verify network connectivity between monitoring system and scheduler endpoints to confirm if connectivity issues are preventing monitoring.

5. Retrieve the Pod `<pod-name>` in namespace `kube-system` and check scheduler resource usage and verify if resource constraints are affecting operation.

6. Verify API server connectivity from scheduler perspective by checking API server endpoint accessibility as scheduler depends on API server.

## Diagnosis

Compare scheduler unavailability timestamps with scheduler pod restart or failure timestamps within 5 minutes and verify whether unavailability coincides with pod failures, using pod events and scheduler status as supporting evidence.

Correlate scheduler failures with API server connectivity failure timestamps within 2 minutes and verify whether scheduler failures align with API server unavailability, using API server health status and scheduler logs as supporting evidence.

Compare scheduler log error timestamps with certificate expiration times within 2 minutes and verify whether scheduler failures began after certificate expiration, using scheduler logs and certificate metadata as supporting evidence.

Analyze scheduler error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using scheduler logs and pod resource usage metrics as supporting evidence.

Correlate scheduler unavailability with control plane node condition transitions within 5 minutes and verify whether node failures caused scheduler unavailability, using node conditions and scheduler pod status as supporting evidence.

Compare scheduler pod resource usage metrics with resource limits at failure times and verify whether resource constraints caused scheduler failures, using pod metrics and resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review scheduler configuration, check for API server connectivity issues, verify control plane node health, examine historical scheduler stability patterns. Scheduler failures may result from control plane node issues, API server problems, or resource constraints rather than immediate configuration changes.
