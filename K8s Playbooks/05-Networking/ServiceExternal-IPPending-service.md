---
title: Service External-IP Pending - Service
weight: 241
categories:
  - kubernetes
  - service
---

# ServiceExternal-IPPending-service

## Meaning

LoadBalancer services are stuck with External-IP in Pending state (triggering service-related alerts) because the cloud provider's load balancer provisioning is failing, cloud provider integration is misconfigured, insufficient permissions prevent load balancer creation, or the cloud provider API is unavailable. Services show External-IP Pending in status, service events show FailedToCreateLoadBalancer errors, and cloud controller manager pods may show failures in kube-system namespace. This affects the network plane and prevents external access to services, typically caused by cloud provider integration issues or permission problems; applications are unreachable from outside the cluster.

## Impact

LoadBalancer services have no external IP; external traffic cannot reach services; services remain in Pending state; load balancer provisioning fails; KubeServiceNotReady alerts may fire; service status shows External-IP Pending; applications are unreachable from outside the cluster; cloud provider integration issues prevent service exposure. Services show External-IP Pending indefinitely; service events show FailedToCreateLoadBalancer errors; cloud controller manager pods may show failures; applications are unreachable from outside the cluster and may show errors.

## Playbook

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its status, `status.loadBalancer.ingress`, and conditions to verify External-IP Pending state.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify load balancer provisioning failures.

3. List nodes and check their cloud provider labels and annotations to verify if the cluster is properly integrated with the cloud provider.

4. Check cloud provider integration by verifying node provider IDs, cloud controller manager pod status, or cloud provider service account permissions.

5. Retrieve logs from the service controller or cloud controller manager pod in the `kube-system` namespace and filter for load balancer provisioning errors.

6. Verify cloud provider account permissions and quotas to ensure load balancer creation is allowed and quota limits are not exceeded.

## Diagnosis

1. Analyze service events from Playbook to identify load balancer provisioning errors. If events show FailedToCreateLoadBalancer or similar errors, the event message indicates the specific provisioning failure reason.

2. If events show provisioning failures, check cloud controller manager pod status from Playbook. If cloud-controller-manager pods are not running, crashing, or showing errors, load balancer provisioning requests are not processed.

3. If cloud controller manager is healthy, review cloud controller manager logs from Playbook for API errors. If logs show authentication failures, permission denied, or API quota exceeded errors, cloud provider credentials or permissions are insufficient.

4. If credentials are valid, check service configuration from Playbook. If service lacks required annotations for cloud provider (e.g., load balancer type, subnet selection), provisioning fails due to incomplete configuration.

5. If configuration is complete, verify node cloud provider labels from Playbook. If nodes lack required provider ID or cloud labels, cloud controller cannot determine where to provision load balancer.

6. If node labels are correct, check cloud provider quota and limits. If load balancer quota is exhausted or account limits are reached, new load balancers cannot be created until resources are freed.

**If no provisioning issue is found**: Verify cloud provider API endpoint is reachable from the cluster, check if VPC or subnet configuration supports load balancer creation, review if required IAM roles/service accounts have load balancer management permissions, and examine if cloud provider is experiencing regional outages or service degradation.

