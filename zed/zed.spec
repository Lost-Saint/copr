Name:           zed
Version:        nightly
Release:        1%{?dist}
Summary:        Zed Nightly App

License:        GPL
URL:            https://github.com/zed-industries/zed
%define _disable_source_fetch 0
Source0:        https://zed.dev/api/releases/nightly/latest/zed-linux-x86_64.tar.gz
BuildArch:      x86_64


%description
Zed Nightly App

%licence licences.md

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
* Fri May 03 2024 sigmasd - nightly
- Initial package
