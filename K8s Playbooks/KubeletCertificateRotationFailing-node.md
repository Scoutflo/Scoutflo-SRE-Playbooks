---
title: Kubelet Certificate Rotation Failing - Node
weight: 257
categories:
  - kubernetes
  - node
---

# KubeletCertificateRotationFailing-node

## Meaning

Kubelet certificate rotation is failing (triggering KubeletDown or certificate-related alerts) because certificates are expired, certificate signing requests cannot be approved, the certificate authority is unavailable, or RBAC permissions prevent certificate renewal. Kubelet logs show certificate rotation errors or expiration warnings, CertificateSigningRequest resources show pending approval, and certificate authority status may indicate unavailability. This affects the data plane and prevents kubelet from authenticating to the API server with expired certificates, causing node communication failures; applications running on affected nodes may experience errors.

## Impact

Kubelet cannot authenticate to API server; nodes become NotReady; pod status cannot be reported; new pods cannot be scheduled; KubeletDown alerts fire; KubeNodeNotReady alerts fire; certificate expiration errors occur; TLS handshake failures; node loses control plane connectivity. Kubelet logs show certificate rotation errors or expiration warnings; CertificateSigningRequest resources show pending approval indefinitely; nodes remain in NotReady state; applications running on affected nodes may experience errors or become unreachable.

## Playbook

1. On the node, check kubelet certificate expiration by inspecting certificate files or kubelet logs using Pod Exec tool or SSH if node access is available.

2. Retrieve kubelet logs from the node and filter for certificate rotation errors, expiration warnings, or certificate signing request failures.

3. List CertificateSigningRequest objects in the cluster and check if kubelet certificate signing requests are pending approval.

4. Check the certificate authority (CA) status and verify if the CA is available and can sign certificates.

5. Verify RBAC permissions for kubelet to create and approve certificate signing requests.

6. List events on the node and filter for certificate-related events, focusing on events with reasons such as `CertificateExpired` or messages indicating certificate rotation failures.

## Diagnosis

1. Compare the kubelet certificate rotation failure timestamps with kubelet certificate expiration timestamps, and check whether certificates expired within 1 hour before rotation failures.

2. Compare the kubelet certificate rotation failure timestamps with CertificateSigningRequest creation or approval failure timestamps, and check whether CSR processing failures occurred within 30 minutes before rotation failures.

3. Compare the kubelet certificate rotation failure timestamps with certificate authority unavailability timestamps, and check whether CA issues occurred within 10 minutes before rotation failures.

4. Compare the kubelet certificate rotation failure timestamps with RBAC permission modification timestamps, and check whether permission changes occurred within 30 minutes before rotation failures.

5. Compare the kubelet certificate rotation failure timestamps with cluster upgrade or certificate authority update timestamps, and check whether infrastructure changes occurred within 1 hour before rotation failures.

6. Compare the kubelet certificate rotation failure timestamps with kubelet restart or configuration modification timestamps, and check whether kubelet changes occurred within 30 minutes before rotation failures.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 24 hours for certificate expiration), review kubelet logs for gradual certificate rotation issues, check for intermittent certificate authority connectivity problems, examine if certificate rotation was always failing but only recently enforced, verify if RBAC permissions were gradually restricted, and check for certificate authority performance degradation that may have developed. Certificate rotation failures may result from gradual certificate management issues rather than immediate expiration.

