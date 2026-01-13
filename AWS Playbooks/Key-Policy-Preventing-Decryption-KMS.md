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

1. Compare KMS key policy modification timestamps with decryption failure timestamps within 5 minutes and verify whether decryption failures began after key policy changes, using KMS key policy configuration data as supporting evidence.
2. Correlate IAM permission change timestamps with KMS operation failure timestamps and verify whether permission changes caused decryption failures, using IAM permission configuration data as supporting evidence.
3. Compare key policy principal modification timestamps with access denial timestamps within 5 minutes and verify whether principal removal blocked key access, using KMS key policy events as supporting evidence.
4. Compare key alias modification timestamps with decryption failure timestamps within 5 minutes and verify whether alias changes pointed to wrong key, using KMS alias configuration events as supporting evidence.
5. Analyze decryption failure frequency over the last 15 minutes to determine if failures are constant (policy configuration issue) or intermittent (key availability).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including CloudWatch Logs containing KMS events, check for gradual issues like key rotation, verify external dependencies like cross-account trust relationships, examine historical patterns of KMS key access, check for multi-region key replication issues. Decryption failures may result from key rotation issues, cross-account policy conflicts, key alias configuration problems, key policy size limits, or multi-region key replication delays rather than immediate key policy changes.
