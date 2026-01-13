# IAM Role Not Attaching to EC2 Instance

## Meaning

IAM roles fail to attach or function correctly on EC2 instances (triggering permission errors or EC2InstanceRoleMissing alarms) because IAM role is not attached to instance, instance profile is missing, role permissions are incorrect, instance metadata service (IMDSv2) is not accessible, AWS CLI commands fail, or CloudTrail logs show permission errors. EC2 instances cannot access AWS services, IAM role permissions are ineffective, and instance metadata service returns permission denied errors. This affects the compute and security layers and blocks service access, typically caused by instance profile configuration issues, IMDS configuration problems, or IAM role trust policy misconfiguration; if instances host container workloads, container applications may fail to access AWS services and pod IAM roles may not function correctly.

## Impact

EC2 instances cannot access AWS services; IAM role permissions are ineffective; instance metadata service fails; AWS CLI operations error; permission denied errors occur; service-to-service communication breaks; applications cannot access S3, DynamoDB, or other AWS services; instance-based authentication fails. EC2InstanceRoleMissing alarms fire; if instances host container workloads, container applications cannot access AWS services, pod IAM roles fail, and container orchestration tasks may show permission errors; applications may experience errors or performance degradation due to service access failures.

## Playbook

1. Verify instance `<instance-id>` is in "running" state and AWS service health for EC2 and IAM in region `<region>` is normal.
2. Retrieve the EC2 Instance `<instance-id>` IAM role configuration and verify IAM role attached to the instance, checking instance profile association (not just IAM role name).
3. Retrieve the EC2 Instance `<instance-id>` instance profile configuration and verify instance profile exists and is attached, checking instance profile path and name.
4. Retrieve the IAM role `<role-name>` attached to instance and ensure correct permissions (s3:ListBucket, s3:GetObject) by checking role policies.
5. Retrieve the IAM role `<role-name>` trust policy and verify trust policy allows EC2 service to assume the role, checking trust relationship configuration.
6. Retrieve the EC2 Instance `<instance-id>` metadata service configuration and confirm instance metadata service (IMDSv2) is accessible, verifying IMDSv2 enforcement settings and hop limit.
7. Query CloudWatch Logs for log groups containing EC2 instance logs or CloudTrail events and filter for IAM role assumption errors, permission denied errors, or AssumeRole failures related to instance `<instance-id>` within the last 1 hour.
8. Retrieve the IAM role `<role-name>` permissions boundary and verify permissions boundary is not restricting required permissions, and verify if instance profile can only be attached at launch by checking instance launch configuration and instance profile attachment timing.

## Diagnosis

1. Compare IAM role attachment change timestamps with permission error timestamps within 5 minutes and verify whether permission errors began after role attachment or detachment, using EC2 instance events as supporting evidence.
2. Correlate instance profile attachment change timestamps with permission failure timestamps and verify whether instance profile issues caused permission failures, using EC2 instance configuration data as supporting evidence.
3. Compare IAM role policy modification timestamps with permission failure timestamps and verify whether policy changes caused permission failures, using IAM role policy configuration data as supporting evidence.
4. Compare instance metadata service configuration change timestamps with metadata access failure timestamps within 5 minutes and verify whether IMDS configuration changes prevented role access, using instance metadata events as supporting evidence.
5. Analyze permission error frequency over the last 15 minutes to determine if errors are constant (role configuration issue) or intermittent (metadata service availability).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including instance system logs and metadata service logs, check for gradual issues like metadata service throttling, verify external dependencies like IAM service availability, examine historical patterns of IAM role attachment, check for IAM role assumption from other services, verify IAM role chaining scenarios. Permission failures may result from instance-level firewall rules blocking metadata service, network connectivity issues, IAM service throttling, IAM role tag-based access control restrictions, or session policy limitations rather than immediate role configuration changes.
