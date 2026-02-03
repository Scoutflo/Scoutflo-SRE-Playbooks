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

1. Describe the namespace `<namespace-name>` to inspect namespace deletion timestamp, finalizers, and status to confirm Terminating state and identify which finalizers are present (kubernetes finalizer or custom finalizers).

2. Retrieve events for the namespace `<namespace-name>` sorted by timestamp to identify deletion-related events and finalizer processing failures.

3. List all resources in namespace `<namespace-name>` to identify resources that have finalizers preventing deletion.

4. Check API server finalizer processing by reviewing API server logs for finalizer processing timeouts or errors.

5. Check custom resource controllers or operators responsible for finalizers and verify if they are running and processing finalizers correctly by checking controller pod status.

6. Retrieve CustomResourceDefinition objects and check if finalizer processing controllers are available and functioning.

7. Verify if resources with finalizers can be deleted or if finalizer controllers are experiencing issues by checking controller logs.

## Diagnosis

1. Analyze namespace status and finalizers from Playbook to identify deletion blockers. Check metadata.finalizers to see which finalizers remain on the namespace. The namespace cannot be deleted until all finalizers are removed.

2. If the namespace has remaining resources with finalizers, identify those resources from Playbook. Resources must be deleted before the namespace can be deleted. Each resource with finalizers requires its controller to process the finalizer before deletion completes.

3. If events indicate finalizer controller failures or timeouts, identify which controller is responsible for the stuck finalizers. Common controllers include Istio, Prometheus Operator, cert-manager, or custom operators. Verify the controller is running and healthy.

4. If the responsible controller has been deleted or is not running, the finalizers will never be processed automatically. The finalizers must be manually removed from the affected resources. Identify the specific resources and finalizer names from Playbook.

5. If events indicate API server errors during finalizer processing, verify API server health and connectivity. Finalizer processing requires successful API server communication. Check API server logs for errors related to the namespace.

6. If resources reference deleted CustomResourceDefinitions, those resources become orphaned and cannot be processed normally. Check if any CRDs used by resources in the namespace have been deleted, leaving resources without a functioning API.

7. If all visible resources are deleted but namespace remains Terminating, the namespace-level "kubernetes" finalizer may be stuck. Verify kube-controller-manager is healthy and can process namespace deletions. Check controller-manager logs for namespace controller errors.

