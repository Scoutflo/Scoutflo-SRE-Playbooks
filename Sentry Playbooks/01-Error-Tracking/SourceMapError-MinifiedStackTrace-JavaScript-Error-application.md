# Minified JavaScript Stack Traces

## Meaning

Sentry captured a browser JavaScript exception but displays generated bundle names and line or column numbers. The captured frame could not be matched to source artifacts from the deployed build. Recent Sentry SDKs and build tools use Debug IDs to match a JavaScript file to its source map. Older setups use release artifacts, where the event's release, distribution and frame URL determine which uploaded file is used. Either setup can fail when the upload is missing, uses a different build, targets another project, or finishes after the event is captured.

## Impact

Teams can still see and count exceptions, but minified frames make it harder to locate the affected file and code. This can slow triage during a rollout and make separate failures harder to distinguish. Confirm the impact on a specific event before changing the deployment pipeline, especially when only a single CDN path, environment or release is affected.

## Playbook

### For AI Agents (NLP)

1. Retrieve an affected event `<event-id>` in `<project-slug>` and note its timestamp, release and distribution. Pick an event with a browser JavaScript frame that still appears minified.
2. Retrieve the event's source-map diagnostic report. Check whether the event includes Debug IDs and whether Sentry found the source file and source map for the affected frame.
3. Compare the affected frame's Debug ID with the deployed JavaScript and its matching source map from the same production build. Check the exact chunk and use the retained build output. A missing ID in the event also warrants checking the SDK version and whether the affected bundle included the injection snippet.
4. Confirm the build produced a readable map containing source files and mappings. Verify that the map contains `sourcesContent` if source context is expected.
5. For legacy uploads, or uploads explicitly scoped to a release or distribution, compare the event values with the values used by the upload job. Confirm that the job uploaded to `<project-slug>` in `<organization-slug>`.
6. For legacy uploads, compare the frame's absolute URL and source-map reference with the matching uploaded artifact names. The URL prefix must include the deployed path (for example, `~/static/js`).
7. Compare the successful upload timestamp from CI with the affected event timestamp and the deploy or CDN publish time. A later upload will only affect subsequent events.
8. **Change, needs approval.** Once the service owner approves a correction, fix the build or upload settings in CI. When using the Debug ID CLI workflow, inject before uploading, and deploy the JavaScript from that same build only after the upload succeeds. For legacy uploads, correct the release, distribution or URL prefix using the same build artifacts.
9. Verify a new event from the corrected build after the upload and deploy. If generating a test exception is necessary, use an approved staging environment. Confirm the affected frame now points to the original source in Sentry.

### For DevOps/SREs (CLI)

Run these blocks in the same Bash shell with `curl` 7.76 or newer and `jq`. Replace the angle-bracket values, use the HTTPS base URL of your trusted Sentry instance, and load `SENTRY_AUTH_TOKEN` from your secret store. Use a read token with `project:read` for the GET requests. Stop on a failed request and check the token, project and event ID before continuing. The upload commands in step 8 need separate upload permissions.

1. Retrieve a representative event and read its timestamp and tags.

   ```bash
   sentry_url='https://sentry.io'
   sentry_project_path='/api/0/projects/<organization-slug>/<project-slug>'
   event_id='<event-id>'
   set -o pipefail
   sentry_get() {
     curl --silent --show-error --fail-with-body --header @- "${sentry_url%/}$1" \
       <<< "Authorization: Bearer ${SENTRY_AUTH_TOKEN:?Load a read token}"
   }
   event=$(sentry_get "$sentry_project_path/events/$event_id/")
   jq '{eventID, dateCreated, tags: [.tags[]? | select(.key == "release" or .key == "dist")]}' <<< "$event"
   ```

2. Request source-map diagnostics for that event.

   ```bash
   diagnostics=$(sentry_get "$sentry_project_path/events/$event_id/source-map-debug/")
   jq '{has_debug_ids, sdk_version, frames: [.exceptions[]?.frames[]? | {debug_id_process, release_process}]}' \
     <<< "$diagnostics"
   ```

3. Compare an affected frame's Debug ID with the corresponding production build artifacts.

   ```bash
   bundle='<retained-build-directory>/<affected-bundle-filename>'
   source_map='<retained-build-directory>/<affected-source-map-filename>'
   grep -oE 'debugId=[[:xdigit:]-]+' "$bundle"
   jq -er '.debug_id // .debugId | strings' "$source_map"
   jq -r '.exceptions[]?.frames[]?.debug_id_process.debug_id // empty' <<< "$diagnostics"
   ```

4. Inspect source-map contents without printing source code.

   ```bash
   jq -e '(.sources | type == "array" and length > 0) and (.mappings | type == "string" and length > 0)' "$source_map"
   jq '{source_count: (.sources | length), embedded_source_count: ([.sourcesContent[]? | strings] | length)}' "$source_map"
   ```

5. When the release or distribution is part of matching, compare the event values with the upload configuration. Use an empty value for an intentionally unset distribution.

   ```bash
   jq --arg release '<upload-release>' --arg dist '<upload-dist-or-empty>' \
     '{release, dist, release_matches: (.release == $release), dist_matches: ((.dist // "") == $dist)}' \
     <<< "$diagnostics"
   ```

6. For a legacy upload, inspect the affected frame URL and the matching artifact names.

   ```bash
   jq '.exceptions[]?.frames[]?.release_process | select(. != null) |
     {abs_path, source_map_reference, matching_source_file_names, matching_source_map_name, source_map_lookup_result}' \
     <<< "$diagnostics"
   ```

7. Compare the event time against the CI job's upload-completion and deployment timestamps in UTC.

   ```bash
   jq --arg uploaded '<upload-completed-at-utc>' --arg deployed '<deployment-at-utc>' \
     '{event_at: .dateCreated, upload_completed_at: $uploaded, deployment_at: $deployed}' <<< "$event"
   ```

8. **Change, needs approval.** If CI uses manual Debug ID injection, run the following in the approved build job with its upload token. Deploy only the output from this build after upload succeeds.

   ```bash
   build_dir='<production-build-directory>'
   SENTRY_ORG='<organization-slug>' SENTRY_PROJECT='<project-slug>' \
     sentry-cli sourcemaps inject "$build_dir" && \
   SENTRY_ORG='<organization-slug>' SENTRY_PROJECT='<project-slug>' \
     sentry-cli sourcemaps upload "$build_dir"
   ```

   For an approved legacy correction, use the configured release and a prefix matching the actual frame URL. Append `--dist '<upload-dist>'` only for a build configured with a distribution.

   ```bash
   SENTRY_ORG='<organization-slug>' SENTRY_PROJECT='<project-slug>' \
     sentry-cli sourcemaps upload --release '<upload-release>' \
       --url-prefix '<artifact-url-prefix>' '<production-build-directory>'
   ```

9. Check a new event from the updated deployment, then confirm its original source frame in the Sentry event view.

   ```bash
   new_event_id='<new-event-id>'
   sentry_get "$sentry_project_path/events/$new_event_id/source-map-debug/" \
     | jq '{has_debug_ids, frames: [.exceptions[]?.frames[]? | {debug_id_process, release_process}]}'
   ```

## Diagnosis

1. If the event has no Debug IDs and the deployed bundle also lacks them, inspect the production build or injection step. If the bundle contains an ID but the event does not, check the SDK version and whether the browser loaded that exact bundle. For a legacy setup, use release matching instead.
2. If Sentry sees a Debug ID but cannot find both matching files, check the destination project, uploaded file list, and CI build identity. A rebuilt or post-processed asset can differ from the one uploaded.
3. If a legacy event has a different release or distribution, set the SDK and upload job to share their value from the same build. If those values match but the absolute frame path has no candidate file, inspect the deployed CDN path, `sourceMappingURL`, and prefix.
4. If the first affected event arrived before the upload completed, verify a newer event. Compare when the bundle was first made available with the upload time and move the upload earlier in CI if needed.
5. If the latest affected event finds both files but mapping is wrong, check the retained map with a local source-map consumer at the recorded line and column. Compare a working chunk from the same deployment. Escalate with event IDs, Debug IDs, build and upload timestamps, and sanitized paths.

### References

- [Sentry source-map troubleshooting](https://docs.sentry.io/platforms/javascript/sourcemaps/troubleshooting_js/)
- [Sentry CLI source-map upload](https://docs.sentry.io/platforms/javascript/sourcemaps/uploading/cli/)
- [Sentry legacy source-map upload](https://docs.sentry.io/platforms/javascript/sourcemaps/troubleshooting_js/legacy-uploading-methods/)
- [Sentry event source-map diagnostics API](https://docs.sentry.io/api/events/get-debug-information-related-to-source-maps-for-a-given-event/)
