#!/usr/bin/env bash
# Generate a deterministic, submodule-complete source archive and rendered spec.
# Usage: ./make-source.sh [output-directory]
# Optional overrides: MOONLIGHT_REPO=... MOONLIGHT_REF=...
set -euo pipefail

name="moonlight-nightly"
repo="${MOONLIGHT_REPO:-https://github.com/moonlight-stream/moonlight-qt.git}"
ref="${MOONLIGHT_REF:-master}"
outdir="${1:-$PWD}"

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
template="${script_dir}/moonlight-nightly.spec.in"

[[ -f "${template}" ]] || {
    echo "Missing template: ${template}" >&2
    exit 1
}

mkdir -p "${outdir}"
outdir="$(cd -- "${outdir}" && pwd)"

workdir="$(mktemp -d)"
trap 'rm -rf "${workdir}"' EXIT

src="${workdir}/src"

git clone --depth 1 --recurse-submodules --shallow-submodules \
    --branch "${ref}" "${repo}" "${src}"

git -C "${src}" submodule update --init --recursive

version="$(tr -d '\r\n' < "${src}/app/version.txt")"
version="${version#v}"

commit="$(git -C "${src}" rev-parse HEAD)"
shortcommit="${commit:0:7}"
epoch="$(git -C "${src}" show -s --format=%ct HEAD)"
git_date="$(LC_ALL=C TZ=UTC date -d "@${epoch}" +%Y%m%dT%H%M%SZ)"
changelog_date="$(LC_ALL=C TZ=UTC date -d "@${epoch}" '+%a %b %d %Y')"

# Match the Lutris GitHub-snapshot convention: source directory by full commit.
topdir="${name}-${commit}"
archive="${topdir}.tar.gz"

mkdir -p "${workdir}/${topdir}"

# Include checked-out submodules, but exclude Git metadata.
tar --exclude-vcs -C "${src}" -cf - . |
    tar -C "${workdir}/${topdir}" -xf -

# Deterministic tarball metadata; gzip -n omits timestamp and filename metadata.
tar --sort=name \
    --mtime="@${epoch}" \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    -C "${workdir}" \
    -cf - "${topdir}" |
    gzip -n > "${outdir}/${archive}"

sed \
    -e "s/@VERSION@/${version}/g" \
    -e "s/@GIT_DATE@/${git_date}/g" \
    -e "s/@COMMIT@/${commit}/g" \
    -e "s/@SHORTCOMMIT@/${shortcommit}/g" \
    -e "s/@CHANGELOG_DATE@/${changelog_date}/g" \
    "${template}" > "${outdir}/${name}.spec"

printf 'Wrote:\n  %s\n  %s\n' \
    "${outdir}/${archive}" \
    "${outdir}/${name}.spec"
