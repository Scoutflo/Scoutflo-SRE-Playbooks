# Audit Log Review

## Meaning

Audit log review indicates that Kubernetes audit logs cannot be reviewed or audit log issues are detected (triggering alerts like AuditLogReviewFailed or AuditLogUnavailable) because audit log review tools fail, audit logs are unavailable, audit log analysis indicates problems, audit log configuration is missing, or audit log monitoring detects issues. Audit log reviews show failures, audit logs are unavailable, audit log analysis indicates problems, and audit log review fails. This affects the compliance layer and audit trail management, typically caused by audit log configuration failures, audit log review tool failures, audit log collection issues, or audit log monitoring gaps; if audit log review affects container workloads, container audit logs may be unavailable and applications may experience audit trail gaps.

## Impact

AuditLogReviewFailed alerts fire; AuditLogUnavailable alerts fire; audit logs cannot be reviewed; audit log issues are detected; audit trail management may be compromised; compliance auditing may be limited. Audit log reviews show failures; if audit log review affects container workloads, container audit logs may be unavailable, pod audit trails may be incomplete, and container applications may experience audit trail gaps; applications may experience audit log review gaps or compliance auditing limitations.

## Playbook

1. Describe pods in namespace kube-system with label component=kube-apiserver to verify audit log configuration and policy settings.

2. List recent events in namespace kube-system sorted by timestamp to identify any recent issues with audit logging components.

3. Retrieve configmap audit-policy in namespace kube-system with YAML output to verify audit policy status and log delivery configuration.

4. Retrieve logs from audit log review pods with label app=audit-log-reviewer in namespace <namespace> and filter for audit log analysis patterns or review failures.

5. Retrieve Prometheus metrics for audit log service including log_file_delivery and log_file_validation over the last 7 days to identify audit log delivery issues.

6. Retrieve audit log file integrity validation results and verify log file integrity and validation status, checking audit log integrity.

7. Compare audit log analysis timestamps with audit log event timestamps within 1 hour and verify whether audit log analysis processes events correctly, using audit log data as supporting evidence.

8. List audit log snapshots and verify snapshot availability for audit log review, checking audit log coverage.

## Diagnosis

1. Review the API server audit configuration from Steps 1 and 3. If the audit policy is missing or misconfigured, then audit logs are not being generated correctly. Verify audit policy rules cover required operations.

2. Analyze the audit log delivery metrics from Step 5. If log_file_delivery or log_file_validation shows failures, then log transport infrastructure is the issue. If delivery is healthy, proceed to review tool analysis.

3. If Step 6 log integrity validation shows failures, then audit logs may be corrupted or tampered with. This is a critical security concern requiring immediate investigation.

4. Review the audit log review pod logs from Step 4. If logs show analysis patterns or review failures, identify whether failures are due to log format issues, access permissions, or tooling problems.

5. If Step 8 snapshot availability shows gaps, then historical audit coverage is incomplete. Verify that audit log retention and backup policies are correctly configured.

If analysis is inconclusive: Examine events from Step 2 for audit logging component issues. Compare audit log analysis timestamps from Step 7 to verify event processing is functioning. Determine whether review failures affect all audit sources (suggesting infrastructure issues) or specific sources (suggesting source-specific configuration problems).
