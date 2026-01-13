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

1. List pods in `kube-system` and filter for API server pods (or the managed control plane workload) to check whether they are running, CrashLooping, or not scheduled.

2. Retrieve cluster configuration to confirm the API server endpoint, IP, and port that clients and controllers are using.

3. On each control plane node, check the kubelet service status and logs to confirm that kubelet is running, healthy, and able to start or supervise the API server pod or static pod.

## Diagnosis

1. Compare the connection refused error timestamps with API server pod restart timestamps and check whether restarts occur within 2 minutes of the first connection refused errors.

2. Compare the connection refused error timestamps with kubelet restart timestamps from the control plane node logs, and check whether kubelet restarts occur within 5 minutes of the errors.

3. Compare the connection refused error timestamps with static pod manifest or API server Deployment modification timestamps, and check whether configuration changes occurred within 1 hour before the errors began.

4. Compare the connection refused error timestamps with node maintenance timestamps from your infrastructure or change records, and check for maintenance activity within 5 minutes of the errors.

5. Compare the connection refused error timestamps with certificate expiration dates from `kubeadm certs check-expiration`, and check whether errors started within 5 minutes of a certificate's expiration time.

6. Compare the connection refused error timestamps with cluster maintenance or upgrade window timestamps from your change management system, and check whether errors began within 1 hour of those activities.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review kubelet logs for earlier API server connection attempts, check for certificate expiration that may have occurred just before the errors, examine control plane node system logs for process failures, and verify if static pod manifests were modified outside of recorded changes. Connection refused errors may indicate API server process issues that developed gradually.

