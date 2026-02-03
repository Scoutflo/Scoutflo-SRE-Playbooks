---
title: Error Connection Refused When Accessing Service - Service
weight: 289
categories:
  - kubernetes
  - service
---

# ErrorConnectionRefusedWhenAccessingService-service

## Meaning

Connections to Kubernetes Services are being refused (triggering KubeServiceNotReady alerts) because the service has no endpoints, the service port is not listening, pods are not ready, or kube-proxy is not forwarding traffic correctly. Service connections return connection refused errors, Endpoints resources show no ready addresses, and pods matching the service selector may show NotReady state. This affects the network plane and prevents service connectivity, typically caused by pod readiness failures, port configuration issues, or kube-proxy problems; applications cannot connect to services and may show errors.

## Impact

Service connections are refused; applications cannot connect to services; service endpoints exist but are not accepting connections; KubeServiceNotReady alerts fire; load balancing fails; cluster-internal service communication is blocked; service DNS resolves but connections fail; applications cannot reach backend services. Service connections return connection refused errors indefinitely; Endpoints resources show no ready addresses; applications cannot connect to services and may experience errors or performance degradation; cluster-internal service communication is blocked.

## Playbook

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its configuration, ports, selector, and current state.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify recent issues.

3. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

4. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, have the correct labels, and are ready to accept connections.

5. From a test pod, execute curl or telnet to the service endpoint to test connectivity and verify if connections are refused.

6. Check the pod `<pod-name>` associated with the service and verify if the application is listening on the expected port by executing port checks.

7. Check kube-proxy pod status in the `kube-system` namespace to verify if the service proxy is functioning correctly.

## Diagnosis

1. Analyze service endpoints from Playbook to verify service has ready endpoints. If endpoints list is empty or shows no ready addresses, connections are refused because no backend pods are available.

2. If endpoints are empty, check service selector against pod labels from Playbook. If selector does not match pod labels, no pods are selected as endpoints and all connections are refused.

3. If selector matches, check pod Ready condition from Playbook. If pods are not Ready (failing readiness probes or still starting), they are excluded from endpoints. Check pod events for readiness probe failure details.

4. If pods are Ready and in endpoints, verify application is listening on the expected port from Playbook. If container process is not bound to the targetPort, connections reach the pod but are refused by the OS.

5. If application is listening, check service port and targetPort configuration from Playbook. If port mismatch exists (service port differs from targetPort or container port), traffic is forwarded to wrong ports.

6. If port configuration is correct, check kube-proxy status from Playbook. If kube-proxy is not running or iptables/ipvs rules are stale, traffic routing to endpoints fails.

7. If kube-proxy is healthy, check NetworkPolicy rules from Playbook for ingress policies. If policies block traffic on the service port or from the client source, connections are refused at the network layer.

**If no configuration issue is found**: Check if pods have multiple containers and traffic is routed to wrong container port, verify if init containers are blocking main container startup, review if liveness probes are killing pods before readiness is achieved, and examine if resource limits cause application crashes after startup.

