---
title: Kube Job Failed
weight: 20
---

# KubeJobFailed

## Meaning

Job has failed to complete successfully (triggering KubeJobFailed alerts) because the job pods have failed, exceeded retry limits, or encountered errors during execution. Jobs show Failed state in kubectl, job pods show Failed or CrashLoopBackOff state, and job logs show fatal errors, panic messages, or exceptions. This affects the workload plane and indicates application errors, resource constraints, or configuration issues preventing job completion, typically caused by application bugs, resource exhaustion, configuration problems, or external dependency failures; application errors may appear in application monitoring.

## Impact

KubeJobFailed alerts fire; failure of processing scheduled tasks; job cannot complete; job remains in Failed state; batch processing tasks fail; dependent workflows may be blocked; data processing or migration tasks do not complete; job pods have failed or exceeded retry limits; job restart policy prevents successful completion. Jobs show Failed state indefinitely; job pods show Failed or CrashLoopBackOff state; application errors may appear in application monitoring; applications cannot complete batch processing tasks and may experience errors or performance degradation.

## Playbook

1. Retrieve the Job `<job-name>` in namespace `<namespace>` and inspect its status to check completion status, failed pod count, and failure reason.

2. Retrieve events for the Job `<job-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'Error', 'BackoffLimitExceeded' to identify failure causes.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the Job `<job-name>` and check pod status to identify failed pods.

4. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` for container `<container-name>` and filter for error patterns including 'fatal', 'panic', 'exception', 'failed', 'error' to identify application errors.

5. Retrieve the Job `<job-name>` in namespace `<namespace>` and check job configuration including backoff limit, active deadline seconds, and restart policy to verify configuration issues.

6. Retrieve the Node `<node-name>` for nodes where job pods ran and verify node resource availability and conditions to identify resource constraints.

## Diagnosis

Compare job failure timestamps with job creation or start timestamps within the job execution window and verify whether job failed immediately after start (configuration issue) or after running (application error), using job events and pod status as supporting evidence.

Correlate job pod failure timestamps with node condition transitions within 5 minutes and verify whether node resource pressure or failures caused job pod failures, using node conditions and pod events as supporting evidence.

Compare job failure patterns across multiple job pods to determine if failures are consistent (application bug) or isolated (resource constraints), using pod logs and exit codes as supporting evidence.

Analyze job pod exit codes and log error patterns to identify root cause categories (application errors, resource constraints, configuration issues), using pod logs and container status as supporting evidence.

Correlate job failures with resource quota exhaustion timestamps within 30 minutes and verify whether quota limits prevented job pod creation or caused failures, using resource quota status and job events as supporting evidence.

Compare job resource requests with node available resources at failure times and verify whether resource constraints caused job failures, using node metrics and job resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to job execution duration, review job application logic, check for external dependency failures, verify job configuration parameters, examine historical job execution patterns. Job failures may result from application bugs, data issues, or external dependency problems rather than immediate infrastructure changes.
