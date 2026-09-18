#!/bin/sh
set -eu

test_dir=$(mktemp -d)
trap 'rm -rf "$test_dir"' EXIT

mkdir -p \
    "$test_dir/bin" \
    "$test_dir/repo/android-studio" \
    "$test_dir/repo/cava" \
    "$test_dir/repo/easyeffects" \
    "$test_dir/repo/eden" \
    "$test_dir/repo/ghostty" \
    "$test_dir/repo/helium" \
    "$test_dir/repo/herdr" \
    "$test_dir/repo/zed" \
    "$test_dir/repo/zed-lost-saint" \
    "$test_dir/repo/zen-browser"

cat > "$test_dir/bin/gh" <<'EOF'
#!/bin/sh
case "$2" in
    repos/karlstav/cava/releases/latest) echo v1.0.0 ;;
    'repos/wwmm/easyeffects/tags?per_page=100') printf '%s\n' v8.2.8 v8.2.9 ;;
    'repos/ghostty-org/ghostty/tags?per_page=100') printf '%s\n' v1.3.0 v1.3.1 ;;
    repos/imputnet/helium-linux/releases/latest) echo 0.17.0.1 ;;
    repos/herdrdev/herdr/releases/latest) echo v0.9.0 ;;
    repos/zed-industries/zed/releases/latest) echo v1.19.2 ;;
    repos/Lost-Saint/zed/releases/latest) echo v1.18.0 ;;
    repos/zen-browser/desktop/releases/latest) echo 1.22.1b ;;
    *) echo "unexpected gh request: $*" >&2; exit 1 ;;
esac
EOF

cat > "$test_dir/bin/curl" <<'EOF'
#!/bin/sh
case "$*" in
    *developer.android.com/studio*)
        echo 'https://example.test/android/studio/ide-zips/2026.1.4.7/android-studio-quail4-linux.tar.gz'
        ;;
    *git.eden-emu.dev*) echo '{"tag_name":"v0.2.1"}' ;;
    *) echo "unexpected curl request: $*" >&2; exit 1 ;;
esac
EOF

chmod +x "$test_dir/bin/gh" "$test_dir/bin/curl"

make_spec() {
    path=$1 version=$2 release=${3:-7}
    printf 'Name: test\nVersion:        %s\nRelease:        %s%%{?dist}\n' \
        "$version" "$release" > "$test_dir/repo/$path"
}

# Android Studio is deliberately current. This is the state that previously
# returned status 1 and stopped every subsequent package from being checked.
cat > "$test_dir/repo/android-studio/android-studio.spec" <<'EOF'
%define suffixS quail4
Name: android-studio
Version:        2026.1.4.7
Release:        7%{?dist}
EOF

make_spec cava/cava.spec 0.1.0
make_spec easyeffects/easyeffects.spec 8.0.0
make_spec eden/eden.spec 0.1.0
make_spec ghostty/ghostty.spec 1.0.0
make_spec helium/helium.spec 0.1.0
make_spec herdr/herdr.spec 0.1.0
make_spec zed/zed.spec 1.0.0
make_spec zed/zed-aarch64.spec 1.0.0
make_spec zed-lost-saint/zed-lost-saint.spec 1.18.0
make_spec zen-browser/zen-browser.spec 1.0.0
make_spec zen-browser/zen-browser-aarch64.spec 1.0.0

PATH="$test_dir/bin:$PATH" scripts/update-package-versions.sh "$test_dir/repo"

check_version() {
    grep -q "^Version:[[:space:]]*$2$" "$test_dir/repo/$1"
}

check_version android-studio/android-studio.spec 2026.1.4.7
check_version cava/cava.spec 1.0.0
check_version easyeffects/easyeffects.spec 8.2.9
check_version eden/eden.spec 0.2.1
check_version ghostty/ghostty.spec 1.3.1
check_version helium/helium.spec 0.17.0.1
check_version herdr/herdr.spec 0.9.0
check_version zed/zed.spec 1.19.2
check_version zed/zed-aarch64.spec 1.19.2
check_version zed-lost-saint/zed-lost-saint.spec 1.18.0
check_version zen-browser/zen-browser.spec 1.22.1b
check_version zen-browser/zen-browser-aarch64.spec 1.22.1b

# Numeric releases reset for changed versions; current packages stay untouched.
grep -q '^Release:[[:space:]]*1%{?dist}$' "$test_dir/repo/helium/helium.spec"
grep -q '^Release:[[:space:]]*7%{?dist}$' "$test_dir/repo/android-studio/android-studio.spec"

# Suffix-only updates still work, and a local version ahead of upstream is not
# downgraded or treated as a failed update.
sed -Ei 's/^%define suffixS .*/%define suffixS stale/' \
    "$test_dir/repo/android-studio/android-studio.spec"
sed -Ei 's/^Version:.*/Version:        9.0.0/' "$test_dir/repo/cava/cava.spec"
PATH="$test_dir/bin:$PATH" scripts/update-package-versions.sh "$test_dir/repo"
grep -q '^%define suffixS quail4$' "$test_dir/repo/android-studio/android-studio.spec"
check_version cava/cava.spec 9.0.0
