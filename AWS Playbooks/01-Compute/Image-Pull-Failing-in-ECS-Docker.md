# Docker Image Pull Failing in ECS

## Meaning

Docker image pull is failing in ECS (triggering image pull errors or ECSImagePullFailed alarms) because ECR repository access is denied, IAM task execution role lacks ECR permissions, image does not exist in repository, image tag is incorrect, ECR repository policy restricts access, or ECS task network configuration prevents ECR access. ECS tasks cannot pull Docker images, container image pull errors occur, and task startup fails. This affects the container orchestration layer and blocks container deployment, typically caused by ECR permission issues, image availability problems, or network configuration errors; if using ECS with Fargate, ECR access behavior may differ and applications may experience image pull failures.

## Impact

ECS tasks cannot pull Docker images; container image pull errors occur; task startup fails; ECR image access is denied; container deployment is blocked; image pull automation fails; task definition cannot launch containers; application containers cannot start. ECSImagePullFailed alarms may fire; if using ECS with Fargate, ECR access behavior may differ; applications may experience errors or performance degradation due to failed container startup; container workloads cannot be deployed.

## Playbook

1. Verify ECS task definition `<task-definition-arn>` exists and AWS service health for ECS and ECR in region `<region>` is normal.
2. Retrieve the ECS Task Definition `<task-definition-arn>` and inspect its container image configurations, image URIs, and ECR repository references, verifying image URI format.
3. Retrieve the IAM role `<role-name>` used for ECS task execution and inspect its policy permissions for ECR operations including GetAuthorizationToken, BatchGetImage, and GetDownloadUrlForLayer, verifying IAM permissions.
4. Query CloudWatch Logs for log groups containing ECS task logs and filter for image pull failure patterns, ECR access denied errors, or Docker pull errors, including error message details.
5. Retrieve the ECR Repository `<repository-name>` referenced in task definition and inspect its repository policy, image tags, and repository access settings, verifying image exists.
6. List ECS task failures in cluster `<cluster-name>` and check for image pull error patterns and task failure reasons, analyzing failure patterns.
7. Retrieve the ECS Task Definition `<task-definition-arn>` network configuration if using VPC and verify network connectivity to ECR, checking if VPC configuration blocks ECR access.
8. Retrieve CloudWatch metrics for ECR repository `<repository-name>` including ImagePullCount if available and verify repository activity, checking if repository is accessible.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for ECR repository policy or IAM role policy modification events related to task execution role `<role-name>` within the last 24 hours, checking for permission changes.

## Diagnosis

1. Analyze CloudWatch Logs containing ECS task logs (from Playbook step 4) to identify specific image pull error messages. If errors indicate "AccessDeniedException" or "authorization token", proceed immediately to IAM permission verification. If errors indicate "CannotPullContainerError" with "not found", the image or tag does not exist. If errors indicate network timeout, VPC or endpoint configuration is the issue.

2. For access-denied errors, verify IAM task execution role permissions (from Playbook step 3) to ensure the role has ecr:GetAuthorizationToken, ecr:BatchGetImage, and ecr:GetDownloadUrlForLayer permissions. If any of these permissions are missing, image pulls will fail. Also verify the role can access the specific ECR repository.

3. Review ECR repository configuration (from Playbook step 5) to verify the image exists with the correct tag. If the image tag referenced in the task definition does not exist in the repository, the pull fails. Check if lifecycle policies may have deleted the image.

4. Examine task definition image URI configuration (from Playbook step 2) to verify the ECR repository URI and image tag are correctly formatted. If the repository URI is malformed or points to a non-existent repository, image pulls fail.

5. For Fargate tasks, verify VPC network configuration (from Playbook step 7) to ensure the task can reach ECR. If using private subnets without NAT gateway or ECR VPC endpoints, the task cannot pull images from ECR.

6. Correlate CloudTrail events (from Playbook step 9) with image pull failure timestamps within 5 minutes to identify any ECR repository policy or IAM role policy modifications. If permission changes coincide with when image pulls started failing, those changes are the likely cause.

7. Compare image pull failure patterns across different task definitions within 1 hour. If failures are task definition-specific, the issue is with that task's image URI or configuration. If failures affect all tasks using the same execution role, IAM permissions are the root cause.

8. Review ECR repository metrics (from Playbook step 8) if available to verify repository activity and accessibility. If the repository shows no recent image pull activity, there may be broader access issues.

If no correlation is found within the specified time windows: extend timeframes to 48 hours, review alternative evidence sources including ECR repository image availability and image tag existence, check for gradual issues like ECR repository policy changes or image lifecycle policy deletions, verify external dependencies like ECR service availability or network connectivity to ECR, examine historical patterns of image pull failures, check for ECS Fargate ECR access VPC endpoint requirements, verify ECR image scanning blocking pulls. Image pull failures may result from image tag deletion, ECR repository lifecycle policy actions, ECR service issues, ECS Fargate ECR VPC endpoint requirements, or ECR image scanning failures rather than immediate task definition changes.
