#!/bin/sh
set -eu

only_spec_path() {
    paths=$(sed -n '1,/workflow_dispatch:/p' "$1" | sed -n '/paths:/,/^[^ ]/p')
    test "$(printf '%s\n' "$paths" | grep -c '^      - ')" -eq 1
    printf '%s\n' "$paths" | grep -q '^      - "\*\*/\*\.spec"$'
}

only_spec_path .github/workflows/pr_build-changed-spec-files.yaml

trigger_paths=$(sed -n '1,/workflow_dispatch:/p' \
    .github/workflows/trigger-copr-builds.yaml | sed -n '/paths:/,/^[^ ]/p')
test "$(printf '%s\n' "$trigger_paths" | grep -c '^      - ')" -eq 2
printf '%s\n' "$trigger_paths" | grep -q '^      - "\*\*/\*\.spec"$'
printf '%s\n' "$trigger_paths" |
    grep -q '^      - "\.github/workflows/trigger-copr-builds\.yaml"$'

grep -q 'cron: "43 7 \* \* \*"' .github/workflows/update-package-version.yaml
! grep -q 'workflow_dispatch' .github/workflows/update-package-version.yaml
grep -q '^          scripts/update-package-versions.sh$' .github/workflows/update-package-version.yaml
grep -Fq "git diff --name-only --diff-filter=ACM -- '*.spec'" .github/workflows/update-package-version.yaml
grep -Fq 'spec_file="$spec"' .github/workflows/update-package-version.yaml
