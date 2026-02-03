# Log Coverage Analysis

## Meaning

Log coverage analysis indicates that log collection coverage is incomplete or log coverage gaps are detected (triggering alarms like LogCoverageIncomplete or LogCollectionGapDetected) because CloudWatch Logs are not configured for services, log groups are missing, log collection agents are not installed, log coverage analysis tools fail, or log coverage monitoring indicates gaps. Log coverage gaps are detected, CloudWatch Logs are not configured, log groups are missing, and log coverage analysis fails. This affects the observability layer and log monitoring coverage, typically caused by log configuration failures, log collection agent installation issues, log coverage analysis tool failures, or log coverage monitoring gaps; if log coverage affects container workloads, container logs may not be collected and applications may experience log monitoring blind spots.

## Impact

LogCoverageIncomplete alarms fire; LogCollectionGapDetected alarms fire; log collection coverage is incomplete; log coverage gaps are detected; log monitoring may be insufficient; troubleshooting may be difficult. Log coverage gaps are detected; if log coverage affects container workloads, container logs may not be collected, pod logs may be missing, and container applications may experience log monitoring blind spots; applications may experience log coverage gaps or log collection failures.

## Playbook

1. List CloudWatch Logs log groups in region `<region>` and verify log group coverage for services to identify services without log groups, checking log coverage gaps.
2. List EC2 instances in region `<region>` and verify CloudWatch Logs agent installation status and log collection configuration, checking instance-level log coverage.
3. List Lambda functions in region `<region>` and verify CloudWatch Logs configuration and log group association, checking Lambda log coverage.
4. List ECS services in region `<region>` and verify CloudWatch Logs configuration and container log collection settings, checking container log coverage.
5. Query CloudWatch Logs for log groups and verify log stream activity over the last 7 days to identify inactive log groups or log collection failures, checking log collection health.
6. Compare log coverage analysis results with service deployment timestamps and verify whether new services have log groups configured upon deployment, using service configuration data as supporting evidence.
7. Retrieve CloudWatch Logs agent status for EC2 instances in region `<region>` and verify agent health and log collection status, checking log agent coverage.
8. List CloudWatch Logs subscription filters and verify filter coverage for log groups to identify log groups without subscription filters, checking log processing coverage.

## Diagnosis

1. **Analyze log group inventory from Step 1**: If services have no log groups, prioritize log configuration for those services. If log groups exist but are not receiving logs, collection is failing. If log group count is low relative to service count, systematic gaps exist.

2. **Evaluate EC2 log agent status from Step 2 and Step 7**: If CloudWatch agent is not installed, logs cannot be collected. If agent is installed but unhealthy, troubleshoot agent configuration. If agent is healthy but logs are missing, log file paths may be misconfigured.

3. **Review Lambda and ECS logging from Step 3 and Step 4**: If Lambda functions have logging disabled, enable CloudWatch Logs integration. If ECS tasks are not configured for awslogs driver, container logs are lost. If log group permissions are incorrect, logs may fail to write.

4. **Cross-reference with deployments from Step 6**: If newly deployed services lack log groups, deployment automation does not include log configuration. If log configuration fails during deployment, investigate IaC templates.

5. **Assess log activity from Step 5**: If log groups show no activity, logs are not being generated or collected. If activity stopped recently, investigate when and why collection stopped. If activity is intermittent, agent or application issues exist.

If the above analysis is inconclusive: Review log agent configuration files for errors. Check IAM roles for log write permissions. Verify VPC endpoints if logging from private subnets. Consider centralized logging solutions for unified coverage.
