---
title: Error Unauthorized when Accessing API Server - RBAC
weight: 266
categories:
  - kubernetes
  - rbac
---

# ErrorUnauthorizedwhenAccessingAPIServer-rbac

## Meaning

API server requests return Unauthorized (401) errors (triggering KubeAPIErrorsHigh or KubeClientErrors alerts) because authentication tokens are expired, invalid, or missing, kubeconfig credentials are incorrect, or certificate-based authentication has failed. API requests return 401 status codes, authentication tokens may show expired status, and client certificates may show expiration errors. This affects the authentication and authorization plane and prevents cluster access, typically caused by expired credentials, certificate expiration, or kubeconfig misconfiguration; applications using Kubernetes API may show errors.

## Impact

kubectl commands fail with Unauthorized errors; API server access is denied; cluster operations are blocked; KubeAPIErrorsHigh alerts fire; KubeClientErrors alerts fire; API server returns 401 status codes; authentication failures prevent all cluster access; service accounts cannot authenticate; applications fail to connect to API server. API requests return 401 status codes indefinitely; authentication tokens may show expired status; applications using Kubernetes API may experience errors or performance degradation; cluster operations are blocked.

## Playbook

1. Test basic API access using `kubectl auth can-i --list` to confirm the 401 Unauthorized error - if this fails with 401, authentication is broken (not authorization).

2. Check current context and credentials using `kubectl config current-context` and `kubectl config view --minify` to verify the kubeconfig points to the correct cluster and user.

3. Verify your identity is recognized using `kubectl auth whoami` (K8s 1.27+) - a 401 error here confirms the authentication token/certificate is invalid.

4. For token-based auth, check token expiration by decoding the JWT: `kubectl config view --raw -o jsonpath='{.users[0].user.token}' | cut -d'.' -f2 | base64 -d | jq '.exp'` and compare with current time.

5. For certificate-based auth, check certificate expiration: `kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d | openssl x509 -noout -dates`.

6. For service account auth inside a pod, verify the token is mounted: `cat /var/run/secrets/kubernetes.io/serviceaccount/token` and check if the ServiceAccount still exists.

7. Check API server logs for authentication failures: `kubectl logs -n kube-system -l component=kube-apiserver --tail=100 | grep -i "401\|unauthorized\|authentication"` to identify the failing auth method.

## Diagnosis

1. Compare the Unauthorized error timestamps with authentication token expiration timestamps, and check whether tokens expired within 5 minutes before Unauthorized errors.

2. Compare the Unauthorized error timestamps with kubeconfig file modification timestamps, and check whether credential changes occurred within 30 minutes before Unauthorized errors.

3. Compare the Unauthorized error timestamps with client certificate expiration timestamps, and check whether certificates expired within 1 hour before Unauthorized errors.

4. Compare the Unauthorized error timestamps with service account token secret deletion timestamps, and check whether token secrets were removed within 30 minutes before Unauthorized errors.

5. Compare the Unauthorized error timestamps with API server authentication configuration modification timestamps, and check whether authentication settings were changed within 30 minutes before Unauthorized errors.

6. Compare the Unauthorized error timestamps with cluster upgrade or certificate rotation timestamps, and check whether infrastructure changes occurred within 1 hour before Unauthorized errors, affecting authentication mechanisms.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 24 hours for certificate expiration), review API server logs for gradual authentication issues, check for intermittent token refresh problems, examine if authentication configurations drifted over time, verify if certificates gradually approached expiration, and check for API server or authentication provider issues affecting token validation. Unauthorized errors may result from gradual authentication credential expiration or configuration drift rather than immediate changes.

