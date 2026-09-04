#!/bin/sh
set -eu

commit=$1
git_date=$2
tag=$3
spec=${4:-lutris-git/lutris.spec}

printf '%s\n' "$commit" | grep -Eq '^[0-9a-f]{40}$'
printf '%s\n' "$git_date" | grep -Eq '^[0-9]{8}T[0-9]{6}Z$'
printf '%s\n' "$tag" | grep -Eq '^v[0-9][0-9A-Za-z._-]*$'
test -f "$spec"

sed -Ei "s/^%global commit .*/%global commit $commit/" "$spec"
sed -Ei "s/^%global git_date .*/%global git_date $git_date/" "$spec"
sed -Ei "s/^%global tag .*/%global tag $tag/" "$spec"
