---
title: Kube Pod Not Ready
weight: 20
---

# KubePodNotReady

## Meaning

Pod has been in a non-ready state for more than 15 minutes (triggering alerts like KubePodNotReady or KubePodPending) because readiness probes are failing, pods are stuck in Pending phase, or containers are not passing health checks. Pods show NotReady condition in kubectl, readiness probe failures appear in pod events, and application logs may show startup errors or health check failures. This affects the workload plane and indicates application health issues, configuration problems, or resource constraints preventing pods from becoming ready, typically caused by misconfigured health probes, application startup failures, resource constraints, or missing dependencies; application errors may appear in application monitoring; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may block container initialization.

## Impact

KubePodNotReady alerts fire; service degradation or unavailability; pod not attached to service endpoints; traffic is not routed to pod; pods remain in non-ready state; readiness probes fail; applications cannot serve traffic; deployments may fail to complete; replica counts mismatch desired state. Pods show NotReady condition indefinitely in kubectl; service endpoints are removed from service; applications cannot serve traffic; rolling updates cannot complete; scheduled tasks fail. Application errors increase; application exceptions occur when health checks fail; application performance degrades; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may cause initialization failures.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect its phase, ready condition, and container status to verify NotReady state.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'Error', 'Unhealthy', 'Readiness probe failed' to identify health check issues.

3. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` for container `<container-name>` and filter for error patterns related to application startup or health checks to identify application issues.

4. Retrieve the Deployment or StatefulSet `<workload-name>` in namespace `<namespace>` and check pod template parameters including readiness and liveness probe configurations, resource requests and limits, and security context settings to verify configuration issues.

5. Retrieve the Node `<node-name>` where pod `<pod-name>` is scheduled and verify node resource availability and conditions to identify resource constraints.

6. Retrieve ConfigMap, Secret, and PersistentVolumeClaim resources referenced by pod `<pod-name>` in namespace `<namespace>` and check for missing dependencies that block container initialization.

## Diagnosis

Compare pod NotReady detection timestamps with deployment or StatefulSet change timestamps within 30 minutes and verify whether pods became NotReady shortly after configuration changes, using pod events and deployment rollout history as supporting evidence.

Correlate pod NotReady timestamps with readiness probe failure timestamps within 5 minutes and verify whether readiness probe failures caused NotReady state, using pod events and probe status as supporting evidence.

Compare pod NotReady timestamps with node condition transitions within 5 minutes and verify whether node resource pressure or NotReady conditions affected pod health, using node conditions and pod status as supporting evidence.

Analyze pod NotReady patterns over the last 15 minutes to determine if NotReady is persistent (application issue) or intermittent (resource constraints), using pod status history and container health as supporting evidence.

Correlate pod NotReady with ConfigMap or Secret update timestamps within 5 minutes and verify whether configuration changes caused application failures leading to NotReady state, using pod events and resource modification times as supporting evidence.

Compare pod resource requests with node available resources at NotReady times and verify whether resource constraints prevented pods from becoming ready, using node metrics and pod resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for deployment changes, review application logs for gradual degradation patterns, check for external dependency failures (databases, APIs), examine historical pod readiness patterns, verify container image changes. Pod NotReady may result from application bugs, misconfigured health probes, or runtime environment issues rather than immediate configuration changes.
