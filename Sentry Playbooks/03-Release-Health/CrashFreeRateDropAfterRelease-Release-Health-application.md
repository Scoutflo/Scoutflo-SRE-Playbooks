# Crash-Free Rate Drop After a Release

## Meaning

The crash-free sessions or crash-free users rate for a release in Sentry Release Health falls sharply after a deploy, or an alert on `crash_free_rate` fires. A new release introduced crashes or unhandled errors, or the measurement itself changed: session tracking was added or removed, a small number of sessions makes the rate noisy, the environment or release tag changed, or an old release's sessions are ending as users upgrade.

## Impact

More users hit crashes or failed sessions, which hurts retention and support load. If the drop is a measurement artifact, a rollback may be triggered unnecessarily; if it is real and ignored, the regression keeps affecting users during rollout.

## Playbook

### For AI Agents (NLP)

1. Identify the release `<release-version>`, environment `<environment>` and project `<project-slug>` in organization `<organization-slug>`, and the time the drop started.
2. Retrieve the crash-free session and user rates for the new release and for the previous release over the same window, plus the session counts, to see whether the sample size is large enough to trust the rate.
3. Retrieve the release details: deploy time, commit count and adoption (share of sessions on the new release), to judge how far the rollout has progressed.
4. List new and regressed issues first seen in the new release and sort by event count and affected users, to find the likely cause of the crashes.
5. Check whether session tracking, SDK version or environment/release naming changed in this deploy, which could change the metric without a real regression.
6. Compare the affected platform, OS or app version dimensions of the new issues to see whether the problem is limited to a segment.
7. Summarise whether the drop is real (with the top suspect issues and commits) or a measurement artifact, and recommend continue, pause rollout, or roll back. Treat the rollback itself as a change needing approval.

### For DevOps/SREs (CLI)

Load `SENTRY_AUTH_TOKEN` (read scopes: `org:read`, `project:read`, `event:read`) from your secret store and set `sentry_url` to your Sentry base URL.

1. Compare crash-free session rate and session counts per release (last 24 hours):
   ```bash
   sentry_url='https://sentry.io'
   curl -sS --fail-with-body -G "$sentry_url/api/0/organizations/<organization-slug>/sessions/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?load a read token}" \
     --data-urlencode "project=<project-id>" --data-urlencode "environment=<environment>" \
     --data-urlencode "statsPeriod=24h" --data-urlencode "interval=1h" \
     --data-urlencode "groupBy=release" \
     --data-urlencode "field=crash_free_rate(session)" --data-urlencode "field=sum(session)" \
     | jq '.groups[] | {release: .by.release, crash_free: .totals["crash_free_rate(session)"], sessions: .totals["sum(session)"]}'
   ```

2. Get the release details (deploys, commits, adoption fields):
   ```bash
   curl -sS --fail-with-body "$sentry_url/api/0/organizations/<organization-slug>/releases/<release-version>/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?}" \
     | jq '{version, dateCreated, commitCount, deployCount, lastDeploy, newGroups}'
   ```

3. List issues first seen in the release:
   ```bash
   curl -sS --fail-with-body -G "$sentry_url/api/0/organizations/<organization-slug>/issues/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?}" \
     --data-urlencode "query=firstRelease:<release-version> is:unresolved" \
     --data-urlencode "sort=freq" --data-urlencode "statsPeriod=24h" \
     | jq '.[:10] | .[] | {shortId, title, count, userCount, permalink}'
   ```

4. Check the release in the CLI view and its deploys:
   ```bash
   sentry-cli releases list --org <organization-slug> --project <project-slug> | head
   sentry-cli releases deploys <release-version> list --org <organization-slug>
   ```

5. If rolling back is decided (change, needs approval), do it through your deployment system, then watch the old release's crash-free rate recover in step 1.

## Diagnosis

1. If the new release's crash-free rate is lower than the previous release's with a comparable, large session count, and new issues with high user counts exist in step 3, the regression is real: pause or roll back the rollout and fix the top issue.
2. If session counts for the new release are small (tens of sessions), the rate is noisy: wait for more sessions before acting.
3. If the drop coincides with an SDK upgrade, a change in `release`/`environment` naming or enabling session tracking, the metric changed, not necessarily the crash behaviour: compare error counts per release to confirm.
4. If crashes concentrate in one platform, OS or app version, the regression is segment-specific: scope the rollback or fix to that segment.
5. If the drop appears on the old release as users upgrade, it is a mix-shift artifact; compare the same release over time instead.
6. If no new issue explains the drop but crashes rose, look for regressed (previously resolved) issues and errors without a release tag.

Inline references:
- [Sentry Release Health](https://docs.sentry.io/product/releases/health/)
- [Sessions API](https://docs.sentry.io/api/releases/retrieve-release-health-session-statistics/)
