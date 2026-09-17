%global debug_package %{nil}

Name:           helium
Version:        0.17.1.1
Release:        1%{?dist}
Summary:        Private, fast, and honest web browser

License:        GPL-3.0-only
URL:            https://github.com/imputnet/helium-linux

Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz
Source1:        %{url}/releases/download/%{version}/helium-%{version}-arm64_linux.tar.xz
Source2:        https://raw.githubusercontent.com/imputnet/helium-linux/%{version}/package/net.imput.helium.metainfo.xml

ExclusiveArch:  x86_64 aarch64

Recommends:     ca-certificates
Recommends:     liberation-fonts
Recommends:     vulkan-loader
Recommends:     xdg-utils

%description
Helium is a private, fast, and honest Chromium-based web browser.


%prep
%ifarch x86_64
%setup -q -n helium-%{version}-x86_64_linux
%endif

%ifarch aarch64
%setup -q -T -b 1 -n helium-%{version}-arm64_linux
%endif


%build
# Prebuilt upstream binaries.


%install
install -d %{buildroot}%{_libdir}/helium
cp -a . %{buildroot}%{_libdir}/helium/

# Identify the Fedora package in Helium's version information.
sed -Ei 's/(CHROME_VERSION_EXTRA=).*/\1Fedora/' \
    %{buildroot}%{_libdir}/helium/helium-wrapper

install -d %{buildroot}%{_bindir}
ln -s %{_libdir}/helium/helium-wrapper \
    %{buildroot}%{_bindir}/helium

install -Dm0644 helium.desktop \
    %{buildroot}%{_datadir}/applications/helium.desktop

install -Dm0644 product_logo_256.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

install -Dm0644 %{SOURCE2} \
    %{buildroot}%{_metainfodir}/net.imput.helium.metainfo.xml


%files
%{_bindir}/helium
%{_libdir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png
%{_metainfodir}/net.imput.helium.metainfo.xml


%changelog
%autochangelog
