# ECS Service Not Scaling as Expected

## Meaning

ECS service does not scale as expected (triggering scaling failures or ECSServiceScalingFailure alarms) because Auto Scaling target tracking is misconfigured, service desired count does not match scaling policy targets, ECS service scaling policies are incorrect, cluster capacity is insufficient, scaling metric thresholds are not met, or ECS service deployment conflicts prevent scaling. ECS service cannot scale, desired task count is not achieved, and application capacity is insufficient. This affects the container orchestration layer and prevents service scaling, typically caused by Auto Scaling configuration issues, capacity constraints, or metric threshold problems; if using ECS Fargate vs EC2, scaling behavior differs and applications may experience scaling delays.

## Impact

ECS service cannot scale; desired task count is not achieved; application capacity is insufficient; Auto Scaling policies fail to trigger; service scaling alarms fire; application performance degrades under load; service cannot meet demand; scaling automation is ineffective. ECSServiceScalingFailure alarms may fire; if using ECS Fargate vs EC2, scaling behavior differs; applications may experience errors or performance degradation due to insufficient capacity; container workloads cannot meet demand.

## Playbook

1. Verify ECS service `<service-name>` and cluster `<cluster-name>` exist, and AWS service health for ECS in region `<region>` is normal.
2. Retrieve the ECS Service `<service-name>` in cluster `<cluster-name>` in region `<region>` and inspect its desired count, running count, scaling configuration, and service events, verifying desired vs running count mismatch.
3. Retrieve CloudWatch metrics for ECS Service `<service-name>` including CPUUtilization, MemoryUtilization, and DesiredTaskCount over the last 1 hour to identify scaling patterns, analyzing metric trends.
4. Retrieve the Application Auto Scaling target for ECS Service `<service-name>` and inspect its target tracking policies, scaling policies, and metric thresholds, verifying scaling policy configuration.
5. Query CloudWatch Logs for log groups containing ECS service events and filter for scaling failure events or task placement errors related to service `<service-name>`, including failure reason details.
6. Retrieve the ECS Cluster `<cluster-name>` and inspect its capacity, registered container instances, and available resources for task placement, verifying cluster capacity.
7. Retrieve CloudWatch metrics for ECS Cluster `<cluster-name>` including CPUReservation and MemoryReservation to verify resource availability, checking if capacity constraints prevent scaling.
8. Retrieve the ECS Service `<service-name>` deployment configuration and verify deployment status, checking if active deployments prevent scaling operations.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for ECS service or Application Auto Scaling modification events related to service `<service-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze ECS service events (from Playbook step 5) to identify when scaling failures or task placement failures first appeared. These event timestamps establish the correlation baseline.

2. If CloudWatch metrics (from Playbook step 3) show CPUUtilization or MemoryUtilization not reaching scaling policy thresholds (from Playbook step 4), scaling is not triggered because thresholds are not met - this is expected behavior rather than a failure.

3. If Auto Scaling target configuration (from Playbook step 4) was modified around the issue timestamp (check CloudTrail from Playbook step 9), verify target tracking policies have correct metric specifications and threshold values.

4. If ECS cluster capacity (from Playbook step 6) shows CPUReservation or MemoryReservation (from Playbook step 7) near 100%, cluster capacity is exhausted preventing task placement. Additional EC2 instances or capacity provider scaling is needed.

5. If service deployment configuration (from Playbook step 8) shows active deployments, deployment maximumPercent or minimumHealthyPercent constraints may be limiting scaling during deployment transitions.

6. If service events (from Playbook step 5) show task placement failures with specific constraint messages, placement constraints (availability zones, instance types, attributes) are preventing task scheduling.

7. If comparing Fargate vs EC2 launch types (from Playbook step 6), note that Fargate capacity is managed by AWS while EC2 requires sufficient cluster container instances.

If no correlation is found: extend analysis to 24 hours, verify CloudWatch metric availability for scaling triggers, check capacity provider configuration, examine task definition resource requirements, and review placement constraint compatibility.
