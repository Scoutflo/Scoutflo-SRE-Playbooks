# CodeBuild Failing Due to Dependency Errors

## Meaning

CodeBuild builds fail due to dependency errors (triggering build failures or CodeBuildDependencyError alarms) because build dependencies are missing or incompatible, package manager configuration is incorrect, dependency versions conflict, build environment lacks required tools, dependency installation scripts fail, or build environment image changes remove dependencies. CodeBuild builds fail, build processes cannot complete, and CI/CD pipelines are blocked. This affects the CI/CD layer and blocks deployments, typically caused by dependency configuration issues, build environment problems, or version conflicts; if using CodeBuild with container images, dependency behavior may differ and applications may experience build failures.

## Impact

CodeBuild builds fail; build processes cannot complete; CI/CD pipelines are blocked; application deployments fail; dependency installation errors occur; build logs show dependency-related failures; build automation is interrupted; development workflows are impacted. CodeBuildDependencyError alarms may fire; if using CodeBuild with container images, dependency behavior may differ; applications may experience errors or performance degradation due to failed builds; deployment pipelines may be completely blocked.

## Playbook

1. Verify CodeBuild project `<build-project-name>` exists and AWS service health for CodeBuild in region `<region>` is normal.
2. Retrieve CodeBuild build history for build project `<build-project-name>` and inspect recent build failures, build logs, and error messages related to dependency issues, analyzing failure patterns.
3. Query CloudWatch Logs for log group `/aws/codebuild/<build-project-name>` and filter for dependency error patterns, package manager failures, or installation errors, including error message details.
4. Retrieve the CodeBuild Project `<build-project-name>` in region `<region>` and inspect its build environment configuration, buildspec file, and environment variables, verifying buildspec syntax.
5. Retrieve CloudWatch metrics for CodeBuild project `<build-project-name>` including FailedBuilds over the last 24 hours to identify build failure patterns, analyzing failure frequency.
6. Retrieve the CodeBuild Project `<build-project-name>` build environment image configuration and verify build image version, checking if image changes removed dependencies.
7. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CodeBuild project or buildspec modification events related to project `<build-project-name>` within the last 24 hours, checking for configuration changes.
8. List CodeBuild build artifacts for project `<build-project-name>` and check for missing dependencies or build output issues, analyzing artifact contents.
9. Retrieve the CodeBuild Project `<build-project-name>` VPC configuration if using VPC and verify network connectivity for dependency downloads, checking if network issues affect dependency installation.

## Diagnosis

1. Analyze CodeBuild build history (from Playbook step 2) to identify when dependency failures first appeared. The timestamp of the first failed build establishes the correlation baseline.

2. If build logs (from Playbook step 3) show dependency download failures or package manager errors, and CloudTrail (from Playbook step 7) shows no project changes, external dependency repositories may be unavailable or blocking access.

3. If CloudTrail shows buildspec modifications around the failure timestamp, compare buildspec versions. New dependency specifications or version constraints may conflict with available packages.

4. If build environment image (from Playbook step 6) was updated around the failure time, the new image may lack required tools or have incompatible package versions. Reverting to a previous image version can confirm this.

5. If build failures are project-specific (from Playbook step 2 comparing projects), the issue is buildspec or source code. If multiple projects using the same image fail, the build image is the root cause.

6. If VPC configuration (from Playbook step 9) is used and failures show network timeouts, verify NAT gateway or internet gateway connectivity for dependency downloads from external repositories.

7. If source code commits (from CloudWatch Logs analysis in Playbook step 3) introduced package.json, requirements.txt, or similar dependency file changes around the failure time, new dependencies or version constraints are the cause.

8. If CodeBuild artifacts (from Playbook step 8) show missing files that should contain cached dependencies, caching configuration may need adjustment.

If no correlation is found: extend analysis to 48 hours, review package manager lock files for version pinning, check external package repository availability, verify private artifact repository access, and examine build environment network connectivity.
