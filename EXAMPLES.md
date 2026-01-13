# Examples & Use Cases

Real-world scenarios showing how to use the SRE Playbooks effectively.

## Quick Examples

### Example 1: Pod Stuck in CrashLoopBackOff

**Scenario**: Your application pod keeps crashing and restarting.

**Steps:**
1. Navigate to `K8s Playbooks/03-Pods/`
2. Open `CrashLoopBackOff-pod.md`
3. Follow the Playbook steps:
   ```bash
   # Step 1: Get pod logs
   kubectl logs <pod-name> -n <namespace> --previous
   
   # Step 2: Check pod events
   kubectl describe pod <pod-name> -n <namespace>
   
   # Step 3: Verify container image
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'
   ```
4. Use the Diagnosis section to correlate with recent changes
5. Apply the fix based on findings

**Outcome**: Identified missing environment variable causing application crash. Fixed by updating the deployment configuration.

---

### Example 2: EC2 Instance SSH Connection Timeout

**Scenario**: You can't SSH into your EC2 instance.

**Steps:**
1. Navigate to `AWS Playbooks/`
2. Open `Connection-Timeout-SSH-Issues-EC2.md`
3. Follow the Playbook steps:
   ```bash
   # Step 1: Check instance state
   aws ec2 describe-instances --instance-ids <instance-id>
   
   # Step 2: Verify security group rules
   aws ec2 describe-security-groups --group-ids <security-group-id>
   
   # Step 3: Check public IP assignment
   aws ec2 describe-instances --instance-ids <instance-id> --query 'Reservations[0].Instances[0].PublicIpAddress'
   ```
4. Use CloudTrail logs to check for recent security group changes
5. Apply the fix (in this case, added SSH rule to security group)

**Outcome**: Security group was missing SSH (port 22) rule. Added the rule and connection restored.

---

### Example 3: Service Not Resolving DNS

**Scenario**: Pods can't reach a Kubernetes service by name.

**Steps:**
1. Navigate to `K8s Playbooks/05-Networking/`
2. Open `ServiceNotResolvingDNS-dns.md`
3. Follow the Playbook steps:
   ```bash
   # Step 1: Check service exists
   kubectl get service <service-name> -n <namespace>
   
   # Step 2: Verify CoreDNS pods
   kubectl get pods -n kube-system | grep coredns
   
   # Step 3: Test DNS resolution
   kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>.<namespace>.svc.cluster.local
   ```
4. Check CoreDNS logs for errors
5. Found CoreDNS pod was crashing, restarted it

**Outcome**: CoreDNS pod was in CrashLoopBackOff. Restarted the pod and DNS resolution restored.

---

### Example 4: RDS Database Connection Timeout

**Scenario**: Lambda function can't connect to RDS database.

**Steps:**
1. Navigate to `AWS Playbooks/`
2. Open `Connection-Timeout-from-Lambda-RDS.md`
3. Follow the Playbook steps:
   ```bash
   # Step 1: Check RDS instance status
   aws rds describe-db-instances --db-instance-identifier <rds-instance-id>
   
   # Step 2: Verify security group rules
   aws ec2 describe-security-groups --group-ids <rds-security-group-id>
   
   # Step 3: Check Lambda VPC configuration
   aws lambda get-function-configuration --function-name <function-name>
   ```
4. Correlated with recent VPC configuration change
5. Found Lambda was in wrong subnet, moved to correct subnet

**Outcome**: Lambda function was in a subnet without route to RDS. Updated VPC configuration and connection restored.

---

### Example 5: Deployment Not Scaling

**Scenario**: HPA should scale your deployment but it's not working.

**Steps:**
1. Navigate to `K8s Playbooks/04-Workloads/`
2. Open `HPAHorizontalPodAutoscalerNotScaling-workload.md`
3. Follow the Playbook steps:
   ```bash
   # Step 1: Check HPA status
   kubectl get hpa -n <namespace>
   
   # Step 2: Verify Metrics Server
   kubectl get pods -n kube-system | grep metrics-server
   
   # Step 3: Check resource metrics
   kubectl top pods -n <namespace>
   ```
4. Found Metrics Server was down
5. Restarted Metrics Server pod

**Outcome**: Metrics Server pod was down, preventing HPA from getting metrics. Restarted pod and HPA started scaling correctly.

---

## Common Workflows

### Workflow 1: On-Call Incident Response

**When**: You're on-call and get an alert.

1. **Identify the issue**: Match alert to playbook title
2. **Navigate quickly**: Use category folders for K8s issues
3. **Follow playbook**: Execute steps in order
4. **Use Diagnosis**: Correlate with recent changes
5. **Document**: Note what you found and fixed

**Time Saved**: Reduced MTTR from 45 minutes to 15 minutes

---

### Workflow 2: New Team Member Training

**When**: Onboarding a new SRE team member.

1. **Review structure**: Show them the repository organization
2. **Walk through example**: Use a common playbook together
3. **Practice**: Have them follow a playbook for a test issue
4. **Bookmark**: Save frequently used playbooks
5. **Contribute**: Encourage them to improve playbooks

**Outcome**: New team member productive in 2 days instead of 2 weeks

---

### Workflow 3: Post-Incident Review

**When**: After resolving an incident.

1. **Review playbook used**: Did it help? What was missing?
2. **Improve playbook**: Add steps that would have helped
3. **Share learnings**: Update playbook with new insights
4. **Contribute back**: Submit improvements to the repository

**Outcome**: Playbooks continuously improve based on real incidents

---

## Advanced Use Cases

### Use Case 1: Multi-Cloud Troubleshooting

**Scenario**: Application spans AWS and Kubernetes (EKS).

**Approach:**
1. Use AWS playbooks for AWS-specific issues (EC2, RDS, etc.)
2. Use K8s playbooks for Kubernetes issues (pods, services, etc.)
3. Cross-reference when issues span both (e.g., EKS control plane)

**Example**: EC2 instance can't reach EKS cluster
- Check AWS playbooks for EC2 networking
- Check K8s playbooks for service accessibility
- Found security group misconfiguration affecting both

---

### Use Case 2: Automation Integration

**Scenario**: Integrate playbooks into your incident response automation.

**Approach:**
1. Parse playbook steps into automated checks
2. Use playbook structure for runbook automation
3. Correlate with monitoring data using Diagnosis section

**Example**: Automated health checks based on playbook steps
- Script checks pod status (from playbook Step 1)
- Script checks node resources (from playbook Step 2)
- Alerts when thresholds exceeded

---

### Use Case 3: Documentation Standardization

**Scenario**: Standardize troubleshooting procedures across teams.

**Approach:**
1. Use playbook structure as template
2. Customize for organization-specific tools
3. Maintain consistency across all runbooks

**Example**: All team runbooks now follow same structure
- Consistent format makes knowledge transfer easier
- New team members can follow any runbook
- Easier to maintain and update

---

## Tips for Success

### Tip 1: Start with Common Issues

Focus on playbooks for issues you encounter most:
- Pod crashes (CrashLoopBackOff)
- Service connectivity
- Resource quotas
- Network policies

### Tip 2: Customize for Your Environment

Fork the repository and:
- Add organization-specific steps
- Include internal tool commands
- Add team-specific notes

### Tip 3: Build a Playbook Library

Create your own collection:
- Bookmark frequently used playbooks
- Add custom playbooks for your infrastructure
- Share with your team

### Tip 4: Use During Post-Mortems

After incidents:
- Review which playbook was used
- Identify gaps
- Improve the playbook
- Contribute improvements back

---

## Success Stories

### Story 1: Reduced MTTR by 60%

**Before**: Average 45 minutes to resolve incidents
**After**: Average 18 minutes using playbooks
**Key Factor**: Systematic approach eliminated guesswork

### Story 2: Improved Team Confidence

**Before**: Junior engineers hesitant to handle incidents
**After**: All engineers confident following playbooks
**Key Factor**: Clear, step-by-step guidance

### Story 3: Better Documentation

**Before**: Inconsistent troubleshooting notes
**After**: Standardized playbook format
**Key Factor**: Consistent structure across all runbooks

---

**Have your own success story?** Share it in [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)!

**Need help with a specific scenario?** [Ask the community](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions/categories/q-a)!
