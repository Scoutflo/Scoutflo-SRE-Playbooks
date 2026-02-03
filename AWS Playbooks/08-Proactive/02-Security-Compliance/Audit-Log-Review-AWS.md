# Audit Log Review

## Meaning

Audit log review indicates that audit logs cannot be reviewed or audit log issues are detected (triggering alarms like AuditLogReviewFailed or AuditLogUnavailable) because audit log review tools fail, audit logs are unavailable, audit log analysis indicates problems, audit log configuration is missing, or audit log monitoring detects issues. Audit log reviews show failures, audit logs are unavailable, audit log analysis indicates problems, and audit log review fails. This affects the compliance layer and audit trail management, typically caused by audit log configuration failures, audit log review tool failures, audit log collection issues, or audit log monitoring gaps; if audit log review affects container workloads, container audit logs may be unavailable and applications may experience audit trail gaps.

## Impact

AuditLogReviewFailed alarms fire; AuditLogUnavailable alarms fire; audit logs cannot be reviewed; audit log issues are detected; audit trail management may be compromised; compliance auditing may be limited. Audit log reviews show failures; if audit log review affects container workloads, container audit logs may be unavailable, pod audit trails may be incomplete, and container applications may experience audit trail gaps; applications may experience audit log review gaps or compliance auditing limitations.

## Playbook

1. Query CloudWatch Logs for log groups containing CloudTrail events and verify CloudTrail log group availability and log stream activity over the last 7 days to identify audit log collection issues.
2. Retrieve CloudTrail trail configuration for account `<account-id>` in region `<region>` and verify trail status and log delivery configuration, checking CloudTrail audit log configuration.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for audit log analysis patterns or review failures within the last 7 days.
4. Retrieve CloudWatch metrics for CloudTrail including LogFileDelivery and LogFileValidation over the last 7 days to identify audit log delivery issues.
5. Compare audit log review failure timestamps with CloudTrail log delivery failure timestamps within 1 hour and verify whether delivery failures cause review failures, using CloudTrail trail configuration data as supporting evidence.
6. Retrieve CloudTrail log file integrity validation results and verify log file integrity and validation status, checking audit log integrity.
7. Compare audit log analysis timestamps with CloudTrail event timestamps within 1 hour and verify whether audit log analysis processes events correctly, using CloudWatch Logs containing CloudTrail events as supporting evidence.
8. List Config configuration snapshots and verify snapshot availability for audit log review, checking Config audit log coverage.

## Diagnosis

1. **Analyze CloudTrail trail status from Step 2**: If trail status shows logging disabled, enable CloudTrail logging immediately. If trail is enabled but logs are missing from Step 1, log delivery is failing. If trail configuration is correct but delivery fails, check S3 bucket permissions.

2. **Evaluate log delivery metrics from Step 4**: If LogFileDelivery shows failures, S3 bucket permissions or bucket existence is the issue. If LogFileValidation shows failures, log integrity is compromised. If both metrics are healthy, log delivery is working.

3. **Review log integrity from Step 6**: If log file integrity validation fails, logs may have been tampered with or corrupted. If validation passes, log integrity is maintained. If validation is not enabled, consider enabling for compliance requirements.

4. **Cross-reference with log availability from Step 1**: If CloudTrail log groups exist but are empty, log delivery is configured incorrectly. If log groups have recent activity, collection is working. If activity stopped recently, investigate when logging stopped.

5. **Assess Config snapshots from Step 8**: If Config snapshots are available, configuration audit trail exists. If snapshots are missing, enable Config recording for audit coverage. If snapshots are outdated, verify Config recorder status.

If the above analysis is inconclusive: Verify CloudTrail S3 bucket policy allows log delivery. Check KMS key permissions if using encrypted trails. Review CloudTrail organization trail configuration for multi-account. Consider CloudTrail Lake for enhanced analysis capabilities.
