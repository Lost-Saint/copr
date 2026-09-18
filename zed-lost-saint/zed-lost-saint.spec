Name:           zed-lost-saint
Version:        1.22.0
Release:        1%{?dist}
Summary:        Feature-enhanced fork of the Zed code editor

License:        GPL-3.0-or-later AND Apache-2.0
URL:            https://github.com/Lost-Saint/zed
Source0:        %{url}/releases/download/v%{version}/zed-linux-x86_64.tar.gz

ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Conflicts:      zed
Conflicts:      zed-aarch64

AutoReqProv:    no
%global debug_package %{nil}
%global zed_home %{_prefix}/lib/zed-lost-saint

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

%post
%{_bindir}/update-desktop-database &>/dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%postun
%{_bindir}/update-desktop-database &>/dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%files
%license %{_licensedir}/%{name}/licenses.md
%{_bindir}/zed
%{zed_home}/
%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed-Dev.png
%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed-Dev.png
%{_datadir}/applications/dev.zed.Zed-Dev.desktop

%changelog
%autochangelog
