# RDS Instance Not Connecting

## Meaning

RDS database connections timeout or fail (triggering alarms like RDSInstanceUnavailable or DatabaseConnectionErrors) because security group rules block access, the database is in an unavailable state, network connectivity issues exist, connection limits are reached, database credentials are incorrect, or RDS Proxy configuration blocks connections. Database connections return "Connection timed out" or "Connection refused" errors, RDS instance status shows "available" but connections fail, and CloudWatch metrics indicate connection failures. This affects the database layer and prevents data access, typically caused by security group restrictions, network configuration issues, connection pool exhaustion, or RDS Proxy misconfiguration; if using RDS Aurora, storage model differences may affect connection behavior and applications may experience database connection errors.

## Impact

Database connections fail; applications cannot access data; read/write operations timeout; connection pool exhaustion occurs; application errors increase; RDSInstanceUnavailable or DatabaseConnectionErrors alarms fire; connection refused errors appear in application logs; database becomes effectively inaccessible to applications. Database queries timeout; transaction failures occur; if using RDS Aurora, read replica connections may fail; applications may experience errors or performance degradation due to database unavailability; connection pool limits may be reached preventing new connections.

## Playbook

1. Verify RDS instance `<rds-instance-id>` exists and is in "available" state, and AWS service health for RDS in region `<region>` is normal.
2. Retrieve the RDS Instance `<rds-instance-id>` in region `<region>` and verify it is in the "available" state, inspecting its status and maintenance window status.
3. Retrieve the Security Group `<security-group-id>` associated with RDS instance `<rds-instance-id>` and check inbound rules allowing traffic on the correct port (e.g., 3306 for MySQL, 5432 for PostgreSQL), verifying source security groups or CIDR blocks.
4. Verify database credentials configuration by retrieving RDS instance parameter group settings and checking authentication-related parameters.
5. Retrieve the RDS Instance `<rds-instance-id>` connection endpoint and verify endpoint configuration, checking if using RDS Proxy endpoint or direct instance endpoint.
6. Retrieve the RDS Proxy `<proxy-name>` configuration if using RDS Proxy and verify proxy endpoint, target group configuration, and IAM authentication settings.
7. Retrieve CloudWatch metrics for RDS instance `<rds-instance-id>` including DatabaseConnections and verify connection count against max_connections parameter to check for connection limit exhaustion.
8. Query CloudWatch Logs for log groups containing VPC Flow Logs or RDS instance logs and filter for blocked traffic to RDS endpoint `<rds-endpoint>` on port `<port>` or connection errors, authentication failures, or database errors, checking flow log and RDS log analysis.
9. Retrieve the Route Table `<route-table-id>` for subnet containing RDS instance `<rds-instance-id>` and verify route table configuration allows traffic from application subnets.

## Diagnosis

1. Compare RDS instance state change timestamps with database connection failure timestamps within 5 minutes and verify whether connection failures began when the instance transitioned to unavailable state, using RDS events as supporting evidence.
2. Correlate security group rule modification timestamps with connection timeout timestamps and verify whether connection failures occurred shortly after security group changes, using security group configuration data as supporting evidence.
3. Compare parameter group modification timestamps with connection authentication failure timestamps within 5 minutes and verify whether authentication failures began after parameter group changes, using RDS configuration events as supporting evidence.
4. Compare RDS Proxy configuration change timestamps with connection failure timestamps within 5 minutes and verify whether proxy configuration changes blocked connections, using RDS Proxy configuration events as supporting evidence.
5. Analyze connection failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (network connectivity or capacity limits).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including VPC flow logs and network ACL rules, check for gradual issues like connection limit exhaustion, verify external dependencies like DNS resolution, examine historical patterns of database connectivity, check for RDS Aurora storage model differences. Connection failures may result from network-level routing issues, DNS resolution problems, application-level connection pool exhaustion, RDS Multi-AZ failover endpoint changes, or RDS Performance Insights data retention issues rather than immediate RDS configuration changes.
