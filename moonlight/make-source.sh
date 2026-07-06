#!/usr/bin/env bash
# Generate a reproducible, submodule-complete source archive and final spec.
# Usage: ./make-source.sh [output-directory]
# Optional overrides: MOONLIGHT_REPO=... MOONLIGHT_REF=...
set -euo pipefail

repo="${MOONLIGHT_REPO:-https://github.com/moonlight-stream/moonlight-qt.git}"
ref="${MOONLIGHT_REF:-master}"
outdir="${1:-$PWD}"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
template="${script_dir}/moonlight-nightly.spec.in"

[[ -f "${template}" ]] || { echo "Missing template: ${template}" >&2; exit 1; }
mkdir -p "${outdir}"
outdir="$(cd -- "${outdir}" && pwd)"

workdir="$(mktemp -d)"
trap 'rm -rf "${workdir}"' EXIT
src="${workdir}/src"

git clone --depth 1 --recurse-submodules --shallow-submodules \
    --branch "${ref}" "${repo}" "${src}"

version="$(tr -d '\r\n' < "${src}/app/version.txt")"
commit="$(git -C "${src}" rev-parse HEAD)"
shortcommit="${commit:0:12}"
gitdate="$(git -C "${src}" show -s --format=%cd --date=format:%Y%m%d HEAD)"
epoch="$(git -C "${src}" show -s --format=%ct HEAD)"
topdir="moonlight-nightly-${version}-${gitdate}git${shortcommit}"
archive="${topdir}.tar.xz"

mkdir -p "${workdir}/${topdir}"
# A working tree copy includes submodule contents while excluding every .git dir.
tar --exclude-vcs -C "${src}" -cf - . | tar -C "${workdir}/${topdir}" -xf -

# Normalize archive metadata so the same commit produces the same source file.
tar --sort=name --mtime="@${epoch}" --owner=0 --group=0 --numeric-owner \
    -C "${workdir}" -cJf "${outdir}/${archive}" "${topdir}"

sed \
    -e "s/@VERSION@/${version}/g" \
    -e "s/@GITDATE@/${gitdate}/g" \
    -e "s/@COMMIT@/${commit}/g" \
    "${template}" > "${outdir}/moonlight-nightly.spec"

printf 'Wrote:\n  %s\n  %s\n' \
    "${outdir}/${archive}" \
    "${outdir}/moonlight-nightly.spec"
