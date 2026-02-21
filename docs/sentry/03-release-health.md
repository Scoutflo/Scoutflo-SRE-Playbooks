# Sentry Release Health Playbooks

> Playbooks for release correlation and deployment health monitoring.

## Overview

Release Health playbooks help you correlate errors and performance issues with specific releases, enabling faster identification of regressions introduced by deployments.

## Coming Soon

This category is a placeholder for upcoming playbooks that will cover:

| Topic | Description |
|-------|-------------|
| Release Regression Detection | Identify error spikes after deployments |
| Crash-Free Session Monitoring | Track crash-free user sessions |
| Release Adoption Tracking | Monitor rollout progress |
| Release Comparison | Compare error rates across releases |
| Deploy Correlation | Link errors to specific commits |
| Rollback Decision Support | Data-driven rollback analysis |

## Best Practices

### Release Tagging

Ensure your Sentry SDK is configured to send release information:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-dsn",
    release="my-app@1.2.3",
    environment="production"
)
```

### Commit Integration

Link commits to releases for better error context:

```bash
sentry-cli releases new my-app@1.2.3
sentry-cli releases set-commits my-app@1.2.3 --auto
sentry-cli releases finalize my-app@1.2.3
```

### Session Health

Enable session tracking to monitor crash-free rates:

```python
sentry_sdk.init(
    dsn="your-dsn",
    release="my-app@1.2.3",
    auto_session_tracking=True
)
```

---

[Back to Sentry Overview](/sentry/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/Sentry%20Playbooks/03-Release-Health)
