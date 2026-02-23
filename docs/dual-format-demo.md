# Dual-Format Playbooks Demo

> **Try the toggle!** Use the **NLP / CLI / Both** buttons in the top-right corner to switch between formats.

This page showcases our new dual-format playbook structure. Each playbook now includes:
- **For AI Agents (NLP)** - Natural language instructions for AI-powered automation
- **For DevOps/SREs (CLI)** - Copy-paste ready CLI commands

---

## Pilot Playbook 1: CrashLoopBackOff (Kubernetes)

**File:** `K8s Playbooks/03-Pods/CrashLoopBackOff-pod.md`

### Meaning

A pod container repeatedly starts and exits with errors shortly after launch, causing Kubernetes to back off and restart it in a CrashLoopBackOff state (triggering KubePodCrashLooping alerts) instead of reaching a stable Running state. This indicates application configuration errors, resource constraints, dependency failures, or container image issues preventing successful pod startup.

### Impact

Application pods fail to start; services become unavailable; deployments cannot achieve desired replica count; applications experience downtime; dependent services may fail; KubePodCrashLooping alerts fire; pods remain in CrashLoopBackOff state; containers exit repeatedly; application errors prevent pod stability; replica counts mismatch desired state.

### Playbook

#### For AI Agents (NLP)

1. Describe pod `<pod-name>` in namespace `<namespace>` to see pod status, restart count, termination reason (OOMKilled, Error, etc.), and recent events - this immediately shows why the pod is crashing.

2. Retrieve events in namespace `<namespace>` for pod `<pod-name>` sorted by timestamp to see the sequence of failures with timestamps.

3. Retrieve pod `<pod-name>` in namespace `<namespace>` and check container termination reason from container status - if OOMKilled, the issue is memory limits.

4. Retrieve logs from pod `<pod-name>` in namespace `<namespace>` from the previous (crashed) container to see what happened before the crash.

5. Describe deployment `<deployment-name>` in namespace `<namespace>` to check container image, resource limits, environment variables, and liveness/readiness probe configuration.

6. Retrieve rollout history for deployment `<deployment-name>` in namespace `<namespace>` to check if the issue started after a recent deployment.

#### For DevOps/SREs (CLI)

1. Check pod status, restart count, and events:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. Get events sorted by timestamp:
   ```bash
   kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name> --sort-by='.lastTimestamp'
   ```

3. Check container termination reason:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[*].lastState.terminated}'
   ```

4. Get logs from previous crashed container:
   ```bash
   kubectl logs <pod-name> -n <namespace> --previous
   ```

5. Check deployment configuration:
   ```bash
   kubectl describe deployment <deployment-name> -n <namespace>
   kubectl get deployment <deployment-name> -n <namespace> -o yaml
   ```

6. Check rollout history:
   ```bash
   kubectl rollout history deployment/<deployment-name> -n <namespace>
   ```

### Diagnosis

1. Analyze pod events to identify the primary failure reason. Events showing "BackOff" with "CrashLoopBackOff" indicate container crashes.

2. If termination reason shows "OOMKilled", the container exceeded its memory limit. Increase memory limits or investigate memory leaks.

3. If termination reason shows "Error" with a non-zero exit code, analyze container logs for application-level errors.

---

## Pilot Playbook 2: ImagePullBackOff (Kubernetes)

**File:** `K8s Playbooks/03-Pods/ImagePullBackOff-registry.md`

### Meaning

Kubelet is repeatedly failing to pull a container image from the registry (triggering ImagePullBackOff or ErrImagePull pod states) because the image reference is invalid, credentials are wrong, image pull secrets are missing or expired, or the registry or network path to it is unavailable.

### Impact

Pods cannot start; deployments remain at 0 replicas; rolling updates fail; applications fail to deploy; services become unavailable; pods stuck in ImagePullBackOff state.

### Playbook

#### For AI Agents (NLP)

1. Describe pod `<pod-name>` in namespace `<namespace>` to see the exact error message for image pull failure - look in Events section for "Failed to pull image" with the specific reason (auth error, not found, timeout).

2. Retrieve events for pod `<pod-name>` in namespace `<namespace>` filtered by reason Failed and sorted by timestamp to see the sequence of image pull failures.

3. Verify the image exists and is accessible: retrieve the image name for pod `<pod-name>` in namespace `<namespace>` and test image pull manually on the node.

4. Check imagePullSecrets configuration: retrieve the imagePullSecrets for pod `<pod-name>` in namespace `<namespace>`, verify the secret exists, and decode and verify the credentials.

5. Describe Deployment `<deployment-name>` in namespace `<namespace>` to verify the image reference is correct (registry, repository, tag) and check if imagePullSecrets are properly configured.

6. Test registry connectivity from a pod in the same namespace by executing a request to the registry URL.

7. Check node disk space where pod is scheduled - insufficient disk prevents image pulls.

#### For DevOps/SREs (CLI)

1. Check pod events for image pull errors:
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Events:"
   ```

2. Get events filtered by image pull failures:
   ```bash
   kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>,reason=Failed --sort-by='.lastTimestamp'
   ```

3. Verify image reference and test pull:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'
   # On node: docker pull <image-name> OR crictl pull <image-name>
   ```

4. Check imagePullSecrets and decode credentials:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.imagePullSecrets[*].name}'
   kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d
   ```

5. Check deployment image configuration:
   ```bash
   kubectl describe deployment <deployment-name> -n <namespace>
   kubectl get deployment <deployment-name> -n <namespace> -o jsonpath='{.spec.template.spec.containers[*].image}'
   ```

6. Test registry connectivity from a debug pod:
   ```bash
   kubectl run test-registry --rm -it --image=curlimages/curl -- curl -I https://<registry-url>/v2/
   ```

7. Check node disk space:
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.nodeName}'
   kubectl debug node/<node-name> -it --image=busybox -- df -h
   ```

### Diagnosis

1. Events showing "unauthorized" indicate credential issues. Events showing "not found" indicate the image doesn't exist.

2. If authentication fails, verify imagePullSecrets configuration and credentials.

3. If network issues, check if the node can reach the registry and DNS resolution works.

---

## Pilot Playbook 3: EC2 SSH Connection Timeout (AWS)

**File:** `AWS Playbooks/01-Compute/Connection-Timeout-SSH-Issues-EC2.md`

### Meaning

EC2 instance SSH connections timeout or fail because security group rules block SSH access, the instance lacks a public IP address, key pair mismatches occur, or network connectivity issues prevent SSH access.

### Impact

Administrators cannot access instances; SSH connection timeout errors occur; remote management fails; troubleshooting is blocked; operational tasks delayed.

### Playbook

#### For AI Agents (NLP)

1. Verify instance `<instance-id>` is in "running" state and AWS service health for EC2 in region `<region>` is normal.

2. Retrieve the Security Group `<security-group-id>` associated with EC2 instance `<instance-id>` and inspect inbound rules for SSH port 22 access.

3. Retrieve the EC2 Instance `<instance-id>` in region `<region>` and verify public IP address or Elastic IP assignment.

4. Verify the key pair `<key-pair-name>` matches the key pair assigned to instance `<instance-id>`.

5. Retrieve the EC2 Instance `<instance-id>` metadata service configuration and verify IMDSv2 enforcement settings.

6. Retrieve the EC2 Instance `<instance-id>` IAM role configuration and verify instance profile is attached.

7. Retrieve CloudWatch Logs for EC2 serial console output for instance `<instance-id>` and filter for connection errors.

8. Retrieve the Route Table and Network ACL for subnet containing instance `<instance-id>` and verify routes and rules allow SSH traffic.

9. Query VPC Flow Logs and filter for blocked traffic to instance `<instance-id>` on port 22.

#### For DevOps/SREs (CLI)

1. Check instance state and AWS service health:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id> --region <region> --query 'Reservations[*].Instances[*].[State.Name,InstanceId]' --output table
   aws health describe-events --filter services=EC2 --region <region>
   ```

2. Check security group inbound rules for SSH:
   ```bash
   aws ec2 describe-security-groups --group-ids <security-group-id> --region <region> --query 'SecurityGroups[*].IpPermissions[?FromPort==`22`]' --output json
   ```

3. Verify public IP and subnet configuration:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id> --region <region> --query 'Reservations[*].Instances[*].[PublicIpAddress,SubnetId,VpcId]' --output table
   ```

4. Check key pair assignment:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id> --region <region> --query 'Reservations[*].Instances[*].KeyName' --output text
   ```

5. Check IMDSv2 configuration:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id> --region <region> --query 'Reservations[*].Instances[*].MetadataOptions' --output json
   ```

6. Check IAM instance profile:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id> --region <region> --query 'Reservations[*].Instances[*].IamInstanceProfile' --output json
   ```

7. Get EC2 serial console output:
   ```bash
   aws ec2 get-console-output --instance-id <instance-id> --region <region> --output text
   ```

8. Check route table and NACL rules:
   ```bash
   aws ec2 describe-route-tables --route-table-ids <route-table-id> --region <region> --output table
   aws ec2 describe-network-acls --network-acl-ids <nacl-id> --region <region> --query 'NetworkAcls[*].Entries' --output json
   ```

9. Query VPC Flow Logs for blocked SSH traffic:
   ```bash
   aws logs filter-log-events --log-group-name <vpc-flow-logs-group> --filter-pattern "REJECT <instance-id> 22" --region <region>
   ```

### Diagnosis

1. If security group rules don't allow SSH from the client IP, network access is blocked at the security group level.

2. If instance has no public IP and is in a private subnet, SSH is only possible via bastion host or VPN.

3. If key pair doesn't match, authentication will fail with "Permission denied" errors.

---

## Feedback Requested

We'd love your feedback on this dual-format approach:

1. **Is the structure clear?** Can you easily find both NLP and CLI versions?
2. **Is the toggle useful?** Would you prefer NLP, CLI, or Both as default?
3. **Are CLI commands accurate?** Any commands that need adjustment?
4. **Missing information?** Anything else you'd like to see in playbooks?

---

[Back to Home](/) | [View Contributing Guidelines](/contributing)
