%global commit         9b6432a9a0791333828938ee19170595811eeb1d
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
# Bump this alongside %%commit -- it just records when you took the
# snapshot, doesn't need to match the commit date exactly.
%global snapshot_date  20260721

Name:           ladybird
Version:        0^%{snapshot_date}git%{shortcommit}
Release:        %autorelease
Summary:        Truly independent web browser and engine

License:        BSD-2-Clause
URL:            https://ladybird.org
Source0:        https://github.com/LadybirdBrowser/ladybird/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

ExclusiveArch:  x86_64 aarch64

%ifarch aarch64
%global vcpkg_triplet arm64-linux
%else
%global vcpkg_triplet x64-linux
%endif

BuildRequires:  cmake >= 3.30
BuildRequires:  ninja-build
BuildRequires:  make

# Ladybird requires GCC 14+ or Clang 19+.
BuildRequires:  gcc-c++ >= 14

BuildRequires:  python3
BuildRequires:  rust
BuildRequires:  cargo

# vcpkg bootstrap and downloads
BuildRequires:  git-core
BuildRequires:  curl
BuildRequires:  tar
BuildRequires:  unzip
BuildRequires:  zip

# General build tools used by vcpkg ports
BuildRequires:  pkgconf-pkg-config
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  ccache
BuildRequires:  patchelf

# Required by vcpkg/OpenSSL and other ports
BuildRequires:  perl-FindBin
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-lib
BuildRequires:  perl-Time-Piece

# Fedora/Linux platform dependencies
BuildRequires:  libdrm-devel
BuildRequires:  libglvnd-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-ng-compat-static
BuildRequires:  liberation-sans-fonts

# Linux uses the system Qt build
BuildRequires:  qt6-qtbase-devel >= 6.9
BuildRequires:  qt6-qttools-devel >= 6.9
BuildRequires:  qt6-qtwayland-devel >= 6.9

# Optional but recommended; enables the Vulkan DMA-BUF shader path
BuildRequires:  glslang

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
export LADYBIRD_SOURCE_DIR="$PWD"
export VCPKG_ROOT="$PWD/Build/vcpkg"
export VCPKG_MAX_CONCURRENCY="%{_smp_build_ncpus}"

# Clones vcpkg and checks out the baseline pinned by vcpkg.json.
python3 Meta/Utils/build_vcpkg.py

%cmake \
    -DCMAKE_TOOLCHAIN_FILE="$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" \
    -DVCPKG_OVERLAY_TRIPLETS="$PWD/Meta/CMake/vcpkg/distribution-triplets" \
    -DVCPKG_TARGET_TRIPLET=%{vcpkg_triplet} \
    -DVCPKG_HOST_TRIPLET=%{vcpkg_triplet} \
    -DVCPKG_INSTALL_OPTIONS=--no-print-usage \
    -DBUILD_SHARED_LIBS=OFF \
    -DBUILD_TESTING=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DLADYBIRD_GUI_FRAMEWORK=Qt \
    -DENABLE_INSTALL_FREEDESKTOP_FILES=ON \
    -DENABLE_LTO_FOR_RELEASE=OFF

%cmake_build

%install
DESTDIR="%{buildroot}" \
    cmake --install "%{_vpath_builddir}" \
    --component ladybird_Runtime

%check
# Ladybird's test suite (LibWeb layout tests, Test262, etc.) is large,
# needs a display/GPU, and is not well suited to a chroot build
# environment, so it is intentionally not run here. Enable selectively
# with ctest if you need it:
# %%ctest

%files
%license LICENSE
%doc README.md

%{_bindir}/Ladybird

%{_libexecdir}/Compositor
%{_libexecdir}/ImageDecoder
%{_libexecdir}/RequestServer
%{_libexecdir}/WebContent
%{_libexecdir}/WebWorker

%{_datadir}/Lagom/

%{_datadir}/applications/org.ladybird.Ladybird.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.ladybird.Ladybird.svg
%{_datadir}/dbus-1/services/org.ladybird.Ladybird.service
%{_datadir}/metainfo/org.ladybird.Ladybird.metainfo.xml

%changelog
%autochangelog
