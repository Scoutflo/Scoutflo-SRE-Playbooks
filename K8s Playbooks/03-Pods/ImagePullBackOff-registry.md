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

### For AI Agents (NLP)

1. Describe pod `<pod-name>` in namespace `<namespace>` to see the exact error message for image pull failure - look in Events section for "Failed to pull image" with the specific reason (auth error, not found, timeout).

2. Retrieve events for pod `<pod-name>` in namespace `<namespace>` filtered by reason Failed and sorted by timestamp to see the sequence of image pull failures.

3. Verify the image exists and is accessible: retrieve the image name for pod `<pod-name>` in namespace `<namespace>` and test image pull manually on the node.

4. Check imagePullSecrets configuration: retrieve the imagePullSecrets for pod `<pod-name>` in namespace `<namespace>`, verify the secret exists, and decode and verify the credentials.

5. Describe Deployment `<deployment-name>` in namespace `<namespace>` to verify the image reference is correct (registry, repository, tag) and check if imagePullSecrets are properly configured in the pod template.

6. Test registry connectivity from a pod in the same namespace by executing a request to the registry URL.

7. Check node disk space where pod is scheduled by SSH to the node - insufficient disk prevents image pulls.

### For DevOps/SREs (CLI)

1. Check pod events for image pull errors:
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Events:"
   ```

2. Get events filtered by image pull failures:
   ```bash
   kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>,reason=Failed --sort-by='.lastTimestamp'
   ```

3. Verify image reference and test pull:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'
   # On node: docker pull <image-name> OR crictl pull <image-name>
   ```

4. Check imagePullSecrets and decode credentials:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.imagePullSecrets[*].name}'
   kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d
   ```

5. Check deployment image configuration:
   ```bash
   kubectl describe deployment <deployment-name> -n <namespace>
   kubectl get deployment <deployment-name> -n <namespace> -o jsonpath='{.spec.template.spec.containers[*].image}'
   ```

6. Test registry connectivity from a debug pod:
   ```bash
   kubectl run test-registry --rm -it --image=curlimages/curl -- curl -I https://<registry-url>/v2/
   ```

7. Check node disk space:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.nodeName}'
   kubectl debug node/<node-name> -it --image=busybox -- df -h
   ```

## Diagnosis

1. Analyze pod events from Playbook to identify the specific image pull error. Events showing "unauthorized" or "authentication required" indicate credential issues. Events showing "not found" or "manifest unknown" indicate the image or tag does not exist. Events showing "timeout" or "connection refused" indicate network or registry availability issues.

2. If events indicate authentication failure, verify imagePullSecrets configuration from Playbook output. Check if the Secret exists, contains valid credentials, and is of type kubernetes.io/dockerconfigjson. Decode and verify the registry URL in the Secret matches the image registry.

3. If events indicate image not found, verify the image name and tag exist in the registry. Check if the image was recently deleted, the tag was overwritten, or if the repository name is incorrect. Verify the full image path including registry hostname.

4. If events indicate network or connectivity issues, use the Playbook registry connectivity test results. Check if the node can reach the registry, if DNS resolution works, and if any NetworkPolicies are blocking egress to the registry.

5. If events indicate rate limiting (e.g., "too many requests"), check if the registry has pull quotas. For Docker Hub, anonymous pulls are limited - verify imagePullSecrets are configured for authenticated pulls.

6. If events indicate disk space issues or "no space left on device", verify node disk space from Playbook checks. The kubelet requires sufficient disk space in the image storage directory to pull and extract images.

**If no clear cause is identified from events**: Check if the image uses a digest that no longer exists, verify if a private registry requires VPN or specific network access, examine if the registry certificate is expired or untrusted by the node, and review if a recent cluster or node upgrade changed container runtime behavior.

