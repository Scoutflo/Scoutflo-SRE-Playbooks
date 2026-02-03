# ECS Logs Not Appearing in CloudWatch

## Meaning

ECS logs are not appearing in CloudWatch (triggering observability gaps or ECSLogsMissing alarms) because CloudWatch log configuration is missing in task definition, IAM task execution role lacks log permissions, log group does not exist, log stream creation fails, CloudWatch Logs service encounters errors, or ECS task log driver configuration is incorrect. ECS task logs are not visible in CloudWatch, observability is compromised, and log-based debugging fails. This affects the monitoring and observability layer and reduces troubleshooting capabilities, typically caused by log configuration issues, permission problems, or log driver errors; if using ECS with Fargate, log configuration may differ and applications may experience log visibility issues.

## Impact

ECS task logs are not visible in CloudWatch; observability is compromised; log-based debugging fails; CloudWatch log streams are missing; application logs are not collected; log-based monitoring is ineffective; troubleshooting capabilities are reduced; log retention policies cannot be applied. ECSLogsMissing alarms may fire; if using ECS with Fargate, log configuration may differ; applications may experience errors or performance degradation due to reduced observability; troubleshooting is significantly impaired.

## Playbook

1. Verify ECS cluster `<cluster-name>` and task definition `<task-definition-arn>` exist, and AWS service health for ECS and CloudWatch Logs in region `<region>` is normal.
2. Retrieve the ECS Task Definition `<task-definition-arn>` and inspect its log configuration, CloudWatch log group settings, and log driver configuration, verifying log driver is configured.
3. Retrieve the IAM role `<role-name>` used for ECS task execution and inspect its policy permissions for CloudWatch Logs operations including CreateLogGroup, CreateLogStream, and PutLogEvents, verifying IAM permissions.
4. Query CloudWatch Logs for log groups matching ECS task log group patterns and check if log groups exist and are accessible, verifying log group existence.
5. Retrieve CloudWatch metrics for CloudWatch Logs including IncomingLogEvents over the last 1 hour to identify log ingestion patterns, analyzing log ingestion.
6. List ECS tasks in cluster `<cluster-name>` with task definition `<task-definition-arn>` and check task log configuration and log stream status, verifying log stream creation.
7. Retrieve the ECS Task Definition `<task-definition-arn>` container definitions and verify each container has log configuration, checking container-level log settings.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudWatch Logs log group creation or IAM role policy modification events related to task execution role `<role-name>` within the last 24 hours, checking for configuration changes.
9. Retrieve CloudWatch metrics for CloudWatch Logs including BytesIngested and verify log group quota limits, checking if quota limits prevent log ingestion.

## Diagnosis

1. Analyze CloudWatch Logs ingestion metrics (from Playbook step 5) to verify if logs are being received by CloudWatch. If IncomingLogEvents metric shows zero for the expected log group, logs are not being sent from the ECS tasks. If metrics show log ingestion but logs are not visible, check log group permissions or retention settings.

2. Verify IAM task execution role permissions (from Playbook step 3) to ensure the role has logs:CreateLogGroup, logs:CreateLogStream, and logs:PutLogEvents permissions. If any of these permissions are missing, the task cannot create log streams or send log data. This is the most common cause of missing ECS logs.

3. Review ECS task definition log configuration (from Playbook steps 2 and 7) to verify the awslogs driver is properly configured with correct log group name, region, and stream prefix. If log driver configuration is missing or has incorrect values, logs will not be sent to CloudWatch.

4. Verify CloudWatch log group existence (from Playbook step 4) to confirm the log group specified in the task definition exists. If logConfiguration.options.awslogs-create-group is not set to "true" and the log group does not exist, the task cannot create logs. Either create the log group manually or enable auto-creation.

5. Check CloudWatch Logs quota limits (from Playbook step 9) to verify the account has not exceeded log group or log ingestion limits. If quota limits are reached, new log streams or log events may be rejected.

6. Correlate CloudTrail events (from Playbook step 8) with log absence timestamps within 5 minutes to identify any IAM role policy modifications or log group changes. If permission changes coincide with when logs stopped appearing, those changes are the likely cause.

7. Compare log absence patterns across different task definitions within 1 hour. If log absence is task definition-specific, verify that task's log configuration. If log absence is cluster-wide affecting all tasks, IAM task execution role permissions are the root cause.

8. For Fargate tasks, verify the task definition specifies the awslogs log driver correctly, as Fargate has specific log driver requirements and does not support all log driver options available on EC2.

If no correlation is found within the specified time windows: extend timeframes to 48 hours, review alternative evidence sources including task execution role permissions and log driver configuration, check for gradual issues like IAM permission drift or log group retention policy changes, verify external dependencies like CloudWatch Logs service availability or log group quota limits, examine historical patterns of log absence, check for ECS Fargate log driver configuration differences, verify ECS task log group naming conventions. Log absence may result from log group quota limits, log driver configuration errors, CloudWatch Logs service issues, ECS Fargate log driver configuration differences, or ECS task log group naming convention mismatches rather than immediate task definition changes.
