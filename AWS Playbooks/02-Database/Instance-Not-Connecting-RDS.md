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

1. Analyze AWS service health from Playbook step 1 to verify RDS service availability in the region. If service health indicates issues, connection failures may be AWS-side requiring monitoring rather than configuration changes.

2. If RDS instance status from Playbook step 2 is not "available" (e.g., "maintenance", "backing-up", "rebooting"), the database is temporarily inaccessible. Check the maintenance window status and expected completion time.

3. If security group inbound rules from Playbook step 3 do not allow traffic from the client security group or IP on the database port (3306 for MySQL, 5432 for PostgreSQL), network access is blocked. Verify source configurations.

4. If RDS endpoint from Playbook step 5 differs from the endpoint used by the application, connection attempts are targeting the wrong address. This commonly occurs after Multi-AZ failover when applications cache the old IP.

5. If RDS Proxy configuration from Playbook step 6 shows proxy is enabled but misconfigured, verify proxy endpoint, target group, and IAM authentication settings. Proxy misconfigurations cause connection failures even when RDS is healthy.

6. If DatabaseConnections metric from Playbook step 7 equals or exceeds max_connections parameter, connection limit exhaustion is occurring. New connections are rejected when the pool is full.

7. If VPC Flow Logs or RDS logs from Playbook step 8 show blocked traffic or authentication failures, identify the specific failure cause (network rejection vs. credential errors vs. SSL/TLS issues).

8. If route table from Playbook step 9 does not allow traffic between application subnets and RDS subnets, routing configuration prevents connectivity. Verify VPC peering or Transit Gateway routes if cross-VPC.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 30 minutes, verify DNS resolution of RDS endpoint, check for application-side connection pool exhaustion, and examine SSL certificate requirements. Connection failures may result from credential expiration, SSL/TLS version mismatches, or RDS Performance Insights resource consumption.
