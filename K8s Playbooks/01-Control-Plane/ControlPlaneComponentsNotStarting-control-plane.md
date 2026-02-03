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

1. Describe control plane component pods in namespace kube-system with label tier=control-plane to retrieve detailed information about all control plane component pods including API server, controller manager, scheduler, and etcd.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for component startup failures, CrashLoopBackOff, or configuration errors.

3. List all nodes and identify control plane nodes, checking their Ready status and any conditions indicating resource or network issues.

4. Retrieve logs from the failing control plane component pods (for example, kube-apiserver or etcd) in kube-system, or from systemd services on the control plane nodes, and look for configuration, certificate, or resource errors.

5. On control plane nodes, inspect the static pod manifest files (such as /etc/kubernetes/manifests/kube-apiserver.yaml and /etc/kubernetes/manifests/etcd.yaml) to verify configuration, file paths, certificates, and arguments.

6. Retrieve resource usage metrics for all nodes and confirm that control plane nodes have sufficient CPU and memory headroom.

7. Check disk space and inode availability on control plane nodes, especially on volumes hosting etcd data and Kubernetes manifests.

8. From the API server pod or control plane node, verify network connectivity to etcd endpoints to ensure the API server can reach its datastore.

## Diagnosis

1. Analyze control plane component events from Playbook to identify which components are failing and the nature of failures. If events show CrashLoopBackOff, Failed, or ImagePullBackOff, use event timestamps and error messages to identify the specific failure cause.

2. If events indicate configuration errors or invalid arguments, examine static pod manifests from Playbook step 5. If events show validation failures or argument parsing errors at component startup timestamps, configuration issues are the root cause.

3. If events indicate certificate errors or TLS failures, verify certificate expiration status from Playbook. If certificate-related events appear at timestamps when components stopped starting, expired or invalid certificates are causing failures.

4. If events indicate resource pressure (OOMKilled, Evicted), check node resource metrics from Playbook step 6. If resource usage approached limits at event timestamps, resource exhaustion is preventing component startup.

5. If events indicate disk space or storage issues, verify disk availability from Playbook step 7. If disk space was low or exhausted at event timestamps, storage constraints are blocking component startup.

6. If events indicate kubelet failures or node issues, analyze kubelet status from Playbook step 4. If kubelet events show restarts or failures preceding component failures, kubelet problems are preventing static pod management.

7. If events show etcd connectivity failures, verify etcd status and network connectivity from Playbook step 8. If etcd events show unavailability at timestamps when other components failed to start, etcd issues are the root cause.

8. If events indicate recent upgrade or maintenance activity, correlate activity timestamps with component failure onset. If failures began during or shortly after upgrade operations, the upgrade process may have introduced issues.

**If no correlation is found**: Review component logs for earlier warning messages or gradual failures, check for resource exhaustion that developed over time, examine certificate expiration, verify disk space and inode availability trends, and check if configuration files were modified outside of standard deployment processes. Component startup failures may result from cumulative issues rather than immediate changes.

