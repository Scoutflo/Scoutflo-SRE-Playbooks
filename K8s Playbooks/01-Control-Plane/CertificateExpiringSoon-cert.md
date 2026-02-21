---
title: Certificate Expiring Soon
weight: 41
categories: [kubernetes, cert-manager]
---

# CertificateExpiringSoon

## Meaning

Certificate is approaching expiration (triggering CertificateExpiringSoon, CertManagerCertExpirySoon alerts, typically 30 days or less before expiry) because automatic renewal has not occurred and the certificate will expire soon. Certificate resource shows upcoming expiration date, renewal may be failing silently, and services will fail when the certificate expires. This affects all services using this certificate; proactive renewal is needed to prevent outage; HTTPS will fail after expiration.

## Impact

CertificateExpiringSoon alerts fire; warning of impending outage; if not resolved, HTTPS will fail at expiration; browsers will block access; API connections will fail; mobile apps will reject certificates; mTLS will break; ingress will serve invalid certificates; compliance violations will occur; customer-facing services will be impacted.

## Playbook

1. Retrieve the Certificate `<certificate-name>` in namespace `<namespace>` and verify expiration date and renewal status.

2. Check the renewBefore setting and calculate when cert-manager should have attempted renewal.

3. Retrieve CertificateRequest resources to see if renewal requests are being created and their status.

4. Verify the Issuer or ClusterIssuer is still functioning and can issue new certificates.

5. Check cert-manager controller logs for renewal attempt failures.

6. Verify DNS and ingress configuration still allows ACME challenges if using Let's Encrypt.

7. Manually trigger renewal by deleting the Certificate's Secret if automatic renewal is stuck.

## Diagnosis

Compare current time with renewBefore threshold and verify whether cert-manager should have renewed already, using certificate spec and current timestamp as supporting evidence.

Check for failed CertificateRequest resources that indicate renewal was attempted but failed, using CertificateRequest status and events as supporting evidence.

Verify Issuer configuration has not changed and credentials are still valid (API keys, service account permissions), using Issuer status and credential validity as supporting evidence.

Check for network changes that may block ACME validation (firewall rules, ingress changes, DNS changes), using connectivity tests and configuration history as supporting evidence.

Analyze cert-manager controller logs for any errors during renewal process, using log analysis and error patterns as supporting evidence.

If no correlation is found within the specified time windows: manually delete the secret to trigger re-issuance, verify issuer is working with a test certificate, check for cert-manager webhook issues, consider manually issuing certificate as temporary fix, escalate if issuer is permanently broken.
