---
title: Container Restarts Frequent
weight: 24
categories: [kubernetes, container]
---

# ContainerRestartsFrequent

## Meaning

Container is restarting frequently (triggering ContainerRestartsFrequent alerts) because the container is experiencing repeated failures and restarts, indicating systemic issues with the application or its environment. Container restart count is increasing rapidly, pod events show multiple restart cycles, and the application cannot maintain stable operation. This affects the workload plane and indicates persistent problems that prevent stable operation; service availability is degraded; data may be lost during restarts; users experience intermittent failures.

## Impact

ContainerRestartsFrequent alerts fire; service availability degrades due to restart cycles; in-flight requests are lost during restarts; connections are reset; startup time adds to unavailability; data in memory is lost on each restart; dependent services experience connection failures; restart backoff delays increase over time; pod may enter CrashLoopBackOff; service endpoints are repeatedly removed and added; load balancer health checks fail intermittently.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect restart count, last restart time, and container exit codes.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for restart-related events including 'Killing', 'Started', 'Created', 'Failed' to identify restart patterns.

3. Retrieve logs from the container across multiple restart cycles using --previous flag to capture logs from crashed instances and identify root cause.

4. Analyze container exit codes: 0 (clean exit), 1 (application error), 137 (SIGKILL/OOMKilled), 143 (SIGTERM), 139 (segfault) to categorize failure type.

5. Retrieve liveness and readiness probe configurations and verify if aggressive probe settings are causing unnecessary restarts.

6. Check resource utilization (CPU, memory) leading up to each restart to identify resource exhaustion patterns.

7. Retrieve node conditions and events to verify if node-level issues are causing container failures.

## Diagnosis

Compare restart timestamps with OOMKilled events and verify whether restarts are caused by memory exhaustion (exit code 137), using container status and memory metrics as supporting evidence.

Correlate restarts with liveness probe failures and verify whether the probe is too aggressive (short timeout, low failure threshold), using probe configuration and pod events as supporting evidence.

Analyze application logs across restart cycles for consistent error patterns and verify whether the same error repeats, using log aggregation and error pattern matching as supporting evidence.

Compare restart patterns with external dependency availability (databases, APIs) and verify whether connection failures cause application crashes, using dependency health and connection error logs as supporting evidence.

Check if restarts follow a pattern (time of day, after specific operations) and verify whether scheduled tasks or load patterns trigger failures, using restart timestamps and job schedules as supporting evidence.

If no correlation is found within the specified time windows: enable core dumps for crash analysis, add debug logging before crash points, check for race conditions in startup sequence, verify container image integrity, review init container completion for dependencies.
