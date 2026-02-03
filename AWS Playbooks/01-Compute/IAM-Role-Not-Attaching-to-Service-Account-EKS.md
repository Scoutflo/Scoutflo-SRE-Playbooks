# EKS IAM Role Not Attaching to Service Account

## Meaning

EKS IAM role is not attaching to service account (triggering permission failures or EKSServiceAccountIRSAFailure alarms) because IAM role trust policy does not allow service account, service account annotation is incorrect, IAM role ARN is wrong, OIDC provider is not configured, service account and IAM role are in different accounts, or EKS cluster OIDC provider is missing. EKS service account cannot assume IAM role, pod permissions are insufficient, and application pods cannot access AWS services. This affects the container orchestration and security layer and blocks service access, typically caused by IRSA (IAM Roles for Service Accounts) configuration issues, OIDC provider problems, or trust policy errors; if using EKS with multiple namespaces, service account configuration may differ and applications may experience permission failures.

## Impact

EKS service account cannot assume IAM role; pod permissions are insufficient; service account IAM integration fails; pod IAM role attachment errors occur; application pods cannot access AWS services; IAM role-based access fails; Kubernetes service account automation is ineffective. EKSServiceAccountIRSAFailure alarms may fire; if using EKS with multiple namespaces, service account configuration may differ; applications may experience errors or performance degradation due to missing AWS service permissions; pods cannot access required AWS resources.

## Playbook

1. Verify EKS cluster `<cluster-name>` exists and AWS service health for EKS and IAM in region `<region>` is normal.
2. Retrieve the EKS Cluster `<cluster-name>` in region `<region>` and inspect its OIDC provider configuration, OIDC provider URL, and IAM role trust relationships, verifying OIDC provider is configured.
3. Query CloudWatch Logs for log groups containing EKS pod logs and filter for IAM role attachment failure patterns, permission errors, or service account annotation errors, including pod error messages.
4. Retrieve the IAM role `<role-arn>` that should attach to service account and inspect its trust policy, service account trust relationships, and OIDC provider configuration, verifying trust policy format.
5. List EKS service accounts in cluster `<cluster-name>` and check service account annotations, IAM role annotations, and service account configurations, verifying annotation format.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for EKS service account IAM role assumption failures or permission denied events, including AssumeRole failures.
7. Retrieve the EKS Cluster `<cluster-name>` OIDC provider issuer URL and verify OIDC provider is accessible, checking OIDC provider status.
8. Retrieve the IAM role `<role-arn>` trust policy and verify trust policy condition matches service account namespace and name, checking trust policy condition format.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for EKS cluster OIDC provider or IAM role trust policy modification events related to cluster `<cluster-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs containing EKS pod logs and CloudTrail events (from Playbook steps 3 and 6) to identify specific permission error messages. If errors show "AccessDenied" or "AssumeRoleWithWebIdentity failed", this indicates IAM role trust policy or OIDC configuration issues. If errors show "InvalidIdentityToken", the OIDC provider configuration is incorrect.

2. Verify EKS cluster OIDC provider configuration (from Playbook step 2) to confirm OIDC provider is properly associated with the cluster. If OIDC provider URL is missing or incorrect, IAM Roles for Service Accounts (IRSA) cannot function. The OIDC provider issuer URL must match the cluster's OIDC endpoint.

3. Examine IAM role trust policy (from Playbook steps 4 and 8) to verify the trust policy correctly references the EKS cluster's OIDC provider and includes proper conditions for the service account. If the trust policy condition does not match the service account namespace and name format "system:serviceaccount:NAMESPACE:SERVICE_ACCOUNT_NAME", role assumption fails.

4. Review service account annotations (from Playbook step 5) to verify the `eks.amazonaws.com/role-arn` annotation contains the correct IAM role ARN. If the annotation is missing, malformed, or references a non-existent role, pods cannot assume the IAM role.

5. Correlate CloudTrail events (from Playbook step 9) with IAM role attachment failure timestamps within 5 minutes to identify any recent modifications to the OIDC provider, IAM role trust policy, or service account configuration.

6. Compare attachment failure patterns across different service accounts within 1 hour. If failures are service account-specific, verify that particular service account's annotation and namespace configuration. If failures affect all service accounts using the same IAM role, the trust policy is misconfigured. If failures are cluster-wide affecting all IRSA configurations, the OIDC provider association is the issue.

7. Verify OIDC provider accessibility (from Playbook step 7) to ensure the OIDC endpoint is reachable and the certificate is valid. If OIDC provider certificate has expired or endpoint is unreachable, all IRSA operations fail.

If no correlation is found within the specified time windows: extend timeframes to 48 hours, review alternative evidence sources including service account namespace configuration and IAM role ARN format, check for gradual issues like OIDC provider certificate expiration or trust policy condition changes, verify external dependencies like OIDC provider availability or IAM service health, examine historical patterns of IAM role attachment failures, check for EKS cluster OIDC provider association issues, verify EKS service account annotation namespace format. Attachment failures may result from OIDC provider configuration issues, service account annotation format errors, IAM role trust policy condition problems, EKS cluster OIDC provider association issues, or service account annotation namespace format errors rather than immediate service account configuration changes.
