---
title: Node Exporter Down
weight: 39
categories: [kubernetes, node]
---

# NodeExporterDown

## Meaning

Node Exporter is not running or not responding (triggering NodeExporterDown alerts) because the monitoring agent that collects node-level metrics has failed or is unreachable. Prometheus cannot scrape node metrics, node health visibility is lost, and node-level alerting is blind. This affects cluster observability; node issues may go undetected; capacity planning data is incomplete; troubleshooting is impaired.

## Impact

NodeExporterDown alerts fire; no node-level metrics available; CPU, memory, disk, network monitoring is blind; other node alerts cannot fire due to missing data; dashboards show gaps; capacity planning is affected; proactive alerting is disabled for this node; troubleshooting requires manual inspection; SRE visibility is reduced.

## Playbook

1. Verify node-exporter pod or DaemonSet status in the monitoring namespace (often prometheus, monitoring, or kube-system).

2. Check if node-exporter pod is running on the affected node using kubectl get pods -o wide.

3. Retrieve node-exporter pod logs for errors preventing operation.

4. Verify Prometheus ServiceMonitor or scrape configuration targets the correct port and path.

5. Check network connectivity from Prometheus to node-exporter port (usually 9100).

6. Verify node-exporter DaemonSet tolerations allow scheduling on all nodes including tainted nodes.

7. Check if network policies are blocking Prometheus from scraping node-exporter.

## Diagnosis

Verify pod existence and status on the affected node and identify if pod is missing, crashed, or pending, using pod status and events as supporting evidence.

Check DaemonSet tolerations and verify whether the node has taints that prevent node-exporter scheduling, using node taints and DaemonSet spec as supporting evidence.

Verify Prometheus scrape configuration and confirm service discovery is working correctly for node-exporter endpoints, using Prometheus targets page and service discovery as supporting evidence.

Check network policies and verify whether ingress to port 9100 from Prometheus namespace is allowed, using network policy rules and connectivity tests as supporting evidence.

Analyze node-exporter pod logs for startup failures (port already in use, permission denied, configuration errors), using pod logs as supporting evidence.

If no correlation is found within the specified time windows: restart node-exporter pod, update DaemonSet tolerations, fix network policy rules, verify ServiceMonitor configuration, check resource constraints preventing pod scheduling.
