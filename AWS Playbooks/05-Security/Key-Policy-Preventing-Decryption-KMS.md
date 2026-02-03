# AWS KMS Key Policy Preventing Decryption

## Meaning

KMS key decryption operations fail (triggering decryption errors or KMSAccessDenied exceptions) because KMS key policy blocks access, IAM role or user lacks kms:Decrypt and kms:Encrypt permissions, principal using the key is not listed in key policy, key is disabled, cross-account access is not allowed in resource policy, or key alias points to wrong key. KMS API calls return "AccessDenied" or "InvalidKeyUsageException" errors, CloudWatch Logs show KMS permission errors, and encrypted resources cannot be accessed. This affects the security and encryption layer and blocks data access, typically caused by key policy restrictions, IAM permission issues, key alias misconfiguration, or cross-account access problems; if using multi-region keys, key replication issues may affect decryption and applications may experience encryption-related errors.

## Impact

KMS decryption operations fail; encrypted data cannot be accessed; kms:Decrypt permission errors occur; encryption and decryption operations error; data access is blocked; encrypted resources become inaccessible; KMS key policy errors appear; cross-account access fails; encryption workflows break. Encrypted S3 objects cannot be retrieved; encrypted RDS snapshots cannot be restored; encrypted EBS volumes cannot be attached; applications may experience errors or performance degradation due to encryption failures; if using multi-region keys, cross-region decryption may fail.

## Playbook

1. Verify KMS key `<key-id>` exists and is not scheduled for deletion, and AWS service health for KMS in region `<region>` is normal.
2. Retrieve the KMS Key `<key-id>` key policy and check KMS key policy for access restrictions, verifying principal ARNs and action permissions (kms:Decrypt, kms:Encrypt, kms:ReEncrypt).
3. Retrieve the KMS Key `<key-id>` alias configuration and verify key alias points to correct key ID, checking for alias misconfiguration.
4. Retrieve the IAM role `<role-name>` or user `<user-name>` and ensure IAM role or user has kms:Decrypt and kms:Encrypt permissions in IAM policies, checking for policy evaluation order issues.
5. Retrieve the KMS Key `<key-id>` key policy and verify that the principal using the key is listed in the key policy, checking for principal ARN format mismatches.
6. Retrieve the KMS Key `<key-id>` status and check if the key is enabled, verifying key state is not "Disabled" or "PendingDeletion".
7. Retrieve the KMS Key `<key-id>` resource policy, grants, and key rotation status and check if cross-account access is configured in the resource policy, verify grant-based access permissions and if key rotation affected key policy or key ID, verifying cross-account principal ARNs, trust relationships, grants override key policy restrictions, and rotation-related policy changes.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for KMS API call failures related to key `<key-id>`, including AccessDenied errors.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify KMS service availability in the region. If service health indicates issues, decryption failures may be AWS-side requiring monitoring rather than configuration changes.

2. If key status from Playbook step 6 shows the key is "Disabled" or "PendingDeletion", the key cannot be used for any operations. Re-enable the key or cancel deletion to restore access.

3. If key policy from Playbook step 2 does not include the requesting principal (IAM user, role, or service) in the allowed principals, key access is denied. Verify the principal ARN format matches exactly (account ID, role/user name).

4. If key policy from Playbook step 2 allows access only through specific conditions (e.g., kms:ViaService, kms:CallerAccount) that are not met by the request, conditional access is blocking the operation.

5. If IAM policy from Playbook step 4 does not include kms:Decrypt and kms:Encrypt permissions for the specific key ARN, IAM denies the operation before key policy is evaluated.

6. If key alias from Playbook step 3 points to a different key ID than expected, applications using the alias are accessing the wrong key. Verify alias target matches the intended key.

7. If key policy, grants, and rotation status from Playbook step 7 show cross-account access requirements, verify both the key policy allows the external account AND the external account's IAM policy allows KMS access. For grants, verify grant tokens are being used correctly.

8. If CloudTrail events from Playbook step 8 show specific AccessDenied error codes, the error context indicates whether the denial is from key policy, IAM policy, or VPC endpoint policy.

If no correlation is found from the collected data: extend CloudTrail query timeframes to 1 hour, verify key rotation has not changed the key material unexpectedly, check for VPC endpoint policies restricting KMS access, and examine multi-region key replication status. Decryption failures may result from key policy size limits (32 KB), grant limits, or cross-account STS session policy restrictions.
