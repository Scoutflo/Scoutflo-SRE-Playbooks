# ECS Task Stuck in Pending State

## Meaning

ECS tasks remain stuck in Pending state (triggering task placement failures or ECSTaskPending alarms) because ECS cluster lacks sufficient EC2 instances, task definition is invalid or incorrectly configured, insufficient resources (CPU, memory) are available, IAM roles lack correct permissions, ECS service logs show task placement errors, task placement constraints prevent scheduling, or capacity provider issues block task placement. ECS tasks cannot start, applications remain unavailable, and task status shows "PENDING" indefinitely. This affects the container orchestration layer and blocks task execution, typically caused by resource constraints, configuration issues, or capacity provider problems; if using ECS Fargate vs EC2, troubleshooting approaches differ and container applications may experience deployment failures.

## Impact

ECS tasks cannot start; applications remain unavailable; task placement fails; ECS service cannot scale; task pending alarms may fire; desired task count cannot be met; container workloads cannot run; service deployments fail; application capacity is reduced. ECSTaskPending alarms fire; if using ECS Fargate vs EC2, capacity provider issues may differ; applications may experience errors or performance degradation due to missing task capacity; container orchestration tasks may show placement failures.

## Playbook

1. Verify ECS cluster `<cluster-name>` and task definition `<task-definition-family>:<revision>` exist, and AWS service health for ECS in region `<region>` is normal.
2. Retrieve the ECS Cluster `<cluster-name>` and ensure the cluster has sufficient EC2 instances by checking cluster instance count and capacity, verifying available CPU and memory.
3. Retrieve the ECS Task Definition `<task-definition-family>:<revision>` and verify task definition is valid and correctly configured, checking task definition JSON syntax.
4. Retrieve the ECS Cluster `<cluster-name>` resource availability and confirm there are enough resources (CPU, memory) to run the task, analyzing resource utilization.
5. Retrieve the IAM role `<role-name>` for ECS service and check IAM roles for correct permissions including AmazonECSServiceRole, verifying both task execution role and task role.
6. Query CloudWatch Logs for log group `/aws/ecs/<cluster-name>` and filter for task placement errors, resource constraint messages, or ECS service errors, including placement constraint violations.
7. Retrieve the ECS Service `<service-name>` placement constraints and verify placement constraints are not preventing task placement, checking constraint configuration.
8. Retrieve the ECS Cluster `<cluster-name>` capacity provider configuration and verify capacity provider (Fargate vs EC2) is available and configured correctly, checking capacity provider status.
9. Retrieve the ECS Service `<service-name>` network configuration and ECS Task Definition `<task-definition-family>:<revision>` task IAM roles and verify network mode (awsvpc, bridge, host) requirements are met and task execution role and task role are configured correctly, checking subnet and security group configuration and role permissions.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify ECS service availability in the region. If service health indicates issues, task pending may be AWS-side requiring monitoring rather than configuration changes.

2. If ECS service logs from Playbook step 6 show specific placement failure reasons, use these to identify the constraint. Common reasons include "no container instances", "insufficient CPU", "insufficient memory", or "placement constraint mismatch".

3. If cluster capacity from Playbook step 2 shows insufficient EC2 instances (for EC2 launch type) or zero registered instances, tasks cannot be placed. Scale the cluster capacity or verify capacity provider auto-scaling.

4. If task definition from Playbook step 3 shows invalid configuration (missing container definition, invalid image reference, syntax errors), the task cannot be created. Verify task definition JSON is valid.

5. If resource availability from Playbook step 4 shows insufficient CPU or memory for the requested task size, tasks cannot be placed. Either reduce task resource requirements or add cluster capacity.

6. If IAM roles from Playbook step 5 lack AmazonECSTaskExecutionRolePolicy or required permissions, task execution fails. Verify both task execution role (for ECR access, logging) and task role (for application permissions).

7. If placement constraints from Playbook step 7 specify instance types, availability zones, or custom attributes not available in the cluster, tasks cannot be placed. Verify constraints match cluster instance attributes.

8. If capacity provider from Playbook step 8 shows Fargate but Fargate capacity is unavailable in the region, or EC2 capacity provider but no instances are available, switch to an available capacity provider or wait for capacity.

9. If network configuration from Playbook step 9 shows awsvpc network mode but ENI limits are reached, or security groups block required traffic, network setup prevents task startup. Verify ENI availability and security group rules.

If no correlation is found from the collected data: extend ECS service event query timeframes to 30 minutes, verify container image exists and is accessible in ECR or Docker Hub, check for Secrets Manager or Parameter Store access failures, and examine ECS service event messages. Task pending may result from ECR pull throttling, container image layer download failures, or ECS agent connectivity issues on container instances.

