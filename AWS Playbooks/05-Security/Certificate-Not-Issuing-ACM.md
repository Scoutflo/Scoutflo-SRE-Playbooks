# AWS Certificate Manager (ACM) Certificate Not Issuing

## Meaning

ACM certificate is not issuing (triggering certificate provisioning failures or ACMCertificateIssuanceFailed alarms) because domain validation fails, DNS validation records are incorrect, email validation is not completed, certificate request has errors, certificate authority encounters issues during issuance, or ACM certificate request configuration is invalid. ACM certificates are not issued, SSL/TLS certificates cannot be provisioned, and certificate validation fails. This affects the security and certificate management layer and blocks secure connections, typically caused by validation issues, DNS configuration problems, or request errors; if using ACM with CloudFront or API Gateway, certificate validation requirements may differ and applications may experience certificate provisioning failures.

## Impact

ACM certificates are not issued; SSL/TLS certificates cannot be provisioned; certificate validation fails; domain validation is incomplete; certificate requests remain pending; certificate automation fails; certificate issuance alarms fire; secure connections cannot be established. ACMCertificateIssuanceFailed alarms may fire; if using ACM with CloudFront or API Gateway, certificate validation requirements may differ; applications may experience errors or performance degradation due to missing certificates; secure HTTPS connections cannot be established.

## Playbook

1. Verify ACM certificate `<certificate-arn>` exists and AWS service health for ACM in region `<region>` is normal.
2. Retrieve the ACM Certificate `<certificate-arn>` in region `<region>` and inspect its certificate status, domain validation status, validation method, and certificate request details, verifying validation status.
3. Query CloudWatch Logs for log groups containing ACM events and filter for certificate validation failure events or issuance error patterns related to certificate `<certificate-arn>`, including validation error details.
4. Retrieve CloudWatch metrics for ACM certificate validation including validation attempt patterns over the last 7 days to identify validation issues, analyzing validation attempts.
5. List ACM certificate domain validation records for certificate `<certificate-arn>` and check DNS record configuration or email validation status, verifying validation records.
6. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` if using Route 53 for DNS validation and verify DNS validation records are correctly configured, checking record existence.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for ACM certificate request or validation events related to certificate `<certificate-arn>`, checking request details.
8. Retrieve the ACM Certificate `<certificate-arn>` domain names and verify all domain names in certificate request are valid, checking domain name configuration.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for ACM certificate request modification events related to certificate `<certificate-arn>` within the last 7 days, checking for request changes.

## Diagnosis

1. Analyze ACM certificate status and domain validation status (from Playbook step 2) to identify the current state of certificate issuance. If status shows "Pending validation", the domain validation process has not completed. If status shows "Failed", examine the failure reason for specific guidance.

2. Review ACM certificate domain validation records (from Playbook step 5) to verify DNS or email validation configuration. If using DNS validation, verify CNAME records are correctly configured in the DNS hosted zone. If CNAME records are missing or incorrect, DNS validation cannot complete. If using email validation, verify validation emails were sent to domain contacts.

3. For DNS validation failures, examine Route 53 hosted zone configuration (from Playbook step 6) to verify validation records exist and are correctly formatted. If validation records have incorrect values or are in the wrong hosted zone, update them to match ACM requirements.

4. Analyze CloudWatch Logs containing CloudTrail events (from Playbook steps 7 and 9) to identify certificate request patterns and any API errors. If logs show RequestCertificate API errors, the certificate request itself has issues such as invalid domain names or exceeding domain limits.

5. Correlate certificate issuance failure timestamps with DNS record modification timestamps within 1 hour. If DNS records were recently changed or deleted, those changes may have disrupted ongoing validation. DNS validation requires records to remain in place until validation completes.

6. Compare certificate issuance failure patterns across different domains in the certificate request. If failures are domain-specific, that particular domain's validation is problematic. If all domains fail validation, the overall certificate request configuration may be incorrect.

7. If certificate has been pending for more than 72 hours, the validation process has likely timed out. For DNS validation, verify records are still in place and accessible. For email validation, check if validation emails need to be resent.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including DNS record propagation and email validation delivery, check for gradual issues like DNS record expiration or email validation timeout, verify external dependencies like DNS service availability or email delivery service, examine historical patterns of certificate issuance failures, check for ACM certificate request rate limits, verify ACM certificate domain limit constraints. Certificate issuance failures may result from DNS record propagation delays, email validation delivery issues, certificate authority service problems, ACM certificate request rate limits, or ACM certificate domain limit constraints rather than immediate certificate request changes.
