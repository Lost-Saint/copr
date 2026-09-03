#!/bin/sh
set -eu

grep -q '^BuildRequires:  ffmpeg-free-devel$' eden/eden.spec
grep -q '^Release:        3%{?dist}$' eden/eden.spec
! grep -q 'FEDORA_VERSION" = "45' .github/workflows/trigger-copr-builds.yaml
