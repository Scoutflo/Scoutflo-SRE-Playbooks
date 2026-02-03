---
title: Job Failing To Complete - Job
weight: 286
categories:
  - kubernetes
  - workload
---

# JobFailingToComplete-job

## Meaning

A Kubernetes Job cannot reach a successful completion state (potentially triggering KubeJobFailed or KubeJobCompletionStuck alerts) because its pods are exiting with non-zero status, being restarted repeatedly, or hitting backoff or activeDeadlineSeconds limits. This indicates job execution failures, pod failures, resource constraints, or job configuration issues preventing successful job completion.

## Impact

Jobs fail to complete successfully; batch processing tasks do not finish; cron jobs fail; data processing pipelines break; scheduled tasks remain incomplete; KubeJobFailed alerts fire; KubeJobCompletionStuck alerts may fire; job pods exit with errors; job backoff limits are reached; job deadlines are exceeded.

## Playbook

1. Describe the job `<job-name>` in namespace `<namespace>` to inspect job status, completion status, and configuration.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify job-related failures and pod errors.

3. Retrieve logs from job pod in namespace `<namespace>` and filter for errors.

4. List pods in namespace `<namespace>` and filter for job pods to check pod status and restart count.

5. Retrieve job `<job-name>` in namespace `<namespace>` and verify job configuration including backoffLimit and activeDeadlineSeconds.

6. Retrieve job pod in namespace `<namespace>` to check for resource constraints.

## Diagnosis

Begin by analyzing the Job describe output, pod logs, and events collected in the Playbook section. The Job conditions, pod exit codes, and container termination reasons provide the primary diagnostic signals.

**If Job status shows backoffLimitExceeded:**
- The job pods failed more times than `backoffLimit` allows. Check pod logs for the actual error causing failures. The application is failing, not the Job configuration.

**If Job status shows DeadlineExceeded:**
- The job exceeded `activeDeadlineSeconds` before completing. Either increase the deadline if the job legitimately needs more time, or investigate why the job takes longer than expected.

**If pod logs show application errors or non-zero exit codes:**
- The job container is failing due to application issues. Review the specific error in logs. Common causes include missing environment variables, failed database connections, or invalid input data.

**If pod shows OOMKilled in termination reason:**
- The job container exceeded memory limits. Increase memory limits in the Job spec, or optimize the job workload to use less memory.

**If pod shows Evicted status:**
- Node resource pressure caused pod eviction. Check node conditions for memory or disk pressure. Consider adding resource requests to protect job pods from eviction.

**If pod is stuck in Pending with scheduling failures:**
- The job pod cannot be scheduled. Check events for `Insufficient cpu`, `Insufficient memory`, or node affinity issues. Adjust resource requests or node selectors.

**If the job runs but never completes (pod stays Running):**
- The job process may be hanging. Check pod logs for the last activity. The application may be waiting on external dependencies or stuck in a loop.

**If events are inconclusive, correlate timestamps:**
1. Check if job failures began after the Job spec was modified.
2. Check if failures correlate with ConfigMap or Secret changes the job depends on.
3. Check if external service dependencies became unavailable.

**If no clear cause is identified:** Run the job container locally or in a debug pod with the same image and environment to reproduce and debug the application failure interactively.
