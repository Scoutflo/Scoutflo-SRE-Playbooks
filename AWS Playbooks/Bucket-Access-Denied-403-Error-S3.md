# S3 Bucket Access Denied (403 Error)

## Meaning

S3 bucket access requests return 403 Forbidden errors (triggering access denied events or S3BucketAccessDenied alarms) because bucket policies contain Deny statements, IAM user or role permissions are insufficient, bucket public access settings block access, incorrect AWS region is used, resource-based policies conflict with identity-based policies, S3 object ownership settings restrict access, or AWS Organizations SCPs override permissions. S3 object retrieval fails, applications cannot access stored data, and CloudWatch Logs show 403 errors. This affects the storage and access control layer and blocks data access, typically caused by policy configuration issues, public access block settings, or SCP restrictions; if using S3 with CloudFront, OAI/OAC configuration may affect access and applications may experience data access failures.

## Impact

S3 object retrieval fails; applications cannot access stored data; file uploads are blocked; bucket operations fail; 403 Forbidden errors appear in application logs; access denied events occur; data access is completely blocked; user-facing features fail; backup and restore operations cannot complete. S3BucketAccessDenied alarms fire; if using S3 with CloudFront, OAI/OAC configuration may affect access; applications may experience errors or performance degradation due to data access failures; service-to-service data access may be blocked.

## Playbook

1. Verify S3 bucket `<bucket-name>` and IAM user `<user-name>` or role `<role-name>` exist, and AWS service health for S3 in region `<region>` is normal.
2. Retrieve the S3 Bucket `<bucket-name>` bucket policy and IAM policy `<policy-name>` attached to user `<user-name>` or role `<role-name>` and inspect bucket policy for Deny statements, verify IAM policy has s3:GetObject and s3:ListBucket permissions, and verify IAM policy vs bucket policy evaluation order, checking policy evaluation order and which policy takes precedence.
5. Retrieve the S3 Bucket `<bucket-name>` public access block configuration and verify public access settings, checking public access block settings.
6. Retrieve the S3 Bucket `<bucket-name>` object ownership configuration and verify object ownership settings (BucketOwnerEnforced vs BucketOwnerPreferred), checking ownership restrictions.
7. Verify the correct AWS region `<region>` is being used for bucket `<bucket-name>` by retrieving bucket region configuration, checking region mismatch.
8. Retrieve the AWS Organizations service control policies (SCPs) if using Organizations and verify SCPs are not overriding S3 access permissions, checking SCP restrictions.
9. Retrieve the S3 Bucket `<bucket-name>` encryption configuration and verify KMS key permissions if using encryption, checking KMS key access.
10. Query CloudWatch Logs for log groups containing CloudFront logs if using CloudFront and filter for 403 errors related to S3 bucket `<bucket-name>`, checking CloudFront origin access logs.

## Diagnosis

1. Compare bucket policy modification timestamps with 403 error timestamps within 5 minutes and verify whether access denials began shortly after bucket policy changes, using bucket policy configuration data as supporting evidence.
2. Correlate IAM policy modification timestamps with access denied event timestamps and verify whether 403 errors occurred after IAM policy changes, using IAM policy configuration data as supporting evidence.
3. Compare public access block configuration change timestamps with access failure timestamps within 5 minutes and verify whether access failures began after public access settings changed, using S3 configuration events as supporting evidence.
4. Correlate AWS Organizations SCP modification timestamps with access failure timestamps and verify whether SCP changes blocked S3 access, using SCP configuration events as supporting evidence.
5. Analyze 403 error frequency over the last 15 minutes to determine if errors are constant (policy configuration issue) or intermittent (temporary permission changes).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including service control policies and resource-based policies, check for gradual issues like policy drift, verify external dependencies like cross-account access configurations, examine historical patterns of S3 access, check for S3 bucket encryption KMS key access issues, verify S3 bucket lifecycle policy conflicts. 403 errors may result from service control policies, cross-account access restrictions, bucket-level encryption requirements, S3 bucket MFA delete requirements, or CloudFront OAI/OAC misconfiguration rather than immediate policy changes.

