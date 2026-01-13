---
title: ImagePullBackOff - Registry
weight: 202
categories:
  - kubernetes
  - registry
---

# ImagePullBackOff-registry

## Meaning

Kubelet is repeatedly failing to pull a container image from the registry (triggering ImagePullBackOff or ErrImagePull pod states) because the image reference is invalid, credentials are wrong, image pull secrets are missing or expired, or the registry or network path to it is unavailable. Pods remain in ImagePullBackOff state preventing container startup.

## Impact

Pods cannot start; deployments remain at 0 replicas; rolling updates fail; applications fail to deploy; services become unavailable; new workloads cannot be created; pods stuck in ImagePullBackOff state; image pull errors occur; container registry connectivity issues; KubePodPending alerts may fire due to image pull failures.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect `status.containerStatuses[].state.waiting.reason` and `message` fields to confirm `ImagePullBackOff` or `ErrImagePull` and capture the exact error.

2. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and verify that each container’s `image` field (registry, repository, tag, or digest) is correct and exists in the target registry.

3. List events in namespace `<namespace>` and filter for image pull errors associated with the pod, focusing on events with reasons such as `Failed` and messages containing "pull" or `ErrImagePull`.

4. From a test pod, execute `curl <registry-url>` or an equivalent HTTP request to verify network connectivity and basic reachability to the container registry endpoint.

5. Check the pod spec for `imagePullSecrets`, then retrieve and validate those Secret objects in namespace `<namespace>` to confirm they exist and contain valid credentials for the registry.

6. On the node where the pod is scheduled, verify disk space availability (for example, using `df -h`) in the image storage directories to ensure there is enough space to pull the image.

## Diagnosis

1. Compare the image pull failure event timestamps (events where `reason="Failed"` and messages contain "pull" or `ErrImagePull`) with image pull secret modification timestamps, and check whether failures began within 10 minutes of a secret update.

2. Compare the image pull failure event timestamps with the results and timestamps of registry connectivity tests (for example, `curl <registry-url>` from a test pod), and check whether network failures or timeouts coincide with the start of image pull errors.

3. Compare the image pull failure event timestamps with Deployment image change times, and check whether failures began within 1 hour after the image reference was changed.

4. Compare the image pull failure event timestamps with Deployment modification timestamps, and check whether a new deployment or rollout occurred within 1 hour before failures started.

5. Compare the image pull failure event timestamps with container registry maintenance windows and node disk space checks, and check whether registry outages or low disk conditions on the pulling node occurred at the same time as failures.

6. Compare the image pull failure event timestamps with NetworkPolicy modification timestamps in namespaces that control egress to the registry, and check whether new or updated policies were applied within 10 minutes before pull errors began.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 1 hour → 2 hours), review registry connectivity from multiple nodes to identify network path issues, check for gradual registry performance degradation, examine image pull secret expiration that may have occurred earlier, verify if registry maintenance or rate limiting was introduced, and check node disk space trends for gradual exhaustion. Image pull failures may result from network or registry issues that developed over time.

