%global commit 5e1ac6df87d44f01785b01c8b5258235410bca76
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20260705T205209Z
%global tag v6.1.0
%global clean_tag %(echo %{tag} | sed 's/^v//')

Name:           moonlight-nightly
Version:        %{clean_tag}^%{git_date}.g%{shortcommit}
Release:        1%{?dist}
Summary:        Nightly Moonlight game-streaming client

License:        GPL-3.0-or-later
URL:            https://github.com/moonlight-stream/moonlight-qt
Source0:        %{name}-%{commit}.tar.gz

BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libavcodec) >= 60
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libplacebo) >= 7.349.0
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-wayland)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)

# Both packages install /usr/bin/moonlight.
Conflicts:       moonlight

%description
Moonlight is an open-source game-streaming client for Sunshine and NVIDIA
GameStream hosts. This package tracks the upstream master branch and is built
entirely from source, including its pinned Git submodules.

%prep
%autosetup -n %{name}-%{commit}

%build
qmake6 \
    "QMAKE_CFLAGS+=%{build_cflags}" \
    "QMAKE_CXXFLAGS+=%{build_cxxflags}" \
    "QMAKE_LFLAGS+=%{build_ldflags}" \
    "PREFIX=%{_prefix}" \
    "BINDIR=bin" \
    "DATADIR=share" \
    "CONFIG+=release" \
    moonlight-qt.pro

%make_build release

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
appstreamcli validate --no-net \
    %{buildroot}%{_datadir}/metainfo/com.moonlight_stream.Moonlight.appdata.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/moonlight
%{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
%{_datadir}/icons/hicolor/scalable/apps/moonlight.svg
%{_datadir}/metainfo/com.moonlight_stream.Moonlight.appdata.xml

%changelog
* Sun Jul 05 2026 Moonlight COPR <noreply@copr.invalid> - 6.1.0^20260705T205209Z.g5e1ac6d-1
- Nightly snapshot
