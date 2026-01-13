---
title: Ingress SSL/TLS Configuration Fails - Ingress
weight: 279
categories:
  - kubernetes
  - ingress
---

# IngressSSLTLSConfigurationFails-ingress

## Meaning

Ingress SSL/TLS configuration is failing (triggering KubeIngressNotReady or KubeIngressCertificateExpiring alerts) because TLS secrets referenced in ingress TLS configuration are missing or invalid, certificate references in ingress annotations (cert-manager.io/issuer) are incorrect, the certificate issuer (cert-manager) is unavailable, or TLS annotations are misconfigured. Ingress endpoints return certificate errors, TLS secrets may show missing or invalid status, and cert-manager pods may show failures. This affects the network plane and prevents secure external access to applications, typically caused by missing TLS secrets, certificate expiration, or cert-manager failures; applications become unavailable to users and may show errors.

## Impact

HTTPS connections fail; SSL/TLS handshake errors occur; certificates cannot be validated; secure traffic is blocked; ingress endpoints return certificate errors; KubeIngressNotReady alerts fire when ingress cannot establish TLS connections; KubeIngressCertificateExpiring alerts fire when certificates are expired or about to expire; users see SSL certificate warnings; TLS termination fails at ingress; ingress status shows TLS configuration errors; secure external access to applications fails. Ingress endpoints return certificate errors indefinitely; TLS secrets may show missing or invalid status; applications become unavailable to users and may experience errors or performance degradation; secure external access to applications fails.

## Playbook

1. Retrieve the Ingress `<ingress-name>` in namespace `<namespace>` and inspect its TLS configuration including TLS section and TLS secret references.

2. Retrieve the Secret `<tls-secret-name>` referenced in the ingress TLS configuration and verify it exists, contains valid certificate and key data, and is not expired.

3. List events in namespace `<namespace>` and filter for TLS-related events, focusing on events with reasons such as `Failed` or messages indicating certificate or secret issues.

4. Check ingress annotations for certificate issuer configurations (e.g., `cert-manager.io/issuer`, `cert-manager.io/cluster-issuer`) and verify if certificate management is configured.

5. Retrieve Certificate or CertificateRequest resources if cert-manager is used and check their status to verify if certificates are being issued or renewed.

6. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for TLS errors, certificate validation failures, or secret access errors.

## Diagnosis

1. Compare the ingress TLS failure timestamps with TLS secret deletion or modification timestamps, and check whether secrets were removed or changed within 10 minutes before TLS failures.

2. Compare the ingress TLS failure timestamps with certificate expiration timestamps, and check whether certificates expired within 1 hour before TLS failures.

3. Compare the ingress TLS failure timestamps with certificate issuer modification or unavailability timestamps, and check whether issuer issues occurred within 30 minutes before TLS failures.

4. Compare the ingress TLS failure timestamps with ingress TLS configuration modification timestamps, and check whether TLS settings were changed within 30 minutes before failures.

5. Compare the ingress TLS failure timestamps with cert-manager pod restart or failure timestamps, and check whether certificate management issues occurred within 5 minutes before TLS failures.

6. Compare the ingress TLS failure timestamps with certificate renewal or issuance failure timestamps, and check whether certificate renewal failed within 1 hour before TLS failures.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 24 hours), review cert-manager logs for gradual certificate processing issues, check for intermittent certificate issuer availability problems, examine if certificate expiration warnings were missed, verify if TLS secret access permissions changed over time, and check for DNS or Let's Encrypt validation issues affecting certificate issuance. TLS configuration failures may result from gradual certificate management issues rather than immediate changes.

