Name:           zed-lost-saint
Version:        1.22.0
Release:        2%{?dist}
Summary:        Feature-enhanced fork of the Zed code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://github.com/Lost-Saint/zed
Source0:        %{url}/releases/download/v%{version}/zed-linux-x86_64.tar.gz

ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Conflicts:      zed
Conflicts:      zed-aarch64

%global debug_package %{nil}
%global zed_home %{_prefix}/lib/zed-lost-saint

# Keep upstream's private library bundle for binary compatibility without
# advertising those libraries as system-wide RPM capabilities.  Filter their
# matching requirements while retaining RPM's automatic requirements for host
# libraries such as ALSA, GLib, glibc, and libgcc.
%global __provides_exclude_from ^%{zed_home}/lib/.*$
%global __requires_exclude ^(libX11-xcb|libXau|libXdmcp|libbsd|libmd|libstdc\+\+|libxcb|libxcb-xkb|libxkbcommon|libxkbcommon-x11)\.so\.

%description
An unofficial, feature-enhanced fork of Zed, a high-performance multiplayer
code editor.

This package installs the prebuilt binary published by Lost-Saint.

%prep
%autosetup -n zed-dev.app

%build

%install
install -Dm755 bin/zed %{buildroot}%{zed_home}/bin/zed
install -Dm755 libexec/zed-editor %{buildroot}%{zed_home}/libexec/zed-editor
install -dm755 %{buildroot}%{zed_home}/lib
cp -a lib/. %{buildroot}%{zed_home}/lib/

install -dm755 %{buildroot}%{_bindir}
ln -sr %{buildroot}%{zed_home}/bin/zed %{buildroot}%{_bindir}/zed

install -Dm644 share/icons/hicolor/512x512/apps/zed.png \
    %{buildroot}%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed-Dev.png
install -Dm644 share/icons/hicolor/1024x1024/apps/zed.png \
    %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed-Dev.png
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --set-icon=dev.zed.Zed-Dev \
    share/applications/dev.zed.Zed-Dev.desktop

install -Dm644 licenses.md %{buildroot}%{_licensedir}/%{name}/licenses.md

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.zed.Zed-Dev.desktop
test -x %{buildroot}%{zed_home}/bin/zed
test -x %{buildroot}%{zed_home}/libexec/zed-editor
test "$(readlink %{buildroot}%{_bindir}/zed)" = \
    "../lib/zed-lost-saint/bin/zed"

%files
%license %{_licensedir}/%{name}/licenses.md
%{_bindir}/zed
%{zed_home}/
%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed-Dev.png
%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed-Dev.png
%{_datadir}/applications/dev.zed.Zed-Dev.desktop

%changelog
%autochangelog
