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

1. Analyze AWS service health from Playbook step 1 to verify CodePipeline service availability in the region. If service health indicates issues, pipeline failures may be AWS-side requiring monitoring rather than configuration changes.

2. If execution history from Playbook step 2 shows which specific stage failed (Source, Build, Deploy), focus investigation on that stage. Examine the failure reason provided in the execution details for the initial failure timestamp.

3. If CodeBuild logs from Playbook step 3 show "Access Denied" or "AccessDenied" errors for S3 operations, the execution role lacks S3 permissions. Identify the specific S3 action (GetObject, PutObject, ListBucket) that failed.

4. If IAM role policies from Playbook step 4 do not include the required S3 permissions for the artifact bucket, the service role cannot access pipeline artifacts. Verify both the pipeline service role and execution role have appropriate S3 permissions.

5. If S3 bucket policy from Playbook step 5 contains explicit Deny statements or does not Allow the pipeline roles, bucket policy is blocking access. Check for conflicting Deny statements that override IAM permissions.

6. If KMS key policy from Playbook step 6 does not allow the pipeline roles to use kms:Encrypt, kms:Decrypt, and kms:GenerateDataKey, encrypted artifacts cannot be processed. Verify KMS key grants include the execution role.

7. If execution status from Playbook step 7 shows the pipeline is stuck at an artifact location, verify the S3 path exists and encryption settings match between pipeline configuration and bucket.

8. If cross-account configuration from Playbook step 8 shows cross-account S3 access, verify both the bucket policy allows cross-account access AND the assuming role has proper trust relationships.

If no correlation is found from the collected data: extend CodeBuild log query timeframes to 24 hours, verify source repository (CodeCommit, GitHub) connectivity, check for S3 bucket versioning that may affect artifact retrieval, and examine bucket lifecycle policies that may delete artifacts prematurely. Pipeline failures may result from source control webhook issues, CodeBuild timeout settings, or VPC endpoint policies restricting S3 access.
