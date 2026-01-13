---
title: Control Plane Components Not Starting - Control Plane
weight: 292
categories:
  - kubernetes
  - control-plane
---

# ControlPlaneComponentsNotStarting-control-plane

## Meaning

Core control-plane components such as kube-apiserver, etcd, controller-manager, or scheduler are failing to start or are crashlooping (potentially triggering KubeAPIDown, KubeSchedulerDown, KubeControllerManagerDown alerts) because of configuration errors, resource exhaustion, certificate issues, or OS/runtime issues on control-plane nodes. Control plane component failures prevent cluster operations.

## Impact

Cluster becomes non-functional; API server unavailable; etcd data store inaccessible; all cluster operations fail; existing workloads may continue but cannot be managed; cluster is effectively down; KubeAPIDown, KubeSchedulerDown, or KubeControllerManagerDown alerts fire; control plane pods in CrashLoopBackOff or Pending state; cluster management impossible.

## Playbook

1. List all nodes and identify control plane nodes, checking their Ready status and any conditions indicating resource or network issues.

2. Retrieve logs from the failing control plane component pods (for example, `kube-apiserver` or `etcd`) in `kube-system`, or from systemd services on the control plane nodes, and look for configuration, certificate, or resource errors.

3. List pods in `kube-system` and filter for all control plane components to see which pods are Pending, CrashLooping, or not scheduled.

4. On control plane nodes, inspect the static pod manifest files (such as `/etc/kubernetes/manifests/kube-apiserver.yaml` and `/etc/kubernetes/manifests/etcd.yaml`) to verify configuration, file paths, certificates, and arguments.

5. Retrieve resource usage metrics for all nodes and confirm that control plane nodes have sufficient CPU and memory headroom.

6. Check disk space and inode availability on control plane nodes (for example, using `df -h`), especially on volumes hosting etcd data and Kubernetes manifests.

7. From the API server pod or control plane node, verify network connectivity to etcd endpoints to ensure the API server can reach its datastore.

## Diagnosis

1. Compare the timestamps when control plane pods report failing or waiting states with static pod manifest or Deployment modification timestamps for those components, and check whether configuration changes occurred within 1 hour before the failures began.

2. Compare the control plane component failure timestamps with node resource usage metrics (CPU, memory, and disk) for control plane nodes and check whether resource usage spiked or remained high during the same period.

3. Compare the control plane component failure timestamps with certificate expiration times from `kubeadm certs check-expiration`, and check whether components started failing within 5 minutes of a certificate expiration.

4. Compare the control plane component failure timestamps with kubelet and system service restart timestamps from the affected nodes, and check whether restarts occurred within 5 minutes before components stopped starting successfully. If kubelet restarts are found, this indicates node-level issues affecting component startup.

5. Compare the control plane component failure timestamps with disk space checks (for example, results of `df -h` on control plane nodes), and check whether low disk conditions or full partitions were present at or just before the failures.

6. Compare the control plane component failure timestamps with cluster upgrade or maintenance window timestamps, and check whether failures started within 1 hour of upgrade or maintenance activities.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review component logs for earlier warning messages or gradual failures, check for resource exhaustion that developed over time, examine certificate expiration that may have occurred earlier, verify disk space and inode availability trends, and check if configuration files were modified outside of standard deployment processes. Component startup failures may result from cumulative issues rather than immediate changes.

