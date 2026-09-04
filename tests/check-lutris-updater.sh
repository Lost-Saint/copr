#!/bin/sh
set -eu

test_dir=$(mktemp -d)
trap 'rm -rf "$test_dir"' EXIT
spec="$test_dir/lutris.spec"
sed -n '1,5p' lutris-git/lutris.spec > "$spec"

scripts/update-lutris-git.sh \
    0123456789abcdef0123456789abcdef01234567 \
    20260904T123456Z \
    v0.5.23 \
    "$spec"

grep -q '^%global commit 0123456789abcdef0123456789abcdef01234567$' "$spec"
grep -q '^%global git_date 20260904T123456Z$' "$spec"
grep -q '^%global tag v0.5.23$' "$spec"
