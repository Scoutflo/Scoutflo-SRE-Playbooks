---
title: Certificate Expiring Critical
weight: 45
categories: [kubernetes, cert-manager]
---

# CertificateExpiringCritical

## Meaning

Certificate is critically close to expiration (triggering CertificateExpiringCritical, CertManagerCertExpiryCritical alerts, typically 7 days or less before expiry) because automatic renewal has failed repeatedly and immediate action is required. Certificate will expire very soon causing service outage, and all renewal attempts have failed. This is a critical issue requiring immediate attention; HTTPS services will fail when the certificate expires; customer impact is imminent.

## Impact

CertificateExpiringCritical alerts fire; imminent service outage; HTTPS will fail within days; urgent action required; browsers will block access; API integrations will break; mobile apps will fail; compliance violations imminent; customer-facing outage is near-certain without intervention; business impact is significant.

## Playbook

1. Immediately check certificate expiration date and calculate exact time until expiry.

2. Retrieve Certificate resource status and identify all failure reasons in conditions.

3. Check all CertificateRequest resources for detailed failure information.

4. Verify Issuer or ClusterIssuer can issue certificates by testing with a new certificate.

5. Attempt manual certificate renewal by deleting the Certificate's secret to force re-issuance.

6. If ACME: verify all challenge requirements are met (DNS, HTTP connectivity).

7. Prepare fallback plan: obtain certificate manually from CA if automation cannot be fixed in time.

## Diagnosis

This is a critical alert - prioritize resolution over root cause analysis initially. Get the certificate renewed first, then investigate why automatic renewal failed.

Check if issuer credentials have expired (ACME account, CA credentials, Vault token) preventing any issuance, using issuer status and credential validation as supporting evidence.

Verify network connectivity for ACME challenges has not been disrupted by firewall or infrastructure changes, using connectivity tests and recent infrastructure changes as supporting evidence.

Check for Let's Encrypt rate limits that may be blocking issuance due to previous failed attempts, using ACME server responses and rate limit status as supporting evidence.

Verify DNS configuration for the domain is correct and resolvable, using DNS queries and propagation checks as supporting evidence.

Emergency actions if automated renewal cannot be fixed: manually obtain certificate from Let's Encrypt using certbot or other ACME client, manually obtain certificate from paid CA, temporarily use self-signed certificate with client-side trust (not recommended for public services).
