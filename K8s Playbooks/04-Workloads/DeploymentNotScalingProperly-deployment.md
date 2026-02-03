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

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Replicas status (desired/current/ready/available)
   - Conditions showing why scaling is failing
   - Events showing FailedCreate, FailedScheduling, or scaling errors

2. List events in namespace <namespace> filtered by involved object name <deployment-name> and sorted by last timestamp to see the sequence of scaling failures.

3. Describe horizontal pod autoscaler <hpa-name> in namespace <namespace> to check HPA configuration if HPA is used.

4. List all nodes and retrieve resource usage metrics to check for resource constraints.

5. List pods in namespace kube-system with label k8s-app=metrics-server to check metrics server status.

6. List pods in namespace <namespace> with label app=<app-label> to verify pod status and readiness.

7. Describe ResourceQuota objects in namespace <namespace> to verify if quotas block scaling.

## Diagnosis

1. Analyze deployment events from Playbook steps 1-2 to identify the primary scaling failure reason. Events showing "FailedScheduling" indicate scheduling constraints. Events showing "FailedCreate" indicate pod creation failures. Events showing "exceeded quota" indicate resource quota limits. Events showing "ScalingReplicaSet" followed by failures indicate scaling operation issues.

2. If events indicate scheduling failures (FailedScheduling with "Insufficient cpu" or "Insufficient memory"), correlate with node resource metrics from Playbook step 4 to confirm cluster capacity is exhausted. Verify which nodes have available capacity and whether node selectors or affinity rules are limiting scheduling options.

3. If events indicate resource quota issues (messages containing "exceeded quota" or "forbidden"), verify quota status from Playbook step 7 and compare with deployment resource requests to determine if quota increase is needed or resource requests should be reduced.

4. If HPA is configured, analyze HPA status from Playbook step 3 to identify scaling decision issues. Check for "unable to get metrics" or "failed to compute desired" messages indicating metrics server problems. Verify current metrics values versus target thresholds.

5. If HPA shows metrics collection failures, verify metrics server pod status from Playbook step 5. If metrics server pods are not running or unhealthy, HPA cannot make scaling decisions.

6. If events indicate pod readiness failures (pods created but not becoming ready), analyze pod status from Playbook step 6 to identify why pods are not passing readiness probes. This may indicate application-level issues preventing scale-up completion.

7. If events indicate image pull failures for new pods, verify image availability and registry connectivity. Scaling cannot complete if new pod images cannot be pulled.

8. If events are inconclusive but scaling is not occurring, verify deployment replicas configuration matches expected values and check if deployment is paused or has conflicting HPA/manual scaling settings.

**If no clear failure reason is identified from events**: Review HPA event history for scaling decision patterns, check if node autoscaler is enabled and functioning, verify cluster-autoscaler logs for pending scale-up decisions, examine if pod disruption budgets are limiting scale-down operations, and check for rate limiting on API server affecting controller operations.
