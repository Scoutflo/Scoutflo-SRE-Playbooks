# AWS Playbooks

[![AWS](https://img.shields.io/badge/AWS-168%20playbooks-orange)](README.md)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](../../CONTRIBUTING.md)

> **168 comprehensive AWS incident response playbooks** organized into 8 categorized folders - Systematic troubleshooting guides for common AWS service issues to help SREs diagnose and resolve infrastructure problems faster.

## 📋 Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Playbook Structure](#playbook-structure)
- [Playbook Categories](#playbook-categories)
- [Getting Started](#getting-started)
- [Usage Guidelines](#usage-guidelines)
- [Terminology & Glossary](#terminology--glossary)
- [Contributing](#contributing)
- [Connect with Us](#connect-with-us)
- [Related Resources](#related-resources)

## Overview

This directory contains **168 AWS incident response playbooks** organized into **8 categorized folders** to help Site Reliability Engineers (SREs) diagnose and resolve common AWS service issues. Each playbook follows a structured format to provide systematic troubleshooting guidance.

### Services Covered

- **Compute Services**: EC2, Lambda, ECS, EKS, Fargate, Auto Scaling, Spot Instances
- **Database**: RDS, DynamoDB
- **Storage**: S3
- **Networking**: VPC, ELB, Route 53, NAT Gateway, API Gateway, CloudFront, Direct Connect, VPN, PrivateLink
- **Security**: IAM, KMS, GuardDuty, WAF, Shield, Cognito, Secrets Manager, ACM, Security Hub
- **Monitoring**: CloudWatch, CloudTrail, Config, X-Ray
- **CI/CD**: CodePipeline, CodeBuild, CodeDeploy, CloudFormation, Step Functions, Glue, Batch, App Runner
- **Proactive**: Capacity planning, security compliance, backup/DR, cost optimization, observability

### Key Topics

- Connection timeouts and network issues
- Access denied and permission problems
- Resource unavailability and capacity issues
- Security breaches and threat detection
- Service integration failures
- Proactive capacity and compliance monitoring
- Cost optimization and resource management

## Directory Structure

Playbooks are organized into numbered folders by category for easy navigation:

```
AWS Playbooks/
├── 01-Compute/                    (27 playbooks)
├── 02-Database/                   (8 playbooks)
├── 03-Storage/                    (7 playbooks)
├── 04-Networking/                 (17 playbooks)
├── 05-Security/                   (17 playbooks)
├── 06-Monitoring/                 (8 playbooks)
├── 07-CI-CD/                      (9 playbooks)
└── 08-Proactive/                  (75 playbooks)
    ├── 01-Capacity-Performance/   (11 playbooks)
    ├── 02-Security-Compliance/    (11 playbooks)
    ├── 03-Backup-DR/              (9 playbooks)
    ├── 04-Cost-Optimization/      (16 playbooks)
    ├── 05-Observability/          (10 playbooks)
    ├── 06-Data-Integrity/         (2 playbooks)
    └── 07-Operational-Readiness/  (8 playbooks)
```

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
Numbered, actionable steps in natural language to diagnose the issue:
- Each step uses natural language instructions for AI agents
- Steps include specific AWS resource identifiers (e.g., `<instance-id>`, `<bucket-name>`)
- Steps reference AWS services, CloudWatch Logs, and configuration checks
- Ordered from most common to more specific diagnostic steps
- **Note**: Playbooks are designed for AI agents using NLP

### 5. **Diagnosis** (H2)
Correlation analysis framework:
- Time-based correlation between events and symptoms
- Comparison of configuration changes with failure timestamps
- Analysis patterns to determine if issues are constant or intermittent
- Guidance for extending time windows if initial correlations aren't found

## Playbook Categories

### 01-Compute/ (27 playbooks)
EC2, Lambda, ECS, EKS, Fargate, Auto Scaling, Spot Instances, CodeDeploy

**Key Topics:**
- Instance connectivity and startup issues
- Lambda timeouts and memory limits
- Container orchestration problems
- Auto scaling failures
- Spot instance interruptions

**Playbooks:**
- `Cold-Start-Delays-Performance-Lambda.md`
- `Connection-Timeout-from-Lambda-RDS.md`
- `Connection-Timeout-SSH-Issues-EC2.md`
- `Exceeds-Memory-Limit-Lambda.md`
- `Failing-on-EC2-Instances-CodeDeploy.md`
- `High-CPU-Utilization-EC2.md`
- `IAM-Role-Not-Attaching-to-Service-Account-EKS.md`
- `Image-Pull-Failing-in-ECS-Docker.md`
- `Ingress-Controller-Not-Routing-Traffic-EKS.md`
- `Instance-Cant-Reach-Internet-via-NAT-Gateway-EC2.md`
- `Instance-Not-Starting-EC2.md`
- `Instance-Unable-to-Reach-the-Internet-EC2.md`
- `Interrupted-Unexpectedly-Spot-Instance.md`
- `Logs-Not-Appearing-in-CloudWatch-ECS.md`
- `Nodes-Not-Joining-Cluster-EKS.md`
- `Not-Launching-New-Instances-Auto-Scaling.md`
- `Not-Scaling-as-Expected-ECS.md`
- `Not-Triggering-from-S3-Event-Lambda.md`
- `Pod-Stuck-in-CrashLoopBackOff-EKS.md`
- `Role-Not-Attaching-to-EC2-Instance-IAM.md`
- `Running-Out-of-Memory-Fargate.md`
- `Spot-Instance-Pricing-Unexpectedly-High-Cost.md`
- `Streams-Not-Triggering-Lambda-DynamoDB.md`
- `Stuck-in-Initializing-State-EC2.md`
- `Task-Stuck-in-Pending-State-ECS.md`
- `Terminating-Instances-Unexpectedly-Auto-Scaling.md`
- `Timeout-Error-Lambda.md`

### 02-Database/ (8 playbooks)
RDS, DynamoDB

**Key Topics:**
- Database connectivity issues
- Storage and performance problems
- Backup failures
- Throttling and replication

**Playbooks:**
- `Automatic-Backup-Not-Working-RDS.md`
- `Backup-Failing-DynamoDB.md`
- `High-CPU-Utilization-RDS.md`
- `Instance-Not-Connecting-RDS.md`
- `Query-Performance-Slower-Than-Expected-DynamoDB.md`
- `Read-Replica-Lagging-Behind-Primary-RDS.md`
- `Storage-Full-Error-RDS.md`
- `Throttling-Errors-DynamoDB.md`

### 03-Storage/ (7 playbooks)
S3

**Key Topics:**
- Bucket access and permissions
- Replication issues
- Lifecycle policies
- Upload performance

**Playbooks:**
- `Bucket-Access-Denied-403-Error-S3.md`
- `Cross-Region-Replication-Not-Working-S3.md`
- `Failing-Due-to-S3-Permissions-CodePipeline.md`
- `File-Upload-Extremely-Slow-S3.md`
- `Intelligent-Tiering-Not-Moving-Data-as-Expected-S3.md`
- `Lifecycle-Policy-Not-Deleting-Objects-S3.md`
- `Public-Access-Block-Preventing-Access-S3.md`

### 04-Networking/ (17 playbooks)
VPC, ELB, Route 53, API Gateway, CloudFront, Direct Connect, VPN, PrivateLink, NACL, Global Accelerator

**Key Topics:**
- Load balancer traffic routing
- DNS resolution failures
- API Gateway errors
- VPC peering and connectivity
- CDN and caching issues

**Playbooks:**
- `Blocking-Expected-Traffic-NACL.md`
- `Certificate-Not-Working-on-ELB.md`
- `Connection-Dropping-Frequently-VPN.md`
- `CORS-Issues-API-Gateway.md`
- `Distribution-Deployment-Stuck-in-Progress-CloudFront.md`
- `DNS-Resolution-Failing-Route-53.md`
- `Endpoint-Not-Working-PrivateLink.md`
- `Latency-Based-Routing-Not-Working-Route-53.md`
- `Latency-Higher-Than-Expected-Direct-Connect.md`
- `Not-Distributing-Traffic-Properly-Global-Accelerator.md`
- `Not-Routing-Traffic-ELB.md`
- `Not-Serving-Updated-Content-CloudFront.md`
- `Peering-Not-Working-VPC.md`
- `Returning-500-Internal-Server-Error-API-Gateway.md`
- `Route-Not-Matching-Requests-API-Gateway.md`
- `Target-Group-Showing-Unhealthy-Instances-ELB.md`
- `Throttling-Requests-API-Gateway.md`

### 05-Security/ (17 playbooks)
IAM, KMS, GuardDuty, WAF, Shield, Cognito, Secrets Manager, ACM, Security Hub, STS, Organizations

**Key Topics:**
- IAM permissions and access keys
- Encryption and key management
- Threat detection
- WAF and DDoS protection
- Certificate management

**Playbooks:**
- `Access-Key-Leaked-Warning-IAM.md`
- `Authentication-Failing-for-IAM-User-MFA.md`
- `Blocking-Legitimate-Traffic-WAF.md`
- `Certificate-Not-Issuing-ACM.md`
- `Key-Policy-Preventing-Decryption-KMS.md`
- `Not-Aggregating-Findings-Security-Hub.md`
- `Not-Detecting-Security-Threats-GuardDuty.md`
- `Not-Detecting-Threats-GuardDuty.md`
- `Not-Mitigating-DDoS-Attacks-Shield.md`
- `Not-Rotating-Credentials-Secrets-Manager.md`
- `Policy-Not-Granting-Expected-Access-IAM.md`
- `Rules-Causing-False-Positives-WAF.md`
- `Rules-Not-Applying-Correctly-Security-Group.md`
- `SCP-Preventing-Service-Access-Organizations.md`
- `Token-Expired-Error-STS.md`
- `User-Pool-Login-Issues-Cognito.md`

### 06-Monitoring/ (8 playbooks)
CloudWatch, CloudTrail, Config, X-Ray

**Key Topics:**
- Alarm and metric issues
- Log capture problems
- Configuration recording
- Distributed tracing

**Playbooks:**
- `Alarm-Not-Triggering-as-Expected-CloudWatch.md`
- `Events-Not-Showing-in-Logs-CloudTrail.md`
- `Logs-Not-Appearing-CloudWatch.md`
- `Logs-Not-Capturing-Events-CloudTrail.md`
- `Metrics-Missing-Data-Points-CloudWatch.md`
- `Not-Recording-Changes-Config.md`
- `Not-Recording-Resource-Changes-Config.md`
- `Traces-Missing-in-Application-Logs-X-Ray.md`

### 07-CI-CD/ (9 playbooks)
CodePipeline, CodeBuild, CloudFormation, Step Functions, Glue, Batch, App Runner, CodeCommit

**Key Topics:**
- Pipeline execution failures
- Build dependency issues
- Infrastructure as code problems
- Job scheduling failures

**Playbooks:**
- `Deployment-Failing-App-Runner.md`
- `Drift-Detection-Not-Detecting-Changes-CloudFormation.md`
- `Execution-Stuck-in-Running-State-Step-Functions.md`
- `Failing-Due-to-Dependency-Errors-CodeBuild.md`
- `Job-Failing-Randomly-Glue.md`
- `Jobs-Not-Starting-Batch.md`
- `Repository-Not-Allowing-Push-CodeCommit.md`
- `Stack-Failing-to-Create-CloudFormation.md`
- `Stuck-in-Progress-CodePipeline.md`

### 08-Proactive/ (75 playbooks)
Proactive monitoring, capacity planning, security compliance, and operational readiness

**Key Topics:**
- Capacity and performance forecasting
- Security and compliance checks
- Backup and disaster recovery
- Cost optimization
- Observability gaps
- Data integrity
- Operational readiness

#### 01-Capacity-Performance (11 playbooks)
- `Baseline-Comparison-AWS.md`
- `Capacity-Trend-Analysis-AWS.md`
- `Cascading-Failure-Analysis-AWS.md`
- `Error-Budget-Tracking-AWS.md`
- `Performance-Regression-Detection-AWS.md`
- `Performance-Trend-Analysis-AWS.md`
- `Quota-Utilization-Tracking-AWS.md`
- `Resource-Exhaustion-Prediction-AWS.md`
- `Resource-Usage-Forecasting-AWS.md`
- `Right-sizing-Analysis-AWS.md`
- `Scaling-Projections-AWS.md`

#### 02-Security-Compliance (11 playbooks)
- `Access-Review-AWS.md`
- `Audit-Log-Review-AWS.md`
- `Compliance-Check-AWS.md`
- `Compliance-Status-Check-AWS.md`
- `IAM-Policy-Review-AWS.md`
- `Network-Security-Audit-AWS.md`
- `Policy-Compliance-Verification-AWS.md`
- `Regulatory-Requirement-Check-AWS.md`
- `Secrets-Rotation-Status-AWS.md`
- `Security-Group-Audit-AWS.md`
- `Vulnerability-Scanning-AWS.md`

#### 03-Backup-DR (9 playbooks)
- `Backup-Integrity-Verification-AWS.md`
- `Backup-Verification-AWS.md`
- `Cross-region-Backup-Sync-AWS.md`
- `Data-Replication-Status-AWS.md`
- `Disaster-Recovery-Runbook-Execution-AWS.md`
- `Multi-region-Failover-AWS.md`
- `Replication-Lag-Monitoring-AWS.md`
- `Restore-Testing-AWS.md`
- `RTO-RPO-Validation-AWS.md`

#### 04-Cost-Optimization (16 playbooks)
- `Budgets-Not-Sending-Alerts-Cost.md`
- `Compute-Savings-Plan-Not-Optimizing-Costs-Cost.md`
- `Cost-Anomaly-Detection-AWS.md`
- `Cost-Explorer-Not-Displaying-Data-Cost.md`
- `Free-Tier-Unexpectedly-Exceeded-Cost.md`
- `Idle-Resource-Detection-AWS.md`
- `On-Demand-Pricing-Higher-Than-Expected-DynamoDB.md`
- `Reserved-Instance-Discount-Not-Applying-Cost.md`
- `Reserved-Instance-Not-Reflecting-in-Billing-RDS.md`
- `Reserved-Instance-Optimization-AWS.md`
- `Spot-Instance-Management-AWS.md`
- `Spot-Instance-Pricing-Unexpectedly-High-Cost.md`
- `Storage-Tier-Optimization-AWS.md`
- `Unexpected-Increase-in-AWS-Bill-Cost.md`
- `Unused-Resource-Cleanup-AWS.md`

#### 05-Observability (10 playbooks)
- `Alert-Coverage-Analysis-AWS.md`
- `Automation-Coverage-AWS.md`
- `Certificate-Expiration-Monitoring-AWS.md`
- `Log-Coverage-Analysis-AWS.md`
- `Metric-Coverage-Gaps-AWS.md`
- `Missing-Instrumentation-AWS.md`
- `SLO-SLI-Monitoring-AWS.md`
- `Trace-Coverage-Issues-AWS.md`
- `Transaction-Log-Analysis-AWS.md`

#### 06-Data-Integrity (2 playbooks)
- `Data-Consistency-Checks-AWS.md`
- `Data-Corruption-Detection-AWS.md`

#### 07-Operational-Readiness (8 playbooks)
- `API-Dependency-Status-AWS.md`
- `Dependency-Health-Check-AWS.md`
- `Documentation-Gaps-AWS.md`
- `Incident-Response-Preparedness-AWS.md`
- `On-call-Readiness-AWS.md`
- `Runbook-Completeness-AWS.md`
- `Service-Dependency-Mapping-AWS.md`
- `Service-Mesh-Health-AWS.md`

## Getting Started

### 1. Documentation

This directory contains 168 AWS incident response playbooks organized into 8 categorized folders. Each playbook provides systematic troubleshooting guidance for common AWS issues.

**Quick Navigation:**
- Browse by category folder (e.g., `01-Compute/` for compute issues)
- Use GitHub's search to find specific playbooks
- Match your symptoms to playbook titles

### 2. Installation

Clone this repository to access the AWS playbooks:

```bash
# Clone the repository
git clone https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git

# Navigate to AWS playbooks
cd scoutflo-SRE-Playbooks/AWS\ Playbooks/

# Browse by category
ls 01-Compute/
ls 04-Networking/

# View a specific playbook
cat 01-Compute/Connection-Timeout-SSH-Issues-EC2.md
```

### 3. Learn More

- **Watch Tutorials**: Check our [YouTube channel](https://www.youtube.com/@scoutflo6727) for AWS troubleshooting walkthroughs
- **AI SRE Demo**: Watch the [Scoutflo AI SRE Demo](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) to see AI-powered incident response
- **AWS Documentation**: Refer to [AWS Official Documentation](https://docs.aws.amazon.com/) for service details
- **Best Practices**: Review [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- **Scoutflo Documentation**: Visit [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) for platform guides
- **Community**: Join discussions in our [Slack workspace](https://scoutflo.slack.com)

## Usage Guidelines

### Step-by-Step Process

1. **Identify the Category**: Determine which category your issue falls into (Compute, Database, Networking, etc.)
2. **Navigate to Folder**: Go to the appropriate numbered folder (e.g., `01-Compute/` for EC2/Lambda issues)
3. **Find the Playbook**: Locate the playbook matching your specific issue
4. **Follow the Playbook**: Execute the numbered steps in order, replacing placeholder values
5. **Review Diagnosis Section**: Use the correlation analysis to identify root causes
6. **Extend Time Windows**: If initial correlations don't reveal the cause, extend time windows as suggested

### Example Workflow

**Scenario**: EC2 instance SSH connection timeout

1. Navigate to `01-Compute/` folder
2. Open `Connection-Timeout-SSH-Issues-EC2.md`
3. Read the **Meaning** section to understand the issue
4. Review the **Impact** section to assess severity
5. Follow **Playbook** steps in order
6. Use **Diagnosis** section to correlate events
7. Apply the identified fix

### Common Placeholders

- `<instance-id>` - EC2 instance identifier
- `<bucket-name>` - S3 bucket name
- `<region>` - AWS region
- `<function-name>` - Lambda function name
- `<role-name>` - IAM role name
- `<security-group-id>` - Security group identifier
- `<vpc-id>` - VPC identifier
- `<rds-instance-id>` - RDS instance identifier
- `<load-balancer-name>` - Load balancer name

## Terminology & Glossary

### AWS Service Abbreviations

- **EC2** - Elastic Compute Cloud (virtual servers)
- **VPC** - Virtual Private Cloud (isolated network)
- **IAM** - Identity and Access Management
- **S3** - Simple Storage Service
- **RDS** - Relational Database Service
- **ELB** - Elastic Load Balancer
- **ECS** - Elastic Container Service
- **EKS** - Elastic Kubernetes Service
- **KMS** - Key Management Service
- **ACM** - AWS Certificate Manager
- **WAF** - Web Application Firewall

### Common Terms

- **Security Group** - Virtual firewall for AWS resources
- **IAM Role** - AWS identity with permissions
- **Region** - Geographic area with AWS data centers
- **Availability Zone** - Isolated data center within a region
- **Target Group** - Resources receiving load balancer traffic

## Quick Navigation Guide

| Issue Type | Folder | Example Playbooks |
|------------|--------|-------------------|
| EC2/Lambda problems | `01-Compute/` | `Instance-Not-Starting-EC2.md`, `Timeout-Error-Lambda.md` |
| Database connectivity | `02-Database/` | `Instance-Not-Connecting-RDS.md`, `Throttling-Errors-DynamoDB.md` |
| S3 access issues | `03-Storage/` | `Bucket-Access-Denied-403-Error-S3.md` |
| Load balancer/DNS | `04-Networking/` | `Not-Routing-Traffic-ELB.md`, `DNS-Resolution-Failing-Route-53.md` |
| IAM/permissions | `05-Security/` | `Policy-Not-Granting-Expected-Access-IAM.md` |
| Alarms/logs | `06-Monitoring/` | `Alarm-Not-Triggering-as-Expected-CloudWatch.md` |
| Pipeline failures | `07-CI-CD/` | `Stuck-in-Progress-CodePipeline.md` |
| Proactive checks | `08-Proactive/` | `Cost-Anomaly-Detection-AWS.md`, `Backup-Verification-AWS.md` |

## Contributing

We welcome contributions to improve AWS playbooks!

### How to Contribute

1. **Fork the Repository**
2. **Create a Branch**: `git checkout -b fix/aws-playbook-name`
3. **Make Your Changes**: Follow the established structure
4. **Place in Correct Folder**: Use appropriate category folder
5. **Create Pull Request**

### Location Guidelines

- Compute issues (EC2, Lambda, ECS, EKS) → `01-Compute/`
- Database issues (RDS, DynamoDB) → `02-Database/`
- Storage issues (S3) → `03-Storage/`
- Networking issues (VPC, ELB, Route 53) → `04-Networking/`
- Security issues (IAM, KMS, WAF) → `05-Security/`
- Monitoring issues (CloudWatch, CloudTrail) → `06-Monitoring/`
- CI/CD issues (CodePipeline, CloudFormation) → `07-CI-CD/`
- Proactive monitoring → `08-Proactive/`

📖 For detailed contribution guidelines, see [CONTRIBUTING.md](../CONTRIBUTING.md)

## Connect with Us

**For Feedback or Feature Requests**:
- Share with us in [Slack](https://scoutflo.slack.com) or create a [GitHub Issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)

**Links:**
- [Slack Community](https://scoutflo.slack.com) | [Roadmap](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/projects) | [Documentation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/wiki)

**Scoutflo Resources:**
- [Official Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) | [Website](https://scoutflo.com/) | [AI SRE Tool](https://ai.scoutflo.com/get-started)
- [YouTube Channel](https://www.youtube.com/@scoutflo6727) | [LinkedIn](https://www.linkedin.com/company/scoutflo/) | [Twitter/X](https://x.com/scout_flo)

## Related Resources

### AWS Official Documentation
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Troubleshooting Guides](https://docs.aws.amazon.com/general/latest/gr/aws_troubleshooting.html)
- [AWS Service Health Dashboard](https://status.aws.amazon.com/)

### AWS Tools & CLI
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CloudShell](https://aws.amazon.com/cloudshell/)
- [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/)

## Statistics

- **Total Playbooks**: 168
- **Categories**: 8 (including Proactive monitoring)
- **Organization**: Numbered folders for easy navigation
- **Coverage**: All major AWS services and proactive monitoring

---

**Back to [Main Repository](../README.md)** | **View [K8s Playbooks](../K8s%20Playbooks/README.md)** | **View [Sentry Playbooks](../Sentry%20Playbooks/README.md)**
