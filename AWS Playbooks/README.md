# AWS Playbooks

This directory contains **25 AWS incident response playbooks** designed to help Site Reliability Engineers (SREs) diagnose and resolve common AWS service issues. Each playbook follows a structured format to provide systematic troubleshooting guidance.

## Overview

These playbooks cover critical AWS services including:
- **Compute**: EC2, Lambda, ECS, EKS
- **Networking**: VPC, ELB, Route 53, NAT Gateway
- **Storage**: S3, EBS, RDS
- **Security**: IAM, KMS, GuardDuty, CloudTrail
- **Integration**: API Gateway, CodePipeline

Each playbook provides step-by-step instructions for identifying root causes and resolving issues quickly.

## Playbook Structure

All playbooks in this directory follow a consistent markdown structure:

### 1. **Title** (H1)
The playbook title describing the issue (e.g., "EC2 Instance Connection Timeout (SSH Issues)")

### 2. **Meaning** (H2)
A comprehensive explanation of what the issue means, including:
- What triggers the issue
- Common symptoms and error messages
- Which AWS service layer is affected
- Typical root causes

### 3. **Impact** (H2)
Description of the business and technical impact, including:
- Service availability implications
- User-facing effects
- Related alarms or alerts
- Cascading effects on dependent services

### 4. **Playbook** (H2)
Numbered, actionable steps to diagnose the issue:
- Each step includes specific AWS resource identifiers (e.g., `<instance-id>`, `<bucket-name>`)
- Steps reference AWS services, CloudWatch Logs, and configuration checks
- Ordered from most common to more specific diagnostic steps

### 5. **Diagnosis** (H2)
Correlation analysis framework:
- Time-based correlation between events and symptoms
- Comparison of configuration changes with failure timestamps
- Analysis patterns to determine if issues are constant or intermittent
- Guidance for extending time windows if initial correlations aren't found
- Alternative evidence sources and gradual issue identification

## Complete Playbook List

1. **Access-Key-Leaked-Warning-IAM.md** - IAM access key security breach detection and response
2. **Bucket-Access-Denied-403-Error-S3.md** - S3 bucket access permission issues
3. **Connection-Timeout-from-Lambda-RDS.md** - Lambda to RDS database connectivity problems
4. **Connection-Timeout-SSH-Issues-EC2.md** - EC2 instance SSH connection failures
5. **DNS-Resolution-Failing-Route-53.md** - Route 53 DNS resolution failures
6. **Failing-Due-to-S3-Permissions-CodePipeline.md** - CodePipeline execution failures due to S3 permissions
7. **Instance-Cant-Reach-Internet-via-NAT-Gateway-EC2.md** - EC2 instances unable to reach internet through NAT Gateway
8. **Instance-Not-Connecting-RDS.md** - RDS database connection failures
9. **Instance-Not-Starting-EC2.md** - EC2 instance launch failures
10. **Instance-Unable-to-Reach-the-Internet-EC2.md** - EC2 instances without internet connectivity
11. **Key-Policy-Preventing-Decryption-KMS.md** - KMS key decryption permission issues
12. **Logs-Not-Capturing-Events-CloudTrail.md** - CloudTrail event logging gaps
13. **Not-Detecting-Threats-GuardDuty.md** - GuardDuty threat detection failures
14. **Not-Routing-Traffic-ELB.md** - Elastic Load Balancer traffic routing failures
15. **Not-Triggering-from-S3-Event-Lambda.md** - Lambda functions not triggering from S3 events
16. **Peering-Not-Working-VPC.md** - VPC peering connection failures
17. **Pod-Stuck-in-CrashLoopBackOff-EKS.md** - EKS pod crash loop issues
18. **Policy-Not-Granting-Expected-Access-IAM.md** - IAM policy permission issues
19. **Returning-500-Internal-Server-Error-API-Gateway.md** - API Gateway 500 error responses
20. **Role-Not-Attaching-to-EC2-Instance-IAM.md** - IAM role attachment failures on EC2 instances
21. **Rules-Not-Applying-Correctly-Security-Group.md** - Security group rule effectiveness issues
22. **Storage-Full-Error-RDS.md** - RDS database storage capacity exhaustion
23. **Target-Group-Showing-Unhealthy-Instances-ELB.md** - ELB target group health check failures
24. **Task-Stuck-in-Pending-State-ECS.md** - ECS task placement failures
25. **Timeout-Error-Lambda.md** - Lambda function execution timeouts

## Usage Guidelines

1. **Identify the Issue**: Match your symptoms to the appropriate playbook title
2. **Follow the Playbook**: Execute the numbered steps in order, replacing placeholder values (e.g., `<instance-id>`) with your actual resource identifiers
3. **Review Diagnosis Section**: Use the correlation analysis to identify root causes
4. **Extend Time Windows**: If initial correlations don't reveal the cause, extend time windows as suggested
5. **Check Alternative Sources**: Review alternative evidence sources mentioned in the Diagnosis section

## Common Placeholders

Playbooks use the following placeholder format that should be replaced with actual values:
- `<instance-id>` - EC2 instance identifier
- `<bucket-name>` - S3 bucket name
- `<region>` - AWS region
- `<function-name>` - Lambda function name
- `<role-name>` - IAM role name
- `<user-name>` - IAM user name
- `<security-group-id>` - Security group identifier
- `<vpc-id>` - VPC identifier

## Best Practices

- Start with the most common causes (earlier steps in the Playbook section)
- Use CloudWatch Logs Insights for efficient log analysis
- Correlate timestamps between configuration changes and failures
- Document findings for future reference
- Consider gradual issues if immediate correlations aren't found
