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

1. Describe pod <pod-name> in namespace <namespace> to see:
   - Conditions section showing Ready=False and the reason
   - Container status showing waiting/running state
   - Events section showing probe failures or other errors

2. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to see readiness probe failures, startup issues, or dependency errors with timestamps.

3. Retrieve the conditions for pod <pod-name> in namespace <namespace> and identify which condition is failing (Ready, ContainersReady, PodScheduled, or Initialized).

4. Retrieve logs from pod <pod-name> in namespace <namespace> to see application startup issues - look for errors during initialization or health check endpoint failures.

5. Describe Deployment <deployment-name> in namespace <namespace> to check:
   - Readiness probe configuration (path, port, timeoutSeconds, failureThreshold)
   - Resource requests/limits that may cause slow startup
   - Environment variables or ConfigMap/Secret references

6. Verify dependencies exist: check ConfigMap <name>, Secret <name>, and PVC <name> in namespace <namespace>.

7. Describe node <node-name> where pod is running and check Conditions section to see if node issues are affecting pod health.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify why the pod is NotReady. Events showing probe failures, startup errors, or dependency issues indicate the specific cause.

2. If pod conditions show Ready=False with reason (from Playbook step 3), identify the failing condition:
   - ContainersReady=False: Container health checks failing
   - PodScheduled=False: Pod cannot be scheduled (still Pending)
   - Initialized=False: Init containers not complete

3. If events show "Readiness probe failed" (from Playbook step 2):
   - Check probe configuration (Playbook step 5)
   - Verify application responds on probe endpoint
   - Adjust initialDelaySeconds if startup is slow
   - Review application logs for errors (Playbook step 4)

4. If pod shows CrashLoopBackOff or container restarts:
   - Check termination reason (OOMKilled, Error)
   - Review previous container logs for crash cause
   - Verify resource limits are adequate

5. If events show missing dependencies (from Playbook step 6):
   - ConfigMap or Secret does not exist
   - PVC cannot be bound
   - Service dependencies unavailable

6. If node shows issues (from Playbook step 7):
   - Node NotReady affects all pods on that node
   - Node resource pressure may cause pod eviction
   - Check node conditions and resource usage

7. If application logs show startup or runtime errors (from Playbook step 4):
   - Application configuration issues
   - Database or external API connectivity problems
   - Missing environment variables or files

**To resolve NotReady pods**: Fix the underlying issue identified in events and logs. For readiness probe failures, adjust probe configuration or fix application health endpoints. For crashes, address the root cause in application code or configuration. For missing dependencies, create required resources.
