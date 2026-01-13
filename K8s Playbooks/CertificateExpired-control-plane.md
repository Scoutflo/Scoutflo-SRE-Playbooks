---
title: Certificate Expired - Control Plane
weight: 249
categories:
  - kubernetes
  - control-plane
---

# CertificateExpired-control-plane

## Meaning

One or more cluster X.509 certificates (for the API server, kubelets, or etcd) have passed their validity period, causing TLS handshakes and authenticated requests between core Kubernetes components to start failing. Certificate expiration triggers x509 certificate errors, authentication failures, and component communication breakdowns.

## Impact

All API operations fail; cluster becomes completely non-functional; nodes cannot communicate with control plane; kubectl commands fail; controllers stop reconciling; cluster is effectively down; certificate expiration errors appear in logs; TLS handshake failures occur; KubeAPIDown or KubeletDown alerts may fire; authentication errors prevent cluster operations.

## Playbook

1. On a control plane node, execute `kubeadm certs check-expiration` (or the equivalent certificate inspection command) to list all control plane, kubelet, and etcd certificate expiration dates.

2. Retrieve logs from the API server pod in `kube-system` (or system logs if running as a service) and filter for certificate errors such as `x509: certificate has expired` or failed TLS handshakes.

3. List all nodes and inspect their Ready status and conditions to identify nodes that have lost contact with the control plane around the time of certificate errors.

4. Check the status of any certificate rotation automation (such as cert-manager or external-secrets operators) by listing their pods and verifying they are running without errors.

5. Using the certificate inspection output and any stored CA files, verify that cluster CA certificates are still valid and have not reached or exceeded their expiration dates.

## Diagnosis

1. Compare the certificate expiration timestamps from `kubeadm certs check-expiration` with the authentication error timestamps in API server logs (log lines containing `x509: certificate has expired`), and verify that errors start within 5 minutes of a certificate's expiration.

2. Compare the certificate expiration timestamps with the last cluster upgrade timestamp from your change records, and check whether expirations occur within 24 hours after an upgrade that may have failed to renew certificates.

3. Compare the certificate expiration timestamps with kubelet CSR approval transition times and check whether CSR approvals began failing or stopping within 24 hours of certificate expiration.

4. Compare the certificate expiration timestamps with control plane component restart timestamps and check whether components began restarting repeatedly around the time the certificates expired.

5. Compare authentication error timestamps from API server logs (containing `x509: certificate has expired`) with the corresponding certificate expiration times, and confirm that errors begin at or within 5 minutes after the configured expiration.

6. Compare certificate expiration timestamps with ConfigMap and Deployment change times in `kube-system` and check whether configuration changes related to certificates occurred within 24 hours of expiration.

**If no correlation is found within the specified time windows**: Extend the search window (double the initial timeframe), check infrastructure logs and change management systems for unrecorded changes, review historical certificate rotation patterns, and examine related components (etcd, kubelet) for delayed error manifestations. Certificate-related issues may have cascading effects that appear hours after the initial expiration.

