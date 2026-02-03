---
title: Ingress Controller Pods CrashLooping - Ingress
weight: 256
categories:
  - kubernetes
  - ingress
---

# IngressControllerPodsCrashLooping-ingress

## Meaning

Ingress controller pods are repeatedly crashing and restarting (triggering KubePodCrashLooping alerts) because configuration errors prevent startup, invalid ingress resources cause controller failures, resource constraints cause crashes, or the controller cannot access required resources. Ingress controller pods show CrashLoopBackOff state in kubectl, ingress controller logs show startup failures or configuration errors, and pod restart counts increase continuously. This affects the network plane and prevents traffic routing through ingress resources, typically caused by configuration errors, invalid ingress resources, or resource constraints; applications become unavailable to users and may show errors.

## Impact

Ingress controller is unavailable; all ingress resources stop routing traffic; external traffic cannot reach applications; ingress endpoints return errors; applications become unreachable from outside the cluster; KubePodCrashLooping alerts fire; ingress controller logs show startup failures; cluster ingress functionality is completely broken. Ingress controller pods remain in CrashLoopBackOff state indefinitely; ingress controller logs show startup failures; applications become unavailable to users and may experience errors or performance degradation; cluster ingress functionality is completely broken.

## Playbook

1. Describe the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` using `kubectl describe pod <controller-pod-name> -n <namespace>` and inspect pod restart count, container termination reason, and conditions to confirm crash loop and identify restart causes.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<controller-pod-name> --sort-by='.lastTimestamp'` and filter for ingress controller-related events, focusing on events with reasons such as `Failed`, `CrashLoopBackOff`, or messages indicating configuration or startup errors.

3. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for configuration errors, startup failures, or crash messages that explain why the controller cannot start.

4. Retrieve the ingress controller Deployment or DaemonSet in namespace `<namespace>` and review configuration, environment variables, and resource limits to verify if configuration issues are causing crashes.

5. List all Ingress resources in the cluster and check for invalid or misconfigured ingress resources that may be causing the controller to crash.

6. Check the ingress controller pod resource usage metrics to verify if resource constraints or OOM conditions are causing crashes.

## Diagnosis

Begin by analyzing the pod describe output and events collected in the Playbook section. The container termination reason, restart count, and controller logs provide the primary diagnostic signals.

**If events show OOMKilled in the container termination reason:**
- The ingress controller is running out of memory. Check memory limits in the Deployment and compare with controller memory usage patterns. Increase memory limits or reduce the number of Ingress resources if the cluster has many routes.

**If logs show configuration parsing errors or invalid annotation warnings:**
- An Ingress resource has invalid configuration. Review the list of all Ingress resources for syntax errors, unsupported annotations, or invalid backend references. Fix or remove the problematic Ingress resource.

**If logs show TLS secret not found or certificate loading errors:**
- A referenced TLS secret is missing or invalid. Check the Ingress TLS section for secret references. Verify the secrets exist in the same namespace as the Ingress and contain valid `tls.crt` and `tls.key` data.

**If logs show failed to start or listen on port errors:**
- The controller cannot bind to required ports. Check if another process is using ports 80/443 on the node (for hostNetwork mode) or if the service port configuration conflicts.

**If events show ImagePullBackOff or ErrImagePull:**
- The controller image cannot be pulled. Verify image name and tag are correct. Check registry authentication if using a private registry.

**If events are inconclusive, correlate timestamps:**
1. Check if crashes began after a Deployment update by comparing crash timestamps with Deployment revision changes.
2. Check if crashes align with new Ingress resource creation by examining Ingress creation timestamps across all namespaces.
3. Check if a specific ConfigMap or Secret was deleted by reviewing deletion events in the controller namespace.

**If no clear cause is identified:** Enable debug logging on the ingress controller by modifying its configuration, then reproduce the crash to capture detailed error information. Check if the controller version is compatible with the Kubernetes version.

