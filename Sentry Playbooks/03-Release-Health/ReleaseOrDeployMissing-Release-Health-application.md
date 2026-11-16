# Release or Deploy Missing in Sentry

## Meaning

A new version does not appear under Releases in Sentry, deploy markers are missing, or errors are not associated with a release (events show "no release" or an unexpected release name). The release string in the SDK does not match what CI created, the CI release step failed or never ran, the `environment` differs, the release was created in a different project or organization, or commits were never associated.

## Impact

Release Health, "new in release" and regression detection do not work, suspect-commit and resolve-in-next-release features break, and teams cannot correlate errors with deploys during an incident.

## Playbook

### For AI Agents (NLP)

1. Retrieve a recent event from `<project-slug>` that should belong to the new deploy and note its `release` and `environment` tags (or their absence).
2. List releases in organization `<organization-slug>` for the project and check whether `<release-version>` exists, and compare the exact strings character for character with the one the SDK sends.
3. Retrieve the release details to see its deploys and whether commits are associated.
4. Check the CI/CD logs for the release steps (create, set commits, finalize, deploy) for the build that shipped `<release-version>` and identify any failed or skipped step and its error.
5. Check the SDK configuration in the shipped build for the `release` and `environment` values and how they are injected (environment variable, build define, git SHA).
6. Verify the auth token used by CI has access to the right organization and project and the required release scopes.
7. Recommend the minimal fix (align release naming, add or repair the CI steps, correct the token or project) and apply it only after approval, then verify with a new event.

### For DevOps/SREs (CLI)

1. Check which release and environment recent events carry:
   ```bash
   sentry_url='https://sentry.io'
   curl -sS --fail-with-body "$sentry_url/api/0/projects/<organization-slug>/<project-slug>/events/<event-id>/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?load a read token}" \
     | jq '{eventID, dateCreated, tags: [.tags[] | select(.key=="release" or .key=="environment")]}'
   ```

2. List releases and look for the expected version:
   ```bash
   sentry-cli releases list --org <organization-slug> --project <project-slug> | head -20
   ```

3. Inspect the release, its deploys and commits:
   ```bash
   curl -sS --fail-with-body "$sentry_url/api/0/organizations/<organization-slug>/releases/<release-version>/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?}" | jq '{version, dateCreated, commitCount, deployCount, lastDeploy}'
   sentry-cli releases deploys <release-version> list --org <organization-slug>
   ```

4. Verify the CLI is authenticated to the intended organization:
   ```bash
   sentry-cli info
   ```

5. Repair the CI release steps (change, needs approval; run in the CI job with the CI token):
   ```bash
   export SENTRY_ORG=<organization-slug> SENTRY_PROJECT=<project-slug>
   sentry-cli releases new "<release-version>"
   sentry-cli releases set-commits "<release-version>" --auto
   sentry-cli releases finalize "<release-version>"
   sentry-cli releases deploys "<release-version>" new -e <environment>
   ```

## Diagnosis

1. If recent events have a release that differs from `<release-version>` only by format (prefix, git SHA length, `app@1.2.3` versus `1.2.3`), make the SDK and CI use one shared value from the same build step.
2. If events have no release at all, the SDK is not configured with `release`: set it at init (from the build) and redeploy.
3. If the release exists but has no deploys, add the `releases deploys ... new -e <environment>` step; if it has no commits, add `set-commits` and check the repository integration is connected.
4. If the release does not exist and the CI log shows an authentication or 403 error, fix the token's organization, project and scopes.
5. If the release exists in another project or organization, the CI `SENTRY_ORG`/`SENTRY_PROJECT` values are wrong.
6. If steps ran in the wrong order (finalize before the build was deployed, or deploy recorded before the release was created), reorder them in CI.

Inline references:
- [Sentry releases and CLI](https://docs.sentry.io/product/cli/releases/)
- [Associate commits](https://docs.sentry.io/product/releases/setup/release-automation/)
