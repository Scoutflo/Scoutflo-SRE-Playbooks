---
title: Deployment Not Scaling Properly - Deployment
weight: 235
categories:
  - kubernetes
  - deployment
---

# DeploymentNotScalingProperly-deployment

## Meaning

A Deployment is not changing its replica count as expected in response to configuration, HPA signals, or load (potentially triggering KubeDeploymentReplicasMismatch alerts), even though conditions suggest it should scale up or down. This indicates scaling failures due to resource constraints, HPA misconfiguration, metrics server issues, or pod readiness problems preventing replica count adjustments.

## Impact

Deployments cannot scale to desired replica count; applications experience insufficient capacity; services may be overloaded; HPA scaling fails; applications cannot handle traffic spikes; KubeDeploymentReplicasMismatch alerts fire; replica counts mismatch desired state; pods fail to be created; scaling operations hang or fail.

## Playbook

1. Retrieve deployment `<deployment-name>` in namespace `<namespace>` and check current number of replicas versus desired replicas.

2. List all nodes and retrieve resource usage metrics to check for resource constraints.

3. Retrieve horizontal pod autoscaler `<hpa-name>` in namespace `<namespace>` and check HPA configuration if HPA is used.

4. List pods in namespace `kube-system` and filter for metrics server pods to check status.

5. List events in namespace `<namespace>` and filter for deployment-related events to check for scaling issues.

6. List pods in namespace `<namespace>` and filter for deployment pods to verify pod status and readiness.

7. Retrieve ResourceQuota objects in namespace `<namespace>` to verify if quotas block scaling.

## Diagnosis

1. Compare the timestamps when deployment scaling failures occurred (from replica count mismatches) with HPA configuration change timestamps, and check whether scaling failures begin within 30 minutes of HPA changes.

2. Compare the scaling failure timestamps with resource constraint event timestamps from node resource usage and failed pod creation events, and verify whether scaling failures correlate with resource constraints at the same time.

3. Compare the scaling failure timestamps with metrics server pod status issue timestamps, and check whether scaling failures begin within 5 minutes of metrics server problems.

4. Compare the scaling failure timestamps with deployment modification timestamps, and verify whether scaling failures correlate with deployment changes within 30 minutes.

5. Compare the scaling failure timestamps with node capacity constraint timestamps from node resource metrics, and check whether scaling failures correlate with insufficient node capacity.

6. Compare the scaling failure timestamps with pod readiness issue timestamps and resource quota limit timestamps, and verify whether scaling failures correlate with pod readiness problems or quota exhaustion at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 5 minutes → 10 minutes), review HPA metrics for calculation issues, check metrics server availability and accuracy, examine pod readiness probe failures, verify if resource quotas were recently tightened, check for node taint or affinity constraints, and review deployment strategy settings. Scaling failures may result from cumulative resource pressure or HPA calculation issues not immediately visible in single event timestamps.
