#!/usr/bin/env bash
set -euo pipefail

repo_root=${1:-.}
cd "$repo_root"

github_release() {
    gh api "repos/$1/releases/latest" --jq .tag_name | sed 's/^v//'
}

github_tag() {
    gh api "repos/$1/tags?per_page=100" --jq '.[].name' |
        sed 's/^v//' |
        grep -E '^[0-9]+(\.[0-9]+)*$' |
        sort -V |
        tail -n 1
}

update() {
    local package=$1 version=$2 suffix=${3:-}
    local current newest spec current_suffix
    local -a specs

    if ! [[ $version =~ ^[0-9][0-9A-Za-z._+~-]*$ ]]; then
        echo "::error::$package returned an invalid version: $version" >&2
        return 1
    fi

    case $package in
        android-studio) specs=(android-studio/android-studio.spec) ;;
        cava) specs=(cava/cava.spec) ;;
        easyeffects) specs=(easyeffects/easyeffects.spec) ;;
        eden) specs=(eden/eden.spec) ;;
        ghostty) specs=(ghostty/ghostty.spec) ;;
        helium) specs=(helium/helium.spec) ;;
        herdr) specs=(herdr/herdr.spec) ;;
        zed) specs=(zed/zed.spec zed/zed-aarch64.spec) ;;
        zed-lost-saint) specs=(zed-lost-saint/zed-lost-saint.spec) ;;
        zen-browser) specs=(zen-browser/zen-browser.spec zen-browser/zen-browser-aarch64.spec) ;;
        *)
            echo "::error::Unknown package: $package" >&2
            return 1
            ;;
    esac

    current=$(sed -nE '0,/^Version:/s/^Version:[[:space:]]*//p' "${specs[0]}")
    if [[ $current != "$version" ]]; then
        newest=$(printf '%s\n%s\n' "$current" "$version" | sort -V | tail -n 1)
        if [[ $newest != "$version" ]]; then
            echo "::notice::$package is ahead of upstream ($current > $version)"
            return 0
        fi

        for spec in "${specs[@]}"; do
            sed -Ei "0,/^Version:/s/^(Version:[[:space:]]*).*/\\1$version/" "$spec"
            sed -Ei \
                '0,/^Release:[[:space:]]*[0-9]+/s/^Release:.*/Release:        1%{?dist}/' \
                "$spec"
        done
    fi

    if [[ $package == android-studio && -n $suffix ]]; then
        if ! [[ $suffix =~ ^[a-z0-9-]+$ ]]; then
            echo "::error::Invalid Android Studio archive suffix: $suffix" >&2
            return 1
        fi

        current_suffix=$(sed -nE 's/^%define suffixS[[:space:]]+//p' "${specs[0]}")
        if [[ $current_suffix != "$suffix" ]]; then
            sed -Ei "s/^%define suffixS .*/%define suffixS $suffix/" "${specs[0]}"
        fi
    fi

    return 0
}

studio_url() {
    curl --retry 3 -fsSL https://developer.android.com/studio |
        grep -oE 'https://[^" ]+/android/studio/ide-zips/[0-9.]+/android-studio-[a-z0-9-]+-linux\.tar\.gz' |
        sed -n '1p'
}

studio_url=$(studio_url)
studio_version=$(sed -E 's|.*/ide-zips/([^/]+)/.*|\1|' <<< "$studio_url")
studio_suffix=$(sed -E 's|.*/android-studio-(.*)-linux\.tar\.gz|\1|' <<< "$studio_url")

update android-studio "$studio_version" "$studio_suffix"
update cava "$(github_release karlstav/cava)"
update easyeffects "$(github_tag wwmm/easyeffects)"
update eden "$(curl --retry 3 -fsSL \
    https://git.eden-emu.dev/api/v1/repos/eden-emu/eden/releases/latest |
    jq -r .tag_name | sed 's/^v//')"
update ghostty "$(github_tag ghostty-org/ghostty)"
update helium "$(github_release imputnet/helium-linux)"
update herdr "$(github_release herdrdev/herdr)"
update zed "$(github_release zed-industries/zed)"
update zed-lost-saint "$(github_release Lost-Saint/zed)"
update zen-browser "$(github_release zen-browser/desktop)"
