---
title: HPA Horizontal Pod Autoscaler Not Scaling - Workload
weight: 215
categories:
  - kubernetes
  - workload
---

# HPAHorizontalPodAutoscalerNotScaling-workload

## Meaning

The Horizontal Pod Autoscaler (HPA) is not scaling pods as expected (triggering KubeHPAReplicasMismatch or KubeDeploymentReplicasMismatch alerts) because CPU or memory metrics are unavailable from metrics-server, resource requests are not defined in deployment pod templates, the metrics-server pods are not functioning in kube-system namespace, HPA min or max replica configuration is incorrect, or HPA target utilization thresholds are misconfigured. HPAs show metrics unavailable conditions, metrics-server pods may show failures in kube-system namespace, and HPA status shows scaling issues. This affects the workload plane and prevents automatic scaling, typically caused by metrics-server failures or missing resource requests; applications cannot handle traffic spikes and may show errors.

## Impact

Pods are not scaled up during high load when CPU or memory exceeds target utilization; pods are not scaled down during low load when resources are underutilized; applications cannot handle traffic spikes; resources are wasted during low utilization; deployments maintain fixed replica count; HPA status shows scaling issues and conditions indicating metrics unavailable or scaling disabled; KubeHPAReplicasMismatch alerts fire when HPA desired replicas do not match deployment replicas; KubeDeploymentReplicasMismatch alerts fire when deployment cannot achieve desired replica count; applications experience performance degradation under load; manual scaling is required. HPAs show metrics unavailable conditions indefinitely; metrics-server pods may show failures; applications cannot handle traffic spikes and may experience errors or performance degradation; deployments maintain fixed replica count.

## Playbook

1. Describe HPA <hpa-name> in namespace <namespace> to see:
   - Current metrics versus target metrics
   - Desired replicas versus current replicas
   - Min/max replicas configuration
   - Conditions showing why scaling is not working
   - Events showing FailedGetObjectMetric, FailedComputeMetricsReplicas, or other errors

2. Retrieve events for HPA <hpa-name> in namespace <namespace> sorted by timestamp to see the sequence of scaling failures.

3. Describe deployment <deployment-name> in namespace <namespace> to verify that resource requests are defined, as HPA requires resource metrics to function.

4. Check the metrics-server pod status in kube-system namespace by listing pods with label k8s-app=metrics-server and retrieve metrics-server logs to verify it is running and healthy.

5. Retrieve deployment <deployment-name> configuration in namespace <namespace> and review resource requests and limits to ensure they are properly configured for HPA scaling.

6. Retrieve HPA <hpa-name> status and configuration in namespace <namespace> to verify if metrics are being collected and if scaling decisions are being made.

## Diagnosis

1. Analyze HPA events from Playbook to identify scaling failure reasons. If events show FailedGetObjectMetric, FailedComputeMetricsReplicas, "ScalingDisabled", or metrics unavailable conditions, use event timestamps and error messages to identify the specific issue.

2. If events indicate metrics unavailability, verify metrics-server status from Playbook step 4. If metrics-server events show failures, restarts, or unavailability at timestamps when scaling stopped, metrics-server is the root cause.

3. If events indicate missing resource requests, examine deployment configuration from Playbook step 3. If the deployment lacks CPU or memory resource requests, add resource requests to enable HPA metrics calculation.

4. If events indicate HPA configuration issues, verify HPA settings from Playbook step 6. If min/max replicas are equal, or target metrics are misconfigured, adjust HPA configuration to enable scaling.

5. If events indicate resource constraints preventing scale-up, verify cluster capacity and quotas. If scaling events show scheduling failures or quota exhaustion, capacity constraints are blocking scaling rather than HPA misconfiguration.

6. If events indicate recent deployment changes, correlate deployment rollout timestamps with scaling failures. If deployment events occurred before scaling stopped working, new deployment configuration may have affected HPA behavior.

7. If events indicate scale-down being blocked, verify pod disruption budgets and deployment strategy. If PDB or minimum availability constraints prevent pod termination, scale-down cannot proceed.

**If no correlation is found**: Extend the search window (5 minutes to 10 minutes, 30 minutes to 1 hour, 1 hour to 2 hours), review metrics-server logs for gradual performance degradation, check for intermittent metrics collection failures, examine if HPA was always misconfigured but only recently enforced, verify if resource quota constraints developed over time, and check for cumulative resource pressure that may have prevented scaling. HPA scaling failures may result from gradual metrics or infrastructure issues rather than immediate configuration changes.

