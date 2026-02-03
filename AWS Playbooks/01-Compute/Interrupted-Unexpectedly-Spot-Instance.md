# EC2 Spot Instance Interrupted Unexpectedly

## Meaning

An EC2 Spot Instance is interrupted unexpectedly (triggering alarms like EC2SpotInstanceInterruption or SpotInstanceInterruptionWarning) because AWS reclaims capacity due to spot price exceeding maximum bid, capacity demand increases, spot instance termination requests are initiated, spot fleet configuration causes interruptions, or regional capacity constraints trigger reclaiming. Spot instances terminate unexpectedly, applications lose state, and workloads are interrupted with a 2-minute warning. This affects the compute layer and disrupts workloads, typically caused by spot price volatility, capacity constraints, or bid configuration issues; if instances host container workloads, spot interruptions may affect pod scheduling and applications may experience workload interruptions.

## Impact

Spot instances terminate unexpectedly; applications lose state; workloads are interrupted; data processing jobs fail; EC2SpotInstanceInterruption alarms fire; services become unavailable; running tasks are lost; spot instance workloads cannot complete; capacity is reclaimed by AWS. SpotInstanceInterruptionWarning alarms may fire; if instances host container workloads, spot interruptions may affect pod scheduling and applications may experience workload interruptions; application workflows are disrupted; data processing may be incomplete.

## Playbook

1. Verify spot instance `<instance-id>` exists and AWS service health for EC2 in region `<region>` is normal.
2. Retrieve the EC2 Spot Instance `<instance-id>` in region `<region>` and inspect its spot instance request status, interruption reason, termination timestamp, and spot instance request ID.
3. Retrieve CloudWatch metrics for spot instance pricing in region `<region>` including SpotPrice over the last 24 hours to identify price fluctuations, analyzing price trends.
4. Query CloudWatch Logs for log groups containing CloudTrail events and filter for spot instance interruption events related to instance `<instance-id>`, including interruption reason details.
5. List EC2 Spot Instance Requests in region `<region>` and check their status, maximum price, and interruption patterns, verifying bid configuration.
6. Retrieve CloudWatch alarms associated with spot instance interruptions and check for alarms in ALARM state related to spot instance termination, verifying alarm configurations.
7. Retrieve the EC2 Spot Instance Request `<spot-request-id>` associated with instance `<instance-id>` and inspect its maximum price, instance type requirements, and availability zone preferences, checking bid configuration.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for spot fleet or spot instance request modification events related to request `<spot-request-id>` within the last 24 hours, checking for configuration changes.
9. Retrieve CloudWatch metrics for EC2 spot instance capacity in region `<region>` and analyze capacity trends, checking if capacity constraints contributed to interruptions.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 6) and CloudTrail events (from Playbook step 4) to identify when EC2SpotInstanceInterruption events first appeared. The interruption notice timestamp (2 minutes before termination) establishes the correlation baseline.

2. If spot instance request details (from Playbook step 2) show interruption reason as "price" and spot price metrics (from Playbook step 3) show price exceeded maximum bid around the interruption time, insufficient bid price is the root cause.

3. If interruption reason shows "capacity" rather than "price", AWS reclaimed capacity due to demand. Check regional capacity metrics (from Playbook step 9) for capacity constraint patterns.

4. If multiple instances in the same region or availability zone were interrupted simultaneously (from Playbook step 5), regional capacity issues are affecting the entire zone rather than individual instances.

5. If spot instance request configuration (from Playbook step 7) shows one-time request type, interrupted instances are not automatically replaced. Persistent requests or spot fleets would launch replacement instances.

6. If Auto Scaling Group activity (from CloudTrail in Playbook step 8) shows replacement launches around interruption timestamps, verify the ASG is correctly configured with mixed instance types to reduce interruption impact.

7. If interruption patterns (from Playbook step 3 and step 5) show predictable timing (specific hours or days), capacity demand follows patterns that can be anticipated through instance type diversification.

If no correlation is found: extend analysis to 48 hours, review spot price history trends, check spot fleet configuration for instance type diversification, verify interruption notification delivery to applications, and examine spot instance hibernation vs termination settings.
