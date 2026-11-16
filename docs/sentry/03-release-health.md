# Sentry Release Health Playbooks

> Playbooks for release correlation and deployment health monitoring.

## Overview

Release Health playbooks help you correlate errors and performance issues with specific releases, enabling faster identification of regressions introduced by deployments.

## Playbooks

| Playbook | Description |
|----------|-------------|
| [Crash-free rate drop after a release](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/03-Release-Health/CrashFreeRateDropAfterRelease-Release-Health-application.md) | Real regression or measurement artifact? Compare releases, find new issues, decide continue/pause/roll back |
| [Release or deploy missing in Sentry](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/03-Release-Health/ReleaseOrDeployMissing-Release-Health-application.md) | Releases, deploys or commits not showing: naming mismatch, CI steps, token scope |

### Still to come

| Topic | Description |
|-------|-------------|
| Release Adoption Tracking | Monitor rollout progress |
| Release Comparison | Compare error rates across releases |
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
