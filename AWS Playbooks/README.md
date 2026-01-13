# AWS Playbooks

[![AWS](https://img.shields.io/badge/AWS-25%20playbooks-orange)](README.md)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](../../CONTRIBUTING.md)

> **25 comprehensive AWS incident response playbooks** - Systematic troubleshooting guides for common AWS service issues to help SREs diagnose and resolve infrastructure problems faster.

## 📋 Table of Contents

- [Overview](#overview)
- [Playbook Structure](#playbook-structure)
- [Complete Playbook List](#complete-playbook-list)
- [Getting Started](#getting-started)
- [Usage Guidelines](#usage-guidelines)
- [Contributing](#contributing)
- [Connect with Us](#connect-with-us)
- [Related Resources](#related-resources)

## Overview

This directory contains **25 AWS incident response playbooks** designed to help Site Reliability Engineers (SREs) diagnose and resolve common AWS service issues. Each playbook follows a structured format to provide systematic troubleshooting guidance.

### Services Covered

- **Compute Services**: EC2, Lambda, ECS, EKS
- **Networking**: VPC, ELB, Route 53, NAT Gateway
- **Storage**: S3, EBS, RDS
- **Security**: IAM, KMS, GuardDuty, CloudTrail
- **Integration**: API Gateway, CodePipeline

### Key Topics

- Connection timeouts and network issues
- Access denied and permission problems
- Resource unavailability and capacity issues
- Security breaches and threat detection
- Service integration failures

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

## Getting Started

### 1. Documentation

This directory contains 25 AWS incident response playbooks covering critical AWS services. Each playbook provides systematic troubleshooting guidance for common AWS issues.

**Quick Navigation:**
- Browse all playbooks in this directory
- Use Ctrl+F (or Cmd+F) to search for specific issues
- Match your symptoms to playbook titles

### 2. Installation

Clone this repository to access the AWS playbooks:

```bash
# Clone the repository
git clone https://github.com/Scoutflo/scoutflo-SRE-Playbooks.git

# Navigate to AWS playbooks
cd scoutflo-SRE-Playbooks/AWS\ Playbooks/

# List all available playbooks
ls *.md

# View a specific playbook
cat Connection-Timeout-SSH-Issues-EC2.md
```

**Quick Access Options:**
- **Bookmark this directory** for quick reference during incidents
- **Add to your SRE runbook collection** for easy access
- **Use GitHub web interface** to search and view playbooks online
- **Clone locally** for offline access and customization

### 3. Learn More

- **Watch Tutorials**: Check our [YouTube channel](https://www.youtube.com/@scoutflo6727) for AWS troubleshooting walkthroughs
- **AI SRE Demo**: Watch the [Scoutflo AI SRE Demo](https://youtu.be/P6xzFUtRqRc?si=0VN9oMV05rNzXFs8) to see AI-powered incident response
- **AWS Documentation**: Refer to [AWS Official Documentation](https://docs.aws.amazon.com/) for service details
- **Best Practices**: Review [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- **Scoutflo Documentation**: Visit [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) for platform guides
- **Community**: Join discussions in our [Slack workspace](https://scoutflo.slack.com)

## Usage Guidelines

### Step-by-Step Process

1. **Identify the Issue**: Match your symptoms to the appropriate playbook title
2. **Open the Playbook**: Navigate to the relevant `.md` file
3. **Follow the Playbook**: Execute the numbered steps in order, replacing placeholder values (e.g., `<instance-id>`) with your actual resource identifiers
4. **Review Diagnosis Section**: Use the correlation analysis to identify root causes
5. **Extend Time Windows**: If initial correlations don't reveal the cause, extend time windows as suggested
6. **Check Alternative Sources**: Review alternative evidence sources mentioned in the Diagnosis section

### Example Workflow

**Scenario**: EC2 instance SSH connection timeout

1. Open `Connection-Timeout-SSH-Issues-EC2.md`
2. Read the **Meaning** section to understand the issue
3. Review the **Impact** section to assess severity
4. Follow **Playbook** steps:
   - Step 1: Verify instance is running
   - Step 2: Check security group rules
   - Step 3: Verify public IP assignment
   - ... (continue through all steps)
5. Use **Diagnosis** section to correlate events:
   - Compare security group changes with connection failures
   - Check if failures began after recent changes
6. Apply the identified fix

### Common Placeholders

Playbooks use the following placeholder format that should be replaced with actual values:
- `<instance-id>` - EC2 instance identifier
- `<bucket-name>` - S3 bucket name
- `<region>` - AWS region
- `<function-name>` - Lambda function name
- `<role-name>` - IAM role name
- `<user-name>` - IAM user name
- `<security-group-id>` - Security group identifier
- `<vpc-id>` - VPC identifier
- `<rds-instance-id>` - RDS instance identifier
- `<load-balancer-name>` - Load balancer name

## Terminology & Glossary

### AWS Service Abbreviations

**EC2 (Elastic Compute Cloud)**
- AWS's virtual server service. An "EC2 instance" is a virtual machine running on AWS.

**VPC (Virtual Private Cloud)**
- An isolated network environment within AWS where you can launch resources like EC2 instances.

**IAM (Identity and Access Management)**
- AWS service that manages user access, roles, and permissions to AWS resources.

**S3 (Simple Storage Service)**
- AWS's object storage service for storing files, backups, and data.

**RDS (Relational Database Service)**
- AWS's managed database service for relational databases like MySQL, PostgreSQL, Oracle, etc.

**Lambda**
- AWS's serverless computing service that runs code without managing servers. You just upload code and it runs.

**ELB (Elastic Load Balancer)**
- AWS service that distributes incoming traffic across multiple targets (like EC2 instances) to ensure high availability.

**CloudWatch**
- AWS's monitoring and observability service for collecting metrics, logs, and events from AWS resources.

**CloudTrail**
- AWS service that logs API calls and changes made to your AWS account for security and compliance.

**GuardDuty**
- AWS's threat detection service that continuously monitors for malicious activity and unauthorized behavior.

**KMS (Key Management Service)**
- AWS service for creating and managing encryption keys used to encrypt your data.

**NAT Gateway**
- A network address translation service that allows resources in private subnets to access the internet securely.

**Route 53**
- AWS's DNS (Domain Name System) web service that routes internet traffic to your applications.

**EKS (Elastic Kubernetes Service)**
- AWS's managed Kubernetes service for running containerized applications.

**ECS (Elastic Container Service)**
- AWS's container orchestration service for running Docker containers.

**API Gateway**
- AWS service that creates, publishes, and manages APIs for your applications.

**CodePipeline**
- AWS's continuous delivery service for automating release pipelines.

### Common AWS Terms

**Security Group**
- A virtual firewall that controls inbound and outbound traffic for AWS resources.

**IAM Role**
- An AWS identity with permissions that can be assumed by AWS services or users.

**IAM Policy**
- A document that defines permissions for AWS resources. Attached to users, groups, or roles.

**Region**
- A geographic area where AWS has data centers (e.g., us-east-1, eu-west-1).

**Availability Zone (AZ)**
- One or more discrete data centers within a region, designed to be isolated from failures in other zones.

**Subnet**
- A range of IP addresses in your VPC where you can launch resources.

**Internet Gateway**
- A horizontally scaled, redundant component that allows communication between your VPC and the internet.

**Target Group**
- A group of resources (like EC2 instances) that receive traffic from a load balancer.

**Health Check**
- A periodic check to determine if a resource is healthy and should receive traffic.

### Playbook Terms

**Diagnosis Section**
- Part of each playbook that helps you correlate events (like configuration changes) with failures using time-based analysis.

**Placeholder**
- A value in playbooks (like `<instance-id>`) that you replace with your actual AWS resource identifier.

**Correlation Window**
- A time period you examine to find relationships between events and failures (e.g., "check CloudTrail logs from the last 30 minutes").

**Root Cause**
- The underlying reason why an issue occurred, as opposed to just the symptoms you're seeing.

**CloudWatch Logs Insights**
- A feature that allows you to search and analyze log data from CloudWatch Logs using a query language.

---

**Need more help?** Check out:
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Scoutflo Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation)

### Best Practices

- **Start Early**: Begin with the most common causes (earlier steps in the Playbook section)
- **Use CloudWatch Logs Insights**: Efficient log analysis for troubleshooting
- **Correlate Timestamps**: Use the Diagnosis section to correlate events with failures
- **Document Findings**: Keep notes of what you've checked and what you found
- **Consider Gradual Issues**: If immediate correlations aren't found, check for gradual degradation
- **Check AWS Service Health**: Verify if AWS service issues are affecting your resources
- **Review CloudTrail Events**: Check for configuration changes that might have caused the issue

## Contributing

We welcome contributions to improve AWS playbooks! Your contributions help the entire SRE community.

### How to Contribute

#### 1. Raising Issues

If you find an error, unclear instructions, or have suggestions:

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) first
2. **Create a New Issue**:
   - Use clear, descriptive title (e.g., "Fix: Incorrect step in Connection-Timeout-SSH-Issues-EC2.md")
   - Describe the problem or suggestion
   - Include relevant AWS service, error messages, or examples
   - Tag with `aws-playbook` label

#### 2. Updating Existing Playbooks

To improve or fix existing AWS playbooks:

1. **Fork the Repository**: Create your own fork
2. **Create a Branch**:
   ```bash
   git checkout -b fix/aws-playbook-name
   ```
3. **Make Your Changes**:
   - Follow the established structure (Title, Meaning, Impact, Playbook, Diagnosis)
   - Use consistent placeholder naming (`<instance-id>`, `<bucket-name>`, etc.)
   - Maintain accuracy and clarity
   - Ensure steps are actionable and specific
4. **Test Your Changes**: Verify the playbook works with real AWS scenarios
5. **Commit and Push**:
   ```bash
   git add AWS\ Playbooks/Your-Playbook-Name.md
   git commit -m "Fix: Improve [playbook-name] - [description]"
   git push origin fix/aws-playbook-name
   ```
6. **Create a Pull Request**: 
   - Reference the issue (if applicable)
   - Describe your changes clearly
   - Request review from maintainers

#### 3. Adding New AWS Playbooks

To add a new playbook for an uncovered AWS issue:

1. **Check for Duplicates**: Ensure a similar playbook doesn't exist
2. **Follow Naming Convention**: `<IssueOrSymptom>-<Component>.md`
   - Example: `Connection-Timeout-SSH-Issues-EC2.md`
   - Example: `Bucket-Access-Denied-403-Error-S3.md`
3. **Include All Required Sections**:
   - **Title** (H1): Clear, descriptive title
   - **Meaning** (H2): What the issue means, triggers, symptoms, affected service layer
   - **Impact** (H2): Business and technical impact, alarms, cascading effects
   - **Playbook** (H2): 8-10 numbered diagnostic steps with AWS resource identifiers
   - **Diagnosis** (H2): 5 correlation analysis steps with time windows
4. **Use AWS MCP Tools**: Ensure playbook steps use only available AWS MCP tools
5. **Update README**: Add the new playbook to the "Complete Playbook List" section above
6. **Create Pull Request**: Follow standard contribution process

### Contribution Guidelines

- **Follow Structure**: Maintain consistency with existing playbooks
- **Use Placeholders**: Replace specific values with placeholders
- **Be Actionable**: Provide clear, step-by-step instructions
- **Include Correlation**: Add time-based correlation in Diagnosis section
- **Test Accuracy**: Verify playbooks work with real AWS scenarios
- **Document Changes**: Clearly describe what and why you changed

### Review Process

1. All contributions require maintainer review
2. Feedback provided within 2-3 business days
3. Address requested changes promptly
4. Once approved, your contribution will be merged

📖 For detailed contribution guidelines, see [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Connect with Us

**Want to contribute?** Read our [Contributing Guidelines](#contributing) above.

**For Feedback or Feature Requests**: 
- Share with us in [Slack](https://scoutflo.slack.com) or create a [GitHub Issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)

**Bug Report?** 
- Create a detailed issue and share it with us on [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues) or [Slack](https://scoutflo.slack.com)

**Links:**
- [Slack Community](https://scoutflo.slack.com) | [Roadmap](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/projects) | [Documentation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/wiki)

**Scoutflo Resources:**
- [Official Documentation](https://scoutflo-documentation.gitbook.io/scoutflo-documentation) | [Website](https://scoutflo.com/) | [AI SRE Tool](https://ai.scoutflo.com/get-started)
- [Infra Management Tool](https://deploy.scoutflo.com/) | [YouTube Channel](https://www.youtube.com/@scoutflo6727) | [LinkedIn](https://www.linkedin.com/company/scoutflo/)
- [Twitter/X](https://x.com/scout_flo) | [Blog](https://scoutflo.com/blog) | [Pricing](https://scoutflo.com/pricing)

## Related Resources

### AWS Documentation
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Troubleshooting Guides](https://docs.aws.amazon.com/general/latest/gr/aws_troubleshooting.html)
- [AWS Service Health Dashboard](https://status.aws.amazon.com/)

### AWS Tools
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
- [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/)

### SRE Resources
- [Google SRE Book](https://sre.google/books/)
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)

---

**Back to [Main Repository](../../README.md)** | **View [K8s Playbooks](../K8s%20Playbooks/README.md)**
