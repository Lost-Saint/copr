# %%commit is resolved to the current tip of master when the spec is
# parsed (i.e. every SRPM build), so there's no hash to hand-edit before
# each build. This does mean builds are NOT reproducible -- two builds
# on different days can pick up different upstream commits. It also
# needs network access at SRPM-generation time, same as %%build (see the
# COPR networking note below). If you want a fixed, reproducible
# snapshot instead, replace this with a literal 40-character commit
# hash, e.g.:
#   %%global commit c1b0e180ba64d2ea7e815e2c2e93087ae9a26500
%global commit         %(git ls-remote https://github.com/LadybirdBrowser/ladybird.git HEAD | cut -f1)
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
%global snapshot_date  %(date +%Y%m%d)

Name:           ladybird
Version:        0^%{snapshot_date}git%{shortcommit}
Release:        %autorelease
Summary:        Truly independent web browser and engine

License:        BSD-2-Clause
URL:            https://ladybird.org
Source0:        https://github.com/LadybirdBrowser/ladybird/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

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
