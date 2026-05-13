%global appid dev.eden_emu.eden

# Enable PGO build with: --with pgo
%bcond_with pgo

# When PGO is enabled, use the clang compiler instead
%if %{with pgo}
%global toolchain clang
%endif

# Build preset to use. One of: custom, generic, v3, zen2, zen4, native
%if ! %{defined build_preset}
%global build_preset v3
%endif

Name:           eden
Version:        0.2.0
Release:        1%{?dist}
Summary:        Nintendo Switch emulator/debugger (Eden)
License:        GPL-3.0-or-later
URL:            https://eden-emu.dev

Source0:        https://git.eden-emu.dev/eden-emu/eden/archive/v%{version}-rc2.tar.gz
Source1:        https://github.com/Eden-CI/PGO/releases/download/v020525/eden.profdata

ExclusiveArch:  x86_64 aarch64

BuildRequires:  boost-devel >= 1.75.0
BuildRequires:  cmake >= 3.15
BuildRequires:  discord-rpc-devel
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  graphviz
BuildRequires:  hicolor-icon-theme
BuildRequires:  libboost_container-devel-impl >= 1.75.0
BuildRequires:  libboost_context-devel-impl >= 1.75.0
BuildRequires:  libboost_filesystem-devel-impl >= 1.75.0
BuildRequires:  libboost_headers-devel >= 1.75.0
BuildRequires:  libboost_process-devel-impl >= 1.75.0
BuildRequires:  libzstd-devel-static
BuildRequires:  llvm-devel
BuildRequires:  mold
BuildRequires:  nasm
BuildRequires:  ninja
BuildRequires:  shaderc
BuildRequires:  sndio-devel
BuildRequires:  vulkan-utility-libraries-devel

BuildRequires:  boost-devel >= 1.75.0
BuildRequires:  cmake >= 3.15
BuildRequires:  discord-rpc-devel
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  graphviz
BuildRequires:  hicolor-icon-theme
BuildRequires:  libboost_container-devel-impl >= 1.75.0
BuildRequires:  libboost_context-devel-impl >= 1.75.0
BuildRequires:  libboost_filesystem-devel-impl >= 1.75.0
BuildRequires:  libboost_headers-devel >= 1.75.0
BuildRequires:  libboost_process-devel-impl >= 1.75.0
BuildRequires:  libzstd-devel-static
BuildRequires:  llvm-devel
BuildRequires:  mold
BuildRequires:  nasm
BuildRequires:  ninja
BuildRequires:  shaderc
BuildRequires:  sndio-devel
BuildRequires:  unzip
BuildRequires:  vulkan-utility-libraries-devel

%description
Eden is an experimental open-source emulator for the Nintendo Switch, built with performance and stability in mind. It is written in C++ with cross-platform support for Windows, Linux, FreeBSD, Solaris, OpenBSD, and Android.

%prep
%setup -q -n eden


%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_DISCORD_PRESENCE=ON \
    -DYUZU_USE_BUNDLED_FFMPEG=OFF \
    -DYUZU_USE_BUNDLED_SDL2=OFF \
    -DYUZU_USE_EXTERNAL_SDL2=OFF \
    -DYUZU_USE_BUNDLED_QT=OFF \
    -DENABLE_QT_TRANSLATION=ON \
    -DYUZU_USE_QT_MULTIMEDIA=ON \
    -DYUZU_USE_QT_WEB_ENGINE=ON \
    -Dhttplib_FORCE_BUNDLED=ON \
    -DYUZU_TESTS=OFF \
    -DDYNARMIC_TESTS=OFF \
    -DBUILD_TESTING=OFF \
    -DUSE_FASTER_LINKER=ON \
    -DENABLE_LTO=ON \
    -DDYNARMIC_ENABLE_LTO=ON \
    -DYUZU_BUILD_PRESET=%{build_preset} \
    -DENABLE_RENDERDOC=ON \
%if %{with pgo}
    # Use precomputed LLVM PGO profile
    -DCMAKE_C_FLAGS="%{build_cflags} -fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
    -DCMAKE_CXX_FLAGS="%{build_cxxflags} -fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
%endif
    -Wno-dev

%cmake_build

%install
%cmake_install

%check
# Tests are disabled

%files
%license LICENSE.txt
%license LICENSES/*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-room
%{_datadir}/applications/%{appid}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datarootdir}/mime/packages/%{appid}.xml

%changelog
%autochangelog
