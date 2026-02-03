# ImportError-ModuleNotFound-Error-application

## Meaning

Module import error occurs (triggering Sentry error issue with exception type ImportError) because Python module is not found, causing application operations to fail when attempting to import unavailable modules. Error events display in Sentry Issue Details page with error message patterns "module not found", "import error", "no module named", stack traces show import statements, and error levels indicate Error or Fatal severity. This affects the application layer and indicates module dependency issues typically caused by missing dependencies, incorrect module paths, or package installation failures; application operations fail; if errors correlate with deployment issues, dependency management problems may be visible in deployment logs.

## Impact

Sentry error issue alerts fire; module import errors occur; application operations fail; applications fail to start or execute; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate import failures; error events display in Sentry Issue Details page. Application startup fails; affected user count grows; error count increases continuously; issues show Medium or High priority in Sentry dashboard; application functionality degrades completely; import failures occur. Import errors increase; dependency problems occur; if errors correlate with deployment issues, dependency management problems may cause deployment failures.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ImportError with "module not found", "import error", or "no module named" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected import statements and missing module name
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract module name from error message (`metadata.value`) matching pattern "no module named [module_name]" to identify missing Python module and whether it's a first-party or third-party dependency.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze the stack trace frames from the most recent event (`entries[].data.values[].stacktrace.frames[]`) and error message (`metadata.value`) matching pattern "no module named [module_name]" to identify the missing module and import context. If the missing module is a third-party package, the issue is likely a missing or incompatible dependency. If the missing module is a first-party module, the issue is likely a refactoring error, incorrect module path, or missing package structure file.

2. Compare the event's `firstSeen` timestamp with `firstRelease` deployment time from issue details. If the ImportError first appeared within 30 minutes after a release deployment, the root cause is likely a deployment configuration issue such as missing requirements.txt entry, incomplete Docker image build, or failed package installation during deployment. If the error predates recent releases, investigate environment-specific issues, Python path configuration, or conditional import failures.

3. Examine event frequency patterns and affected deployment environments from event data. If errors occur consistently across all instances since a specific timestamp, a deployment or dependency configuration change is the likely cause. If errors are intermittent or affect only specific server instances, the issue correlates with partial deployments, environment-specific package installation failures, or inconsistent container builds across replicas.