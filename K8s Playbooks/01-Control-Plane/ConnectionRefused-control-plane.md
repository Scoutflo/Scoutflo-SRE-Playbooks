---
title: Connection Refused - Control Plane
weight: 221
categories:
  - kubernetes
  - control-plane
---

# ConnectionRefused-control-plane

## Meaning

TCP connections to the Kubernetes API server address and port are being actively refused (potentially triggering KubeAPIDown or KubeletDown alerts), indicating that the API server process is not listening, not healthy, crashed, or not reachable on the expected interface. Connection refused errors indicate API server process failures or network binding issues.

## Impact

All kubectl commands fail with connection refused; cluster management operations cannot be performed; controllers cannot reconcile state; cluster becomes unmanageable; existing workloads may continue running but cannot be updated; KubeAPIDown alerts fire; API server process not running; connection refused errors occur; control plane components cannot communicate.

## Playbook

1. Describe API server pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, restart count, and container states to identify connection refused causes.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for API server failures or connection errors.

3. Retrieve cluster configuration to confirm the API server endpoint, IP, and port that clients and controllers are using.

4. On each control plane node, check the kubelet service status and logs to confirm that kubelet is running, healthy, and able to start or supervise the API server pod or static pod.

## Diagnosis

1. Analyze API server pod events from Playbook to identify if API server pods are crashing, failing to start, or being terminated. If events show CrashLoopBackOff, Failed, or pod termination, API server process failure is the root cause.

2. If events indicate API server pod restarts, correlate restart event timestamps with connection refused error onset. If restarts occurred at or just before connection failures began, pod instability is causing the connection issues.

3. If events indicate container startup failures or configuration errors, examine API server container status and logs. If events show image pull failures, probe failures, or configuration validation errors, container-level issues are preventing API server startup.

4. If events indicate kubelet issues on control plane nodes, verify kubelet status from Playbook step 4. If kubelet events show restarts or failures at timestamps preceding connection errors, kubelet problems are preventing API server pod management.

5. If events indicate certificate-related errors, verify certificate expiration status from Playbook. If certificate events or TLS errors appear at timestamps near connection refused errors, expired certificates may have caused API server failure.

6. If events show configuration changes (static pod manifests, Deployments, ConfigMaps), correlate change timestamps with error onset. If configuration modifications occurred before connection refused errors began, recent changes may have broken API server configuration.

7. If events indicate node-level issues or maintenance activity, correlate node condition changes with connection error timestamps. If node events show NotReady, MemoryPressure, or maintenance cordoning, node-level problems are affecting API server availability.

**If no correlation is found**: Review kubelet logs for earlier API server connection attempts, check for certificate expiration, examine control plane node system logs for process failures, and verify if static pod manifests were modified outside of recorded changes. Connection refused errors may indicate API server process issues that developed gradually.

