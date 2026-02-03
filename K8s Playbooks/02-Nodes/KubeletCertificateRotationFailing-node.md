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

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and certificate-related conditions
   - Events section showing certificate expiration or rotation failures
   - System Info showing kubelet version and certificate details

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of certificate-related issues.

3. On the node, check kubelet certificate expiration by inspecting certificate files or kubelet logs using Pod Exec tool or SSH if node access is available.

4. Retrieve kubelet logs from the node and filter for certificate rotation errors, expiration warnings, or certificate signing request failures.

5. List CertificateSigningRequest objects in the cluster and check if kubelet certificate signing requests are pending approval.

6. Check the certificate authority (CA) status and verify if the CA is available and can sign certificates.

7. Verify RBAC permissions for kubelet to create and approve certificate signing requests.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify certificate-related issues. Events showing "CertificateRotationFailed", "TLSHandshakeError", or authentication failures indicate certificate problems. Note event timestamps to establish when rotation failures began.

2. If node events indicate certificate expiration, check kubelet certificate expiration from Playbook step 3. Compare the certificate expiry timestamp with current time and with when kubelet started failing to authenticate.

3. If kubelet logs from Playbook step 4 show CSR (CertificateSigningRequest) creation or submission errors, check pending CSRs from Playbook step 5. CSRs stuck in "Pending" status indicate approval process issues.

4. If CSRs are pending, check certificate authority status from Playbook step 6. CA unavailability or overload prevents CSR approval and certificate issuance.

5. If kubelet logs show permission denied errors when creating or approving CSRs, verify RBAC permissions from Playbook step 7. Insufficient permissions prevent kubelet from requesting certificate renewal.

6. If kubelet logs show connectivity errors when contacting the CA or API server for CSR submission, verify network connectivity between kubelet and control plane components.

7. If certificate rotation was working previously and recently failed, check for cluster upgrades, CA certificate rotation, or RBAC policy changes that may have affected the rotation process.

**If no root cause is identified from events**: Review kubelet configuration for certificate rotation settings, check if automatic rotation is enabled, verify CA certificate chain validity, and examine if certificate rotation has been failing silently and only recently caused visible issues when certificates finally expired.

