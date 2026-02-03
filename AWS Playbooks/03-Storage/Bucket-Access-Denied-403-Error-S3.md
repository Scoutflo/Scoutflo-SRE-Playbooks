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

1. Analyze AWS service health from Playbook step 1 to verify S3 service availability in the region. If service health indicates issues, 403 errors may be AWS-side requiring monitoring rather than configuration changes.

2. If bucket policy from Playbook step 2 contains explicit Deny statements matching the requesting principal, the bucket policy is blocking access. Identify the specific Deny statement and the timestamp of its creation.

3. If IAM policy from Playbook step 2 lacks s3:GetObject or s3:ListBucket permissions for the bucket resource, the identity-based policy is insufficient. Check policy attachment status and permission scope.

4. If public access block configuration from Playbook step 5 shows BlockPublicAccess is enabled, verify whether the access pattern requires public access. Public access blocks override bucket policies allowing public access.

5. If object ownership configuration from Playbook step 6 shows BucketOwnerEnforced, ACL-based access is disabled. Applications relying on ACLs for cross-account access will receive 403 errors.

6. If bucket region from Playbook step 7 differs from the region used in the request, region mismatch causes access failures. S3 requests must target the correct regional endpoint.

7. If SCPs from Playbook step 8 contain S3 Deny statements, organization policies override IAM permissions. Identify the specific SCP blocking access.

8. If encryption configuration from Playbook step 9 shows KMS encryption and the requesting principal lacks kms:Decrypt permissions for the key, encrypted objects cannot be accessed.

9. If CloudFront logs from Playbook step 10 show 403 errors, verify OAI/OAC configuration. Misconfigured origin access settings cause CloudFront to receive 403 from S3.

If no correlation is found from the collected data: extend timeframes to 1 hour, review cross-account access configurations, check for S3 bucket MFA delete requirements, and examine bucket lifecycle policies that may affect object availability. 403 errors may result from VPC endpoint policies, cross-account trust issues, or temporary credential expiration.

