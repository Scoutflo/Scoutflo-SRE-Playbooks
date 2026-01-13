---
title: Namespace Deletion Stuck - Namespace
weight: 228
categories:
  - kubernetes
  - namespace
---

# NamespaceDeletionStuck-namespace

## Meaning

Namespaces are stuck in Terminating state (triggering namespace-related alerts) because resources with finalizers cannot be deleted, custom resource controllers are not processing finalizers, or the API server cannot complete resource cleanup. Namespaces show Terminating state indefinitely in kubectl, namespace finalizers prevent deletion, and custom resource controllers may show failures. This affects the workload plane and blocks namespace cleanup, typically caused by finalizer processing failures or custom resource controller issues; applications may experience resource allocation issues.

## Impact

Namespaces remain in Terminating state indefinitely; namespace cleanup is blocked; resources remain allocated; finalizers prevent resource deletion; KubeNamespaceTerminating alerts may fire; namespace status shows Terminating; cluster resource management is impaired; new namespaces with same name cannot be created. Namespaces show Terminating state indefinitely; namespace finalizers prevent deletion; applications may experience resource allocation issues; cluster resource management is impaired.

## Playbook

1. Retrieve the namespace `<namespace-name>` and inspect namespace deletion timestamp and finalizers to confirm Terminating state and identify which finalizers are preventing deletion.

2. List all resources in namespace `<namespace-name>` and identify resources that remain and have finalizers.

3. List events in namespace `<namespace-name>` and filter for deletion-related events, focusing on events with reasons such as `FailedDelete` or messages indicating why resources cannot be deleted.

4. Check custom resource controllers or operators responsible for finalizers and verify if they are running and can process finalizers.

5. Retrieve CustomResourceDefinition objects and check if finalizer processing is configured correctly.

6. Verify API server connectivity and performance to ensure finalizer processing can complete.

## Diagnosis

1. Compare the namespace deletion stuck timestamps with resource finalizer addition timestamps, and check whether finalizers were added within 30 minutes before namespace became stuck.

2. Compare the namespace deletion stuck timestamps with finalizer controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before namespace became stuck.

3. Compare the namespace deletion stuck timestamps with custom resource creation timestamps in the namespace, and check whether resources with finalizers were created within 30 minutes before deletion issues.

4. Compare the namespace deletion stuck timestamps with API server unavailability or performance degradation timestamps, and check whether API server issues occurred within 5 minutes before finalizer processing failures.

5. Compare the namespace deletion stuck timestamps with cluster upgrade or operator update timestamps, and check whether infrastructure changes occurred within 1 hour before namespace became stuck, affecting finalizer processing.

6. Compare the namespace deletion stuck timestamps with resource quota or limit constraint timestamps, and check whether constraints prevented resource deletion within 30 minutes before namespace became stuck.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review finalizer controller logs for gradual processing issues, check for intermittent API server connectivity problems, examine if finalizers were always present but only recently enforced, verify if finalizer controllers experienced gradual performance degradation, and check for cumulative resource cleanup issues. Namespace deletion stuck issues may result from cumulative finalizer processing problems rather than immediate changes.

