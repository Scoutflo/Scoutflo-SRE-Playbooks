---
title: Service Not Forwarding Traffic - Service
weight: 265
categories:
  - kubernetes
  - service
---

# ServiceNotForwardingTraffic-service

## Meaning

Kubernetes Services are not forwarding traffic to backend pods (triggering KubeServiceNotReady alerts) because the service has no endpoints, the selector does not match any pods, port configurations are incorrect, or kube-proxy is not functioning. Services show no endpoints in kubectl, Endpoints resources show no ready addresses, and kube-proxy pods may show failures in kube-system namespace. This affects the network plane and prevents traffic forwarding, typically caused by pod selector mismatches, kube-proxy failures, or port configuration errors; applications cannot access services and may show errors.

## Impact

Services cannot route traffic to pods; applications are unreachable through service endpoints; service DNS resolution works but connections fail; load balancing does not work; pods receive no traffic; KubeServiceNotReady alerts fire; service endpoints show no ready addresses; cluster-internal service communication fails. Services show no endpoints indefinitely; Endpoints resources show no ready addresses; kube-proxy pods may show failures; applications cannot access services and may experience errors or performance degradation.

## Playbook

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its spec, selector, and port configuration.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify endpoint update failures.

3. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

4. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, have the correct labels that match the service selector, and are ready.

5. From a test pod, execute curl or wget to the service endpoint to test connectivity and verify if traffic forwarding works.

6. Check kube-proxy pod status in the `kube-system` namespace to verify if the service proxy is functioning correctly.

## Diagnosis

1. Analyze service endpoints from Playbook to identify if service has any ready endpoints. If endpoints list is empty or shows no ready addresses, the issue is pod selection (selector mismatch or no matching pods).

2. If endpoints are empty, check service selector against pod labels from Playbook data. If service selector keys or values do not match any pod labels in the namespace, no pods are selected as endpoints.

3. If selector matches pods, check pod Ready condition from Playbook. If pods exist but are NotReady, they are excluded from service endpoints until they pass readiness probes.

4. If pods are Ready and should be endpoints, verify service port configuration from Playbook matches pod container ports. If targetPort does not match container port, traffic forwarding fails.

5. If port configuration is correct, check kube-proxy status from Playbook data. If kube-proxy pods are not running or show failures, iptables/ipvs rules for service routing are not programmed.

6. If kube-proxy is healthy, check NetworkPolicy rules from Playbook for ingress policies blocking traffic to service pods. If policies restrict ingress from service CIDR or other pods, traffic is blocked at the network level.

**If no configuration issue is found**: Verify endpoint controller is functioning by checking kube-controller-manager logs, review if EndpointSlice controller is enabled and working (Kubernetes 1.21+), and check if service account tokens or RBAC permissions prevent endpoint updates.

