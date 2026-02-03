# Release Health Playbooks

This directory contains playbooks for diagnosing and resolving issues related to release correlation and deployment problems in Sentry.

## Purpose

Release Health playbooks help SRE teams:
- Correlate errors with specific releases or deployments
- Diagnose deployment-related failures
- Track version-specific issues
- Analyze release rollout problems

## Planned Playbooks

The following types of playbooks are planned for this category:

1. **Release Regression Detection**
   - Identifying error spikes correlated with new releases
   - Comparing error rates between versions

2. **Deployment Failure Analysis**
   - Build/deployment pipeline errors captured in Sentry
   - Container/pod startup failures post-deployment

3. **Version Mismatch Issues**
   - Errors caused by version incompatibilities
   - API contract violations between service versions

4. **Rollback Decision Playbooks**
   - Criteria for triggering rollbacks based on Sentry data
   - Error threshold monitoring post-deployment

## Adding Playbooks

When adding release-related playbooks to this directory:
1. Focus on issues where the root cause is tied to releases, versions, or deployments
2. Include steps to correlate Sentry data with release timelines
3. Reference `firstRelease` and `lastRelease` fields in Sentry issue details
4. Include rollback and mitigation procedures where applicable

## Related Categories

Some errors may span multiple categories:
- Errors that appear after deployment may start here but resolve in `01-Error-Tracking/`
- Performance degradation after releases may involve `02-Performance/` playbooks
