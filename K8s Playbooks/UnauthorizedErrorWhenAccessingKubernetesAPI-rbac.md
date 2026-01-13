---
title: Unauthorized Error When Accessing Kubernetes API - RBAC
weight: 214
categories:
  - kubernetes
  - rbac
---

# UnauthorizedErrorWhenAccessingKubernetesAPI-rbac

## Meaning

Kubernetes API requests return Unauthorized (401) errors (triggering KubeAPIErrorsHigh or KubeClientErrors alerts) because authentication credentials are invalid, expired, or missing, kubeconfig is misconfigured, or certificate-based authentication has failed. API requests return 401 status codes, authentication tokens may show expired status, and client certificates may show expiration errors. This affects the authentication and authorization plane and prevents cluster operations, typically caused by expired credentials, certificate expiration, or kubeconfig misconfiguration; applications using Kubernetes API may show errors.

## Impact

API requests fail with Unauthorized errors; kubectl commands are denied; cluster operations are blocked; KubeAPIErrorsHigh alerts fire; KubeClientErrors alerts fire; API server returns 401 status codes; authentication failures prevent all cluster access; service accounts cannot authenticate; applications fail to connect to API server. API requests return 401 status codes indefinitely; authentication tokens may show expired status; applications using Kubernetes API may experience errors or performance degradation; cluster operations are blocked.

## Playbook

1. Verify the kubeconfig file configuration and check if the current context, user credentials, and cluster endpoint are correct.

2. Check if authentication tokens are expired by inspecting token expiration times or attempting token refresh operations.

3. Verify certificate-based authentication by checking client certificate validity, expiration, and certificate chain if certificates are used.

4. Test API server connectivity and authentication by executing a simple API request to verify if authentication is working.

5. Check API server logs if accessible to review authentication failures and identify which authentication method is failing.

6. Verify service account token validity if using service account authentication by checking token expiration and secret existence in the pod or service account.

## Diagnosis

1. Compare the Unauthorized error timestamps with authentication token expiration timestamps, and check whether tokens expired within 5 minutes before Unauthorized errors.

2. Compare the Unauthorized error timestamps with kubeconfig file modification timestamps, and check whether credential changes occurred within 30 minutes before Unauthorized errors.

3. Compare the Unauthorized error timestamps with client certificate expiration timestamps, and check whether certificates expired within 1 hour before Unauthorized errors.

4. Compare the Unauthorized error timestamps with service account token secret deletion timestamps, and check whether token secrets were removed within 30 minutes before Unauthorized errors.

5. Compare the Unauthorized error timestamps with API server authentication configuration modification timestamps, and check whether authentication settings were changed within 30 minutes before Unauthorized errors.

6. Compare the Unauthorized error timestamps with cluster upgrade or certificate rotation timestamps, and check whether infrastructure changes occurred within 1 hour before Unauthorized errors, affecting authentication mechanisms.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 24 hours for certificate expiration), review API server logs for gradual authentication issues, check for intermittent token refresh problems, examine if authentication configurations drifted over time, verify if certificates gradually approached expiration, and check for API server or authentication provider issues affecting token validation. Unauthorized errors may result from gradual authentication credential expiration or configuration drift rather than immediate changes.

