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

1. Compare ECS cluster instance count change timestamps with task pending timestamps within 5 minutes and verify whether task pending began when cluster capacity decreased, using ECS cluster events as supporting evidence.
2. Correlate task definition modification timestamps with task placement failure timestamps and verify whether task definition changes caused placement failures, using ECS task definition events as supporting evidence.
3. Compare cluster resource utilization timestamps with task pending timestamps within 5 minutes and verify whether resource exhaustion prevented task placement, using ECS cluster metrics as supporting evidence.
4. Compare IAM role permission change timestamps with task placement failure timestamps within 5 minutes and verify whether permission changes prevented task execution, using IAM role configuration data as supporting evidence.
5. Analyze task pending frequency over the last 15 minutes to determine if pending is constant (resource constraint) or intermittent (capacity fluctuations).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including ECS service events and container instance logs, check for gradual issues like cluster capacity exhaustion, verify external dependencies like container image availability, examine historical patterns of ECS task placement, check for ECS Fargate vs EC2 capacity provider differences, verify ECS task definition platform version compatibility. Task pending may result from container image pull failures, network connectivity issues, container instance health problems, ECS Windows container scenarios, or ECS task definition platform version mismatches rather than immediate ECS configuration changes.
