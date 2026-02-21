# Real-World Examples

> See how teams use SRE Playbooks to resolve incidents faster.

## Example 1: Production Pod CrashLoopBackOff

### Scenario
A critical production service starts experiencing `CrashLoopBackOff` after a deployment.

### Using the Playbook

**Step 1**: Navigate to [CrashLoopBackOff playbook](/k8s/03-pods?id=crashloopbackoff)

**Step 2**: Follow diagnostic steps:

```bash
# Check pod status
kubectl get pod payment-service-abc123 -n production

# Output:
# NAME                     READY   STATUS             RESTARTS   AGE
# payment-service-abc123   0/1     CrashLoopBackOff   5          10m
```

**Step 3**: Check events:

```bash
kubectl describe pod payment-service-abc123 -n production | grep -A 10 Events

# Found: OOMKilled - container exceeded memory limits
```

**Step 4**: Apply diagnosis from playbook:

> "If OOMKilled events found, the container exceeded memory limits. Increase memory limits or optimize application."

**Resolution**: Increased memory limits from 512Mi to 1Gi. Deployment recovered.

---

## Example 2: Service Connection Refused

### Scenario
Users report "Connection Refused" errors when accessing the API.

### Using the Playbook

**Step 1**: Navigate to [Service Not Accessible playbook](/k8s/05-networking?id=servicenotaccessible)

**Step 2**: Check service endpoints:

```bash
kubectl get endpoints api-service -n production

# Output:
# NAME          ENDPOINTS   AGE
# api-service   <none>      45d
```

**Step 3**: No endpoints! Check pod labels:

```bash
kubectl get pods -n production --show-labels | grep api

# Pods have label: app=api-v2
# Service selector: app=api
```

**Step 4**: Apply diagnosis:

> "If endpoints is empty, verify pod labels match service selector."

**Resolution**: Updated service selector to `app=api-v2`. Endpoints populated, traffic restored.

---

## Example 3: Lambda Timeout Spike

### Scenario
CloudWatch alerts show Lambda function timeout rate increased from 0.1% to 15%.

### Using the Playbook

**Step 1**: Navigate to [Lambda Timeout playbook](/aws/01-compute?id=lambda-timeout)

**Step 2**: Check CloudWatch Logs:

```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/process-orders \
  --filter-pattern "Task timed out"

# Found: Multiple timeouts during DynamoDB calls
```

**Step 3**: Check DynamoDB:

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ThrottledRequests \
  --dimensions Name=TableName,Value=orders \
  --start-time 2026-02-21T00:00:00Z \
  --end-time 2026-02-21T12:00:00Z \
  --period 300 \
  --statistics Sum

# Found: Throttling events correlate with Lambda timeouts
```

**Step 4**: Apply diagnosis:

> "If DynamoDB throttling correlates with timeout spikes, increase provisioned capacity or enable auto-scaling."

**Resolution**: Enabled DynamoDB auto-scaling. Timeout rate dropped to normal.

---

## Example 4: Sentry Error Spike After Deployment

### Scenario
Sentry shows 500% increase in `NullPointerException` after v2.3.1 deployment.

### Using the Playbook

**Step 1**: Navigate to [NullPointerException playbook](/sentry/01-error-tracking)

**Step 2**: Check release correlation in Sentry:
- Error first seen in v2.3.1
- All affected users on v2.3.1

**Step 3**: Analyze stack trace:
```
NullPointerException at UserService.getProfile(UserService.java:142)
  user.getPreferences().getNotificationSettings()
```

**Step 4**: Apply diagnosis:

> "If errors correlate with specific release, check code changes in that release for null handling."

**Resolution**: Added null check for `user.getPreferences()`. Deployed v2.3.2 hotfix.

---

## Workflow Integration

### Incident Response Workflow

```
1. Alert fires (PagerDuty, Prometheus, CloudWatch)
         ↓
2. Identify alert type (K8s, AWS, Sentry)
         ↓
3. Find matching playbook
         ↓
4. Follow diagnostic steps
         ↓
5. Apply diagnosis logic
         ↓
6. Implement resolution
         ↓
7. Document in incident report
```

### AI Agent Workflow

These playbooks are designed for AI agents in tools like:
- Voyager (Scoutflo's AI agent)
- Custom LLM-powered SRE bots
- ChatOps integrations

Example prompt to AI agent:
> "My pods are in CrashLoopBackOff. Help me diagnose."

The agent retrieves the playbook and executes steps automatically.

---

## Contributing Examples

Have a real-world example? [Submit a PR](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/pulls) adding to this page!

---

[Back to Home](/)
