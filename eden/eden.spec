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

# Build tools
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  mold
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  jq

# LLVM
BuildRequires:  cmake(LLVM)

# Qt6 - core modules
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  qt6-qtsvg-devel

# Qt6 - multimedia (YUZU_USE_QT_MULTIMEDIA=ON)
BuildRequires:  cmake(Qt6Multimedia)

# Qt6 - web engine (YUZU_USE_QT_WEB_ENGINE=ON)
BuildRequires:  cmake(Qt6WebEngineCore)
BuildRequires:  cmake(Qt6WebEngineWidgets)

# Qt6 - charts (used by telemetry/stats UI)
BuildRequires:  cmake(Qt6Charts)

# FFmpeg - system package required (RPM Fusion free must be enabled)
BuildRequires:  ffmpeg-devel

# Vulkan
BuildRequires:  cmake(SPIRV-Headers)
BuildRequires:  cmake(SPIRV-Tools)
BuildRequires:  vulkan-utility-libraries-devel
BuildRequires:  VulkanMemoryAllocator-devel
BuildRequires:  glslang

# Audio
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(libpulse)

# Input / HID
BuildRequires:  pkgconfig(hidapi)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libudev)

# Graphics / display
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libXext)

# Compression / serialization
BuildRequires:  cmake(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)

# Networking / crypto
BuildRequires:  pkgconfig(openssl)

# Data / config
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  boost-devel

# SDL2 - system package (YUZU_USE_BUNDLED_SDL2=OFF, YUZU_USE_EXTERNAL_SDL2=OFF)
BuildRequires:  cmake(SDL2)

# Miscellaneous
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_resize-devel
BuildRequires:  renderdoc-devel

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
