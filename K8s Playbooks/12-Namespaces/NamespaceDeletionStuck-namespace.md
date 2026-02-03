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

1. Describe the namespace `<namespace-name>` to inspect namespace deletion timestamp, finalizers, and status to confirm Terminating state and identify which finalizers are preventing deletion.

2. Retrieve events for the namespace `<namespace-name>` sorted by timestamp to identify deletion-related events and finalizer processing failures.

3. List all resources in namespace `<namespace-name>` and identify resources that remain and have finalizers.

4. Check custom resource controllers or operators responsible for finalizers and verify if they are running and can process finalizers.

5. Retrieve CustomResourceDefinition objects and check if finalizer processing is configured correctly.

6. Verify API server connectivity and performance to ensure finalizer processing can complete.

## Diagnosis

1. Analyze namespace events and finalizers from Playbook to identify what is blocking deletion. Check the namespace's metadata.finalizers field to see which finalizers remain. Common finalizers include "kubernetes" (built-in) and custom finalizers from operators.

2. If the kubernetes finalizer remains, resources still exist within the namespace that must be deleted first. List all resources in the namespace from Playbook to identify remaining resources. Focus on resources with their own finalizers that may be blocking cleanup.

3. If custom resource finalizers remain (e.g., from operators like Istio, Prometheus, or custom controllers), verify the controller responsible for that finalizer is running and healthy. If the controller was deleted before its resources, finalizers will never be processed.

4. If resources with finalizers exist but their controllers are missing or deleted, the finalizers must be manually removed. Identify the specific resources and their finalizers from Playbook output.

5. If events indicate API server errors or timeouts during finalizer processing, verify API server health and connectivity. Finalizer processing requires the API server to update resource metadata.

6. If the namespace contains CustomResourceDefinitions that have been deleted, resources of those types become orphaned and cannot be deleted normally. Check for resources whose API group no longer exists.

7. If all resources appear deleted but the namespace is still Terminating, the namespace-level kubernetes finalizer may be stuck. This can occur if the namespace controller cannot complete its cleanup. Verify kube-controller-manager health and check for namespace controller errors in logs.

