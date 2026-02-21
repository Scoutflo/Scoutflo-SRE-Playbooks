# Sentry Playbooks

> **25 playbooks** for application error tracking and performance monitoring with Sentry.

## Categories

| Category | Playbooks | Description |
|----------|-----------|-------------|
| [01 - Error Tracking](/sentry/01-error-tracking) | 19 | Exception handling, error patterns |
| [02 - Performance](/sentry/02-performance) | 6 | Timeout, latency, slow transactions |
| [03 - Release Health](/sentry/03-release-health) | - | Release correlation (coming soon) |

## Quick Navigation

### Most Common Issues

| Issue | Playbook |
|-------|----------|
| Unhandled exception | [UnhandledException](/sentry/01-error-tracking?id=unhandledexception) |
| Null pointer error | [NullPointerException](/sentry/01-error-tracking?id=nullpointerexception) |
| Timeout errors | [TimeoutError](/sentry/02-performance?id=timeouterror) |
| High latency | [HighLatency](/sentry/02-performance?id=highlatency) |
| Memory issues | [OutOfMemoryError](/sentry/01-error-tracking?id=outofmemoryerror) |

### By Error Type

**Runtime Errors:**
- NullPointerException
- IndexOutOfBoundsException
- TypeError
- ValueError

**Network Errors:**
- ConnectionError
- TimeoutError
- HTTPError

**Resource Errors:**
- OutOfMemoryError
- StackOverflowError
- DiskFullError

**Performance Issues:**
- Slow transactions
- High latency
- Database query timeouts

## Understanding Sentry Playbook Steps

Sentry playbooks follow the same 4-section structure:

1. **Meaning**: What the error means and common causes
2. **Impact**: User experience and business impact
3. **Playbook**: Investigation steps
4. **Diagnosis**: Root cause analysis with conditional logic

### Example Step

> "Retrieve error details from Sentry and analyze stack trace for root cause"

<details>
<summary>CLI Equivalent (Sentry CLI)</summary>

```bash
# View recent events
sentry-cli events list --project <project>

# Get event details
sentry-cli events get <event-id>

# Check release info
sentry-cli releases info <version>
```

</details>

## All Categories

<details>
<summary><strong>01 - Error Tracking (19 playbooks)</strong></summary>

Exception handling and error pattern playbooks.

See [01 - Error Tracking](/sentry/01-error-tracking) for the full list.

</details>

<details>
<summary><strong>02 - Performance (6 playbooks)</strong></summary>

Timeout, latency, and performance playbooks.

See [02 - Performance](/sentry/02-performance) for the full list.

</details>

<details>
<summary><strong>03 - Release Health (coming soon)</strong></summary>

Release correlation and deployment impact playbooks.

</details>

## Integration with Other Playbooks

Sentry errors often correlate with infrastructure issues:

| Sentry Error | Related K8s Playbook | Related AWS Playbook |
|--------------|---------------------|---------------------|
| OutOfMemoryError | [KubeContainerOOMKilled](/k8s/03-pods) | [EC2 Memory Issues](/aws/01-compute) |
| ConnectionError | [Service Not Accessible](/k8s/05-networking) | [RDS Connection Issues](/aws/02-database) |
| TimeoutError | [High Latency](/k8s/05-networking) | [Lambda Timeout](/aws/01-compute) |
| DatabaseError | [PVC Issues](/k8s/06-storage) | [RDS Issues](/aws/02-database) |

## Best Practices

1. **Set up alerts** for new error types
2. **Configure release tracking** to correlate errors with deployments
3. **Use breadcrumbs** to understand error context
4. **Monitor error rates** not just error counts
5. **Link commits** to identify which changes caused issues
