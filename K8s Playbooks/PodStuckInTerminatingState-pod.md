---
title: Pod Stuck In Terminating State - Pod
weight: 206
categories:
  - kubernetes
  - pod
---

# PodStuckInTerminatingState-pod

## Meaning

A pod is stuck in the Terminating phase (potentially triggering KubePodNotReady alerts) because shutdown cannot complete cleanly, often due to hanging processes, blocking finalizers, or attached volumes and endpoints that cannot be detached. Pods show Terminating state indefinitely in kubectl, pod finalizers prevent deletion, and pod events may show deletion-related errors. This indicates pod deletion failures, finalizer issues, or resource dependency problems preventing graceful pod termination; PersistentVolumeClaim detachments may fail.

## Impact

Pods cannot be deleted; deployments cannot update; rolling updates hang; resources remain in terminating state; cluster state becomes inconsistent; new pods may not start if resources are blocked; KubePodNotReady alerts may fire; pods remain in Terminating state; finalizers prevent deletion; volume detachments fail. Pods show Terminating state indefinitely; pod finalizers prevent deletion; PersistentVolumeClaim detachments may fail; applications may experience resource allocation issues.

## Playbook

1. Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod details and reason for termination delay.

2. List events in namespace `<namespace>` and filter for deletion-related events.

3. Retrieve pod `<pod-name>` in namespace `<namespace>` and check finalizers preventing deletion.

4. Check dependent resources like persistent volume claims, services, or other pods.

5. Retrieve deployment `<deployment-name>` in namespace `<namespace>` and verify terminationGracePeriodSeconds setting.

6. Retrieve pod `<pod-name>` in namespace `<namespace>` and check for volume mount issues.

## Diagnosis

1. Compare the timestamps when pod deletion delays occurred (from pod deletion timestamps) with finalizer change timestamps, and check whether deletion delays begin within 30 minutes of finalizer modifications.

2. Compare the pod deletion delay timestamps with dependent resource change timestamps from PVC, service, or pod modifications, and verify whether deletion delays correlate with dependent resource changes at the same time.

3. Compare the pod deletion delay timestamps with terminationGracePeriodSeconds change timestamps from deployment modifications, and check whether deletion delays begin within 1 hour of termination period changes.

4. Compare the pod deletion delay timestamps with deployment modification timestamps, and verify whether deletion delays correlate with deployment changes within 1 hour.

5. Compare the pod deletion delay timestamps with volume mount issue timestamps, and check whether deletion delays correlate with volume detachment problems at the same time.

6. Compare the pod deletion delay timestamps with node status or network connectivity issue timestamps, and verify whether deletion delays correlate with node problems.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod logs for hanging processes, check for finalizer controller failures, examine volume attachment status, verify if service endpoints are blocking deletion, check for network policy constraints, and review pod preStop hook execution. Terminating pods may result from application-level shutdown issues or finalizer controller problems not immediately visible in Kubernetes resource changes.
