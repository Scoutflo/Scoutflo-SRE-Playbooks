# CodePipeline Failing Due to S3 Permissions

## Meaning

AWS CodePipeline fails during execution (triggering pipeline execution failures or CodePipelineExecutionFailed alarms) because pipeline execution history shows stage failures, CodeBuild logs show errors, IAM role permissions are insufficient, pipeline role lacks required policies, S3 bucket permissions block pipeline operations, or KMS key policies prevent artifact encryption. Pipeline execution history shows failed stages, CodeBuild logs show permission denied errors, and S3 access logs indicate access failures. This affects the CI/CD layer and blocks deployments, typically caused by IAM permission issues, S3 bucket policy restrictions, KMS key access problems, or cross-account access configuration; if pipelines manage infrastructure, CloudFormation stack deployments may fail and applications may experience deployment delays.

## Impact

CodePipeline executions fail; CI/CD workflows break; pipeline stages cannot complete; CodeBuild errors occur; deployment pipelines fail; application deployments are blocked; pipeline execution history shows failures; build artifacts cannot be stored; release processes are interrupted. CodePipelineExecutionFailed alarms fire; build artifacts cannot be uploaded to S3; deployment stages timeout; if pipelines manage infrastructure, CloudFormation stack deployments fail and infrastructure changes cannot be applied; applications may experience errors or performance degradation due to failed deployments.

## Playbook

1. Verify pipeline `<pipeline-name>` exists and AWS service health for CodePipeline in region `<region>` is normal.
2. Retrieve the CodePipeline `<pipeline-name>` and check execution history to identify the stage causing the issue (Source, Build, Deploy).
3. Query CloudWatch Logs for log groups containing CodeBuild logs and filter for build errors, permission failures, or execution failures, including S3 access denied errors.
4. Retrieve the IAM role `<role-name>` for CodePipeline service role and execution role and verify service role permissions include required policies for Pipeline Role (AWSCodePipelineServiceRole) and execution role has permissions for artifact bucket access and deployment operations.
5. Retrieve the S3 Bucket `<bucket-name>` bucket policy and check S3 bucket permissions for CodePipeline access, verify bucket policy allows pipeline service role and execution role, and verify IAM policy vs bucket policy evaluation order, checking for conflicting Deny statements.
6. Retrieve the KMS Key `<key-id>` key policy if S3 bucket uses encryption and verify KMS key policy allows CodePipeline service role and execution role to use the key for encryption/decryption.
7. Retrieve the CodePipeline `<pipeline-name>` execution status and check current execution state and failed stage details, including artifact location and encryption settings.
8. Verify if pipeline `<pipeline-name>` uses cross-account S3 access by checking bucket policy for cross-account role assumptions and trust relationships.

## Diagnosis

1. Compare CodePipeline execution start timestamps with stage failure timestamps within 30 minutes and verify whether stage failures began during pipeline execution, using CodePipeline execution events as supporting evidence.
2. Correlate IAM role permission change timestamps with pipeline failure timestamps and verify whether permission changes caused pipeline failures, using IAM role configuration data as supporting evidence.
3. Compare S3 bucket policy modification timestamps with pipeline access failure timestamps within 30 minutes and verify whether bucket policy changes blocked pipeline operations, using S3 access events as supporting evidence.
4. Compare KMS key policy modification timestamps with pipeline encryption failure timestamps within 30 minutes and verify whether KMS key policy changes prevented artifact encryption, using KMS access events as supporting evidence.
5. Analyze pipeline failure frequency over the last 1 hour to determine if failures are constant (permission issue) or intermittent (resource availability).

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including CodeBuild build logs and S3 access logs, check for gradual issues like S3 bucket capacity, verify external dependencies like source repository access, examine historical patterns of CodePipeline execution, check for S3 bucket versioning or lifecycle policy conflicts. Pipeline failures may result from source repository connectivity issues, CodeBuild resource constraints, artifact storage problems, S3 bucket notification configuration conflicts, or multi-region pipeline scenarios rather than immediate permission changes.
