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

1. Compare S3 event notification configuration change timestamps with Lambda invocation failure timestamps within 5 minutes and verify whether invocation failures began after event notification changes, using S3 configuration events as supporting evidence.
2. Correlate Lambda execution role modification timestamps with invocation failure timestamps and verify whether role changes prevented S3 event processing, using Lambda execution role configuration data as supporting evidence.
3. Compare Lambda permission policy modification timestamps with S3 invocation failure timestamps within 5 minutes and verify whether permission changes blocked S3 invocations, using Lambda permission events as supporting evidence.
4. Compare S3 event notification filter modification timestamps with invocation failure timestamps within 5 minutes and verify whether filter changes excluded events, using S3 event notification configuration events as supporting evidence.
5. Analyze invocation failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (event delivery delays).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including S3 access logs and Lambda invocation metrics, check for gradual issues like event notification delivery delays, verify external dependencies like S3 bucket configuration, examine historical patterns of S3 to Lambda event delivery, check for S3 multipart upload event behavior, verify S3 event notification queue (SQS) configuration. Invocation failures may result from S3 event notification delivery delays, Lambda function concurrency limits, S3 bucket configuration issues, S3 versioned bucket event patterns, or S3 encrypted object KMS permission issues rather than immediate permission changes.
