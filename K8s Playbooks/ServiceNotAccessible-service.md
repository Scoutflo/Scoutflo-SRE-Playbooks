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

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its spec, status, and selector to verify configuration.

2. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and check their readiness status.

3. List EndpointSlice resources for the Service `<service-name>` in namespace `<namespace>` (Kubernetes 1.21+) and verify that pods are registered as endpoints and check their readiness status.

4. Retrieve pods matching the service selector in namespace `<namespace>` and verify they exist, are running, and have the correct labels that match the service selector.

5. Verify kube-proxy mode by checking kube-proxy ConfigMap in kube-system namespace to determine if iptables or ipvs mode is configured.

6. From a test pod, execute `nslookup <service-name>.<namespace>.svc.cluster.local` or equivalent DNS queries using Pod Exec tool to verify service DNS resolution.

7. From a test pod, execute `curl` or `wget` to the service endpoint using Pod Exec tool to test connectivity and verify traffic forwarding.

8. List NetworkPolicy objects in namespace `<namespace>` and review their rules to check if policies are blocking service traffic.

## Diagnosis

1. Compare the service accessibility failure timestamps with pod Ready condition transition times for pods matching the service selector, and check whether pods became NotReady within 5 minutes before service failures.

2. Compare the service accessibility failure timestamps with EndpointSlice controller failure timestamps (Kubernetes 1.21+), and check whether EndpointSlice updates stopped within 5 minutes before service issues.

3. Compare the service accessibility failure timestamps with service selector or port modification timestamps, and check whether service configuration changes occurred within 30 minutes before accessibility issues.

4. Compare the service accessibility failure timestamps with pod label change timestamps, and check whether pod labels were modified within 30 minutes before service selector mismatches.

5. Compare the service accessibility failure timestamps with kube-proxy mode change or restart timestamps, and check whether kube-proxy issues occurred within 5 minutes before service failures.

6. Compare the service accessibility failure timestamps with NetworkPolicy creation or modification timestamps, and check whether new or updated policies were applied within 10 minutes before service traffic was blocked.

7. Compare the service accessibility failure timestamps with endpoint controller restart or failure timestamps, and check whether endpoint updates stopped within 5 minutes before service issues.

8. Compare the service accessibility failure timestamps with cluster network changes, kube-proxy restarts, or service controller issues, and check whether infrastructure changes occurred within 1 hour before service failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review endpoint controller logs for processing delays, check for gradual pod label drift, examine DNS resolution issues that may have developed over time, verify if kube-proxy is experiencing performance degradation, and check for network path issues that may have accumulated. Service accessibility issues may result from gradual system degradation rather than immediate configuration changes.

