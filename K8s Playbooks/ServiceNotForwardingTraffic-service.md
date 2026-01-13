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

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its spec, selector, and port configuration to verify service configuration.

2. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

3. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, have the correct labels that match the service selector, and are ready.

4. From a test pod, execute `curl` or `wget` to the service endpoint using Pod Exec tool to test connectivity and verify if traffic forwarding works.

5. Check kube-proxy pod status in the kube-system namespace to verify if the service proxy is functioning correctly.

6. List events in namespace `<namespace>` and filter for service-related events, focusing on events with reasons such as `FailedToUpdateEndpoint` or messages indicating endpoint update failures.

## Diagnosis

1. Compare the service traffic forwarding failure timestamps with pod Ready condition transition times for pods matching the service selector, and check whether pods became NotReady within 5 minutes before service forwarding failures.

2. Compare the service traffic forwarding failure timestamps with service selector or port modification timestamps, and check whether service configuration changes occurred within 30 minutes before forwarding failures.

3. Compare the service traffic forwarding failure timestamps with pod label change timestamps, and check whether pod labels were modified within 30 minutes before service selector mismatches.

4. Compare the service traffic forwarding failure timestamps with kube-proxy restart or failure timestamps, and check whether proxy issues occurred within 5 minutes before service forwarding failures.

5. Compare the service traffic forwarding failure timestamps with NetworkPolicy modification timestamps that may affect service traffic, and check whether policy changes occurred within 10 minutes before forwarding failures.

6. Compare the service traffic forwarding failure timestamps with endpoint controller restart or failure timestamps, and check whether endpoint updates stopped within 5 minutes before service forwarding failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review kube-proxy logs for gradual performance degradation, check for intermittent endpoint update issues, examine if service selectors drifted over time, verify if network path issues developed gradually, and check for DNS or service discovery issues affecting service connectivity. Service forwarding failures may result from gradual infrastructure degradation rather than immediate configuration changes.

