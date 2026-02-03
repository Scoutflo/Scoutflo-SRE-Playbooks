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

1. Analyze AWS service health from Playbook step 1 to verify EC2 and IAM service availability in the region. If service health indicates issues, role attachment failures may be AWS-side requiring monitoring rather than configuration changes.

2. If IAM role configuration from Playbook step 2 shows no role attached to the instance, the instance has no IAM permissions. Note that IAM roles can only be attached at launch time or by stopping and modifying the instance.

3. If instance profile from Playbook step 3 does not exist or is not attached, the instance cannot assume the IAM role. Instance profiles are the mechanism for associating IAM roles with EC2 instances.

4. If IAM role policies from Playbook step 4 do not include the required permissions (e.g., s3:ListBucket, s3:GetObject), the role is attached but lacks sufficient permissions for the intended operations.

5. If trust policy from Playbook step 5 does not allow ec2.amazonaws.com to assume the role, EC2 cannot use the role. Verify the trust relationship includes the EC2 service principal.

6. If IMDS configuration from Playbook step 6 shows IMDSv2 is required with a hop limit of 1, applications running in containers or through proxies cannot reach the metadata service. Increase hop limit or configure applications for IMDSv2.

7. If CloudTrail events from Playbook step 7 show AssumeRole failures or AccessDenied errors for specific actions, identify the specific permission or trust policy causing the failure.

8. If permissions boundary from Playbook step 8 restricts the effective permissions below what the role policy allows, the boundary is limiting access. Permissions boundaries set maximum effective permissions.

If no correlation is found from the collected data: extend CloudTrail query timeframes to 1 hour, verify instance-level firewall rules allow traffic to 169.254.169.254, check for network routes blocking metadata service access, and examine IMDS request rate limiting. Permission failures may result from metadata service throttling (too many requests), instance profile path issues, or role chaining limitations.

