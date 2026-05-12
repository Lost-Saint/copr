%global appid dev.eden_emu.eden

%if %{with pgo}
%global toolchain clang
%endif

%undefine _hardened_build

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
Source1:        https://github.com/Eden-CI/PGO/releases/latest/download/eden.profdata

ExclusiveArch:  x86_64 aarch64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mold

BuildRequires:  ninja-build
BuildRequires:  clang
BuildRequires:  lld

BuildRequires:  cmake
BuildRequires:  cmake(LLVM)
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(zlib)
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  cmake(SPIRV-Headers)
BuildRequires:  cmake(SPIRV-Tools)
BuildRequires:  cmake(SDL2)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Charts)
BuildRequires:  cmake(Qt6WebEngineCore)
BuildRequires:  cmake(Qt6WebEngineWidgets)

BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  pkgconfig(libudev)

BuildRequires:  glslang
BuildRequires:  automake
BuildRequires:  ffmpeg-devel
BuildRequires:  boost-devel
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_resize-devel
BuildRequires:  renderdoc-devel
BuildRequires:  vulkan-utility-libraries-devel
BuildRequires:  VulkanMemoryAllocator-devel

%description
Eden is an experimental open-source emulator for the Nintendo Switch, built with performance and stability in mind. It is written in C++ with cross-platform support for Windows, Linux, FreeBSD, Solaris, OpenBSD, and Android.

%prep
%setup -q -n eden


%build

cmake -S . -B build -GNinja \
    -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
    -DCMAKE_BUILD_TYPE="Release" \
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
%if %{with pgo}
    -DCMAKE_C_FLAGS="-fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
    -DCMAKE_CXX_FLAGS="-fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
%endif
    -Wno-dev

cmake --build build

%install
cmake --install build

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
%{_udevrulesdir}/72-yuzu-input.rules

%changelog
%autochangelog
