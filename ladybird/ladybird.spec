%global commit         9b6432a9a0791333828938ee19170595811eeb1d
%global shortcommit    %(c=%{commit}; echo ${c:0:7})

# Bump this alongside %%commit -- it records when the snapshot was taken
# and does not need to match the commit date exactly.
%global snapshot_date  20260721

# Ladybird is a very large, mostly static C++ build. Fedora's default LTO
# flags cause GCC's lto1 process to exceed the memory available on many
# Copr builders.
%global _lto_cflags %{nil}

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
BuildRequires:  gcc-c++ >= 14
BuildRequires:  make

BuildRequires:  python3
BuildRequires:  git-core
BuildRequires:  cargo

# vcpkg port build tools
BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  patchelf

# OpenSSL's vcpkg port
BuildRequires:  perl-FindBin
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-lib
BuildRequires:  perl-Time-Piece

# Linux graphics and platform headers
BuildRequires:  mesa-libGL-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-ng-compat-static

# System Qt frontend
BuildRequires:  qt6-qtbase-devel >= 6.9
BuildRequires:  qt6-qttools-devel >= 6.9
BuildRequires:  qt6-qtwayland-devel >= 6.9

# Optional but recommended; enables the Vulkan DMA-BUF shader path
BuildRequires:  glslang

Recommends:     liberation-sans-fonts

# Runtime library dependencies such as Qt 6 are detected automatically by
# RPM's dependency generator from the linked binaries.

%description
Ladybird is an independent web browser and engine built from scratch on
web standards, without basing its rendering engine on Blink, Gecko, or
WebKit.

%prep
%autosetup -n %{name}-%{commit}

# Ladybird enables -march=native for normal native builds. This is unsuitable
# for distribution packages because it can generate binaries that require CPU
# features present on the build host but absent on users' systems.
#
# Fail the build if the expected option is not present, so an upstream change
# does not silently leave -march=native enabled.
grep -Fq 'add_cxx_compile_options(-march=native)' \
    Meta/CMake/compile_options.cmake

sed -i \
    '/add_cxx_compile_options(-march=native)/d' \
    Meta/CMake/compile_options.cmake

%build
export LADYBIRD_SOURCE_DIR="$PWD"
export VCPKG_ROOT="$PWD/Build/vcpkg"

# Keep both the vcpkg dependency build and the main Ladybird build from
# exhausting memory on Copr workers.
export VCPKG_MAX_CONCURRENCY=4
export CMAKE_BUILD_PARALLEL_LEVEL=4

# Clone vcpkg and check out the baseline pinned by vcpkg.json.
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
# Ladybird's test suite, including LibWeb layout tests and Test262, is large
# and may require a display or GPU. It is not run in the chroot build
# environment.
#
# Enable individual tests selectively when suitable:
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
