---
title: Ingress Certificate Expiring
weight: 55
categories: [kubernetes, ingress]
---

# IngressCertificateExpiring

## Meaning

TLS certificate used by ingress is approaching expiration (triggering IngressCertificateExpiring alerts) because the certificate will expire soon and automatic renewal has not occurred or manual renewal is needed. Ingress TLS secret contains a certificate with upcoming expiration date, and HTTPS connections will fail after expiration. This affects all HTTPS traffic through this ingress; users will see certificate warnings then errors; API clients will reject connections.

## Impact

IngressCertificateExpiring alerts fire; warning of impending HTTPS outage; certificate expiration will cause browser security warnings; API clients will fail to connect; mobile apps will reject the certificate; mTLS authentication will break; ingress traffic will be affected; customer-facing services will be impacted; SEO ranking may be affected.

## Playbook

1. Identify the TLS secret referenced by the ingress and retrieve its certificate expiration date.

2. Check if cert-manager is managing this certificate by looking for Certificate resources referencing this secret.

3. If cert-manager managed: check Certificate resource status and renewal conditions.

4. If manually managed: prepare new certificate from CA and update the secret.

5. Verify ingress controller will reload when secret is updated.

6. Check for any dependencies on this certificate (other services using same cert).

7. Plan renewal with minimal disruption, considering ingress controller reload behavior.

## Diagnosis

Check Certificate resource status if managed by cert-manager and identify why renewal has not occurred, using Certificate conditions and events as supporting evidence.

For cert-manager managed certs, verify issuer is healthy and can issue new certificates, using Issuer status and recent issuance history as supporting evidence.

For manually managed certs, check organizational process for certificate renewal and identify responsible team, using certificate metadata and ownership documentation as supporting evidence.

Verify the secret format is correct (tls.crt, tls.key) and will be accepted by ingress controller when updated, using secret structure and ingress requirements as supporting evidence.

Check if the certificate is used by multiple ingresses or services requiring coordinated renewal, using secret references across cluster as supporting evidence.

If no correlation is found within the specified time windows: obtain new certificate from CA immediately, update secret with new certificate, verify ingress controller loads new certificate, set up monitoring and automated renewal, consider migrating to cert-manager for automation.
