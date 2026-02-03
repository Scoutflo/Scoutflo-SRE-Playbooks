# Service Mesh Health

## Meaning

Service mesh health indicates that service mesh components are unhealthy or service mesh connectivity issues are detected (triggering alarms like ServiceMeshUnhealthy or ServiceMeshConnectivityFailed) because service mesh health checks fail, service mesh connectivity is impaired, service mesh configuration errors occur, service mesh monitoring indicates problems, or service mesh components are unavailable. Service mesh health checks show failures, service mesh connectivity is impaired, service mesh configuration errors are detected, and service mesh monitoring indicates problems. This affects the dependency management layer and service mesh reliability, typically caused by service mesh component failures, service mesh configuration issues, service mesh connectivity problems, or service mesh monitoring failures; if service mesh health affects container workloads, container service mesh may be unhealthy and applications may experience service mesh-related failures.

## Impact

ServiceMeshUnhealthy alarms fire; ServiceMeshConnectivityFailed alarms fire; service mesh health cannot be verified; service mesh connectivity issues are detected; service mesh reliability is compromised; service-to-service communication may fail. Service mesh health checks show failures; if service mesh health affects container workloads, container service mesh may be unhealthy, pod service mesh connectivity may fail, and container applications may experience service mesh-related failures; applications may experience service communication failures or service mesh health issues.

## Playbook

1. Retrieve App Mesh service mesh `<mesh-name>` configuration and inspect mesh health status and component availability, verifying service mesh accessibility.
2. Retrieve CloudWatch metrics for App Mesh service mesh including MeshHealthStatus and ServiceConnectivityStatus over the last 24 hours to identify service mesh health issues.
3. Query CloudWatch Logs for log groups containing App Mesh events and filter for service mesh health check failures or connectivity error patterns within the last 24 hours.
4. Retrieve App Mesh virtual service `<virtual-service-name>` configuration and verify virtual service health and routing configuration, checking virtual service health.
5. Retrieve App Mesh virtual node `<virtual-node-name>` configuration and verify virtual node health and backend service connectivity, checking virtual node health.
6. Compare service mesh health check failure timestamps with service mesh component error timestamps within 5 minutes and verify whether component errors cause health check failures, using App Mesh service mesh configuration data as supporting evidence.
7. Retrieve CloudWatch metrics for App Mesh service mesh including RequestCount and ErrorRate over the last 24 hours to identify service mesh performance issues.
8. List App Mesh service mesh routes and verify route health and destination service availability, checking service mesh routing health.

## Diagnosis

1. **Analyze mesh health metrics from Step 2**: If MeshHealthStatus shows unhealthy, identify which component is failing. If ServiceConnectivityStatus shows failures, service-to-service communication is broken. If both are healthy, mesh infrastructure is functional.

2. **Evaluate virtual node health from Step 5**: If virtual nodes are unhealthy, backend services are not responding. If virtual node configuration has errors, connectivity configuration is incorrect. If virtual nodes are healthy, backend connectivity is working.

3. **Review virtual service health from Step 4**: If virtual services show routing errors, traffic cannot reach intended destinations. If virtual service configuration is incorrect, requests may be misrouted.

4. **Cross-reference with error logs from Step 3**: If logs show connection timeout errors, network connectivity issues exist. If logs show TLS errors, certificate configuration is incorrect. If logs show routing errors, mesh route configuration needs review.

5. **Assess mesh traffic metrics from Step 7**: If ErrorRate is high, service mesh is not routing successfully. If RequestCount is zero, no traffic is flowing through the mesh. If traffic patterns are abnormal, investigate the cause.

If the above analysis is inconclusive: Verify Envoy proxy sidecar deployment in services. Check security group rules allowing mesh traffic. Review App Mesh virtual gateway configuration. Consider mesh-level observability with X-Ray integration.
