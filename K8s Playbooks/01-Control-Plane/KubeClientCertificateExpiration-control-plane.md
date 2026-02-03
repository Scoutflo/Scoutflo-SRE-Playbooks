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

1. List all CertificateSigningRequest resources to identify any pending, denied, or failed certificate requests.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for certificate expiration warnings, TLS handshake failures, or authentication errors.

3. Retrieve certificate expiration information for client certificates used by service accounts, controllers, or API clients in the cluster and identify certificates expiring within 7 days (warning) or 24 hours (critical).

4. Retrieve ServiceAccount resources used by pods and controllers and check service account token expiration to verify if token expiration aligns with certificate expiration.

5. Verify certificate issuance and expiration timestamps for client certificates to determine remaining validity period and identify certificates approaching expiration.

6. Retrieve CertificateSigningRequest resources and check for certificate rotation or renewal processes that should have updated certificates to identify failed rotation attempts.

7. Retrieve events and logs from the Pod `<pod-name>` in namespace `<namespace>` using expiring certificates and filter for certificate-related error patterns including 'certificate expired', 'TLS handshake failure', 'authentication failed'.

8. Retrieve Secret resources containing certificate authority (CA) configuration and verify certificate authority (CA) configuration and certificate signing request (CSR) processes to identify configuration issues.

## Diagnosis

1. Analyze certificate-related events from Playbook to identify which certificates are approaching expiration and their current status. If events show certificate expiration warnings or TLS handshake preparation failures, use event timestamps to determine urgency.

2. If events indicate pending or failed CertificateSigningRequests, examine CSR status from Playbook step 1. If CSR events show denied, failed, or pending states, certificate rotation processes have failed and require investigation.

3. If events indicate certificate rotation process failures, verify certificate management system status. If rotation-related events show errors or failures at timestamps preceding expiration warnings, automatic renewal has failed.

4. If events indicate service account token issues, verify service account token expiration from Playbook step 4. If token expiration aligns with certificate expiration timestamps, both need to be addressed together.

5. If events show certificate expiration across multiple clients, analyze expiration patterns. If multiple certificates are expiring at similar timestamps, a certificate management system failure or batch issuance issue is likely.

6. If events indicate CA rotation or update activity, verify CA configuration impact. If CA events occurred before certificate expiration warnings, CA changes may have affected certificate validity or trust chain.

7. If events show certificates expiring earlier than expected based on issuance date, verify certificate lifetime configuration. If certificates have shorter-than-expected lifetimes, misconfigured certificate parameters need correction.

**If no correlation is found**: Extend timeframes to certificate validity period, review certificate rotation configuration, check for certificate management system failures, verify CA configuration, examine historical certificate lifecycle patterns. Certificate expiration may result from misconfigured certificate lifetimes, failed rotation processes, or certificate management system issues rather than immediate operational changes.
