Name:           zed
Version:        1.10.0
Release:        1%{?dist}
Summary:        Zed is a high-performance, multiplayer code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://zed.dev/
Source0:        https://github.com/zed-industries/zed/releases/download/v%{version}/zed-linux-x86_64.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

Conflicts:  zed-aarch64

AutoReqProv: no

# Prebuilt upstream binary — no debug info to extract
%global debug_package %{nil}

# Upstream layout must be preserved under a private dir so that the
# hardcoded RPATH ($ORIGIN/../lib) and relative libexec path
# (../libexec/zed-editor) both resolve correctly at runtime
%global zed_home %{_prefix}/lib/zed

%description
Code at the speed of thought – Zed is a high-performance, multiplayer code
editor from the creators of Atom and Tree-sitter.

This package installs the official prebuilt binary from the Zed project.

%prep
%autosetup -n zed.app

%build
# Nothing to build — prebuilt upstream binary

%install
# Preserve upstream bin/libexec/lib layout under zed_home so RPATH and
# relative paths work without patching the binary
install -Dm755 bin/zed            %{buildroot}%{zed_home}/bin/zed
install -Dm755 libexec/zed-editor %{buildroot}%{zed_home}/libexec/zed-editor

install -dm755 %{buildroot}%{zed_home}/lib
cp -a lib/. %{buildroot}%{zed_home}/lib/

install -dm755 %{buildroot}%{_bindir}
ln -sr %{buildroot}%{zed_home}/bin/zed %{buildroot}%{_bindir}/zed

install -Dm644 share/icons/hicolor/512x512/apps/zed.png \
    %{buildroot}%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed.png
install -Dm644 share/icons/hicolor/1024x1024/apps/zed.png \
    %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed.png

desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --set-icon=dev.zed.Zed \
    share/applications/dev.zed.Zed.desktop

install -Dm644 licenses.md %{buildroot}%{_datadir}/licenses/%{name}/licenses.md

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.zed.Zed.desktop

%post
%{_bindir}/update-desktop-database &>/dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%postun
%{_bindir}/update-desktop-database &>/dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%files
%license %{_licensedir}/%{name}/licenses.md
%{_bindir}/zed
%{zed_home}/bin/zed
%{zed_home}/libexec/zed-editor
%{zed_home}/lib/
%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed.png
%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed.png
%{_datadir}/applications/dev.zed.Zed.desktop

%changelog
%autochangelog
