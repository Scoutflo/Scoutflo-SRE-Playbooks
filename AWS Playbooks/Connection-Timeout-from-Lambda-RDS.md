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

1. Compare RDS instance state change timestamps with Lambda connection timeout timestamps within 5 minutes and verify whether connection timeouts began when database state changed, using RDS events as supporting evidence.
2. Correlate security group rule modification timestamps with connection blocking timestamps and verify whether connection timeouts occurred after security group changes, using security group configuration data as supporting evidence.
3. Compare Lambda VPC configuration change timestamps with connection timeout timestamps within 5 minutes and verify whether VPC configuration changes caused connection failures, using Lambda VPC configuration events as supporting evidence.
4. Correlate Lambda VPC ENI creation timestamps with connection timeout timestamps and verify whether ENI creation delays caused connection timeouts, using Lambda VPC metrics as supporting evidence.
5. Analyze connection timeout frequency over the last 15 minutes to determine if timeouts are constant (configuration issue) or intermittent (network connectivity).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including VPC configuration and Lambda VPC settings, check for gradual issues like connection limit exhaustion, verify external dependencies like VPC endpoint configuration, examine historical patterns of Lambda to RDS connectivity, check for Lambda container image VPC configuration differences, verify Lambda SnapStart configuration for Java functions. Connection timeouts may result from VPC endpoint misconfiguration, Lambda execution environment networking issues, database connection limit exhaustion, Lambda VPC ENI creation delays, or Lambda container image VPC configuration rather than immediate RDS configuration changes.

