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

1. Describe pods in namespace kube-system with label component=kube-scheduler to retrieve detailed scheduler pod information including status, restart count, container states, and any error conditions.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for scheduler failures, CrashLoopBackOff, or connection errors.

3. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

4. Verify network connectivity between monitoring system and scheduler endpoints to confirm if connectivity issues are preventing monitoring.

5. Retrieve the Pod `<pod-name>` in namespace `kube-system` and check scheduler resource usage and verify if resource constraints are affecting operation.

6. Verify API server connectivity from scheduler perspective by checking API server endpoint accessibility as scheduler depends on API server.

## Diagnosis

1. Analyze scheduler pod events from Playbook to identify the failure mode. If events show CrashLoopBackOff, Failed, or pod termination, use event timestamps and error messages to determine when failures began and the root cause category.

2. If events indicate scheduler crashes or panics, examine logs from Playbook step 3. If logs show panic messages, fatal errors, or startup failures at event timestamps, application-level issues or configuration problems caused the crash.

3. If events indicate API server connectivity failures, verify API server status from Playbook step 6. If API server events show unavailability or connection errors at timestamps preceding scheduler failures, API server is the root cause.

4. If events indicate certificate errors or authentication failures, verify certificate expiration and validity. If certificate-related errors appear at event timestamps, expired or invalid certificates caused scheduler failures.

5. If events indicate resource pressure (OOMKilled, CPU throttling), verify pod resource usage at event timestamps. If resource usage exceeded limits when failures began, resource constraints caused the failure.

6. If events indicate control plane node issues, analyze node condition transitions. If node events show NotReady, MemoryPressure, or DiskPressure at timestamps preceding scheduler failures, node-level problems are the root cause.

7. If events indicate monitoring connectivity issues (Prometheus cannot discover targets), verify network connectivity between monitoring system and scheduler endpoints from Playbook step 4. If network issues are present at failure timestamps, monitoring-specific connectivity problems may exist.

**If no correlation is found**: Extend timeframes to 1 hour for infrastructure changes, review scheduler configuration, check for API server connectivity issues, verify control plane node health, examine historical scheduler stability patterns. Scheduler failures may result from control plane node issues, API server problems, or resource constraints rather than immediate configuration changes.
