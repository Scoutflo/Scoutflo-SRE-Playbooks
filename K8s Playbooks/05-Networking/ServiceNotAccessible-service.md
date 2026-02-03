---
title: Service Not Accessible - Service
weight: 207
categories:
  - kubernetes
  - service
---

# ServiceNotAccessible-service

## Meaning

Kubernetes Services are not exposing or forwarding traffic to backend pods (triggering alerts like KubeServiceNotReady or service-related alerts) because the service has no endpoints, selector mismatches prevent pod association, port configurations are incorrect, network policies are blocking traffic, or the service type configuration is invalid. Services show no endpoints in kubectl, Endpoints resources show no ready addresses, and service DNS resolution fails or returns connection refused errors. This affects the network plane and prevents service discovery and load balancing, typically caused by pod selector mismatches, NetworkPolicy restrictions, or service configuration errors; applications cannot access services and may show errors.

## Impact

KubeServiceNotReady alerts fire; services cannot route traffic to pods; applications are unreachable through service endpoints; service DNS resolution fails; load balancing does not work; pods receive no traffic; service endpoints show no ready addresses; service status shows no endpoints; cluster-internal service discovery fails. Services show no endpoints indefinitely; Endpoints resources show no ready addresses; service DNS resolution fails; applications cannot access services and may experience errors or performance degradation.

## Playbook

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its spec, status, and selector.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify recent issues.

3. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

4. List EndpointSlice resources for the Service `<service-name>` in namespace `<namespace>` (Kubernetes 1.21+) and verify that pods are registered as endpoints and check their readiness status.

5. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, and have the correct labels that match the service selector.

6. Verify kube-proxy mode by checking kube-proxy ConfigMap in `kube-system` namespace to determine if iptables or ipvs mode is configured.

7. From a test pod, execute nslookup for `<service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries to verify service DNS resolution.

8. From a test pod, execute curl or wget to the service endpoint to test connectivity and verify traffic forwarding.

9. List NetworkPolicy objects in namespace `<namespace>` and review their rules to check if policies are blocking service traffic.

## Diagnosis

1. Analyze service events and endpoints from Playbook to identify if service has ready endpoints. If endpoints or EndpointSlice shows no ready addresses, the primary issue is pod selection or readiness.

2. If endpoints are empty, check service selector against pod labels from Playbook. If selector does not match any pods, verify pod labels and service selector configuration for mismatches (typos, missing labels, or incorrect values).

3. If selector matches pods, check pod status and Ready condition from Playbook. If pods are not Ready (failing readiness probes), they are excluded from endpoints. Check pod events for probe failure reasons.

4. If pods are Ready, check NetworkPolicy rules from Playbook for policies blocking ingress to service pods. If restrictive ingress policies exist without rules allowing service traffic, connections are blocked.

5. If NetworkPolicy allows traffic, verify DNS resolution from Playbook connectivity tests. If nslookup for service name fails, CoreDNS is not resolving service names correctly.

6. If DNS works, check kube-proxy status and mode from Playbook. If kube-proxy is not running or ConfigMap shows incorrect iptables/ipvs configuration, service routing rules are not programmed.

7. If kube-proxy is healthy, verify service port and targetPort configuration from Playbook matches pod container ports. If ports do not align, traffic is forwarded to wrong or closed ports.

**If no configuration issue is found**: Check EndpointSlice controller status for Kubernetes 1.21+, verify service type is correctly configured (ClusterIP, NodePort, LoadBalancer), review if externalTrafficPolicy affects accessibility, and examine if service session affinity settings cause unexpected behavior.

