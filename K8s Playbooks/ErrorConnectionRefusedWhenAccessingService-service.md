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

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its configuration, ports, and selector to verify service setup.

2. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

3. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, have the correct labels, and are ready to accept connections.

4. From a test pod, execute `curl` or `telnet` to the service endpoint using Pod Exec tool to test connectivity and verify if connections are refused.

5. Check the pod `<pod-name>` associated with the service and verify if the application is listening on the expected port by executing port checks using Pod Exec tool.

6. Check kube-proxy pod status in the kube-system namespace to verify if the service proxy is functioning correctly.

## Diagnosis

1. Compare the connection refused error timestamps with pod Ready condition transition times for pods matching the service selector, and check whether pods became NotReady within 5 minutes before connection refused errors.

2. Compare the connection refused error timestamps with service port configuration modification timestamps, and check whether port changes occurred within 30 minutes before connection refused errors.

3. Compare the connection refused error timestamps with pod application restart or crash timestamps, and check whether application failures occurred within 5 minutes before connection refused errors.

4. Compare the connection refused error timestamps with endpoint removal timestamps, and check whether endpoints were removed within 5 minutes before connection refused errors.

5. Compare the connection refused error timestamps with kube-proxy restart or failure timestamps, and check whether proxy issues occurred within 5 minutes before connection refused errors.

6. Compare the connection refused error timestamps with NetworkPolicy modification timestamps that may affect service traffic, and check whether policy changes occurred within 10 minutes before connection refused errors.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour), review kube-proxy logs for gradual performance degradation, check for intermittent endpoint update issues, examine if service port configurations drifted over time, verify if application port listening issues developed gradually, and check for network path problems that may have accumulated. Connection refused errors may result from gradual service or infrastructure degradation rather than immediate configuration changes.

