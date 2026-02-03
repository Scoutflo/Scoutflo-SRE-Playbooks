# AWS CodePipeline Stuck in Progress

## Meaning

A CodePipeline execution is stuck in progress (triggering pipeline execution delays or CodePipelineExecutionStuck alarms) because a pipeline stage is waiting for manual approval, a stage action is failing or timing out, IAM permissions are insufficient for stage actions, source or build artifacts are unavailable, a deployment stage cannot complete, or pipeline stage transition conditions are not met. CodePipeline executions are delayed, deployments are blocked, and CI/CD workflows cannot complete. This affects the CI/CD layer and blocks releases, typically caused by approval gates, action failures, or artifact availability issues; if using CodePipeline with multiple stages, stuck states may cascade and applications may experience deployment delays.

## Impact

CodePipeline executions are delayed; deployments are blocked; CI/CD workflows cannot complete; pipeline stages hang; manual intervention is required; deployment automation fails; pipeline execution history shows stuck states; release processes are interrupted. CodePipelineExecutionStuck alarms may fire; if using CodePipeline with multiple stages, stuck states may cascade; applications may experience errors or performance degradation due to blocked deployments; release processes may be completely halted.

## Playbook

1. Verify pipeline `<pipeline-name>` exists and AWS service health for CodePipeline in region `<region>` is normal.
2. Retrieve the CodePipeline `<pipeline-name>` in region `<region>` and inspect its execution history, current execution status, and stage action states, verifying which stage is stuck.
3. Query CloudWatch Logs for log groups containing CodePipeline execution logs and filter for error patterns, timeout events, or stage failure messages related to pipeline `<pipeline-name>`, including stuck stage details.
4. Retrieve CloudWatch metrics for CodePipeline `<pipeline-name>` including FailedExecutions and SucceededExecutions over the last 24 hours to identify execution patterns, analyzing execution history.
5. Retrieve the IAM role `<role-name>` used by CodePipeline `<pipeline-name>` and inspect its policy permissions for pipeline stage actions, verifying IAM permissions.
6. List CodeBuild build history for builds triggered by CodePipeline `<pipeline-name>` and check for build failures or errors that may cause pipeline to hang, analyzing build status.
7. Retrieve the CodePipeline `<pipeline-name>` stage configuration and verify manual approval gates, checking if manual approvals are blocking execution.
8. Retrieve the CodePipeline `<pipeline-name>` artifact configuration and verify artifact availability, checking if artifacts are missing or unavailable.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CodePipeline stage or action modification events related to pipeline `<pipeline-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CodePipeline execution history (from Playbook step 2) to identify which stage is stuck and when the execution entered the stuck state. The stage name and timestamp establish the correlation baseline.

2. If pipeline configuration (from Playbook step 7) shows the stuck stage is a manual approval action, the execution is waiting for human approval. This is expected behavior requiring manual intervention.

3. If execution logs (from Playbook step 3) show the stuck stage is a build or deploy action, check CodeBuild build history (from Playbook step 6). If the associated build is running or failed, build completion or failure is blocking pipeline progression.

4. If artifact configuration (from Playbook step 8) shows artifact access issues, verify S3 bucket permissions. Missing artifact availability blocks subsequent stages from retrieving required inputs.

5. If IAM role permissions (from Playbook step 5) were modified around the stuck timestamp (check CloudTrail from Playbook step 9), missing permissions for stage actions (CodeBuild, CodeDeploy, Lambda invoke) are blocking execution.

6. If CloudWatch metrics (from Playbook step 4) show successful executions before but failures now, compare pipeline configuration before and after to identify the change.

7. If stuck state is at a source stage, verify source repository access (GitHub, CodeCommit, S3). Authentication or connectivity issues block artifact retrieval.

If no correlation is found: extend analysis to 48 hours, verify manual approval gate requirements, check external service integration status, examine cross-region artifact replication delays, and review stage transition condition configurations.
