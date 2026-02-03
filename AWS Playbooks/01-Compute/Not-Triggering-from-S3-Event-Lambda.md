# AWS Lambda Not Triggering from S3 Event

## Meaning

Lambda functions fail to trigger from S3 events (triggering event notification failures or LambdaInvocationFailed alarms) because S3 event notifications are not enabled, Lambda function execution role lacks correct permissions, Lambda function permission policy does not allow S3 to invoke it, S3 event notification configuration is incorrect, S3 event notification filters exclude events, or Lambda logs show invocation failures. Lambda functions do not execute on S3 events, S3 event processing fails, and CloudWatch Logs show no invocation records. This affects the event-driven architecture and blocks automated workflows, typically caused by S3 event notification configuration issues, Lambda permission problems, or event filter misconfiguration; if using S3 versioned buckets or encrypted objects, event behavior may differ and applications may experience event processing failures.

## Impact

Lambda functions do not execute on S3 events; S3 event processing fails; event notifications are not delivered; Lambda invocation errors occur; automated workflows break; file processing pipelines fail; S3 to Lambda integrations fail; event-driven architectures malfunction; data processing is delayed. LambdaInvocationFailed alarms fire; if using S3 versioned buckets, event notifications may behave differently; applications may experience errors or performance degradation due to missing event processing; if using encrypted objects, KMS permission issues may block event delivery.

## Playbook

1. Verify S3 bucket `<bucket-name>` and Lambda function `<function-name>` exist, and AWS service health for S3 and Lambda in region `<region>` is normal.
2. Retrieve the S3 Bucket `<bucket-name>` event notification configuration and verify S3 event notifications are enabled and correctly configured, checking notification destination type (Lambda vs SQS vs SNS).
3. Retrieve the S3 Bucket `<bucket-name>` event notification filters and verify event notification filters (prefix/suffix) are not excluding events, checking filter configuration.
4. Retrieve the IAM role `<role-name>` for Lambda function and check if Lambda function has correct execution role including AWSLambdaS3ExecutionRole, verifying execution role permissions.
5. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for invocation errors, S3 event processing failures, or permission denied errors, including event payload analysis.
6. Retrieve the Lambda Function `<function-name>` permission policy and ensure Lambda function's permission policy allows S3 to invoke it, verifying resource-based policy configuration.
7. Retrieve the S3 Bucket `<bucket-name>` versioning and encryption configuration and verify if bucket versioning or object encryption affects event notification behavior, checking versioned bucket event patterns and KMS key permissions for event delivery.
8. Retrieve the Lambda Function `<function-name>` reserved concurrency settings and S3 Bucket `<bucket-name>` event notification destination configuration and verify reserved concurrency is not preventing invocations and destination ARN matches Lambda function ARN, checking concurrency limits and ARN mismatches.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify S3 and Lambda service availability in the region. If service health indicates issues, event triggering failures may be AWS-side requiring monitoring rather than configuration changes.

2. If S3 event notification configuration from Playbook step 2 shows no event notifications configured or wrong destination type (SQS/SNS instead of Lambda), events are not being sent to Lambda. Verify event types (s3:ObjectCreated:*, s3:ObjectRemoved:*) match expected operations.

3. If event notification filters from Playbook step 3 specify prefix or suffix patterns that do not match uploaded objects, events are filtered out. Verify filter patterns (e.g., prefix: "uploads/", suffix: ".jpg") match the objects triggering events.

4. If Lambda execution role from Playbook step 4 lacks permissions referenced in the function code (e.g., s3:GetObject to read the triggering object), function execution fails after invocation. This is different from invocation permission issues.

5. If CloudWatch Logs from Playbook step 5 show no invocation records during the expected time window, Lambda is not being invoked. If logs show errors after invocation, the function is being called but failing during execution.

6. If Lambda resource-based policy from Playbook step 6 does not allow s3.amazonaws.com to invoke the function for the specific bucket, S3 cannot trigger Lambda. Verify the policy includes the source bucket ARN.

7. If versioning or encryption configuration from Playbook step 7 shows the bucket uses versioning, verify event notifications include version-specific events. For KMS-encrypted buckets, verify Lambda role has kms:Decrypt permissions.

8. If reserved concurrency from Playbook step 8 is set to 0 or function is throttled, invocations are rejected. If destination ARN does not match the Lambda function ARN exactly, events are sent to the wrong destination.

If no correlation is found from the collected data: extend CloudWatch Logs query timeframes to 30 minutes, verify S3 bucket owner and Lambda function are in the same account (cross-account requires additional configuration), check for SQS dead-letter queue messages indicating failed deliveries, and examine Lambda concurrency metrics. Invocation failures may result from S3 replication delays, multipart upload completion event timing, or Lambda cold start failures.

