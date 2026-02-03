---
title: Pods Stuck in ImagePullBackOff - Registry
weight: 271
categories:
  - kubernetes
  - registry
---

# PodsStuckinImagePullBackOff-registry

## Meaning

Kubelet is repeatedly failing to pull a container image from the registry (triggering ImagePullBackOff or ErrImagePull pod states) because the image reference is invalid, credentials are wrong, image pull secrets are missing or expired, or the registry or network path to it is unavailable. Pods show ImagePullBackOff or ErrImagePull state in kubectl, pod events show Failed or ErrImagePull errors, and container waiting state reason indicates image pull failures. This affects the workload plane and prevents container startup, typically caused by invalid image references, missing or expired image pull secrets, or registry connectivity issues; applications cannot start.

## Impact

Pods cannot start; deployments remain at 0 replicas; rolling updates fail; applications fail to deploy; services become unavailable; new workloads cannot be created; pods stuck in ImagePullBackOff state; image pull errors occur; container registry connectivity issues; KubePodPending alerts may fire due to image pull failures. Pods show ImagePullBackOff or ErrImagePull state indefinitely; pod events show Failed or ErrImagePull errors; applications cannot start and may show errors; deployments remain at 0 replicas.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect container waiting state reason and message fields to confirm ImagePullBackOff or ErrImagePull and capture the exact error - look in Events section for "Failed to pull image" with the specific reason (auth error, not found, timeout).

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to see the sequence of image pull errors, focusing on events with reasons such as Failed and messages containing "pull" or ErrImagePull.

3. Retrieve the Deployment <deployment-name> in namespace <namespace> and verify that each container's image field (registry, repository, tag, or digest) is correct and exists in the target registry.

4. Check the pod spec for imagePullSecrets for pod <pod-name> in namespace <namespace>, then retrieve and validate those Secret objects to confirm they exist and contain valid credentials for the registry.

5. Verify network connectivity and basic reachability to the container registry endpoint <registry-url> from a test pod in the cluster.

6. On the node where the pod is scheduled, verify disk space availability in the image storage directories to ensure there is enough space to pull the image.

## Diagnosis

1. Analyze pod events from Playbook to identify the specific image pull error type. Events showing "Failed to pull image" with "unauthorized" indicate authentication issues. Events showing "manifest unknown" or "not found" indicate the image or tag does not exist. Events showing "timeout" or "i/o timeout" indicate network connectivity problems.

2. If events indicate authentication failure, verify imagePullSecrets from Playbook validation results. Confirm the Secret exists, is correctly referenced in the pod spec, and contains valid base64-encoded credentials. Check if the credentials have expired or been rotated.

3. If events indicate image not found, use the image name from Playbook deployment inspection to verify correctness. Check if the registry hostname is correct, the repository path exists, and the tag or digest is valid. Verify the image was not recently deleted or if the tag was moved.

4. If events indicate network issues, use the Playbook connectivity test results to determine if the registry is reachable from cluster nodes. Check for DNS resolution failures, firewall rules blocking registry ports (typically 443), or NetworkPolicies restricting egress.

5. If events indicate rate limiting or quota exhaustion, check if the registry enforces pull limits. For public registries like Docker Hub, configure imagePullSecrets with authenticated credentials to increase rate limits.

6. If events indicate node-level issues, verify disk space availability from Playbook node checks. Check if the node has sufficient space in /var/lib/docker or /var/lib/containerd for image layers.

**If no clear cause is identified from events**: Check if multiple pods on the same node are failing (indicating node-specific issue), verify registry TLS certificates are trusted by the container runtime, examine if a proxy or service mesh is intercepting registry traffic, and review if the image requires specific platform architecture (amd64 vs arm64).

