---
title: Pods Overloaded Due to Missing HPA - Workload
weight: 300
categories:
  - kubernetes
  - workload
---

# PodsOverloadedDuetoMissingHPA-workload

## Meaning

Pods are experiencing high load and performance degradation (triggering KubePodCPUHigh, KubePodMemoryHigh, or KubePodNotReady alerts) because no Horizontal Pod Autoscaler (HPA) is configured to scale the deployment based on CPU or memory metrics from metrics-server. Pods show high CPU or memory usage exceeding resource limits, pod metrics indicate resource utilization approaching thresholds, and application performance degrades. This affects the workload plane and indicates that deployments maintain a fixed replica count regardless of load, typically caused by missing HPA configuration; application errors may appear in application monitoring.

## Impact

Pods become overloaded with CPU or memory usage exceeding resource limits; application performance degrades; response times increase; pods may become unresponsive or crash under load; services experience high latency; pods may be terminated due to resource pressure; resource usage approaches or exceeds limits; KubePodCPUHigh alerts fire when pod CPU usage exceeds thresholds; KubePodMemoryHigh alerts fire when pod memory usage exceeds thresholds; KubePodNotReady alerts fire when pods become unresponsive; applications cannot handle traffic spikes; user-facing services are slow or unavailable; deployments cannot automatically scale to handle increased load. Pods show high CPU or memory usage indefinitely; application errors may appear in application monitoring; applications cannot handle traffic spikes and may experience errors or performance degradation; user-facing services are slow or unavailable.

## Playbook

1. List HorizontalPodAutoscaler objects in namespace `<namespace>` and verify if an HPA exists for the deployment `<deployment-name>`.

2. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and verify that resource requests and limits are defined, as HPA requires resource metrics to function.

3. Check if the metrics-server is running and accessible by listing pods in the kube-system namespace and verifying metrics-server pod status.

4. Retrieve the pod `<pod-name>` in namespace `<namespace>` and check resource usage metrics (CPU, memory) to verify if pods are approaching resource limits.

5. List events in namespace `<namespace>` and filter for resource-related events or performance issues associated with the overloaded pods.

6. Retrieve the Deployment `<deployment-name>` and inspect the current replica count to verify if it matches the expected load requirements.

## Diagnosis

1. Compare the pod overload timestamps with traffic increase or load spike timestamps, and check whether high load occurred within 30 minutes before pods became overloaded.

2. Compare the pod overload timestamps with deployment replica count modification timestamps, and check whether replica counts were reduced within 30 minutes before overload issues began.

3. Compare the pod overload timestamps with HPA deletion or removal timestamps, and check whether HPA was removed within 1 hour before pods became overloaded.

4. Compare the pod overload timestamps with metrics-server failure or unavailability timestamps, and check whether metrics collection stopped within 30 minutes before overload issues, preventing HPA from functioning even if configured.

5. Compare the pod overload timestamps with resource request modification timestamps in the deployment, and check whether resource requests were reduced within 30 minutes before overload issues, making pods less capable of handling load.

6. Compare the pod overload timestamps with application deployment or update timestamps, and check whether application changes occurred within 1 hour before overload issues, indicating the new version may have higher resource requirements or performance issues.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review resource usage trends for gradual load increase, check for intermittent traffic spikes that may have caused overload, examine if HPA was never configured and load gradually increased over time, verify if metrics-server experienced gradual performance degradation, and check for external factors like database slowdowns that may have increased application resource usage. Pod overload may result from gradual load growth rather than immediate changes.

