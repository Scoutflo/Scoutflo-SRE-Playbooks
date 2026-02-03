---
title: Cannot Access API - Control Plane
weight: 255
categories:
  - kubernetes
  - control-plane
---

# CannotAccessAPI-control-plane

## Meaning

External clients such as kubectl, CI/CD systems, or external controllers cannot establish TCP/TLS connections to the Kubernetes API server endpoint (potentially triggering KubeAPIDown alerts), indicating a control-plane reachability or exposure problem. API server connectivity failures prevent external access to the cluster control plane.

## Impact

All kubectl commands fail; cluster management operations cannot be performed; controllers cannot reconcile state; cluster becomes unmanageable; applications may continue running but cannot be updated or scaled; KubeAPIDown alerts may fire; API server unreachable from external networks; connection timeouts or connection refused errors occur; cluster management tools fail.

## Playbook

1. Describe API server pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, restarts, conditions, and any error messages.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for API server connectivity errors or failures.

3. Retrieve cluster information including the API server endpoint and record the exact URL and IP/port being used for API access.

4. From a pod inside the cluster, verify TCP/TLS connectivity to the API server endpoint to test basic connectivity.

5. On a control plane node, verify that the API server is listening on the expected port and interface to confirm the API server process is bound correctly.

6. Check firewall and security group rules on the control plane node and surrounding network (cloud firewall, security groups, NACLs) for rules that might block ingress or egress on port 6443.

7. List NetworkPolicy resources in kube-system and other relevant namespaces and inspect whether any policies restrict traffic from external clients or ingress gateways to the API server.

## Diagnosis

1. Analyze API server pod events from Playbook to identify if API server is running and healthy. If events show pod failures, restarts, or unhealthy status, API server unavailability is the root cause rather than external access issues.

2. If events indicate API server is healthy, verify network connectivity from Playbook steps 4-5. If API server is running but external access fails, network path issues are the likely cause.

3. If events indicate NetworkPolicy changes, examine policy modifications from Playbook step 7. If NetworkPolicy events occurred before access failures began, policy changes may have blocked external client access.

4. If events indicate firewall or security group changes, correlate infrastructure change timestamps with failure onset. If firewall modifications occurred at timestamps preceding access failures, network security changes blocked connectivity.

5. If events indicate load balancer issues, verify load balancer status and configuration. If load balancer events show configuration changes or health check failures at access failure timestamps, load balancer issues are the root cause.

6. If events indicate API server configuration changes (ConfigMaps, Deployments), correlate change timestamps with failure onset. If API server configuration was modified before access failures, configuration changes may have affected binding or TLS settings.

7. If events indicate maintenance or upgrade activity, correlate activity timestamps with access failure onset. If maintenance events occurred within 1 hour before failures, planned changes may have unintentionally affected external access.

**If no correlation is found**: Extend the search window (10 minutes to 30 minutes, 1 hour to 2 hours), check cloud provider logs for firewall or security group changes that may not be recorded in cluster events, review load balancer configuration history, examine network routing changes, and verify if API server endpoints or DNS records were modified. Network connectivity issues may have infrastructure-level causes not immediately visible in Kubernetes resources.

