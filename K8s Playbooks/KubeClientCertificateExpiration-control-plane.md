---
title: Kube Client Certificate Expiration
weight: 20
---

# KubeClientCertificateExpiration

## Meaning

A client certificate used to authenticate to the API server is expiring in less than 7 days (warning) or 24 hours (critical) (triggering KubeClientCertificateExpiration alerts) because the certificate is approaching its expiration date without renewal. Certificate metadata shows expiration dates within the warning or critical threshold, certificate expiration errors appear in logs, and TLS handshake failures may occur as certificates approach expiration. This affects the authentication and authorization plane and indicates certificate lifecycle management issues that will prevent client access to the cluster, typically caused by failed certificate rotation processes, misconfigured certificate lifetimes, or certificate management system failures; applications using expiring certificates may show authentication errors.

## Impact

KubeClientCertificateExpiration alerts fire; clients will not be able to interact with the cluster after expiration; in-cluster services communicating with Kubernetes API may degrade or become unavailable; authentication failures occur; certificate expiration errors appear in logs; TLS handshake failures prevent API access; service account token issues may occur; controllers may fail to reconcile; cluster operations will be blocked for affected clients; API access will be denied after certificate expiration. Certificate expiration errors appear in logs; TLS handshake failures occur as certificates approach expiration; applications using expiring certificates may experience authentication errors or API access failures; CertificateSigningRequest resources may show failed rotation attempts.

## Playbook

1. Retrieve certificate expiration information for client certificates used by service accounts, controllers, or API clients in the cluster and identify certificates expiring within 7 days (warning) or 24 hours (critical).

2. Retrieve ServiceAccount resources used by pods and controllers and check service account token expiration to verify if token expiration aligns with certificate expiration.

3. Verify certificate issuance and expiration timestamps for client certificates to determine remaining validity period and identify certificates approaching expiration.

4. Retrieve CertificateSigningRequest resources and check for certificate rotation or renewal processes that should have updated certificates to identify failed rotation attempts.

5. Retrieve events and logs from the Pod `<pod-name>` in namespace `<namespace>` using expiring certificates and filter for certificate-related error patterns including 'certificate expired', 'TLS handshake failure', 'authentication failed'.

6. Retrieve Secret resources containing certificate authority (CA) configuration and verify certificate authority (CA) configuration and certificate signing request (CSR) processes to identify configuration issues.

## Diagnosis

Compare certificate expiration detection timestamps with certificate issuance times and verify whether certificates are approaching expiration due to normal lifecycle, using certificate metadata and expiration calculations as supporting evidence.

Correlate certificate expiration warnings with certificate rotation process failure timestamps within 24 hours and verify whether automatic rotation failed to renew certificates, using certificate rotation logs and certificate status as supporting evidence.

Compare certificate expiration with service account token expiration times and verify whether token expiration aligns with certificate expiration, using service account metadata and token expiration data as supporting evidence.

Analyze certificate expiration patterns across multiple clients to determine if expiration is isolated (single client issue) or widespread (certificate management system issue), using certificate expiration data and client configurations as supporting evidence.

Correlate certificate expiration with certificate authority (CA) rotation or update timestamps within 24 hours and verify whether CA changes affected certificate validity, using CA configuration and certificate chain validation as supporting evidence.

Compare current certificate expiration dates with historical certificate lifecycle patterns to verify whether certificates are expiring earlier than expected, using certificate history and lifecycle management logs as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to certificate validity period, review certificate rotation configuration, check for certificate management system failures, verify CA configuration, examine historical certificate lifecycle patterns. Certificate expiration may result from misconfigured certificate lifetimes, failed rotation processes, or certificate management system issues rather than immediate operational changes.
