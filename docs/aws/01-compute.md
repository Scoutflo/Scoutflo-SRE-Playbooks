# AWS Compute Playbooks

> **27 playbooks** for EC2, Lambda, ECS, EKS, Fargate, and Auto Scaling issues.

## EC2 Playbooks

| Playbook | Description |
|----------|-------------|
| [Connection Timeout / SSH Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Connection-Timeout-SSH-Issues-EC2.md) | Troubleshoot SSH connection failures to EC2 instances |
| [High CPU Utilization](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/High-CPU-Utilization-EC2.md) | Diagnose and resolve high CPU usage on EC2 |
| [Instance Not Starting](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Instance-Not-Starting-EC2.md) | Fix EC2 instances that fail to start |
| [Instance Can't Reach Internet via NAT](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Instance-Cant-Reach-Internet-via-NAT-Gateway-EC2.md) | Resolve NAT Gateway connectivity issues |
| [Instance Unable to Reach Internet](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Instance-Unable-to-Reach-the-Internet-EC2.md) | General internet connectivity troubleshooting |
| [Stuck in Initializing State](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Stuck-in-Initializing-State-EC2.md) | Fix instances stuck during initialization |
| [Role Not Attaching to Instance](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Role-Not-Attaching-to-EC2-Instance-IAM.md) | Resolve IAM role attachment failures |

## Lambda Playbooks

| Playbook | Description |
|----------|-------------|
| [Cold Start Delays](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Cold-Start-Delays-Performance-Lambda.md) | Optimize Lambda cold start performance |
| [Connection Timeout from Lambda to RDS](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Connection-Timeout-from-Lambda-RDS.md) | Fix Lambda-to-RDS connection timeouts |
| [Exceeds Memory Limit](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Exceeds-Memory-Limit-Lambda.md) | Resolve Lambda memory limit errors |
| [Not Triggering from S3 Event](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Not-Triggering-from-S3-Event-Lambda.md) | Fix S3 event trigger failures |
| [Timeout Error](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Timeout-Error-Lambda.md) | Diagnose Lambda timeout issues |
| [DynamoDB Streams Not Triggering](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Streams-Not-Triggering-Lambda-DynamoDB.md) | Fix DynamoDB stream triggers |

## ECS Playbooks

| Playbook | Description |
|----------|-------------|
| [Image Pull Failing](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Image-Pull-Failing-in-ECS-Docker.md) | Resolve Docker image pull failures in ECS |
| [Logs Not Appearing in CloudWatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Logs-Not-Appearing-in-CloudWatch-ECS.md) | Fix ECS logging to CloudWatch |
| [Not Scaling as Expected](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Not-Scaling-as-Expected-ECS.md) | Troubleshoot ECS auto-scaling |
| [Task Stuck in Pending State](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Task-Stuck-in-Pending-State-ECS.md) | Fix ECS tasks stuck in pending |

## EKS Playbooks

| Playbook | Description |
|----------|-------------|
| [IAM Role Not Attaching to Service Account](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/IAM-Role-Not-Attaching-to-Service-Account-EKS.md) | Fix IRSA configuration issues |
| [Ingress Controller Not Routing Traffic](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Ingress-Controller-Not-Routing-Traffic-EKS.md) | Troubleshoot EKS ingress routing |
| [Nodes Not Joining Cluster](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Nodes-Not-Joining-Cluster-EKS.md) | Fix node registration failures |
| [Pod Stuck in CrashLoopBackOff](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Pod-Stuck-in-CrashLoopBackOff-EKS.md) | Diagnose pod crashes in EKS |

## Auto Scaling Playbooks

| Playbook | Description |
|----------|-------------|
| [Not Launching New Instances](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Not-Launching-New-Instances-Auto-Scaling.md) | Fix Auto Scaling launch failures |
| [Terminating Instances Unexpectedly](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Terminating-Instances-Unexpectedly-Auto-Scaling.md) | Investigate unexpected terminations |

## Spot Instance Playbooks

| Playbook | Description |
|----------|-------------|
| [Interrupted Unexpectedly](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Interrupted-Unexpectedly-Spot-Instance.md) | Handle spot instance interruptions |
| [Pricing Unexpectedly High](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Spot-Instance-Pricing-Unexpectedly-High-Cost.md) | Investigate spot pricing anomalies |

## Other Compute Playbooks

| Playbook | Description |
|----------|-------------|
| [Fargate Running Out of Memory](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Running-Out-of-Memory-Fargate.md) | Fix Fargate memory issues |
| [CodeDeploy Failing on EC2](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/AWS%20Playbooks/01-Compute/Failing-on-EC2-Instances-CodeDeploy.md) | Troubleshoot CodeDeploy failures |

---

[Back to AWS Overview](/aws/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/AWS%20Playbooks/01-Compute)
