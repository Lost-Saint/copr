#!/bin/sh
set -eu

helium_sources=$(rpmspec -P --target aarch64 helium/helium.spec | grep '^Source')
printf '%s\n' "$helium_sources" | grep -q 'Source0:.*x86_64_linux.tar.xz'
printf '%s\n' "$helium_sources" | grep -q 'Source1:.*arm64_linux.tar.xz'
printf '%s\n' "$helium_sources" | grep -q 'Source2:.*net.imput.helium.metainfo.xml'

test "$(jq -r '.spec_overrides["easyeffects/easyeffects.spec"] | join(" ")' \
    .github/spec-build-targets.json)" = "44 45"
