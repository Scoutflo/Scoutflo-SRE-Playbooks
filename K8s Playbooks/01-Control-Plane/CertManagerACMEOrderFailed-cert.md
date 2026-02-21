---
title: Cert Manager ACME Order Failed
weight: 43
categories: [kubernetes, cert-manager]
---

# CertManagerACMEOrderFailed

## Meaning

ACME certificate order has failed (triggering CertManagerACMEOrderFailed alerts) because the ACME challenge (HTTP-01 or DNS-01) could not be completed successfully. Order resource shows Failed state, domain validation did not pass, and the certificate cannot be issued. This affects certificates using ACME issuers like Let's Encrypt; new certificates fail to issue; renewals fail; HTTPS may be unavailable.

## Impact

CertManagerACMEOrderFailed alerts fire; certificate cannot be issued; HTTPS endpoints have no valid certificate; new deployments requiring TLS are blocked; certificate renewals fail; browsers show security errors; API clients reject connections; ingress cannot serve HTTPS traffic securely.

## Playbook

1. Retrieve the Order resource associated with the failing Certificate and check its status and failure reason.

2. Retrieve Challenge resources under the Order and identify which domains failed validation.

3. For HTTP-01 challenges: verify the challenge path is accessible from the internet at http://domain/.well-known/acme-challenge/<token>.

4. For DNS-01 challenges: verify the _acme-challenge TXT record exists and has the correct value.

5. Check ingress configuration to ensure challenge paths are not blocked or redirected.

6. Verify firewall and network policies allow incoming HTTP(S) for validation.

7. Check ACME server response in cert-manager logs for specific error details.

## Diagnosis

For HTTP-01 challenges, verify that the challenge URL returns the expected token value from external internet locations, using curl or HTTP testing tools as supporting evidence.

Check if ingress controllers have configurations that interfere with ACME challenges (forced HTTPS redirects, authentication requirements), using ingress annotations and routing rules as supporting evidence.

For DNS-01 challenges, verify DNS propagation is complete and TXT record is resolvable from multiple locations, using DNS query tools and propagation checkers as supporting evidence.

Check for Let's Encrypt rate limits by examining error messages mentioning rate limiting or too many requests, using ACME server responses in logs as supporting evidence.

Verify domain ownership and DNS configuration points to the correct ingress, using DNS records and domain registration as supporting evidence.

If no correlation is found within the specified time windows: use ACME staging server for testing to avoid rate limits, verify DNS credentials for DNS-01, check for CAA records blocking issuance, temporarily disable HTTPS redirects during challenge, contact ACME provider if persistent failures.
