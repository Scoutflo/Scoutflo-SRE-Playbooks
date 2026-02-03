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

1. List API server pods in namespace kube-system with label component=kube-apiserver to check API server pod status and identify any pods experiencing certificate-related failures.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for certificate errors or TLS handshake failures.

3. On a control plane node, check certificate expiration dates for all control plane, kubelet, and etcd certificates.

4. Retrieve logs from the API server pod in kube-system (or system logs if running as a service) and filter for certificate errors such as x509: certificate has expired or failed TLS handshakes.

5. List all nodes and inspect their Ready status and conditions to identify nodes that have lost contact with the control plane around the time of certificate errors.

6. Check the status of any certificate rotation automation (such as cert-manager or external-secrets operators) by listing their pods and verifying they are running without errors.

7. Using the certificate inspection output and any stored CA files, verify that cluster CA certificates are still valid and have not reached or exceeded their expiration dates.

## Diagnosis

1. Analyze certificate-related events from Playbook to identify which certificates have expired and when expiration occurred. If events show x509 certificate errors or TLS handshake failures, use event timestamps to pinpoint when authentication failures began.

2. If events indicate certificate expiration, verify certificate expiration dates from Playbook step 3. If certificate expiration timestamps from `kubeadm certs check-expiration` align with authentication error event timestamps, certificate expiration is confirmed as root cause.

3. If events indicate control plane component restarts or failures, correlate component restart timestamps from events with certificate expiration times. If restarts began at or shortly after certificate expiration, expired certificates caused component failures.

4. If events indicate CSR approval failures or kubelet communication issues, check whether CSR-related events began failing around certificate expiration timestamps. If CSR events show denied or pending states, certificate rotation processes have failed.

5. If events indicate recent cluster upgrade activity, verify whether upgrade-related events occurred within 24 hours before certificate errors. If upgrade events are found, the upgrade process may have failed to renew certificates properly.

6. If events are inconclusive, examine configuration change events in kube-system namespace. If ConfigMap or Deployment changes related to certificates occurred before expiration errors, configuration issues may have prevented certificate renewal.

**If no correlation is found**: Extend the search window, check infrastructure logs and change management systems for unrecorded changes, review historical certificate rotation patterns, and examine related components (etcd, kubelet) for delayed error manifestations. Certificate-related issues may have cascading effects that appear hours after the initial expiration.

