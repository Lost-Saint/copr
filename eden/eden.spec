%global appid dev.eden_emu.eden

%global toolchain clang
# Build preset: x86_64 supports custom, generic, v3, zen2, zen4, native;
# aarch64 supports custom, generic, armv9, native.
%if ! %{defined build_preset}
%ifarch x86_64
%global build_preset v3
%else
%global build_preset generic
%endif
%endif

Name:           eden
Version:        0.2.1
Release:        2%{?dist}
Summary:        Nintendo Switch emulator/debugger (Eden)
License:        GPL-3.0-or-later
URL:            https://eden-emu.dev

Source0:        https://git.eden-emu.dev/eden-emu/eden/archive/v%{version}.tar.gz
Source1:        https://github.com/Eden-CI/PGO/releases/download/v020525/eden.profdata

%global pgo_flags -fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date

ExclusiveArch:  x86_64 aarch64

BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  mold
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  jq
BuildRequires:  cmake(LLVM)
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
# Qt6
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6WebEngineCore)
BuildRequires:  cmake(Qt6WebEngineWidgets)
BuildRequires:  cmake(Qt6Charts)
# FFmpeg
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
# Input
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libudev)
# Graphics / display
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(wayland-client)
# Compression / serialization
BuildRequires:  cmake(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
# Networking
BuildRequires:  pkgconfig(openssl)
# Data / config
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  boost-devel
# SDL2
BuildRequires:  cmake(SDL2)
# Miscellaneous
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_resize-devel
# Enable the RenderDoc COPR or disable ENABLE_RENDERDOC below.
%if %{defined with_renderdoc}
BuildRequires:  renderdoc-devel
%endif

Requires:       gamemode

Recommends:     xorg-x11-server-Xwayland

%description
Eden is an experimental open-source emulator for the Nintendo Switch, built with performance and stability in mind. It is written in C++ with cross-platform support for Windows, Linux, FreeBSD, Solaris, OpenBSD, and Android.

%prep
%autosetup -n eden

%build
# Fedora's compiler flags already enable LTO; upstream's IPO check fails with them.
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
    -DENABLE_LTO=OFF \
    -DYUZU_BUILD_PRESET=%{build_preset} \
    %if %{defined with_renderdoc}
        -DENABLE_RENDERDOC=ON \
    %else
        -DENABLE_RENDERDOC=OFF \
    %endif
    -DCMAKE_C_FLAGS="%{build_cflags} %{pgo_flags}" \
    -DCMAKE_CXX_FLAGS="%{build_cxxflags} %{pgo_flags}" \
    -Wno-dev

%cmake_build

%install
%cmake_install

# Force XWayland: Wayland is unsupported and causes issues
install -d %{buildroot}%{_libexecdir}
mv %{buildroot}%{_bindir}/eden %{buildroot}%{_libexecdir}/eden

cat > %{buildroot}%{_bindir}/eden << 'EOF'
#!/bin/sh
export QT_QPA_PLATFORM=xcb
exec %{_libexecdir}/eden "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/eden

%check
desktop-file-validate dist/%{appid}.desktop
appstreamcli validate --no-net dist/%{appid}.metainfo.xml

%files
%license LICENSE.txt
%license LICENSES/*
%doc README.md
%{_libexecdir}/eden
%{_bindir}/eden
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-room
%{_datadir}/applications/%{appid}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/mime/packages/%{appid}.xml

%changelog
%autochangelog
