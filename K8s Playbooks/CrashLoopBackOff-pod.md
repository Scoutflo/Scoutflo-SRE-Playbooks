---
title: CrashLoopBackOff - Pod
weight: 201
categories:
  - kubernetes
  - pod
---

# CrashLoopBackOff-pod

## Meaning

A pod container repeatedly starts and exits with errors shortly after launch, causing Kubernetes to back off and restart it in a CrashLoopBackOff state (triggering KubePodCrashLooping alerts) instead of reaching a stable Running state. This indicates application configuration errors, resource constraints, dependency failures, or container image issues preventing successful pod startup.

## Impact

Application pods fail to start; services become unavailable; deployments cannot achieve desired replica count; applications experience downtime; dependent services may fail; KubePodCrashLooping alerts fire; pods remain in CrashLoopBackOff state; containers exit repeatedly; application errors prevent pod stability; replica counts mismatch desired state.

## Playbook

1. Retrieve logs from pod `<pod-name>` in namespace `<namespace>` and analyze error messages and stack traces.

2. Retrieve deployment `<deployment-name>` in namespace `<namespace>` and check container image name and tag.

3. Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status and restart count.

4. Retrieve pod `<pod-name>` in namespace `<namespace>` and check resource limits and requests.

## Diagnosis

1. Compare the timestamps when pod crashes occurred (from pod restart timestamps) with deployment modification timestamps, and check whether crashes begin within 1 hour of deployment changes.

2. Compare the pod crash timestamps with resource usage spike timestamps from pod metrics, and verify whether crashes correlate with resource limits being exceeded at the same time.

3. Compare the pod crash timestamps with container image change timestamps from deployment image modifications, and check whether crashes begin after image changes.

4. Compare the pod crash timestamps with error pattern timestamps from pod logs, and verify whether crash frequency patterns align with specific error patterns in the logs.

5. Compare the pod crash timestamps with deployment configuration change timestamps including environment variables or command changes, and check whether crashes begin within 1 hour of configuration changes.

6. Compare the pod crash timestamps with cluster upgrade or maintenance window timestamps, and verify whether crashes correlate with infrastructure changes within 1 hour.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours), review pod logs for earlier error patterns, check for gradual resource exhaustion, examine container image health, verify if application dependencies are available, check for configuration drift, and review deployment history for delayed effects. CrashLoopBackOff may result from application-level issues or dependency failures not immediately visible in Kubernetes resource changes.
