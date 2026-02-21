---
title: Certificate Not Ready
weight: 40
categories: [kubernetes, cert-manager]
---

# CertificateNotReady

## Meaning

Certificate resource is not in Ready state (triggering CertificateNotReady, CertManagerCertNotReady alerts) because cert-manager cannot issue or renew the TLS certificate due to configuration issues, issuer problems, or ACME challenges failing. Certificate resource shows Ready=False condition, HTTPS endpoints may be using expired or invalid certificates, and secure connections fail. This affects all services relying on the certificate; HTTPS connections fail; TLS handshakes error; users see certificate warnings; service-to-service mTLS breaks.

## Impact

CertificateNotReady alerts fire; HTTPS endpoints use invalid or expired certificates; browsers show security warnings; API clients reject connections; mobile apps fail to connect; webhook calls fail; mTLS authentication breaks; ingress cannot serve HTTPS; secure communication is compromised; compliance requirements are violated.

## Playbook

1. Retrieve the Certificate `<certificate-name>` in namespace `<namespace>` and check the Ready condition and message.

2. Retrieve events for the Certificate resource to identify specific issuance failures.

3. Check the associated CertificateRequest resource for detailed status and failure reasons.

4. Verify the Issuer or ClusterIssuer referenced by the certificate exists and is in Ready state.

5. For ACME issuers, check the Order and Challenge resources for domain validation status.

6. Verify DNS is correctly configured for HTTP-01 or DNS-01 challenges.

7. Check cert-manager controller logs for detailed error messages.

## Diagnosis

Analyze Certificate status conditions and events to categorize failure type (issuer not found, challenge failed, rate limited, invalid configuration), using resource status as supporting evidence.

For ACME HTTP-01 challenges, verify the challenge path is accessible from the internet and ingress is routing challenge traffic correctly, using connectivity tests and ingress configuration as supporting evidence.

For ACME DNS-01 challenges, verify DNS credentials are correct and DNS propagation is working, using DNS query results and credential configuration as supporting evidence.

Check for rate limiting from Let's Encrypt if issuing many certificates, using ACME server responses and certificate history as supporting evidence.

Verify the certificate specification matches issuer capabilities (allowed domains, key types, duration), using issuer policy and certificate spec as supporting evidence.

If no correlation is found within the specified time windows: verify DNS records point to correct endpoints, check firewall rules allow ACME validation, renew issuer credentials, check for Let's Encrypt rate limits, consider using staging issuer for testing.
