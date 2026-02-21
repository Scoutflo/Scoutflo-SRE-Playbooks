---
title: Kube Pod Frequently Restarting
weight: 28
categories: [kubernetes, pod]
---

# KubePodFrequentlyRestarting

## Meaning

Pod is restarting frequently (triggering KubePodFrequentlyRestarting or KubePodContainerRestarting alerts) because the container is experiencing repeated failures and cannot maintain stable operation. Pod restart count is high over a short period, container keeps crashing and restarting, and the application cannot achieve stable running state. This affects the workload plane and indicates persistent issues preventing stable operation; service is intermittently available; users experience unpredictable failures; data may be lost during restarts.

## Impact

KubePodFrequentlyRestarting alerts fire; service availability is degraded; restarts cause service interruptions; in-memory state is lost repeatedly; connections reset on each restart; dependent services see intermittent failures; user experience degrades; SLO violations increase; restart backoff delays grow; may progress to CrashLoopBackOff; deployment appears unhealthy; monitoring shows high churn.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect restart count, last restart time, and restart frequency over the last hour.

2. Retrieve events for the Pod `<pod-name>` and filter for restart-related events to identify patterns and timestamps of failures.

3. Retrieve logs from current and previous container instances using --previous flag to capture error messages leading to each restart.

4. Analyze container termination states and exit codes to categorize failure types (OOMKilled, application error, signal).

5. Retrieve liveness probe configuration and verify if probe settings are appropriate (timeout, period, failureThreshold).

6. Check resource utilization (CPU, memory) patterns leading up to restarts to identify resource exhaustion.

7. Verify external dependencies (databases, APIs, config services) are available and responding correctly.

## Diagnosis

Compare restart timestamps with probe failure events and verify whether liveness probes are causing restarts due to slow application response, using probe configuration and pod events as supporting evidence.

Correlate restarts with application errors in logs and verify whether a consistent error pattern causes failures, using log analysis and error categorization as supporting evidence.

Analyze resource utilization before restarts and verify whether CPU throttling or memory pressure causes application failures, using resource metrics and container status as supporting evidence.

Check for startup race conditions and verify whether the application fails during initialization before becoming ready, using startup logs and readiness probe status as supporting evidence.

Compare with other replicas of the same deployment and verify whether the issue affects all pods or specific instances (suggesting node or data issues), using per-pod metrics and node placement as supporting evidence.

If no correlation is found within the specified time windows: add startup probe to allow longer initialization, increase liveness probe thresholds, review application exception handling, check for external dependency timeout issues, examine application startup dependencies.
