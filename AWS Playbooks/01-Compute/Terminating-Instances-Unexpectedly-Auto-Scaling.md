# AWS Auto Scaling Terminating Instances Unexpectedly

## Meaning

Auto Scaling Group terminates instances unexpectedly (triggering instance termination alarms like EC2InstanceTerminated or AutoScalingGroupInstanceTermination) because scaling policies trigger scale-in actions, health checks fail causing instance replacement, desired capacity is reduced, spot instance interruptions occur, manual termination requests are processed, or Auto Scaling Group instance refresh operations terminate instances. EC2 instances are terminated unexpectedly, application capacity is reduced, and services become unavailable. This affects the compute and scaling layer and reduces service capacity, typically caused by scaling policy misconfiguration, health check issues, or capacity changes; if instances host container workloads, unexpected terminations may affect pod scheduling and applications may experience capacity loss.

## Impact

EC2 instances are terminated unexpectedly; application capacity is reduced; services become unavailable; instance termination alarms fire; Auto Scaling removes healthy instances; desired capacity cannot be maintained; application availability degrades; workloads are interrupted. EC2InstanceTerminated alarms may fire; if instances host container workloads, unexpected terminations may affect pod scheduling and applications may experience capacity loss; service reliability is compromised; user-facing services experience availability issues.

## Playbook

1. Verify Auto Scaling Group `<asg-name>` exists and AWS service health for EC2 and Auto Scaling in region `<region>` is normal.
2. Retrieve the Auto Scaling Group `<asg-name>` in region `<region>` and inspect its scaling activity history, instance termination events, and scaling policy configurations, verifying termination reasons.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Auto Scaling instance termination events related to Auto Scaling Group `<asg-name>`, including termination reason details.
4. Retrieve CloudWatch metrics for Auto Scaling Group `<asg-name>` including GroupDesiredCapacity, GroupInServiceInstances, and GroupTerminatingInstances over the last 1 hour to identify termination patterns, analyzing termination frequency.
5. List EC2 instances terminated by Auto Scaling Group `<asg-name>` and check termination reasons, health check status, and instance state transitions, verifying health check results.
6. Retrieve CloudWatch alarms associated with Auto Scaling Group `<asg-name>` and check for alarms triggering scale-in actions or instance replacements, verifying alarm configurations.
7. Retrieve the Auto Scaling Group `<asg-name>` health check configuration and verify health check settings, checking if health check failures are causing terminations.
8. Retrieve CloudWatch metrics for EC2 instances in Auto Scaling Group `<asg-name>` including StatusCheckFailed and verify instance health, checking if status check failures trigger terminations.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Auto Scaling Group scaling policy or desired capacity modification events related to `<asg-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 6) and Auto Scaling activity history (from Playbook step 2) to identify when terminations first occurred and the stated termination reason.

2. If termination reason indicates "instance was unhealthy" and EC2 status checks (from Playbook step 8) show failures around termination timestamps, health check failures are triggering instance replacement.

3. If Auto Scaling activity (from Playbook step 2) shows desired capacity decreased before terminations, examine CloudTrail (from Playbook step 9) for manual capacity changes or scheduled scaling actions that reduced capacity.

4. If CloudWatch alarms (from Playbook step 6) show scale-in alarm triggered before terminations, scaling policies are functioning as configured. Review policy thresholds to determine if they are too aggressive.

5. If terminated instances (from Playbook step 5) were spot instances with "instance-interrupted" reason in CloudTrail (from Playbook step 3), spot capacity reclamation is the cause rather than ASG configuration.

6. If health check configuration (from Playbook step 7) was modified around the termination timestamp, verify health check grace period and health check type. ELB health checks may be more sensitive than EC2 status checks.

7. If CloudWatch metrics (from Playbook step 4) show GroupDesiredCapacity unchanged but instances still terminated, instance refresh operations or rebalancing may be rotating instances.

If no correlation is found: extend analysis to 24 hours, review load balancer health check integration, check for instance refresh operations, examine termination policies for oldest instance priority, and verify spot instance interruption patterns.
