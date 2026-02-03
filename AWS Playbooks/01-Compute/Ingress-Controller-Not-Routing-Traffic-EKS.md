# EKS Ingress Controller Not Routing Traffic

## Meaning

EKS Ingress Controller is not routing traffic (triggering routing failures or EKSIngressRoutingFailed alarms) because ingress controller is not deployed, ingress resource configuration is incorrect, ingress controller service is not exposed, ingress rules do not match request paths, ingress controller pod is not running, or ingress controller load balancer configuration blocks routing. EKS ingress routing fails, Kubernetes ingress resources do not route traffic, and application ingress access fails. This affects the container orchestration and networking layer and blocks external access, typically caused by ingress controller deployment issues, configuration problems, or load balancer issues; if using EKS with AWS Load Balancer Controller, controller configuration may differ and applications may experience ingress routing failures.

## Impact

EKS ingress routing fails; Kubernetes ingress resources do not route traffic; ingress controller is ineffective; application ingress access fails; ingress rules are not applied; ingress controller service is unreachable; Kubernetes ingress automation fails; external access to services is blocked. EKSIngressRoutingFailed alarms may fire; if using EKS with AWS Load Balancer Controller, controller configuration may differ; applications may experience errors or performance degradation due to blocked ingress access; external users cannot access services.

## Playbook

1. Verify EKS cluster `<cluster-name>` exists and AWS service health for EKS in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing EKS pod logs and filter for ingress controller pod logs, ingress controller errors, or routing failure patterns in cluster `<cluster-name>`, including pod status.
3. Retrieve the EKS Cluster `<cluster-name>` in region `<region>` and inspect its ingress controller deployment status, ingress controller service configuration, and ingress resource configurations, verifying controller is deployed.
4. List EKS pods in namespace for ingress controller and check pod status, pod logs, and ingress controller pod health, verifying pods are running.
5. Query CloudWatch Logs for log groups containing application access logs and filter for ingress routing failures or 404 error patterns related to ingress resources, including routing error details.
6. Retrieve CloudWatch metrics for EKS ingress controller including request count and error rate over the last 1 hour to identify routing patterns, analyzing traffic flow.
7. Retrieve the EKS Ingress Controller service configuration and verify service type and load balancer configuration, checking if load balancer is properly configured.
8. Retrieve the EKS Cluster `<cluster-name>` OIDC provider configuration if using AWS Load Balancer Controller and verify IAM role permissions, checking controller IAM role configuration.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for EKS ingress resource or service modification events related to cluster `<cluster-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs containing ingress controller pod logs (from Playbook step 2) to identify routing failure patterns, error messages, or connection issues. If logs show specific error codes like 404 or 503, this indicates whether the issue is path matching or backend unavailability. If logs show controller startup errors, the controller deployment itself is problematic.

2. Review CloudWatch metrics for ingress controller request count and error rate (from Playbook step 6) to establish baseline traffic patterns. If error rates suddenly increased, correlate the timestamp with recent configuration changes. If metrics show zero traffic reaching the controller, the issue is at the load balancer or service level.

3. Verify ingress controller pod status (from Playbook step 4) to confirm pods are running and healthy. If pods show CrashLoopBackOff or ImagePullBackOff status, the controller cannot route traffic. If pods are running but logs show errors, proceed to configuration analysis.

4. If using AWS Load Balancer Controller, verify IAM role permissions (from Playbook step 8) for the controller service account. If OIDC provider configuration is incorrect or IAM role trust policy is misconfigured, the controller cannot provision or manage load balancers, preventing traffic routing.

5. Examine ingress resource configurations (from Playbook step 3) to verify path rules, backend services, and annotations are correctly defined. If ingress rules do not match incoming request paths, requests return 404 errors. If backend service selectors do not match running pods, traffic cannot reach the application.

6. Correlate CloudTrail events (from Playbook step 9) with routing failure timestamps within 5 minutes to identify any EKS ingress resource or service modifications. If configuration changes coincide with the start of routing failures, those changes are the likely cause.

7. Compare routing failure patterns across different ingress resources within 1 hour. If failures are ingress-specific, the issue is with that particular ingress rule configuration. If failures are controller-wide affecting all ingress resources, the ingress controller deployment or service configuration is the root cause.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including ingress controller deployment configuration and ingress rule path matching, check for gradual issues like ingress controller pod eviction or service endpoint changes, verify external dependencies like load balancer configuration or ingress controller image availability, examine historical patterns of ingress routing failures, check for EKS AWS Load Balancer Controller configuration issues, verify EKS ingress controller class annotation. Routing failures may result from ingress controller deployment issues, ingress rule path matching problems, ingress controller service configuration errors, EKS AWS Load Balancer Controller misconfiguration, or ingress controller class annotation issues rather than immediate ingress resource changes.
