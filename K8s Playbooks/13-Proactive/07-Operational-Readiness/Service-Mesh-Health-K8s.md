# Service Mesh Health

## Meaning

Service mesh health indicates that service mesh components are unhealthy or service mesh connectivity issues are detected (triggering alerts like ServiceMeshUnhealthy or ServiceMeshConnectivityFailed) because service mesh health checks fail, service mesh connectivity is impaired, service mesh configuration errors occur, service mesh monitoring indicates problems, or service mesh components are unavailable. Service mesh health checks show failures, service mesh connectivity is impaired, service mesh configuration errors are detected, and service mesh monitoring indicates problems. This affects the dependency management layer and service mesh reliability, typically caused by service mesh component failures, service mesh configuration issues, service mesh connectivity problems, or service mesh monitoring failures; if service mesh health affects container workloads, container service mesh may be unhealthy and applications may experience service mesh-related failures.

## Impact

ServiceMeshUnhealthy alerts fire; ServiceMeshConnectivityFailed alerts fire; service mesh health cannot be verified; service mesh connectivity issues are detected; service mesh reliability is compromised; service-to-service communication may fail. Service mesh health checks show failures; if service mesh health affects container workloads, container service mesh may be unhealthy, pod service mesh connectivity may fail, and container applications may experience service mesh-related failures; applications may experience service communication failures or service mesh health issues.

## Playbook

1. List pods in namespace <service-mesh-namespace> with label app=istiod and wide output to retrieve service mesh control plane pod status and verify control plane component health.
2. List recent events in namespace <service-mesh-namespace> sorted by timestamp to identify service mesh component failures, connectivity errors, or configuration issues.
3. Describe configmap <service-mesh-configmap-name> in namespace <namespace> to inspect the service mesh configuration and verify mesh health settings and component availability.
4. Retrieve Prometheus metrics for service mesh including mesh_health_status and service_connectivity_status over the last 24 hours to identify service mesh health issues.
5. Retrieve logs from service mesh control plane pods in namespace `<namespace>` and filter for service mesh health check failures or connectivity error patterns within the last 24 hours.
6. Retrieve service mesh virtual service `<virtual-service-name>` configuration and verify virtual service health and routing configuration, checking virtual service health.
7. Compare service mesh health check failure timestamps with service mesh component error timestamps within 5 minutes and verify whether component errors cause health check failures, using service mesh configuration data as supporting evidence.
8. Retrieve Prometheus metrics for service mesh including request_count and error_rate over the last 24 hours to identify service mesh performance issues.
9. List service mesh routes and verify route health and destination service availability, checking service mesh routing health.

## Diagnosis

1. Review the control plane pod status from Step 1. If istiod or other control plane pods are not running or showing errors, this is the root cause of service mesh health issues. Focus on restoring control plane functionality.

2. Analyze the mesh health metrics from Step 4. If mesh_health_status shows unhealthy or service_connectivity_status shows failures, identify which specific components or services are affected based on metric labels.

3. If Step 5 control plane logs show health check failures or connectivity errors, examine the error patterns to determine whether issues are authentication-related, configuration-related, or network-related.

4. Review virtual service health from Step 6. If virtual services show misconfigurations, then routing may be failing. If virtual services are healthy, then underlying connectivity is the issue.

5. If Step 8 request metrics show high error rates or degraded performance, then service mesh is functioning but degraded. If metrics show zero traffic, then connectivity is completely broken.

If analysis is inconclusive: Examine events from Step 2 for component failures or configuration issues. Review route health from Step 9 to determine whether destination services are available. Determine whether health issues are affecting all services (suggesting control plane problems) or specific services (suggesting configuration or network issues for those services).
