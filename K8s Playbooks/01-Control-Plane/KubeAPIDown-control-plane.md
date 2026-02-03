---
title: Kube API Down
weight: 20
---

# KubeAPIDown

## Meaning

Kubernetes API server is unreachable or non-responsive (triggering KubeAPIDown alerts) because all API server instances have failed, lost network connectivity, or are experiencing critical failures. API server pods show CrashLoopBackOff or Failed state in kubectl, API server logs show fatal errors, panic messages, or connection timeout errors, and kubectl commands return connection refused or timeout errors. This affects the control plane and prevents all cluster operations that require API server communication, typically caused by pod crashes, etcd unavailability, certificate expiration, node failures, or network partitions; applications cannot access cluster resources and may show errors in application monitoring.

## Impact

KubeAPIDown alerts fire; all API operations fail; cluster becomes completely non-functional; kubectl commands fail; controllers stop reconciling; nodes cannot communicate with control plane; new pods cannot be scheduled; resource updates are blocked; cluster is effectively down; authentication and authorization fail; service discovery and endpoint updates stop; Prometheus monitoring cannot scrape API server metrics. API server pods remain in CrashLoopBackOff or Failed state; API server endpoints return connection refused or timeout errors; cluster operations are completely blocked; applications cannot access cluster resources and may experience errors or performance degradation.

## Playbook

1. Describe pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, restart count, container states, and any error conditions.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for API server failures, CrashLoopBackOff, or connection errors.

3. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

4. Verify API server endpoint connectivity by checking cluster-info and testing API server health endpoints to confirm if API server is reachable.

5. Retrieve the Node `<node-name>` for control plane nodes hosting API server pods and check node status and network connectivity to verify node health.

6. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=etcd` and check etcd pod status and health to verify etcd availability as API server depends on etcd.

7. Retrieve NetworkPolicy resources and verify network policies and firewall rules that may block Prometheus or monitoring system access to API server endpoints.

## Diagnosis

1. Analyze API server pod events from Playbook to identify the failure mode. If events show CrashLoopBackOff, Failed, or pod termination with specific error messages, use event timestamps to determine when failures began and the root cause category.

2. If events indicate API server crashes or panics, examine API server logs for fatal errors or panic traces at event timestamps. If logs show panic messages or fatal errors, application-level issues or configuration problems caused the crash.

3. If events indicate etcd connectivity failures, analyze etcd pod events and health status from Playbook step 6. If etcd events show unavailability, leader election issues, or failures at timestamps preceding API server failures, etcd is the root cause.

4. If events indicate certificate errors or authentication failures, verify certificate expiration and validity from API server logs. If certificate-related errors appear at event timestamps, expired or invalid certificates caused API server failures.

5. If events indicate resource pressure (OOMKilled, CPU throttling), verify API server pod resource usage against limits. If resource usage exceeded limits at event timestamps, resource constraints caused the failure.

6. If events indicate control plane node issues, analyze node condition transitions from Playbook step 5. If node events show NotReady, MemoryPressure, or DiskPressure at timestamps preceding API server failures, node-level problems are the root cause.

7. If events indicate network policy or firewall changes, correlate network configuration change timestamps with API server failure onset. If network changes occurred before API server became unreachable, network configuration blocked connectivity.

**If no correlation is found**: Extend timeframes to 1 hour for infrastructure changes, review control plane node system logs, check for storage issues affecting etcd, verify external load balancer health, examine historical API server stability patterns. API server failures may result from hardware failures, network infrastructure issues, or control plane node failures rather than immediate configuration changes.
