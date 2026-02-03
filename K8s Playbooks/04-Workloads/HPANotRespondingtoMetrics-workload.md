---
title: HPA Not Responding to Metrics - Workload
weight: 250
categories:
  - kubernetes
  - workload
---

# HPANotRespondingtoMetrics-workload

## Meaning

The Horizontal Pod Autoscaler (HPA) is not responding to resource metrics (triggering KubeHPAReplicasMismatch or KubeDeploymentReplicasMismatch alerts) because the metrics-server pods are unavailable in kube-system namespace, resource metrics cannot be retrieved from the metrics.k8s.io/v1beta1 API, resource requests for CPU or memory are not defined in deployment pod templates, or the metrics API is not accessible due to network or authentication issues. HPAs show metrics unavailable conditions, metrics-server pods show failures in kube-system namespace, and HPA status shows FailedGetObjectMetric or FailedComputeMetricsReplicas errors. This affects the workload plane and prevents automatic scaling, typically caused by metrics-server failures or missing resource requests; applications cannot adapt to load changes and may show errors.

## Impact

HPA cannot scale pods based on CPU or memory metrics; deployments maintain fixed replica count regardless of resource utilization; automatic scaling is disabled; applications cannot adapt to load changes; pods remain at current replica count even when CPU or memory usage exceeds thresholds; HPA status shows metrics unavailable conditions; KubeHPAReplicasMismatch alerts fire when HPA desired replicas do not match deployment replicas; KubeDeploymentReplicasMismatch alerts fire when deployment cannot scale; manual intervention required for scaling; resource-based autoscaling fails. HPAs show metrics unavailable conditions indefinitely; metrics-server pods show failures; applications cannot adapt to load changes and may experience errors or performance degradation; automatic scaling is disabled.

## Playbook

1. Describe HPA <hpa-name> in namespace <namespace> to see:
   - Current metrics versus target metrics
   - Desired replicas versus current replicas
   - Conditions showing why metrics are unavailable
   - Events showing FailedGetObjectMetric, FailedComputeMetricsReplicas, or metrics errors

2. Retrieve events for HPA <hpa-name> in namespace <namespace> sorted by timestamp to see the sequence of metrics failures.

3. Check the metrics-server pod status in kube-system namespace by listing pods with label k8s-app=metrics-server and retrieve metrics-server logs to verify it is running and functioning correctly.

4. Describe deployment <deployment-name> in namespace <namespace> to verify resource requests are defined, as HPA requires resource requests to calculate metrics.

5. Test if metrics are being collected by retrieving pod resource usage metrics in namespace <namespace> to verify metrics API accessibility.

6. Check the metrics-server service and endpoints in kube-system namespace to verify network connectivity and API accessibility for metrics retrieval.

## Diagnosis

1. Analyze HPA events from Playbook to identify metrics-related errors. If events show FailedGetObjectMetric, FailedComputeMetricsReplicas, or "unable to get metrics" errors, use event timestamps to determine when metrics became unavailable.

2. If events indicate metrics-server issues, verify metrics-server pod status from Playbook step 3. If metrics-server events show CrashLoopBackOff, restarts, or failures at timestamps when HPA stopped responding, metrics-server is the root cause.

3. If events indicate missing resource requests, examine deployment configuration from Playbook step 4. If the deployment lacks CPU or memory resource requests, HPA cannot calculate utilization percentages and metrics will appear unavailable.

4. If events indicate metrics API accessibility issues, verify metrics API availability from Playbook step 5. If metrics API requests fail or return errors, investigate metrics-server service and endpoint connectivity.

5. If events indicate service or endpoint changes, verify metrics-server service from Playbook step 6. If service events show modifications at timestamps when metrics became unavailable, service configuration changes affected metrics availability.

6. If events indicate network policy changes, verify if policies affect metrics-server communication. If NetworkPolicy events occurred before metrics failures, policy changes may have blocked metrics collection.

7. If events indicate metrics-server resource pressure, verify metrics-server pod resource usage. If resource-related events show throttling or OOMKilled at failure timestamps, metrics-server resource constraints prevented metrics collection.

**If no correlation is found**: Extend the search window (5 minutes to 10 minutes, 30 minutes to 1 hour, 1 hour to 2 hours), review metrics-server logs for gradual performance degradation, check for intermittent network connectivity issues, examine if metrics API authentication or authorization issues developed over time, verify if metrics-server resource constraints accumulated gradually, and check for DNS or service discovery issues affecting metrics-server accessibility. Metrics unavailability may result from gradual infrastructure degradation rather than immediate changes.

