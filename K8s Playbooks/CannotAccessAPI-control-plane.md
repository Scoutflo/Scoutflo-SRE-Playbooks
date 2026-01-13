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

1. Retrieve cluster information including the API server endpoint and record the exact URL and IP/port being used for API access.

2. From a pod inside the cluster, execute `curl -k https://<api-server-ip>:6443` (or the control plane hostname) to test basic TCP/TLS connectivity to the API server endpoint.

3. On a control plane node, verify that port 6443 is listening by running `netstat -tuln | grep 6443` (or an equivalent command) to confirm the API server process is bound to the expected interface and port.

4. Check firewall and security group rules on the control plane node and surrounding network (cloud firewall, security groups, NACLs) for rules that might block ingress or egress on port 6443.

5. List NetworkPolicy resources in `kube-system` and other relevant namespaces and inspect whether any policies restrict traffic from external clients or ingress gateways to the API server.

6. List pods in `kube-system` and filter for the API server pods or control plane components, verifying that the API server pod is running and not restarting.

## Diagnosis

1. Compare the external access failure timestamps (when `kubectl` or client requests first began to fail) with firewall rule modification timestamps from your infrastructure or cloud provider, and check whether failures begin within 10 minutes after a firewall change.

2. Compare the access failure timestamps with NetworkPolicy modification timestamps from the cluster, and verify whether new or changed policies appear within 10 minutes before failures start.

3. Compare the access failure timestamps with API server pod restart timestamps and ConfigMap/Deployment change timestamps in `kube-system`, and look for changes or restarts occurring within 5 minutes of the first failures.

4. Compare the access failure timestamps with load balancer configuration change timestamps from your load balancer logs or control plane, and check for changes that occurred within 10 minutes before or after the first failures.

5. Compare the access failure timestamps with security group or network ACL update timestamps from your infrastructure, and check whether rules affecting the API server IPs or ports were modified within 10 minutes of the failures.

6. Compare the access failure timestamps with cluster infrastructure or maintenance window timestamps recorded in your change management system, and check whether failures started within 1 hour of planned maintenance or upgrade activities.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 1 hour → 2 hours), check cloud provider logs for firewall or security group changes that may not be recorded in cluster events, review load balancer configuration history, examine network routing changes, and verify if API server endpoints or DNS records were modified. Network connectivity issues may have infrastructure-level causes not immediately visible in Kubernetes resources.

