# AWS App Runner Deployment Failing

## Meaning

AWS App Runner deployment is failing (triggering deployment failures or AppRunnerDeploymentFailed alarms) because source code repository access is denied, build configuration has errors, IAM role permissions are insufficient, build process encounters errors, deployment configuration is invalid, or App Runner service configuration is incorrect. App Runner deployments fail, application updates cannot be deployed, and deployment automation is blocked. This affects the serverless container deployment layer and blocks application updates, typically caused by source access issues, build configuration problems, or permission failures; if using App Runner with different source types, configuration may differ and applications may experience deployment failures.

## Impact

App Runner deployments fail; application updates cannot be deployed; deployment automation is blocked; build process errors occur; source code access is denied; deployment configuration is ineffective; application versions remain outdated; deployment processes cannot complete. AppRunnerDeploymentFailed alarms may fire; if using App Runner with different source types, configuration may differ; applications may experience errors or performance degradation due to failed deployments; application versions may remain outdated.

## Playbook

1. Verify App Runner service `<service-name>` exists and AWS service health for App Runner in region `<region>` is normal.
2. Retrieve the App Runner Service `<service-name>` in region `<region>` and inspect its source configuration, build configuration, deployment status, and service state, verifying source and build configuration.
3. Query CloudWatch Logs for log groups containing App Runner build logs and filter for deployment failure patterns, build errors, or source access errors, including error message details.
4. Retrieve the IAM role `<role-name>` used by App Runner service and inspect its policy permissions for source repository access and build operations, verifying IAM permissions.
5. Retrieve CloudWatch metrics for App Runner Service `<service-name>` including DeploymentCount and FailedDeploymentCount over the last 24 hours to identify deployment failure patterns, analyzing failure frequency.
6. List App Runner service deployments for service `<service-name>` and check deployment status, failure reasons, and deployment timestamps, analyzing deployment history.
7. Retrieve the App Runner Service `<service-name>` source configuration and verify source repository access, checking if source type (GitHub, CodeCommit, or source image) affects configuration.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for App Runner service configuration modification events related to service `<service-name>` within the last 24 hours, checking for configuration changes.
9. Retrieve the App Runner Service `<service-name>` build configuration and verify buildspec or build commands, checking if build configuration causes failures.

## Diagnosis

1. Analyze CloudWatch Logs containing App Runner build logs (from Playbook step 3) to identify specific deployment failure error messages. If errors indicate "AccessDenied" for source repository, proceed to IAM permission verification. If errors indicate build failures, examine build command output for specific errors. If errors indicate image pull failures, check source image authentication.

2. For access-denied errors, review IAM role permissions (from Playbook step 4) associated with the App Runner service. If the IAM role lacks permissions to access the source repository (CodeCommit, GitHub, or ECR), deployment cannot proceed. Verify the role has required permissions for the source type being used.

3. Review CloudWatch metrics for DeploymentCount and FailedDeploymentCount (from Playbook step 5) to establish deployment patterns. If failed deployments suddenly increased, correlate the timestamp with recent configuration changes. If failures are constant, the issue is likely a persistent configuration problem.

4. Examine App Runner service configuration (from Playbook step 2) to verify source and build settings. If source repository URL is incorrect, branch name is wrong, or build commands have syntax errors, deployments will fail consistently.

5. Review deployment history (from Playbook step 6) to identify failure patterns and specific failure reasons. If failures occur at the same build stage consistently, that stage has configuration issues. If failures occur randomly, the issue may be transient connectivity or resource availability.

6. Correlate CloudTrail events (from Playbook step 8) with deployment failure timestamps within 30 minutes to identify any service configuration modifications that coincide with when deployments started failing.

7. Compare deployment failure patterns across different App Runner services within 1 hour. If failures are service-specific, the issue is with that service's configuration. If failures are account-wide affecting multiple services, the issue is likely IAM permissions or service-level problems.

8. For source image deployments, verify source image authentication and ECR repository access (from Playbook step 7). If image pull credentials are expired or ECR repository policy restricts access, deployments will fail during image pull.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including source repository connectivity and build process logs, check for gradual issues like source repository access changes or build dependency updates, verify external dependencies like source repository availability or build service health, examine historical patterns of deployment failures, check for App Runner source image authentication issues, verify App Runner build timeout settings. Deployment failures may result from source repository access issues, build configuration errors, App Runner service problems, App Runner source image authentication failures, or App Runner build timeout settings rather than immediate service configuration changes.
