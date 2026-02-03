# CodeDeploy Failing on EC2 Instances

## Meaning

CodeDeploy deployments fail on EC2 instances (triggering deployment failures or CodeDeployDeploymentFailure alarms) because CodeDeploy agent is not running, IAM instance profile permissions are insufficient, deployment group configuration is incorrect, application stop scripts fail, instance health checks fail during deployment, or CodeDeploy agent version is incompatible. CodeDeploy deployments fail, application updates cannot be deployed, and EC2 instances do not receive new code. This affects the CI/CD and deployment layer and blocks application updates, typically caused by agent issues, permission problems, or configuration errors; if instances host container workloads, CodeDeploy behavior may differ and applications may experience deployment failures.

## Impact

CodeDeploy deployments fail; application updates cannot be deployed; EC2 instances do not receive new code; deployment automation is blocked; instance health checks fail; deployment rollbacks occur; application versions remain outdated; deployment processes are interrupted. CodeDeployDeploymentFailure alarms may fire; if instances host container workloads, CodeDeploy behavior may differ; applications may experience errors or performance degradation due to failed deployments; application versions may remain outdated.

## Playbook

1. Verify CodeDeploy application `<application-name>` and deployment group `<deployment-group-name>` exist, and AWS service health for CodeDeploy in region `<region>` is normal.
2. Retrieve CodeDeploy deployment history for deployment group `<deployment-group-name>` and inspect recent deployment failures, deployment status, and instance deployment states, analyzing failure patterns.
3. Query CloudWatch Logs for log groups containing CodeDeploy agent logs and filter for deployment failure patterns, agent errors, or health check failures, including agent error messages.
4. Retrieve the CodeDeploy Application `<application-name>` and Deployment Group `<deployment-group-name>` in region `<region>` and inspect deployment configuration, health check settings, and instance selection criteria, verifying deployment group configuration.
5. Retrieve the IAM instance profile `<instance-profile-name>` attached to EC2 instances in deployment group `<deployment-group-name>` and inspect its policy permissions for CodeDeploy operations, verifying IAM permissions.
6. List EC2 instances in deployment group `<deployment-group-name>` and check CodeDeploy agent status, instance health, and deployment state, verifying agent is running.
7. Retrieve the CodeDeploy Deployment Group `<deployment-group-name>` deployment configuration and verify deployment configuration settings, checking deployment type and deployment settings.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CodeDeploy deployment group or application modification events related to `<deployment-group-name>` within the last 24 hours, checking for configuration changes.
9. Retrieve CloudWatch metrics for CodeDeploy application `<application-name>` including DeploymentFailures over the last 24 hours to identify deployment failure patterns.

## Diagnosis

1. Analyze CodeDeploy deployment history (from Playbook step 2) to identify when failures first appeared. The deployment ID and failure timestamp establish the correlation baseline.

2. If instance deployment states (from Playbook step 2) show failures on specific instances while others succeed, examine agent status on failed instances (from Playbook step 6). If agent is not running, agent installation or service issues are the root cause.

3. If agent logs (from Playbook step 3) show permission errors, verify IAM instance profile permissions (from Playbook step 5). Missing CodeDeploy or S3 permissions prevent artifact download and deployment execution.

4. If CloudTrail shows deployment group modifications (from Playbook step 8) around the failure timestamp, configuration changes may have introduced incompatible settings or changed instance selection criteria.

5. If CloudWatch Logs (from Playbook step 3) show application lifecycle script failures (ApplicationStop, BeforeInstall, etc.), the deployment is failing at a specific hook. Examine the failing script for errors in custom deployment logic.

6. If deployment configuration (from Playbook step 7) shows health check requirements, verify instances can pass health checks. Aggressive health check settings may fail instances before deployment completes.

7. If deployment metrics (from Playbook step 9) show constant failures, the issue is configuration or script-related. If intermittent, agent connectivity or transient infrastructure issues are the cause.

If no correlation is found: extend analysis to 48 hours, verify CodeDeploy agent version compatibility, check deployment configuration type (in-place vs blue/green), examine application script dependencies, and review health check threshold settings.
