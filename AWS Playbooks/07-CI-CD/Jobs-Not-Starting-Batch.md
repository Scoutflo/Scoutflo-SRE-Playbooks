# AWS Batch Jobs Not Starting

## Meaning

AWS Batch jobs are not starting (triggering job execution failures or BatchJobStartFailed alarms) because compute environment is not available, job queue is misconfigured, IAM permissions are insufficient, job definition has errors, Batch service encounters errors during job submission, or Batch compute environment capacity is insufficient. AWS Batch jobs cannot start, job execution is blocked, and batch processing workflows fail. This affects the batch processing and compute layer and blocks job execution, typically caused by compute environment issues, queue configuration problems, or permission failures; if using Batch with ECS, compute environment behavior may differ and applications may experience job submission failures.

## Impact

AWS Batch jobs cannot start; job execution is blocked; batch processing workflows fail; job queue processing is interrupted; batch job automation is ineffective; job submissions fail; batch processing reliability is compromised; job scheduling fails. BatchJobStartFailed alarms may fire; if using Batch with ECS, compute environment behavior may differ; applications may experience errors or performance degradation due to failed job execution; batch processing pipelines may be completely blocked.

## Playbook

1. Verify Batch job queue `<job-queue-name>` exists and AWS service health for Batch in region `<region>` is normal.
2. Retrieve the Batch Job Queue `<job-queue-name>` in region `<region>` and inspect its queue configuration, compute environment associations, and queue status, verifying queue is in "VALID" state.
3. Retrieve the Batch Compute Environment `<compute-environment-name>` associated with job queue `<job-queue-name>` and inspect its compute environment status, instance configuration, and resource allocation, verifying compute environment is in "VALID" state.
4. Query CloudWatch Logs for log groups containing Batch events and filter for job submission failure patterns, job start errors, or compute environment errors, including error message details.
5. Retrieve the Batch Job Definition `<job-definition-arn>` for submitted jobs and inspect its job definition configuration, resource requirements, and container configuration, verifying job definition is valid.
6. List Batch jobs in queue `<job-queue-name>` and check job status, job submission timestamps, and job failure reasons, analyzing job status patterns.
7. Retrieve the Batch Compute Environment `<compute-environment-name>` compute resources and verify compute resources are available, checking if capacity constraints prevent job starts.
8. Retrieve the IAM role `<role-name>` used by Batch for job execution and verify IAM permissions, checking if permission issues prevent job starts.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Batch job queue or compute environment modification events related to `<job-queue-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs from Step 4**: Review the Batch event logs for job submission failure patterns and error messages. If CloudWatch Logs indicate "compute environment capacity" or "insufficient resources" errors, then the compute environment lacks capacity (proceed to Step 3 data). If CloudWatch Logs show "InvalidParameterException" or "job definition" errors, then the job definition is misconfigured (proceed to Step 5 data). If logs are inconclusive, continue to step 2.

2. **Check IAM Permissions from Step 8**: If the issue involves access denied or permission errors in CloudWatch Logs, verify the IAM role permissions early. If IAM role `<role-name>` lacks `batch:SubmitJob`, `ecs:RunTask`, or required service-linked role permissions, then insufficient permissions are blocking job execution. If IAM permissions appear correct, continue to step 3.

3. **Evaluate Compute Environment Status from Step 3**: If the compute environment from Step 3 shows status other than "VALID" or "ENABLED", then compute environment issues are preventing job starts. If CloudWatch Logs from Step 4 show compute resource errors correlating within 5 minutes of job failures, then resource allocation is the root cause. If compute environment is healthy, continue to step 4.

4. **Correlate Job Queue Configuration from Step 2**: If job queue status from Step 2 is not "VALID" or shows no associated compute environments, then queue misconfiguration is blocking jobs. Compare job start failure timestamps with CloudTrail events from Step 9 - if queue modifications occurred within 5 minutes of failures, then recent configuration changes caused the issue. If queue configuration is valid, continue to step 5.

5. **Validate Job Definition from Step 5**: If job definition from Step 5 shows invalid container configuration, missing required parameters, or resource requirements exceeding compute environment capacity from Step 7, then job definition errors are preventing starts. Correlate job definition modification timestamps from Step 9 with failure onset - if modifications occurred within 30 minutes before failures began, then recent changes introduced the issue.

**If no correlation is found**: Extend analysis to 7 days using job status patterns from Step 6. If failures are constant, suspect configuration issues. If failures are intermittent, suspect resource availability from Step 7 or ECS cluster health. Verify Batch service health from Step 1 and check for compute environment instance type constraints or job queue priority conflicts affecting job scheduling.
