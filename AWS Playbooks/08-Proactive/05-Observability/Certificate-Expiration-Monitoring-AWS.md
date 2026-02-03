# Certificate Expiration Monitoring

## Meaning

Certificate expiration monitoring indicates that SSL/TLS certificates are approaching expiration or have expired, potentially causing service disruptions (triggering alarms like CertificateExpiring or CertificateExpired) because certificate expiration dates are within warning thresholds, certificates have expired, certificate renewal has not occurred, certificate status shows expiration warnings, or certificate monitoring indicates upcoming expirations. Certificates show expiration dates within warning windows, certificate status indicates expiration, certificate renewal status shows failures, and certificate monitoring alerts fire for upcoming expirations. This affects the security layer and service availability, typically caused by certificate lifecycle management failures, certificate renewal automation issues, or certificate monitoring misconfigurations; if certificates protect container workloads, container ingress certificates may expire and applications may experience TLS connection failures.

## Impact

CertificateExpiring alarms fire; CertificateExpired alarms fire; SSL/TLS connections may fail; services may become unavailable; certificate renewal has not occurred; certificate lifecycle management fails. Certificate expiration dates are within warning thresholds; if certificates protect container workloads, container ingress certificates may expire, pod TLS connections may fail, and container applications may experience TLS connection failures; applications may experience service unavailability or TLS handshake failures.

## Playbook

1. List ACM certificates in region `<region>` and retrieve certificate expiration dates and status to identify certificates expiring within 30 days.
2. Retrieve the ACM Certificate `<certificate-arn>` details and inspect its expiration date, status, and renewal configuration, verifying certificate validity.
3. List Application Load Balancer certificates in region `<region>` and retrieve certificate expiration dates to identify load balancer certificates approaching expiration.
4. Query CloudWatch Logs for log groups containing ACM or certificate events and filter for expiration warnings or certificate renewal failures within the last 7 days.
5. Retrieve CloudWatch metrics for ACM service including CertificateExpirationTime and CertificateStatus over the last 30 days to identify certificates approaching expiration.
6. List CloudFront distributions in region `<region>` and retrieve distribution certificate configurations to identify CloudFront certificates approaching expiration.
7. Compare certificate expiration dates with current date and verify whether certificates are within expiration warning windows, using ACM certificate data as supporting evidence.
8. Retrieve the ACM Certificate `<certificate-arn>` renewal status and verify whether automatic renewal is configured and functioning, checking certificate renewal automation.

## Diagnosis

1. **Analyze certificate inventory from Step 1**: If certificates expiring within 30 days are identified, check renewal status from Step 8. If renewal status shows "PENDING_VALIDATION", DNS or email validation is incomplete. If renewal status shows "FAILED", examine the failure reason. If renewal status shows "SUCCESS" but certificate still expiring, a different certificate is in use.

2. **Evaluate certificate usage from Step 3 and Step 6**: If ALB or CloudFront is using a certificate that is expiring, immediate action is required. If multiple resources use the same expiring certificate, impact scope is broader. If resources use different certificates, prioritize by expiration date.

3. **Review renewal configuration from Step 8**: If automatic renewal is not enabled, enable it for domain-validated certificates. If automatic renewal is enabled but failing, DNS validation records may have been removed or domain ownership verification is failing.

4. **Cross-reference with CloudWatch metrics from Step 5**: If CertificateExpirationTime metrics are missing, certificate monitoring is not configured. If metrics show certificates consistently reaching warning thresholds, renewal automation is not working proactively.

5. **Check renewal failure patterns from Step 4**: If logs show "validation failed" errors, verify DNS CNAME records for ACM validation still exist. If logs show "rate limit" errors, too many renewal attempts have occurred. If no renewal attempts logged, automatic renewal trigger is misconfigured.

If the above analysis is inconclusive: Manually trigger certificate renewal to test the renewal process. Verify domain ownership in Route 53 or external DNS. Check if certificates are imported (not managed by ACM) which require manual renewal. Review certificate association with resources to ensure correct certificate is attached.
