---
title: Cannot Delete Namespace - Namespace
weight: 254
categories:
  - kubernetes
  - namespace
---

# CannotDeleteNamespace-namespace

## Meaning

Namespaces cannot be deleted (triggering namespace-related alerts) because finalizers on resources prevent deletion, custom resource controllers are not processing finalizers, or resources with finalizers cannot be cleaned up. Namespaces show Terminating state indefinitely in kubectl, namespace finalizers prevent deletion, and custom resource controllers may show failures. This affects the workload plane and blocks namespace cleanup, typically caused by finalizer processing failures or custom resource controller issues; applications may experience resource allocation issues.

## Impact

Namespaces remain in Terminating state; namespace cleanup is blocked; resources remain allocated; finalizers prevent namespace deletion; KubeNamespaceTerminating alerts may fire; namespace status shows Terminating indefinitely; cluster resource management is impaired; new namespaces with same name cannot be created. Namespaces show Terminating state indefinitely; namespace finalizers prevent deletion; applications may experience resource allocation issues; cluster resource management is impaired.

## Playbook

1. Retrieve the namespace `<namespace-name>` and inspect namespace deletion timestamp and finalizers to confirm Terminating state and identify which finalizers are present (kubernetes finalizer or custom finalizers).

2. List all resources in namespace `<namespace-name>` using `kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -n <namespace-name>` and identify resources that have finalizers preventing deletion.

3. List events in namespace `<namespace-name>` and filter for deletion-related events, focusing on events with reasons such as `FailedDelete` or messages indicating finalizer processing failures.

4. Check API server finalizer processing by reviewing API server logs for finalizer processing timeouts or errors.

5. Check custom resource controllers or operators responsible for finalizers and verify if they are running and processing finalizers correctly by checking controller pod status.

6. Retrieve CustomResourceDefinition objects and check if finalizer processing controllers are available and functioning.

7. Verify if resources with finalizers can be deleted or if finalizer controllers are experiencing issues by checking controller logs.

## Diagnosis

1. Compare the namespace deletion failure timestamps with API server finalizer processing timeout event timestamps, and check whether finalizer processing timeouts occurred within 5 minutes before namespace deletion failures.

2. Compare the namespace deletion failure timestamps with finalizer controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before namespace deletion failures.

3. Compare the namespace deletion failure timestamps with custom resource creation timestamps in the namespace, and check whether resources with finalizers were created within 30 minutes before deletion failures.

4. Compare the namespace deletion failure timestamps with finalizer addition timestamps to resources in the namespace, and check whether finalizers were added within 30 minutes before namespace deletion failures.

5. Compare the namespace deletion failure timestamps with CustomResourceDefinition modification timestamps, and check whether CRD changes occurred within 30 minutes before namespace deletion failures.

6. Compare the namespace deletion failure timestamps with cluster upgrade or operator update timestamps, and check whether infrastructure changes occurred within 1 hour before namespace deletion failures, affecting finalizer processing.

7. Compare the namespace deletion failure timestamps with API server unavailability or performance degradation timestamps, and check whether API server issues occurred within 5 minutes before finalizer processing failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review finalizer controller logs for gradual processing issues, check for intermittent API server connectivity problems, examine if finalizers were always present but only recently enforced, verify if finalizer controllers experienced gradual performance degradation, and check for resource quota or limit constraints that may prevent cleanup operations. Namespace deletion failures may result from cumulative finalizer processing issues rather than immediate changes.

