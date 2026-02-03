# S3 Public Access Block Preventing Access

## Meaning

S3 bucket access is blocked (triggering access denied errors or S3PublicAccessBlocked alarms) because Block Public Access settings prevent public access, bucket ACLs deny public access, bucket policies restrict access, IAM policies do not grant required permissions for bucket operations, or AWS Organizations service control policies override bucket permissions. Public access to S3 buckets is denied, applications cannot access public objects, and 403 Access Denied errors occur. This affects the storage and access control layer and blocks public data access, typically caused by Block Public Access configuration, bucket policy restrictions, or SCP overrides; if using S3 with CloudFront, OAI/OAC configuration may affect access and applications may experience data access failures.

## Impact

Public access to S3 buckets is denied; applications cannot access public objects; bucket policies fail; 403 Access Denied errors occur; public website hosting fails; bucket ACL operations are blocked; cross-account access may be restricted; object retrieval fails for public resources. S3PublicAccessBlocked alarms may fire; if using S3 with CloudFront, OAI/OAC configuration may affect access; applications may experience errors or performance degradation due to blocked public access; public website hosting may fail.

## Playbook

1. Verify S3 bucket `<bucket-name>` exists and AWS service health for S3 in region `<region>` is normal.
2. Retrieve the S3 Bucket `<bucket-name>` in region `<region>` and inspect its Block Public Access settings, public access configuration, and bucket policy, verifying all four Block Public Access settings.
3. Retrieve the S3 Bucket Policy for bucket `<bucket-name>` and inspect policy statements, principal configurations, and action permissions, verifying policy evaluation order.
4. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 access denied events related to bucket `<bucket-name>`, including public access attempt patterns.
5. Retrieve the IAM role `<role-name>` or IAM user `<user-name>` attempting to access bucket `<bucket-name>` and inspect its policy permissions for S3 operations, verifying IAM policy vs bucket policy evaluation.
6. Retrieve the AWS Organizations service control policies (SCPs) if using Organizations and verify SCPs are not overriding S3 public access permissions, checking SCP restrictions.
7. Retrieve the S3 Bucket `<bucket-name>` bucket ACL configuration and verify bucket ACL settings, checking if ACLs restrict public access.
8. Query CloudWatch Logs for log groups containing CloudFront logs if using CloudFront and filter for 403 errors related to S3 bucket `<bucket-name>`, checking CloudFront origin access logs.
9. List S3 bucket access attempts for bucket `<bucket-name>` and check for access denied patterns or permission-related errors, analyzing access attempt patterns.

## Diagnosis

1. Analyze CloudTrail events (from Playbook step 4) to identify when S3 access denied events first appeared. This timestamp establishes when the access block began and serves as the correlation baseline.

2. If bucket Block Public Access settings (from Playbook step 2) show all four settings enabled, and access denials began after these were enabled (check CloudTrail from Playbook step 4), Block Public Access is directly preventing the intended access.

3. If Block Public Access is not the cause, examine bucket policy (from Playbook step 3). Policy statements with Deny effects or missing required Allow statements for the requesting principal cause access denials.

4. If access denial patterns (from Playbook step 4) affect multiple buckets simultaneously, check AWS Organizations SCPs (from Playbook step 6). Account-level or organization-level restrictions may be overriding bucket-level permissions.

5. If IAM policy analysis (from Playbook step 5) shows the requesting role or user lacks s3:GetObject or required permissions, IAM-level restrictions are the root cause rather than bucket configuration.

6. If using CloudFront (from Playbook step 8), verify OAI/OAC configuration. CloudFront 403 errors indicate Origin Access Identity or Origin Access Control misconfiguration preventing CloudFront from accessing S3.

7. If bucket ACL configuration (from Playbook step 7) restricts public access and applications expect public access, the ACL is blocking access. Note that Block Public Access overrides ACL permissions.

If no correlation is found: extend analysis to 2 hours, review VPC endpoint policies if accessing from VPC, check S3 bucket encryption KMS key policies for cross-account access, verify permission boundaries on IAM principals, and examine IAM policy evaluation order.
