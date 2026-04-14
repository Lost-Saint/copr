# Signing key from https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
%global appid com.mitchellh.ghostty

Name:           ghostty
Version:        1.3.1
Release:        1%{?dist}
Summary:        A fast, native terminal emulator written in Zig.

License:        MIT AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0) AND Apache-2.0
URL:            https://ghostty.org/
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig


ExclusiveArch: x86_64 aarch64


BuildRequires:  gettext
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libX11-devel
BuildRequires:  minisign
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  pandoc-cli
BuildRequires:  systemd-rpm-macros
BuildRequires:  zig >= 0.14.0
BuildRequires:  zig-rpm-macros
BuildRequires:  pkgconfig(blueprint-compiler)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(zlib)

Requires:       %{name}-terminfo = %{evr}
Requires:       (%{name}-kio = %{evr} if kf5-kio-core)
Requires:       (%{name}-kio = %{evr} if kf6-kio-core)
Requires:       gtk4
Requires:       gtk4-layer-shell
Requires:       libadwaita
Conflicts:      ghostty-nightly


%description
👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

%prep
%setup -q -n ghostty-%{version}


%build
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs \
    -Demit-themes=true

%if 0%{?fedora} >= 42
    rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%find_lang %{appid}

%files -f %{appid}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/dbus-1/services/%{appid}.service
%{_iconsdir}/hicolor/16x16/apps/%{appid}.png
%{_iconsdir}/hicolor/16x16@2/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32@2/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128@2/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256@2/apps/%{appid}.png
%{_iconsdir}/hicolor/512x512/apps/%{appid}.png
%{_iconsdir}/hicolor/1024x1024/apps/%{appid}.png
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}.5.gz
%{_userunitdir}/app-%{appid}.service

%files terminfo
%if 0%{?fedora} < 42
%{_datadir}/terminfo/g/%{name}
%endif
%{_datadir}/terminfo/x/xterm-%{name}

%post
%systemd_user_post app-%{appid}.service

%preun
%systemd_user_preun app-%{appid}.service

%postun
%systemd_user_postun app-%{appid}.service

%files -n libghostty-vt
%{_libdir}/libghostty-vt.so.*

%files -n libghostty-vt-devel
%{_libdir}/libghostty-vt.so
%{_datadir}/pkgconfig/libghostty-vt.pc

%changelog
%autochangelog
