# SSL Certificate Not Working on ELB

## Meaning

SSL certificate is not working on Elastic Load Balancer (triggering SSL/TLS errors or ELBCertificateFailure alarms) because certificate is expired or invalid, certificate is not attached to listener, certificate ARN is incorrect, certificate domain does not match listener domain, certificate status is not active, or load balancer listener SSL policy configuration is incompatible with certificate. HTTPS connections fail, SSL/TLS handshake errors occur, and secure connections cannot be established. This affects the security and load balancing layer and blocks secure traffic, typically caused by certificate configuration issues, expiration problems, or SSL policy incompatibilities; if using Application Load Balancer vs Classic Load Balancer, certificate configuration may differ and applications may experience SSL connection failures.

## Impact

HTTPS connections fail; SSL/TLS handshake errors occur; secure connections cannot be established; certificate validation errors appear; user-facing SSL errors increase; application security is compromised; load balancer cannot serve HTTPS traffic; SSL certificate alarms fire. ELBCertificateFailure alarms may fire; if using Application Load Balancer vs Classic Load Balancer, certificate configuration may differ; applications may experience errors or performance degradation due to failed HTTPS connections; secure user access may be completely blocked.

## Playbook

1. Verify load balancer `<load-balancer-arn>` exists and AWS service health for ELB in region `<region>` is normal.
2. Retrieve the Load Balancer `<load-balancer-arn>` in region `<region>` and inspect its listener configurations, SSL certificate attachments, and certificate ARNs, verifying certificate attachments.
3. Retrieve the ACM Certificate `<certificate-arn>` attached to Load Balancer `<load-balancer-arn>` and inspect its status, domain validation, expiration date, and certificate chain, verifying certificate is active.
4. Query CloudWatch Logs for log groups containing load balancer access logs and filter for SSL/TLS error patterns or certificate validation failures, including error message details.
5. Retrieve CloudWatch metrics for Load Balancer `<load-balancer-arn>` including HTTPCode_Target_4XX_Count and HTTPCode_Target_5XX_Count over the last 1 hour to identify SSL-related error patterns, analyzing error frequency.
6. List ACM certificates in region `<region>` and check certificate status, expiration dates, and domain validation for certificates associated with the load balancer, verifying certificate validity.
7. Retrieve the Load Balancer `<load-balancer-arn>` listener SSL policy configuration and verify SSL policy compatibility with certificate, checking SSL policy settings.
8. Retrieve the Load Balancer `<load-balancer-arn>` listener protocol configuration and verify HTTPS listener is configured correctly, checking listener configuration.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for load balancer listener or certificate attachment modification events related to `<load-balancer-arn>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for load balancer errors (from Playbook step 5) including HTTPCode_Target_4XX_Count and HTTPCode_Target_5XX_Count to identify SSL-related error patterns. If errors suddenly increased, correlate the timestamp with certificate or listener configuration changes. If errors are constant, the certificate configuration is likely persistently incorrect.

2. Review ACM certificate status (from Playbook step 3) to verify the certificate is active and not expired. If certificate status shows "Expired", the certificate needs renewal. If status shows "Pending validation", domain validation has not completed and the certificate cannot be used.

3. Examine CloudWatch Logs containing load balancer access logs (from Playbook step 4) to identify specific SSL/TLS error patterns. If logs show handshake failures, the SSL policy may be incompatible with client requirements. If logs show certificate validation errors, the certificate chain may be incomplete.

4. Verify load balancer listener configuration (from Playbook step 2) to confirm the certificate is correctly attached to HTTPS listeners. If certificate ARN is missing, incorrect, or the certificate does not cover the domain being accessed, SSL connections fail.

5. Check SSL policy configuration (from Playbook step 7) to verify the policy supports the required TLS versions and cipher suites. If the SSL policy is too restrictive, older clients may fail to connect. If the policy is too permissive for security requirements, consider updating it.

6. Review certificate domain names (from Playbook step 3) to verify the certificate covers all domains being served by the load balancer. If users access a domain not included in the certificate's Subject Alternative Names (SANs), browsers display certificate errors.

7. Correlate CloudTrail events (from Playbook step 9) with SSL error timestamps within 5 minutes to identify any listener modifications or certificate attachments. If configuration changes coincide with when SSL errors started, those changes are the likely cause.

8. Compare SSL error patterns across different listeners on the same load balancer within 1 hour. If errors are listener-specific, verify that listener's certificate attachment. If errors affect all HTTPS listeners, the certificate itself is problematic.

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including certificate chain validation and intermediate certificate status, check for gradual issues like certificate expiration approaching or domain validation expiring, verify external dependencies like certificate authority service availability, examine historical patterns of SSL certificate issues, check for load balancer SSL policy incompatibility, verify load balancer listener certificate association issues. SSL certificate issues may result from certificate chain problems, intermediate certificate expiration, domain validation failures, load balancer SSL policy incompatibility, or load balancer listener certificate association issues rather than immediate certificate attachment changes.
