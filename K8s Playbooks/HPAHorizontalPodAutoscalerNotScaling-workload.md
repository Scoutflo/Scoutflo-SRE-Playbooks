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

1. Retrieve the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and inspect its status, current metrics, desired replicas, and conditions to identify scaling issues.

2. List events in namespace `<namespace>` and filter for HPA-related events, focusing on events with reasons such as `FailedGetObjectMetric` or `FailedComputeMetricsReplicas` that indicate metrics retrieval failures.

3. Verify that the Deployment `<deployment-name>` referenced by the HPA has resource requests defined for CPU and memory, as HPA requires resource metrics to function.

4. List pods in the kube-system namespace and check the metrics-server pod status to verify it is running and healthy, as HPA depends on metrics-server for resource metrics.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review resource requests and limits to ensure they are properly configured for HPA scaling.

6. Check HPA status conditions and metrics to verify if metrics are being collected and if scaling decisions are being made.

## Diagnosis

1. Compare the HPA scaling failure timestamps with metrics-server pod restart or failure timestamps, and check whether metrics-server issues occurred within 5 minutes before HPA stopped scaling.

2. Compare the HPA scaling failure timestamps with deployment resource request modification timestamps, and check whether resource requests were removed or modified within 30 minutes before HPA scaling failures.

3. Compare the HPA scaling failure timestamps with HPA configuration modification timestamps, and check whether HPA min/max replicas or target metrics were changed within 30 minutes before scaling issues.

4. Compare the HPA scaling failure timestamps with metrics-server unavailability or error timestamps, and check whether metrics collection stopped within 5 minutes before HPA scaling failures.

5. Compare the HPA scaling failure timestamps with cluster resource pressure timestamps (node capacity, resource quotas), and check whether resource constraints prevented scaling within 30 minutes before failures.

6. Compare the HPA scaling failure timestamps with deployment rollout or update timestamps, and check whether deployment changes occurred within 1 hour before HPA scaling issues, indicating the new deployment may have different resource requirements affecting HPA calculations.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review metrics-server logs for gradual performance degradation, check for intermittent metrics collection failures, examine if HPA was always misconfigured but only recently enforced, verify if resource quota constraints developed over time, and check for cumulative resource pressure that may have prevented scaling. HPA scaling failures may result from gradual metrics or infrastructure issues rather than immediate configuration changes.

