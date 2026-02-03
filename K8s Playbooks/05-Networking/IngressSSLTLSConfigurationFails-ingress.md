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

1. Describe the Ingress `<ingress-name>` in namespace `<namespace>` using `kubectl describe ingress <ingress-name> -n <namespace>` and inspect its TLS configuration including TLS section, annotations, and TLS secret references.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<ingress-name> --sort-by='.lastTimestamp'` and filter for TLS-related events, focusing on events with reasons such as `Failed`, `Sync`, or messages indicating certificate or secret issues.

3. Retrieve the Secret `<tls-secret-name>` referenced in the ingress TLS configuration and verify it exists, contains valid certificate and key data, and is not expired.

4. Check ingress annotations for certificate issuer configurations (e.g., `cert-manager.io/issuer`, `cert-manager.io/cluster-issuer`) and verify if certificate management is configured.

5. Retrieve Certificate or CertificateRequest resources if cert-manager is used and check their status to verify if certificates are being issued or renewed.

6. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for TLS errors, certificate validation failures, or secret access errors.

## Diagnosis

Begin by analyzing the Ingress describe output, TLS secret status, and cert-manager resources collected in the Playbook section. The TLS secret contents, certificate validity, and issuer status provide the primary diagnostic signals.

**If the TLS secret referenced in the Ingress does not exist:**
- The certificate secret is missing. Check if cert-manager is configured to create it. Verify the Ingress has correct cert-manager annotations. If manually managing certificates, create the secret with valid `tls.crt` and `tls.key` data.

**If the TLS secret exists but contains invalid or expired certificate data:**
- The certificate is expired or malformed. Decode the certificate using `openssl x509 -in <cert> -text -noout` to check validity dates and subject. Renew the certificate manually or trigger cert-manager renewal.

**If cert-manager Certificate resource shows status other than Ready:**
- Certificate issuance or renewal is failing. Check the Certificate status conditions for error messages. Check CertificateRequest and Order resources for detailed failure reasons.

**If cert-manager logs show ACME challenge failures:**
- Let's Encrypt validation is failing. For HTTP-01 challenges, verify the Ingress allows traffic to `/.well-known/acme-challenge/` path. For DNS-01, verify DNS provider credentials and permissions.

**If the Ingress controller logs show TLS handshake errors:**
- The certificate may not match the hostname or the certificate chain is incomplete. Verify the certificate Subject Alternative Names include the Ingress hostname. Check if intermediate certificates are included in `tls.crt`.

**If TLS works for some hostnames but not others:**
- Multiple TLS sections may conflict or a specific hostname lacks a certificate. Verify each hostname in the Ingress has a corresponding TLS entry or is covered by a wildcard certificate.

**If events are inconclusive, correlate timestamps:**
1. Check if TLS failures began after the secret was deleted or modified by examining secret resource version.
2. Check if failures align with cert-manager pod restarts or Issuer modifications.
3. Check certificate expiration dates against failure timestamps.

**If no clear cause is identified:** Test TLS configuration using `openssl s_client -connect <host>:443 -servername <hostname>` to inspect the certificate chain returned by the ingress controller.

