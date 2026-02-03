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

1. Describe the Service `<service-name>` in namespace `<namespace>` to inspect its status and endpoint configuration.

2. Retrieve events for the Service `<service-name>` in namespace `<namespace>` sorted by timestamp to identify patterns in service issues.

3. List Endpoints for the Service `<service-name>` in namespace `<namespace>` over time to identify if endpoints are fluctuating or changing frequently.

4. Retrieve pods associated with the service and monitor their Ready condition transitions to verify if pods are frequently becoming NotReady and back.

5. Check kube-proxy pod status and logs in the kube-system namespace to verify if proxy issues are causing intermittent failures.

6. From a test pod, execute repeated curl or connectivity tests to the service endpoint to verify intermittent connectivity patterns.

## Diagnosis

1. Analyze service events and endpoint changes from Playbook to identify patterns in endpoint availability. If endpoints show frequent additions and removals, backend pods are unstable and transitioning between Ready and NotReady states.

2. If endpoints are fluctuating, check pod Ready condition transitions from Playbook data. If pods frequently transition between Ready and NotReady, investigate pod health check failures (liveness/readiness probe issues).

3. If pods are stable, check service selector against pod labels from Playbook. If selector does not consistently match pods due to label changes or deployment updates, endpoints become intermittently available.

4. If selector matching is correct, check kube-proxy pod status and logs from Playbook. If kube-proxy shows intermittent failures or restarts, iptables/ipvs rules are not consistently programmed.

5. If kube-proxy is stable, check NetworkPolicy rules from Playbook for policies affecting service traffic. If policies intermittently block traffic based on dynamic selectors or namespace conditions, connectivity becomes unreliable.

6. If NetworkPolicy is not affecting traffic, verify DNS resolution for service name from Playbook connectivity tests. If DNS resolution is slow or intermittently fails, service discovery becomes unreliable.

**If no configuration issue is found**: Review pod resource utilization for OOMKilled or CPU throttling events, check node health for intermittent network issues, verify if load balancer health checks are too aggressive causing endpoint flapping, and examine if application startup time exceeds readiness probe initial delay.

