---
title: Kube Pod Image Pull BackOff
weight: 26
categories: [kubernetes, pod]
---

# KubePodImagePullBackOff

## Meaning

Pod is stuck in ImagePullBackOff state (triggering KubePodImagePullBackOff alerts) because Kubernetes cannot pull the container image from the registry due to authentication failures, network issues, non-existent images, or registry unavailability. Pod status shows ImagePullBackOff with exponential backoff delays, container creation is blocked, and the pod cannot start. This affects the workload plane and indicates image or registry access issues; new deployments fail; scaling operations cannot add replicas; rollout is blocked; service capacity cannot increase.

## Impact

KubePodImagePullBackOff alerts fire; pod cannot start; deployment or scaling operations fail; new replicas cannot be created; rollout is blocked; service capacity is reduced; deployments show unavailable replicas; HPA cannot scale up; scheduled jobs cannot start; init containers cannot pull; application updates cannot proceed; service availability is impacted if existing pods fail.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and confirm status is ImagePullBackOff, noting the specific container image that failed.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for 'Failed to pull image', 'ImagePullBackOff', 'ErrImagePull' to identify specific error messages.

3. Verify the image name and tag are correct and the image exists in the registry by checking the registry directly or using docker pull locally.

4. Check if imagePullSecrets are configured correctly in the pod spec and verify the referenced Secret exists in the namespace.

5. Retrieve the imagePullSecret and verify it contains valid credentials for the target registry, checking username and registry server values.

6. Test registry connectivity from the node by checking if nodes can reach the registry endpoint (network policies, firewall rules, proxy settings).

7. Verify the ServiceAccount used by the pod has the imagePullSecrets attached if using ServiceAccount-based image pull credentials.

## Diagnosis

Compare image name in pod spec with available images in registry and verify whether the image tag exists (common issue: using 'latest' that doesn't exist or wrong tag), using registry API or UI as supporting evidence.

Correlate image pull failures with registry availability and verify whether the registry is experiencing an outage or rate limiting, using registry status page and error messages as supporting evidence.

Analyze image pull secret and verify credentials are valid and not expired, especially for tokens with TTL (ECR, GCR temporary tokens), using secret creation time and registry authentication logs as supporting evidence.

Check if image is in a private registry and verify imagePullSecrets are correctly configured for that registry hostname, using pod spec and secret data as supporting evidence.

Verify if nodes have network connectivity to the registry, checking for network policies, firewall rules, or proxy requirements that may block image pulls, using node network configuration and egress rules as supporting evidence.

If no correlation is found within the specified time windows: try pulling image manually on the node, check container runtime logs (containerd/docker) for detailed errors, verify registry TLS certificates are valid, check if image exceeds size limits, verify node disk space for image layer storage.
