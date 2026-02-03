# DynamoDB Streams Not Triggering Lambda

## Meaning

DynamoDB Streams are not triggering Lambda functions (triggering event processing failures or DynamoDBStreamsTriggerFailure alarms) because stream is not enabled on table, Lambda event source mapping is missing or misconfigured, IAM permissions are insufficient, stream view type is incorrect, Lambda function is not subscribed to stream, or DynamoDB stream shard iterator issues prevent event processing. DynamoDB stream events are not processed, Lambda functions are not invoked, and event-driven workflows break. This affects the event processing and serverless layer and blocks real-time processing, typically caused by stream configuration issues, event source mapping problems, or permission failures; if using DynamoDB Streams with multiple Lambda functions, event source mapping may differ and applications may experience trigger failures.

## Impact

DynamoDB stream events are not processed; Lambda functions are not invoked; event-driven workflows break; stream records accumulate; real-time processing fails; Lambda function triggers do not fire; application event processing is interrupted; stream-based integrations fail. DynamoDBStreamsTriggerFailure alarms may fire; if using DynamoDB Streams with multiple Lambda functions, event source mapping may differ; applications may experience errors or performance degradation due to missed events; event-driven workflows may be completely broken.

## Playbook

1. Verify DynamoDB table `<table-name>` exists and AWS service health for DynamoDB and Lambda in region `<region>` is normal.
2. Retrieve the DynamoDB Table `<table-name>` in region `<region>` and inspect its stream specification, stream enabled status, and stream view type configuration, verifying stream is enabled.
3. Retrieve the Lambda Function `<function-name>` that should be triggered by DynamoDB Streams and inspect its event source mappings for table `<table-name>`, verifying event source mapping exists.
4. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for DynamoDB stream event patterns or invocation errors, including invocation error details.
5. Retrieve the IAM role `<role-name>` attached to Lambda function `<function-name>` and inspect its policy permissions for DynamoDB stream read operations, verifying IAM permissions.
6. List DynamoDB stream records for table `<table-name>` and check stream record age and processing status, analyzing stream record backlog.
7. Retrieve CloudWatch metrics for Lambda Function `<function-name>` including Invocations and Errors and verify function invocation patterns, checking if function is being invoked.
8. Retrieve the Lambda Function `<function-name>` event source mapping status and verify event source mapping is enabled, checking if mapping status affects triggers.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB stream or Lambda event source mapping modification events related to table `<table-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs for the Lambda function (from Playbook step 4) to identify specific invocation errors or patterns. If logs show no recent invocations, the event source mapping may be disabled or misconfigured. If logs show "AccessDenied" errors, proceed immediately to IAM permission verification.

2. For access-denied errors, verify IAM role permissions (from Playbook step 5) attached to the Lambda function. The role must have dynamodb:GetRecords, dynamodb:GetShardIterator, dynamodb:DescribeStream, and dynamodb:ListStreams permissions. If any of these permissions are missing, the function cannot read from the stream.

3. Review Lambda function metrics (from Playbook step 7) including Invocations and Errors to determine if the function is being invoked. If Invocations is zero, the event source mapping is not triggering the function. If Errors is high, the function is being invoked but failing.

4. Examine DynamoDB table stream specification (from Playbook step 2) to verify streams are enabled and the stream view type is correctly configured. If streams are disabled or the stream view type does not include the data the function expects, triggers will not work properly.

5. Verify Lambda event source mapping status (from Playbook steps 3 and 8) to confirm the mapping exists, is enabled, and has the correct stream ARN. If event source mapping is disabled or references the wrong stream, triggers will not occur.

6. Review stream record backlog (from Playbook step 6) to identify if records are accumulating without being processed. If records are backing up, the Lambda function may be throttled, timing out, or experiencing errors that prevent successful processing.

7. Correlate CloudTrail events (from Playbook step 9) with trigger failure timestamps within 5 minutes to identify any DynamoDB stream or Lambda event source mapping modifications. If configuration changes coincide with when triggers stopped working, those changes are the likely cause.

8. Compare trigger failure patterns across different Lambda functions subscribed to the same stream. If failures are function-specific, focus on that function's permissions and event source mapping. If failures affect all functions, the stream configuration itself is the issue.

9. Check for Lambda concurrency limits that may prevent function invocations. If the account or function concurrency limit is reached, new invocations are throttled and stream records accumulate.

If no correlation is found within the specified time windows: extend timeframes to 48 hours, review alternative evidence sources including stream record age and Lambda function concurrency limits, check for gradual issues like event source mapping status changes or stream view type mismatches, verify external dependencies like Lambda function availability or stream service health, examine historical patterns of stream trigger failures, check for DynamoDB stream shard iterator expiration, verify Lambda event source mapping batch size configuration. Stream trigger failures may result from event source mapping status issues, Lambda function concurrency exhaustion, stream view type configuration problems, DynamoDB stream shard iterator expiration, or Lambda event source mapping batch size configuration rather than immediate stream configuration changes.
