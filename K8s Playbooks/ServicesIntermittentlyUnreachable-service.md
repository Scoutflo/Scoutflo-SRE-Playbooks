---
title: Services Intermittently Unreachable - Service
weight: 288
categories:
  - kubernetes
  - service
---

# ServicesIntermittentlyUnreachable-service

## Meaning

Kubernetes Services are intermittently unreachable (triggering KubeServiceNotReady alerts) because endpoints are fluctuating, pods are frequently becoming NotReady, kube-proxy is experiencing issues, or network policies are intermittently blocking traffic. Service endpoints fluctuate between available and unavailable, pods show frequent Ready/NotReady transitions, and kube-proxy pods may show intermittent failures. This affects the network plane and causes unstable service connectivity, typically caused by pod instability, kube-proxy issues, or NetworkPolicy restrictions; applications experience sporadic connectivity issues.

## Impact

Services are intermittently unavailable; connections fail randomly; applications experience sporadic connectivity issues; service endpoints fluctuate; KubeServiceNotReady alerts fire intermittently; load balancing is inconsistent; service DNS resolution works intermittently; cluster-internal service communication is unreliable. Service endpoints fluctuate between available and unavailable; pods show frequent Ready/NotReady transitions; applications experience sporadic connectivity issues and may show errors; cluster-internal service communication is unreliable.

## Playbook

1. Retrieve the Service `<service-name>` in namespace `<namespace>` and inspect its status and endpoint configuration to verify service stability.

2. List Endpoints for the Service `<service-name>` in namespace `<namespace>` over time to identify if endpoints are fluctuating or changing frequently.

3. Retrieve pods associated with the service and monitor their Ready condition transitions to verify if pods are frequently becoming NotReady and back.

4. Check kube-proxy pod status and logs in the kube-system namespace to verify if proxy issues are causing intermittent failures.

5. List events in namespace `<namespace>` and filter for service-related events over time to identify patterns in endpoint changes or service issues.

6. From a test pod, execute repeated `curl` or connectivity tests to the service endpoint using Pod Exec tool to verify intermittent connectivity patterns.

## Diagnosis

1. Compare the service unreachable event timestamps with pod Ready condition transition times for backend pods, and check whether pods are frequently transitioning between Ready and NotReady within 5 minutes of unreachable events.

2. Compare the service unreachable event timestamps with endpoint change timestamps, and check whether endpoints are being added or removed frequently within 5 minutes of unreachable events.

3. Compare the service unreachable event timestamps with kube-proxy restart or error timestamps, and check whether proxy issues occur intermittently within 5 minutes of unreachable events.

4. Compare the service unreachable event timestamps with NetworkPolicy modification or enforcement timestamps, and check whether policy changes occur intermittently within 10 minutes of unreachable events.

5. Compare the service unreachable event timestamps with pod restart or crash timestamps, and check whether frequent pod restarts occur within 5 minutes of unreachable events.

6. Compare the service unreachable event timestamps with node network interface or connectivity issue timestamps, and check whether network problems occur intermittently within 10 minutes of unreachable events.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes), review service endpoint controller logs for gradual processing issues, check for intermittent network path problems, examine if pod health checks are flapping, verify if kube-proxy is experiencing gradual performance degradation, and check for DNS resolution issues that may occur intermittently. Intermittent service unreachability may result from cumulative instability rather than immediate failures.

