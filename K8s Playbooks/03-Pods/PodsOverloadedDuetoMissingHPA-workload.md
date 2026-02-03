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

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Current replica count versus expected load requirements
   - Resource requests and limits for all containers
   - Conditions showing pod health issues
   - Events showing resource pressure or performance issues

2. Retrieve events for deployment <deployment-name> in namespace <namespace> sorted by timestamp to see the sequence of resource-related events.

3. List HorizontalPodAutoscaler objects in namespace <namespace> and verify if an HPA exists for the deployment.

4. Check if the metrics-server is running in the kube-system namespace by listing pods with label k8s-app=metrics-server and verify metrics-server pod status.

5. Retrieve resource usage metrics for pods in namespace <namespace> with label app=<app-label> to verify if pods are approaching resource limits.

6. Describe pod <pod-name> in namespace <namespace> and check resource usage to verify if pods are overloaded.

## Diagnosis

1. Analyze deployment and pod events from Playbook to identify resource pressure indicators. If events show OOMKilled, CPU throttling, or pod restarts due to resource limits, use event timestamps to determine when overload began.

2. If events indicate high resource usage, verify whether HPA exists from Playbook step 3. If no HPA is configured for the deployment, missing autoscaling is confirmed as the root cause allowing pods to become overloaded.

3. If events indicate HPA exists but is not scaling, verify metrics-server status from Playbook step 4. If metrics-server events show failures or unavailability at overload timestamps, metrics collection issues prevented HPA from functioning.

4. If events indicate replica count changes, correlate changes with overload onset. If replica count was reduced before overload events, manual scaling down caused insufficient capacity.

5. If events indicate deployment updates or rollouts, verify if new application version has different resource requirements. If deployment events occurred before overload, the new version may require more resources than allocated.

6. If events indicate resource request modifications, verify if requests were reduced. If resource request events show decreases before overload, pods became less capable of handling existing load.

7. If events are inconclusive, analyze pod resource metrics from Playbook step 5. If resource usage consistently approaches limits without overload events, gradual load increase has exceeded static capacity.

**If no correlation is found**: Extend the search window (30 minutes to 1 hour, 1 hour to 2 hours), review resource usage trends for gradual load increase, check for intermittent traffic spikes, examine if HPA was never configured and load gradually increased over time, verify if metrics-server experienced gradual performance degradation, and check for external factors like database slowdowns that may have increased application resource usage. Pod overload may result from gradual load growth rather than immediate changes.

