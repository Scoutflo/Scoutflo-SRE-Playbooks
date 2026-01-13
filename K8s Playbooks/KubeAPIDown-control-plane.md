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

1. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and inspect its status, restart count, and container states to verify if the API server is running.

2. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'etcd', 'timeout', 'certificate' to identify startup or runtime failures.

3. Verify API server endpoint connectivity by checking cluster-info and testing API server health endpoints to confirm if API server is reachable.

4. Retrieve the Node `<node-name>` for control plane nodes hosting API server pods and check node status and network connectivity to verify node health.

5. Retrieve events for the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff', 'Unhealthy' to identify pod lifecycle issues.

6. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=etcd` and check etcd pod status and health to verify etcd availability as API server depends on etcd.

7. Retrieve NetworkPolicy resources and verify network policies and firewall rules that may block Prometheus or monitoring system access to API server endpoints.

## Diagnosis

Compare API server pod restart timestamps with etcd pod status changes within 2 minutes and verify whether API server failures coincide with etcd unavailability, using pod events and etcd health status as supporting evidence.

Correlate API server unavailability timestamps with control plane node condition transitions within 5 minutes and verify whether API server failures align with node NotReady conditions or network partitions, using node conditions and API server pod status as supporting evidence.

Compare API server log error timestamps with certificate expiration times within 2 minutes and verify whether API server failures began after certificate expiration, using API server logs and certificate metadata as supporting evidence.

Analyze API server error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using API server logs and pod resource usage metrics as supporting evidence.

Correlate API server unavailability with network policy or firewall rule change timestamps within 10 minutes and verify whether connectivity issues began after network configuration changes, using network policy events and API server connection logs as supporting evidence.

Compare API server pod resource usage metrics with resource limits at failure times and verify whether resource constraints caused API server failures, using pod metrics and resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review control plane node system logs, check for storage issues affecting etcd, verify external load balancer health, examine historical API server stability patterns. API server failures may result from hardware failures, network infrastructure issues, or control plane node failures rather than immediate configuration changes.
