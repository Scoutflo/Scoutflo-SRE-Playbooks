# EC2 Instance High CPU Utilization

## Meaning

An EC2 instance experiences sustained high CPU utilization (triggering alarms like CPUUtilizationHigh) because CPU-intensive processes consume excessive resources, application code inefficiencies cause high CPU usage, instance type is undersized for workload, background processes compete for CPU resources, or CloudWatch metrics indicate CPU utilization consistently above thresholds. CPU utilization metrics exceed 80-90% for extended periods, CloudWatch alarms trigger for high CPU, and application performance degrades. This affects the compute layer and impacts service performance, typically caused by resource constraints, application inefficiencies, or instance sizing issues; if instances host container workloads, high CPU may affect container scheduling and applications may experience performance degradation.

## Impact

CPUUtilizationHigh alarms fire; application performance degrades; response times increase; user-facing services become slow; instance becomes unresponsive; Auto Scaling may trigger unnecessary scaling; other processes on the instance are starved of CPU resources; system stability is compromised. Instance CPU utilization consistently exceeds 80-90%; if instances host container workloads, container scheduling may be affected and applications may experience performance degradation; application workflows may slow down or fail; user-facing services experience increased latency.

## Playbook

1. Verify instance `<instance-id>` exists and is in "running" state, and AWS service health for EC2 in region `<region>` is normal.
2. Retrieve CloudWatch metrics for EC2 instance `<instance-id>` including CPUUtilization over the last 1 hour to identify CPU usage patterns and spikes, analyzing CPU trend over time.
3. Retrieve the EC2 Instance `<instance-id>` in region `<region>` and inspect its instance type configuration, verifying instance type is appropriate for workload.
4. Query CloudWatch Logs for log groups containing application logs for instance `<instance-id>` and filter for error patterns or performance-related log entries indicating CPU-intensive operations, including process-level CPU usage indicators.
5. Retrieve CloudWatch alarms associated with instance `<instance-id>` with metric CPUUtilization and check for alarms in ALARM state, verifying alarm threshold configurations.
6. List EC2 instances in region `<region>` with the same instance type as `<instance-id>` and compare CPU utilization patterns to determine if the issue is instance-specific, analyzing CPU utilization across similar instances.
7. Retrieve the Auto Scaling Group `<asg-name>` associated with instance `<instance-id>` and inspect scaling policies and target tracking configurations to verify if high CPU triggers scaling actions, checking scaling policy CPU thresholds.
8. Retrieve CloudWatch metrics for EC2 instance `<instance-id>` including NetworkIn, NetworkOut, and DiskReadOps to identify if high CPU correlates with I/O operations, analyzing correlation between CPU and I/O metrics.
9. Query CloudWatch Logs for log groups containing system logs for instance `<instance-id>` and filter for process-related errors or resource contention patterns, checking for background process issues.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when CPUUtilizationHigh alarm first entered ALARM state. This timestamp establishes the correlation baseline for root cause analysis.

2. If application logs (from Playbook step 4) show error patterns or performance-related entries around the alarm timestamp, specific application operations are likely causing the CPU spike.

3. If comparing CPU patterns across similar instances (from Playbook step 6) shows the issue is isolated to one instance, the root cause is instance-specific (runaway process, malware, or local configuration). If multiple instances are affected, the cause is workload-related.

4. If CloudWatch metrics (from Playbook step 2) show sudden CPU spike rather than gradual increase, correlate with I/O metrics (from Playbook step 8). If NetworkIn/Out or DiskReadOps spiked simultaneously, increased I/O workload is driving CPU usage.

5. If the instance is a burstable type (T-series) and CloudWatch shows CPU trending down after sustained high usage, check CPU credit balance. Credit exhaustion causes performance throttling that appears as high CPU wait time.

6. If Auto Scaling Group (from Playbook step 7) shows scaling activity around the alarm time but new instances also show high CPU, the workload exceeds current capacity and requires either more instances or larger instance types.

7. If system logs (from Playbook step 9) show resource contention or background process errors, system-level processes are competing with application workloads for CPU resources.

If no correlation is found: extend analysis to 4 hours, review process-level CPU metrics, check for memory pressure causing CPU thrashing, verify EBS volume IOPS limits affecting CPU wait time, and examine database query performance for external bottlenecks.
