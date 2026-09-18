#!/bin/sh
set -eu

helium_sources=$(rpmspec -P --target aarch64 helium/helium.spec | grep '^Source')
printf '%s\n' "$helium_sources" | grep -q 'Source0:.*x86_64_linux.tar.xz'
printf '%s\n' "$helium_sources" | grep -q 'Source1:.*arm64_linux.tar.xz'
printf '%s\n' "$helium_sources" | grep -q 'Source2:.*net.imput.helium.metainfo.xml'

test "$(jq -r '.spec_overrides["easyeffects/easyeffects.spec"] | join(" ")' \
    .github/spec-build-targets.json)" = "44 45"

# Ghostty must use Fedora's font stack consistently and stage its install
# outside %%{buildroot}; otherwise GTK can resolve symbols into bundled copies
# and a conventional %%install phase would erase the payload.
grep -q '^%global debug_package %{nil}$' ghostty/ghostty.spec
grep -q '^%install$' ghostty/ghostty.spec
grep -q -- '-fsys=fontconfig' ghostty/ghostty.spec
grep -q -- '-fsys=freetype' ghostty/ghostty.spec
grep -q -- '-fsys=harfbuzz' ghostty/ghostty.spec
grep -Fq '%{_libdir}/libghostty-vt.so.0' ghostty/ghostty.spec
