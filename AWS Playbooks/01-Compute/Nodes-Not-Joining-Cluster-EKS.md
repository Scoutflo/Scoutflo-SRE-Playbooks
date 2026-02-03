# EKS Nodes Not Joining the Cluster

## Meaning

EKS nodes are not joining the cluster (triggering node registration failures or EKSNodeRegistrationFailed alarms) because node IAM role permissions are insufficient, node security group rules block cluster communication, node bootstrap script has errors, cluster endpoint access is restricted, node AMI is incompatible with cluster version, or EKS node group configuration is invalid. EKS nodes cannot join the cluster, Kubernetes cluster capacity is insufficient, and node registration fails. This affects the container orchestration layer and prevents cluster scaling, typically caused by IAM permission issues, network configuration problems, or version incompatibilities; if using EKS managed node groups vs self-managed, troubleshooting approaches differ and applications may experience node capacity issues.

## Impact

EKS nodes cannot join the cluster; Kubernetes cluster capacity is insufficient; node registration fails; cluster cannot scale; node NotReady status persists; node bootstrap errors occur; cluster node capacity is reduced; Kubernetes workloads cannot be scheduled. EKSNodeRegistrationFailed alarms may fire; if using EKS managed node groups vs self-managed, troubleshooting approaches differ; applications may experience errors or performance degradation due to insufficient node capacity; pod scheduling may fail.

## Playbook

1. Verify EKS cluster `<cluster-name>` exists and AWS service health for EKS and EC2 in region `<region>` is normal.
2. Retrieve the EKS Cluster `<cluster-name>` in region `<region>` and inspect its cluster endpoint configuration, cluster version, and node group configurations, verifying cluster endpoint access.
3. Retrieve the EC2 Instance `<instance-id>` that should join the cluster and inspect its IAM instance profile, security group rules, and instance state, verifying instance is running.
4. Query CloudWatch Logs for log groups containing EKS node logs and filter for node registration failure patterns, bootstrap errors, or cluster join errors, including bootstrap error messages.
5. Retrieve the IAM role `<role-name>` attached to EC2 instance `<instance-id>` and inspect its policy permissions for EKS cluster access and node registration, verifying IAM permissions.
6. List EC2 instances in node group for cluster `<cluster-name>` and check node registration status, instance health, and cluster join attempts, analyzing node status patterns.
7. Retrieve the EKS Cluster `<cluster-name>` endpoint access configuration and verify cluster endpoint access settings, checking if endpoint is public or private.
8. Retrieve the EKS Node Group `<node-group-name>` configuration and verify node group AMI, instance type, and cluster version compatibility, checking version compatibility.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for EKS cluster endpoint access or security group modification events related to cluster `<cluster-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs containing EKS node logs (from Playbook step 4) to identify specific bootstrap or registration failure messages. If logs show "AccessDenied" errors for EKS API calls, proceed immediately to IAM permission verification. If logs show "unable to connect to server" errors, network or endpoint access configuration is the issue. If logs show bootstrap script errors, examine the bootstrap configuration.

2. For access-denied errors, verify IAM instance profile permissions (from Playbook step 5) to ensure the node role has the required EKS managed policies: AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly, and AmazonEKS_CNI_Policy. If any of these policies are missing or detached, nodes cannot join the cluster.

3. Examine EC2 instance status and configuration (from Playbook step 3) to verify instances are running and have the correct instance profile attached. If instances are in pending or terminated state, or if the instance profile is missing, nodes cannot register with the cluster.

4. Review EKS cluster endpoint access configuration (from Playbook step 7) to verify nodes can reach the cluster API server. If endpoint is private-only and nodes are in subnets without access to the private endpoint, they cannot communicate with the control plane.

5. Verify security group configuration to ensure nodes have proper inbound/outbound rules for cluster communication. Nodes need to communicate with the cluster API server on port 443 and with each other on ports required by kubelet and CNI networking.

6. Check EKS node group configuration (from Playbook step 8) to verify AMI compatibility with the cluster version. If the node AMI version is incompatible with the EKS cluster version, nodes may fail to register properly.

7. Correlate CloudTrail events (from Playbook step 9) with node join failure timestamps within 10 minutes to identify any cluster endpoint access, security group, or IAM modifications. If configuration changes coincide with when nodes stopped joining, those changes are the likely cause.

8. Compare join failure patterns across different node groups within 1 hour. If failures are node group-specific, verify that node group's launch template and configuration. If failures are cluster-wide affecting all node groups, cluster endpoint access or IAM configuration is the root cause.

If no correlation is found within the specified time windows: extend timeframes to 48 hours, review alternative evidence sources including node bootstrap script execution and cluster API server connectivity, check for gradual issues like cluster version compatibility or node AMI updates, verify external dependencies like cluster endpoint availability or node security group configuration, examine historical patterns of node join failures, check for EKS managed node groups vs self-managed differences, verify EKS node group launch template issues. Node join failures may result from cluster endpoint access issues, node bootstrap script errors, cluster version incompatibility, EKS managed node group configuration problems, or EKS node group launch template issues rather than immediate node configuration changes.
