---
title: Pods Stuck in Init State - Pod
weight: 229
categories:
  - kubernetes
  - pod
---

# PodsStuckinInitState-pod

## Meaning

Pods remain stuck in Init state (triggering KubePodPending alerts) because init containers are failing to complete, hanging, or experiencing errors. Pods show Init container status indicating failures or hanging, init container logs show errors or timeout messages, and pod events show init container failure events. This affects the workload plane and prevents pods from transitioning from Init to Running state, typically caused by init container command failures, missing dependencies, or timeout issues; applications cannot start.

## Impact

Pods cannot start; main application containers never begin; deployments remain at 0 ready replicas; services have no endpoints; applications are unavailable; pods remain in Init state indefinitely; KubePodPending alerts fire; pod status shows init container failures; application startup is blocked. Pods show Init container status indicating failures indefinitely; init container logs show errors or timeout messages; applications cannot start and may show errors; deployments remain at 0 ready replicas.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to see which init container is failing - look at Init Containers section for state (Waiting/Running/Terminated) and the reason/message.

2. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to see init container errors with timestamps.

3. Retrieve the init container statuses for pod <pod-name> in namespace <namespace> to see exactly which init container is stuck and why.

4. Retrieve logs from the failing init container <init-container-name> in pod <pod-name> in namespace <namespace> to see what the init container is doing or where it is stuck.

5. Describe Deployment <deployment-name> in namespace <namespace> to check init container configuration - command, args, image, and any dependencies.

6. If init container is waiting for a service, list services in namespace <namespace> and check endpoints for service <service-name> to verify the service exists.

7. If init container is waiting for a database or external resource, test connectivity to <host> on <port> from a debug pod.

8. Check if init container has enough resources by comparing requested resources with node availability using node resource metrics.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify which init container is failing and why. The pod status shows init container states in order, and events provide specific failure reasons.

2. If init container status shows "Waiting" (from Playbook step 1), check the reason:
   - "ImagePullBackOff": Init container image cannot be pulled
   - "CreateContainerConfigError": Missing ConfigMap or Secret
   - "PodInitializing": Init container is still running (may be stuck)

3. If init container status shows "Running" for extended time (from Playbook step 3), check init container logs (Playbook step 4) to understand what it is waiting for:
   - Waiting for a service to become available
   - Waiting for database connectivity
   - Waiting for external resource
   - Infinite loop or hang in init script

4. If init container logs show connection errors or timeouts (from Playbook step 4), verify the dependency is available:
   - Check if target service exists (Playbook step 6)
   - Test connectivity to external resources (Playbook step 7)
   - Verify network policies allow init container traffic

5. If init container status shows "Terminated" with non-zero exit code (from Playbook step 3):
   - Exit code 1: Command failed - check logs for error
   - Exit code 126: Command not found or not executable
   - Exit code 127: Shell or binary missing in image
   - Exit code 137: OOMKilled or SIGKILL

6. If init container needs resources not available (from Playbook steps 5, 8), it may fail or hang:
   - Database not ready or credentials incorrect
   - Required files not present in mounted volumes
   - Schema migration failing

**To resolve init container issues**: Fix the specific error shown in logs, ensure dependencies are available before pod starts, add timeout and retry logic to init scripts, and consider using startup probes instead of init containers for dependency checks.

