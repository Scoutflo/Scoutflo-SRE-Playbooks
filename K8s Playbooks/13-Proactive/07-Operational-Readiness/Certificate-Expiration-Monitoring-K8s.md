# Certificate Expiration Monitoring

## Meaning

Certificate expiration monitoring indicates that SSL/TLS certificates are approaching expiration or have expired, potentially causing service disruptions (triggering alerts like CertificateExpiring or CertificateExpired) because certificate expiration dates are within warning thresholds, certificates have expired, certificate renewal has not occurred, certificate status shows expiration warnings, or certificate monitoring indicates upcoming expirations. Certificates show expiration dates within warning windows, certificate status indicates expiration, certificate renewal status shows failures, and certificate monitoring alerts fire for upcoming expirations. This affects the security layer and service availability, typically caused by certificate lifecycle management failures, certificate renewal automation issues, or certificate monitoring misconfigurations; if certificates protect container workloads, container ingress certificates may expire and applications may experience TLS connection failures.

## Impact

CertificateExpiring alerts fire; CertificateExpired alerts fire; SSL/TLS connections may fail; services may become unavailable; certificate renewal has not occurred; certificate lifecycle management fails. Certificate expiration dates are within warning thresholds; if certificates protect container workloads, container ingress certificates may expire, pod TLS connections may fail, and container applications may experience TLS connection failures; applications may experience service unavailability or TLS handshake failures.

## Playbook

1. List certificates in namespace <namespace> to retrieve all certificates and their current status including expiration dates.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent certificate renewal issues or expiration warnings.

3. Describe certificate <certificate-name> in namespace <namespace> to inspect its expiration date, status, and renewal configuration.

4. Retrieve ingress resources in namespace <namespace> with YAML output to identify ingress certificate configurations and approaching expirations.

5. Retrieve logs from cert-manager pods with label app=cert-manager in namespace cert-manager and filter for expiration warnings or certificate renewal failures.

6. List secrets in namespace <namespace> filtered by type kubernetes.io/tls to retrieve certificate expiration dates.

7. Retrieve Prometheus metrics for certificate service including certificate_expiration_time and certificate_status over the last 30 days to identify certificates approaching expiration.

8. Verify certificate renewal automation by checking the Certificate resource renewal status and cert-manager configuration.

## Diagnosis

1. Review the certificate status from Steps 1 and 3. If certificates show expiration within warning thresholds (e.g., <30 days), then renewal action is needed. If certificates have already expired, immediate renewal is critical.

2. Analyze the cert-manager logs from Step 5. If logs show renewal failures, identify the failure cause (ACME challenges, DNS validation, permissions, or certificate authority issues). If logs show no renewal attempts, then scheduling is the issue.

3. If Step 4 ingress certificates show approaching expirations, verify that cert-manager is configured to manage those certificates. If cert-manager is not managing them, then manual renewal processes are needed.

4. Review the certificate metrics from Step 7. If certificate_expiration_time shows certificates approaching expiration without renewal activity, then renewal automation is failing.

5. If Step 6 TLS secrets show old creation timestamps without recent updates, then certificate rotation is not occurring. If secrets show recent updates, then certificates are being renewed.

If analysis is inconclusive: Examine events from Step 2 for certificate renewal issues or expiration warnings. Review the certificate renewal automation from Step 8 to verify cert-manager configuration. Determine whether expiration issues affect specific certificates (suggesting certificate-specific configuration problems) or all certificates (suggesting cert-manager infrastructure issues).
