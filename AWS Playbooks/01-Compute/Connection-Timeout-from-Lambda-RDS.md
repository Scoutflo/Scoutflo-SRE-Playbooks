# RDS Connection Timeout from Lambda

## Meaning

Lambda functions cannot connect to RDS databases (triggering connection timeout errors or LambdaRDSConnectionTimeout alarms) because database is not running, VPC security groups block inbound access, subnet group configuration is incorrect, database is in wrong availability zone, public access is disabled when needed, Lambda VPC configuration is missing, connectivity tests from same VPC fail, or Lambda ENI creation delays prevent connections. Lambda functions cannot access database, connection timeout errors occur, and CloudWatch Logs show connection failures. This affects the serverless and database integration layer and blocks data access, typically caused by VPC networking issues, security group restrictions, or Lambda VPC configuration problems; if using Lambda container images, VPC configuration may differ and applications may experience database connection errors.

## Impact

Lambda functions cannot access database; connection timeout errors occur; database queries fail; application data operations error; Lambda function execution fails; connection pool exhaustion may occur; RDS connection timeout alarms may fire; service-to-database communication breaks; data processing workflows fail. LambdaRDSConnectionTimeout alarms fire; if using Lambda container images, VPC ENI creation may take longer; applications may experience errors or performance degradation due to database unavailability; Lambda function cold starts with VPC may add significant latency.

## Playbook

1. Verify Lambda function `<function-name>` and RDS instance `<rds-instance-id>` exist, and AWS service health for Lambda and RDS in region `<region>` is normal.
2. Retrieve the RDS Instance `<rds-instance-id>` in region `<region>` and confirm the database is running by checking instance status, verifying instance is in "available" state.
3. Retrieve the Security Group `<security-group-id>` associated with RDS instance `<rds-instance-id>` and check VPC security groups ensuring inbound rules allow access from Lambda execution environment, verifying Lambda security group source.
4. Retrieve the Lambda Function `<function-name>` VPC configuration and verify Lambda is configured in VPC with correct subnets and security groups, verify Lambda security group has outbound rules allowing RDS access, and verify Lambda subnets are in same VPC as RDS subnet group, checking VPC subnet configuration, security group egress rules, and VPC ID match.
5. Retrieve the RDS Instance `<rds-instance-id>` subnet group configuration and verify subnet group and whether the database is in the correct availability zone, checking subnet group availability zones.
6. Query CloudWatch Logs for log groups containing VPC Flow Logs or Lambda function logs and filter for blocked traffic from Lambda security group to RDS endpoint `<rds-endpoint>` or VPC ENI creation errors, including connection timeout errors, checking flow log and Lambda log analysis.
7. Retrieve CloudWatch metrics for Lambda function `<function-name>` including Duration and verify VPC ENI creation time, checking if ENI creation delays cause timeouts.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify Lambda and RDS service availability in the region. If service health indicates issues, connection timeouts may be AWS-side requiring monitoring rather than configuration changes.

2. If RDS instance status from Playbook step 2 shows the database is not in "available" state, the database is unavailable. Check RDS events for the state change timestamp and cause (maintenance, failover, storage issues).

3. If security group from Playbook step 3 lacks inbound rules allowing traffic from the Lambda security group on the database port, network access is blocked. Verify the Lambda security group is listed as an allowed source.

4. If Lambda VPC configuration from Playbook step 4 shows the function is not in a VPC or is in a different VPC than RDS, network connectivity is impossible. Verify VPC IDs match and Lambda subnets can route to RDS subnets.

5. If Lambda security group egress rules from Playbook step 4 do not allow outbound traffic to the RDS port, the Lambda function cannot initiate connections. Verify egress rules permit database port access.

6. If RDS subnet group from Playbook step 5 shows the database is in availability zones not covered by Lambda subnets, cross-AZ routing may fail. Verify Lambda subnets span the same AZs as RDS.

7. If VPC Flow Logs or Lambda logs from Playbook step 6 show blocked traffic or ENI creation errors, identify the specific block reason (security group, NACL, or ENI limits).

8. If Lambda duration metrics from Playbook step 7 show extended cold start times correlating with connection failures, VPC ENI creation delays are causing timeouts on initial invocations.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 30 minutes, review database connection limits (max_connections), check for VPC endpoint misconfigurations, and examine Lambda execution role permissions. Connection timeouts may result from database connection pool exhaustion, DNS resolution failures, or RDS Proxy configuration issues.

