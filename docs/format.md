# Playbook Format

> All playbooks follow a standardized 4-section structure for consistency.

## Required Sections

### 1. Meaning

Explain what the issue means and why it occurs:

```markdown
## Meaning

This alert fires when [condition]. Common causes include:
- Cause 1
- Cause 2
- Cause 3

Related alerts: `AlertName1`, `AlertName2`
```

**Guidelines:**
- Include Prometheus/CloudWatch alert names
- Add cross-domain keywords for searchability
- Explain the underlying mechanism

### 2. Impact

Describe business and technical consequences:

```markdown
## Impact

**Severity:** Critical/High/Medium/Low

**Business Impact:**
- User-facing effect
- Revenue/SLA impact

**Technical Impact:**
- System degradation
- Cascading failures
```

**Guidelines:**
- Be specific about consequences
- Include SLA implications
- Mention affected services

### 3. Playbook

Step-by-step diagnostic procedures:

```markdown
## Playbook

1. Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status and restart count.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

</details>

2. Retrieve logs from pod `<pod-name>` and analyze error messages.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
```

</details>

3. Continue with additional steps...
```

**Guidelines:**
- Use numbered steps (8-10 steps recommended)
- Use NLP-friendly language with action verbs
- Include placeholders in angle brackets: `<pod-name>`
- Add collapsible CLI sections
- Order from most common to specific causes

### 4. Diagnosis

Root cause analysis with conditional logic:

```markdown
## Diagnosis

1. **Analyze events from Playbook step 1:**
   - If `OOMKilled` events found, the container exceeded memory limits. Increase memory limits or optimize application.
   - If `CrashLoopBackOff` status, proceed to log analysis.

2. **Based on logs from Playbook step 2:**
   - If application errors found, check application code and dependencies.
   - If connection errors found, verify network connectivity and service endpoints.
   - If permission errors found, check RBAC configuration.

3. **If no clear cause identified:**
   - Check recent deployments for changes
   - Review resource quotas
   - Escalate to development team with collected evidence
```

**Guidelines:**
- Use events-first approach
- Follow "If X, then Y. If inconclusive, then Z." pattern
- Check permissions early (RBAC/IAM)
- Order by likelihood (most common first)
- Include fallback/escalation path

## Placeholders

Use consistent placeholder format:

| Placeholder | Example |
|-------------|---------|
| `<pod-name>` | my-app-pod-abc123 |
| `<namespace>` | production |
| `<deployment-name>` | my-app |
| `<service-name>` | my-service |
| `<node-name>` | worker-node-1 |
| `<instance-id>` | i-0123456789abcdef |
| `<bucket-name>` | my-s3-bucket |

## Complete Example

```markdown
# CrashLoopBackOff

## Meaning

This alert fires when a Kubernetes pod enters the `CrashLoopBackOff` state, indicating
the container is repeatedly crashing and Kubernetes is backing off restart attempts.

Common causes include:
- Application errors or bugs
- Missing configuration (ConfigMaps, Secrets)
- Resource constraints (OOM)
- Failed health probes
- Missing dependencies

Related Prometheus alerts: `KubePodCrashLooping`, `KubePodNotReady`

## Impact

**Severity:** High

**Business Impact:**
- Service unavailability
- Failed requests and user errors
- Potential SLA breach

**Technical Impact:**
- Pod not serving traffic
- Increased load on other replicas
- Potential cascading failures

## Playbook

1. Retrieve pod `<pod-name>` in namespace `<namespace>` and check pod status, restart count, and recent events.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

</details>

2. Retrieve logs from the crashing container to identify error messages.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
```

</details>

3. Check events in the namespace for scheduling or resource issues.

<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

</details>

4. Verify ConfigMaps and Secrets referenced by the pod exist and are accessible.

5. Check resource requests and limits against node capacity.

6. Verify image exists and is pullable.

7. Check liveness and readiness probe configuration.

8. Review recent deployment changes.

## Diagnosis

1. **Analyze pod events from Playbook step 1:**
   - If `OOMKilled` reason found, container exceeded memory limits. Increase memory limits or optimize application memory usage.
   - If `ImagePullBackOff` found, see ImagePullBackOff playbook.
   - If `CreateContainerConfigError` found, check ConfigMap/Secret references.

2. **Based on container logs from Playbook step 2:**
   - If application stack trace found, identify the exception and fix application code.
   - If "connection refused" or timeout errors, check dependent service availability.
   - If permission/access denied errors, check RBAC and file permissions.

3. **If resource-related:**
   - If CPU throttling suspected, increase CPU limits.
   - If memory growing over time, investigate memory leaks.

4. **If no clear cause identified:**
   - Compare with working replicas of the same deployment.
   - Check if issue correlates with recent code or config changes.
   - Escalate to development team with logs and events collected.
```

---

[Back to Contributing](/contributing)
