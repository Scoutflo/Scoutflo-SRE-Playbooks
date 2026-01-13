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

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its status, `status.loadBalancer.ingress`, and conditions to verify External-IP Pending state.

2. List events in namespace `<namespace>` and filter for service-related events, focusing on events with reasons such as `FailedToCreateLoadBalancer` or messages indicating load balancer provisioning failures.

3. List nodes and check their cloud provider labels and annotations to verify if the cluster is properly integrated with the cloud provider.

4. Check cloud provider integration by verifying node provider IDs, cloud controller manager pod status, or cloud provider service account permissions.

5. Retrieve logs from the service controller or cloud controller manager pod in the kube-system namespace and filter for load balancer provisioning errors.

6. Verify cloud provider account permissions and quotas to ensure load balancer creation is allowed and quota limits are not exceeded.

## Diagnosis

1. Compare the service External-IP Pending timestamps with cloud controller manager pod restart or failure timestamps, and check whether controller issues occurred within 5 minutes before load balancer provisioning failures.

2. Compare the service External-IP Pending timestamps with node cloud provider label or annotation modification timestamps, and check whether cloud provider integration changes occurred within 30 minutes before provisioning failures.

3. Compare the service External-IP Pending timestamps with cloud provider API unavailability or error timestamps, and check whether provider API issues occurred within 10 minutes before provisioning failures.

4. Compare the service External-IP Pending timestamps with service controller configuration modification timestamps, and check whether controller settings were changed within 30 minutes before provisioning failures.

5. Compare the service External-IP Pending timestamps with cloud provider quota or limit exhaustion timestamps, and check whether quota limits were reached within 30 minutes before provisioning failures.

6. Compare the service External-IP Pending timestamps with cluster upgrade or cloud provider integration update timestamps, and check whether infrastructure changes occurred within 1 hour before load balancer provisioning failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review cloud controller manager logs for gradual provisioning issues, check for intermittent cloud provider API connectivity problems, examine if cloud provider permissions were gradually restricted, verify if quota limits accumulated over time, and check for cloud provider service degradation that may have developed gradually. External-IP Pending issues may result from gradual cloud provider integration problems rather than immediate changes.

