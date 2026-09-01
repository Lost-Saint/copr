%global debug_package %{nil}
%global helium_base %{_libdir}/helium

Name:           helium-bin
Version:        0.16.2.1
Release:        1%{?dist}
Summary:        Private, fast, and honest web browser

License:        GPL-3.0-only
URL:            https://github.com/imputnet/helium-linux

Source0:        https://github.com/imputnet/helium-linux/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz
Source1:        https://github.com/imputnet/helium-linux/releases/download/%{version}/helium-%{version}-arm64_linux.tar.xz
Source2:        https://raw.githubusercontent.com/imputnet/helium-linux/%{version}/package/net.imput.helium.metainfo.xml

ExclusiveArch:  x86_64 aarch64

BuildRequires:  appstream
BuildRequires:  desktop-file-utils

Recommends:     ca-certificates
Recommends:     liberation-fonts
Recommends:     vulkan-loader
Recommends:     xdg-utils

%description
Helium is a private, fast, and honest web browser based on Chromium.


%prep
%ifarch x86_64
%setup -q -n helium-%{version}-x86_64_linux
%endif

%ifarch aarch64
%setup -q -T -b 1 -n helium-%{version}-arm64_linux
%endif


%build
# Helium is distributed as a prebuilt binary.


%install
install -d \
    %{buildroot}%{helium_base} \
    %{buildroot}%{_bindir} \
    %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/metainfo \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

cp -a . %{buildroot}%{helium_base}/

# Identify this build as the Fedora package in Helium bug reports.
sed -Ei 's/(CHROME_VERSION_EXTRA=).*/\1Fedora/' \
    %{buildroot}%{helium_base}/helium-wrapper

install -Dm0644 product_logo_256.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

install -Dm0644 helium.desktop \
    %{buildroot}%{_datadir}/applications/helium.desktop

install -Dm0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/metainfo/net.imput.helium.metainfo.xml

ln -s %{helium_base}/helium-wrapper \
    %{buildroot}%{_bindir}/helium


%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/helium.desktop

appstreamcli validate --no-net \
    %{buildroot}%{_datadir}/metainfo/net.imput.helium.metainfo.xml


%files
%{helium_base}/
%{_bindir}/helium
%{_datadir}/applications/helium.desktop
%{_datadir}/metainfo/net.imput.helium.metainfo.xml
%{_datadir}/icons/hicolor/256x256/apps/helium.png
