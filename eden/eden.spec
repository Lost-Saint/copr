%global appid dev.eden_emu.eden

Name:           eden
Version:        0.2.0
Release:        1%{?dist}
Summary:        Nintendo Switch emulator/debugger (Eden)
License:        GPL-3.0-or-later
URL:            https://eden-emu.dev

Source0:        https://git.eden-emu.dev/eden-emu/eden/archive/v%{version}-rc2.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake >= 3.22
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  python3 >= 3.10
BuildRequires:  nasm
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  jq
BuildRequires:  patch

# Qt6
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtwebengine-devel
BuildRequires:  qt6-qtcharts-devel
BuildRequires:  qt6-linguist

# Vulkan / graphics
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-utility-libraries-devel
BuildRequires:  glslang-devel
BuildRequires:  spirv-tools-devel
BuildRequires:  spirv-headers-devel

# Audio / codec
BuildRequires:  ffmpeg-devel
BuildRequires:  opus-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speexdsp-devel

# Compression / crypto
BuildRequires:  lz4-devel
BuildRequires:  libzstd-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

# Misc libraries
BuildRequires:  boost-devel
BuildRequires:  fmt-devel
BuildRequires:  json-devel
BuildRequires:  hidapi-devel
BuildRequires:  libusb1-devel
BuildRequires:  libXext-devel
BuildRequires:  wayland-devel
BuildRequires:  SDL2-devel

# Runtime
Requires:       qt6-qtbase
Requires:       qt6-qtmultimedia
Requires:       SDL2
Requires:       opus
Requires:       openssl
Requires:       vulkan-loader

%description
eden is an open source Nintendo Switch emulator/debugger.

%prep
%setup -q -n eden

%build
# Fedora 36+ with GCC 12 requires Clang for C++ compilation.
# Use clang++ unconditionally to stay consistent across Fedora versions.
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DYUZU_TESTS=OFF \
    -DYUZU_USE_CPM=ON \
    -DYUZU_USE_EXTERNAL_FFMPEG=ON \
    -DYUZU_USE_EXTERNAL_SDL2=ON \
    -DENABLE_QT_TRANSLATION=ON \
    -DYUZU_CHECK_SUBMODULES=OFF

%cmake_build

%install
%cmake_install

# Install desktop entry and icon if present
install -Dm644 dist/%{appid}.desktop \
    %{buildroot}%{_datadir}/applications/%{appid}.desktop
install -Dm644 dist/%{appid}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
install -Dm644 dist/%{appid}.metainfo.xml \
    %{buildroot}%{_datadir}/metainfo/%{appid}.metainfo.xml
install -Dm644 dist/72-yuzu-input.rules \
    %{buildroot}%{_udevrulesdir}/72-yuzu-input.rules

%files
%license LICENSE.txt LICENSES/
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_udevrulesdir}/72-yuzu-input.rules

%changelog
%autochangelog
