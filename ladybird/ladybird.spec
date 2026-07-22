# Fedora spec file for Ladybird, intended for building on COPR.
#
# Ladybird has no tagged upstream releases as of this writing (still
# pre-alpha, git-only), so this packages a git snapshot using Fedora's
# snapshot-versioning scheme. Update %%global commit (and snapshot_date)
# to a real commit each time you cut a new build. See "Assumptions" below
# the spec for important caveats before trying to actually build this.
#
# Release/%%changelog use rpmautospec (%%autorelease/%%autochangelog),
# which reads the packaging repo's own git history -- this only works
# correctly when COPR builds via the SCM method (a git repo containing
# this spec), not a plain spec+tarball/SRPM upload.

%global commit        0000000000000000000000000000000000000000
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
%global snapshot_date  20260721

Name:           ladybird
Version:        0^%{snapshot_date}git%{shortcommit}
Release:        %autorelease
Summary:        Truly independent web browser and engine

License:        BSD-2-Clause
URL:            https://ladybird.org
Source0:        https://github.com/LadybirdBrowser/ladybird/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# Ladybird's CMake build fetches and compiles most of its third-party
# dependencies (Skia, simdjson, simdutf, etc.) via vcpkg during %%build,
# which needs internet access. Mock has no network access during builds
# by default; on COPR you must explicitly enable it for this project:
#   Project Settings -> General -> Networking, or
#   copr-cli create/edit-package ... --enable-net on
# This is a COPR-only accommodation, not something official Fedora
# builds (Koji) allow.

# Ladybird requires a very recent C++23 toolchain (Clang 21 or GCC 14+)
# and CMake 3.30+; adjust/pin these if your COPR chroot doesn't provide
# them by default.
BuildRequires:  cmake >= 3.30
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  nasm
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(Qt6Network)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtwayland-devel

# Runtime library dependencies (Qt6, etc.) are picked up automatically by
# RPM's dependency generator from the linked binaries, so no manual
# Requires: should be needed here.

%description
Ladybird is an independent web browser and engine built from scratch on
web standards, without basing its rendering engine on Blink, Gecko, or
WebKit.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake
%cmake_build

%install
%cmake_install

%check
# Ladybird's test suite (LibWeb layout tests, Test262, etc.) is large,
# needs a display/GPU, and is not well suited to a chroot build
# environment, so it is intentionally not run here. Enable selectively
# with ctest if you need it:
# %%ctest

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/

%changelog
%autochangelog
