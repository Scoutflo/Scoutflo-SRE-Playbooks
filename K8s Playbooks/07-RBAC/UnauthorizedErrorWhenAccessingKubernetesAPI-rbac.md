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

1. Test basic API access using `kubectl auth can-i --list` to immediately verify if authentication is working - a 401 error confirms the authentication issue.

2. Check current context and user using `kubectl config current-context` and `kubectl config view --minify` to verify the kubeconfig is pointing to correct cluster and user.

3. Verify the current identity using `kubectl auth whoami` (K8s 1.27+) or `kubectl get --raw /apis/authentication.k8s.io/v1/selfsubjectreviews -o json` to confirm which identity the API server sees.

4. Check if authentication tokens are expired by running `kubectl config view --raw -o jsonpath='{.users[0].user.token}'` and decoding the JWT token to inspect expiration (`exp` claim).

5. For certificate-based auth, check certificate expiration using `openssl x509 -in <cert-file> -noout -dates` or `kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d | openssl x509 -noout -dates`.

6. If using service account, verify the token exists and is mounted correctly using `kubectl exec <pod-name> -n <namespace> -- cat /var/run/secrets/kubernetes.io/serviceaccount/token` or check if token secret exists.

7. Check API server logs if accessible using `kubectl logs -n kube-system -l component=kube-apiserver --tail=100 | grep -i "401\|unauthorized"` to identify which authentication method is failing.

## Diagnosis

1. Compare the Unauthorized error timestamps with authentication token expiration timestamps, and check whether tokens expired within 5 minutes before Unauthorized errors.

2. Compare the Unauthorized error timestamps with kubeconfig file modification timestamps, and check whether credential changes occurred within 30 minutes before Unauthorized errors.

3. Compare the Unauthorized error timestamps with client certificate expiration timestamps, and check whether certificates expired within 1 hour before Unauthorized errors.

4. Compare the Unauthorized error timestamps with service account token secret deletion timestamps, and check whether token secrets were removed within 30 minutes before Unauthorized errors.

5. Compare the Unauthorized error timestamps with API server authentication configuration modification timestamps, and check whether authentication settings were changed within 30 minutes before Unauthorized errors.

6. Compare the Unauthorized error timestamps with cluster upgrade or certificate rotation timestamps, and check whether infrastructure changes occurred within 1 hour before Unauthorized errors, affecting authentication mechanisms.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 24 hours for certificate expiration), review API server logs for gradual authentication issues, check for intermittent token refresh problems, examine if authentication configurations drifted over time, verify if certificates gradually approached expiration, and check for API server or authentication provider issues affecting token validation. Unauthorized errors may result from gradual authentication credential expiration or configuration drift rather than immediate changes.

