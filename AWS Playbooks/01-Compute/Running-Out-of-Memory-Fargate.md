# Fargate Task Running Out of Memory

## Meaning

Fargate task is running out of memory (triggering out-of-memory errors or FargateMemoryExhaustion alarms) because task memory allocation is insufficient, memory leaks cause gradual memory growth, task processes large datasets exceeding memory, concurrent task executions exhaust available memory, or Fargate task memory configuration is too low. Fargate tasks fail with out-of-memory errors, task executions are terminated, and container memory limits are exceeded. This affects the container orchestration layer and blocks task execution, typically caused by memory allocation issues, memory leaks, or data processing requirements; if using Fargate with ECS, memory configuration options may differ and applications may experience task execution failures.

## Impact

Fargate tasks fail with out-of-memory errors; task executions are terminated; application workflows break; task memory errors increase; FargateMemoryExhaustion alarms fire; retry attempts fail; tasks cannot complete processing; service reliability degrades; container memory limits are exceeded. Fargate task memory errors appear in CloudWatch Logs; if using Fargate with ECS, memory behavior may differ; applications may experience errors or performance degradation due to incomplete task execution; container workloads cannot complete processing.

## Playbook

1. Verify ECS cluster `<cluster-name>` and task `<task-id>` exist, and AWS service health for ECS in region `<region>` is normal.
2. Retrieve CloudWatch metrics for ECS Task `<task-id>` in cluster `<cluster-name>` including MemoryUtilization over the last 1 hour to identify memory usage patterns, analyzing memory trend.
3. Retrieve the ECS Task Definition `<task-definition-arn>` for task `<task-id>` and inspect its memory configuration, container memory limits, and task memory allocation, verifying memory settings.
4. Query CloudWatch Logs for log group `/aws/ecs/<cluster-name>/<task-id>` and filter for out-of-memory error patterns, memory-related exceptions, or task termination errors, including memory error messages.
5. Retrieve CloudWatch alarms associated with ECS Task `<task-id>` with metric MemoryUtilization and check for alarms in ALARM state, verifying alarm configurations.
6. Retrieve the ECS Task Definition `<task-definition-arn>` Fargate configuration and verify Fargate memory limits, checking Fargate-specific memory constraints.
7. List ECS tasks in cluster `<cluster-name>` with the same task definition and compare memory utilization patterns to determine if the issue is task-specific, analyzing memory usage across tasks.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for ECS task definition modification events related to `<task-definition-arn>` within the last 24 hours, checking for memory configuration changes.
9. Retrieve CloudWatch metrics for ECS Task `<task-id>` including CPUUtilization to verify correlation with memory usage, checking if CPU and memory are both constrained.

## Diagnosis

1. Analyze CloudWatch metrics for ECS task memory utilization (from Playbook step 2) over the last hour to identify memory usage patterns. If memory utilization consistently reaches 100% before task termination, the memory allocation is insufficient for the workload. If memory gradually increases over time, there may be a memory leak.

2. Review CloudWatch Logs for ECS task (from Playbook step 4) to identify out-of-memory error messages and the circumstances leading to termination. If logs show "OutOfMemoryError" or container was killed with exit code 137, the task exhausted its memory allocation.

3. Examine ECS task definition memory configuration (from Playbook step 3) to verify memory limits and reservations. If task memory is set too low for the workload requirements, increase the memory allocation. Verify both hard limits (memory) and soft limits (memoryReservation) are appropriate.

4. Review Fargate-specific memory configuration (from Playbook step 6) to ensure the task uses a valid Fargate CPU and memory combination. Fargate has specific CPU/memory combinations; if an invalid combination is specified, task deployment may fail.

5. Correlate CloudTrail events (from Playbook step 8) with memory error timestamps within 30 minutes to identify any task definition modifications. If memory configuration was recently reduced, that change may have caused the out-of-memory errors.

6. Compare memory utilization patterns with task duration. If memory grows linearly over task lifetime (from Playbook step 2), there may be a memory leak in the application code. If memory spikes during specific operations, those operations may process large datasets.

7. Compare memory utilization across tasks using the same task definition (from Playbook step 7). If all tasks experience memory exhaustion, the memory allocation needs to increase. If only some tasks fail, the issue may be related to specific input data or processing patterns.

8. Review CPU utilization alongside memory (from Playbook step 9) to understand overall resource constraints. If both CPU and memory are constrained, consider increasing both. If only memory is constrained, focus on memory allocation or application optimization.

9. Analyze memory trend over the last 4 hours. If memory issues are constant from task start, the base memory allocation is insufficient. If memory issues develop gradually, focus on memory leaks or growing data processing requirements.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including task execution logs and container memory profiling data, check for gradual issues like memory leaks or dataset size growth, verify external dependencies like input data size or container image memory footprint, examine historical patterns of memory utilization, check for Fargate task memory to CPU ratio constraints, verify Fargate ephemeral storage affecting memory. Memory limit issues may result from insufficient memory allocation, memory leaks in task code, large input datasets, Fargate task memory to CPU ratio constraints, or Fargate ephemeral storage constraints rather than immediate task definition changes.
