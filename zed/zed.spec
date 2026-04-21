%global commit 1db292d2fc4e74604bf07e9f7a859aa26ab6ea9b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20260420
%global ver 0.234.0

Name:           zed-nightly
Version:        %ver^%commit_date.%shortcommit
Release:        1%{?dist}
Summary:        Zed is a high-performance, multiplayer code editor
SourceLicense:  AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
License:        ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND ((MIT OR Apache-2.0) AND Unicode-3.0) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 AND ISC) AND AGPL.3.0-only AND AGPL-3.0-or-later AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception) AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR MIT OR Apache-2.0) AND BSD-2-Clause AND (CC0-1.0 OR Apache-2.0 OR Apache-2.0 WITH LLVM-exception) AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND CC0-1.0 AND GPL-3.0-or-later AND (ISC AND (Apache-2.0 OR ISC) AND OpenSSL) AND (ISC AND (Apache-2.0 OR ISC)) AND ISC AND (MIT AND (MIT OR Apache-2.0)) AND (MIT AND BSD-3-Clause) AND (MIT OR Apache-2.0 OR CC0-1.0) AND (MIT OR Apache-2.0 OR NCSA) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND MIT AND MPL-2.0 AND Unicode-3.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT) AND Zlib
URL:            https://zed.dev/
Source0:        https://github.com/zed-industries/zed/archive/%{commit}.tar.gz
BuildArch:      x86_64


%description
Zed Nightly App

%license licenses.md

%prep
%setup -q -n zed-nightly.app

# Patch desktop file
sed -i 's/Icon=zed/Icon=dev.zed.Zed-Nightly/' share/applications/zed-nightly.desktop

%define  debug_package %{nil}

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_bindir}
install -m 755 bin/zed %{buildroot}/%{_bindir}/zed
install -d %{buildroot}/%{_libexecdir}
install -m 755 libexec/zed-editor %{buildroot}/%{_libexecdir}/zed-editor
install -d %{buildroot}/%{_datadir}/applications
install -m 644 share/applications/zed-nightly.desktop %{buildroot}/%{_datadir}/applications/dev.zed.Zed-Nightly.desktop
install -d %{buildroot}/%{_datadir}/icons/hicolor/1024x1024/apps
install -m 644 share/icons/hicolor/1024x1024/apps/zed.png %{buildroot}/%{_datadir}/icons/hicolor/1024x1024/apps/dev.zed.Zed-Nightly.png
install -d %{buildroot}/%{_datadir}/icons/hicolor/512x512/apps
install -m 644 share/icons/hicolor/512x512/apps/zed.png %{buildroot}/%{_datadir}/icons/hicolor/512x512/apps/dev.zed.Zed-Nightly.png

%files
%{_bindir}/zed
%{_libexecdir}/zed-editor
%{_datadir}/applications/dev.zed.Zed-Nightly.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/dev.zed.Zed-Nightly.png
%{_datadir}/icons/hicolor/512x512/apps/dev.zed.Zed-Nightly.png

%changelog
%autochangelog
