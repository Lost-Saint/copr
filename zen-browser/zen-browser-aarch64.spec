%global             appid zen-browser
%global             app_name zen
%global             debug_package %{nil}

Name:               zen-browser
Version:            1.19.10b
Release:            1%{?dist}
Summary:            Zen Browser

License:            MPLv2.0
URL:                https://github.com/zen-browser/desktop

Source0:            https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-aarch64.tar.xz
Source1:            %{appid}.desktop
Source2:            policies.json
Source3:            %{appid}

ExclusiveArch:      aarch64

Recommends:         (plasma-browser-integration if plasma-workspace)
Recommends:         (gnome-browser-connector if gnome-shell)

Requires(post):     gtk-update-icon-cache
Conflicts:          zen-browser-avx2
Conflicts:          zen-browser

%description
This is a package of the Zen web browser. Zen Browser is a fork of Firefox
that aims to improve the browsing experience by focusing on a simple,
performant, private and beautifully designed browser.

Bugs related to Zen should be reported directly to the Zen Browser GitHub repo:
<https://github.com/zen-browser/desktop/issues>

Bugs related to this package should be reported at this Git project:
<https://github.com/lost-saint/copr>

%prep
%setup -q -n %{app_name}

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications,%{_iconsdir}/hicolor/128x128/apps,%{_iconsdir}/hicolor/64x64/apps,%{_iconsdir}/hicolor/48x48/apps,%{_iconsdir}/hicolor/32x32/apps,%{_iconsdir}/hicolor/16x16/apps}

%__cp -r * %{buildroot}/opt/%{app_name}

%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

%__install -D -m 0444 %{SOURCE2} -t %{buildroot}/opt/%{app_name}/distribution

%__install -D -m 0755 %{SOURCE3} -t %{buildroot}%{_bindir}

%__ln_s ../../../../../../opt/%{app_name}/browser/chrome/icons/default/default128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{appid}.png
%__ln_s ../../../../../../opt/%{app_name}/browser/chrome/icons/default/default64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{appid}.png
%__ln_s ../../../../../../opt/%{app_name}/browser/chrome/icons/default/default48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{appid}.png
%__ln_s ../../../../../../opt/%{app_name}/browser/chrome/icons/default/default32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{appid}.png
%__ln_s ../../../../../../opt/%{app_name}/browser/chrome/icons/default/default16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{appid}.png

%post
gtk-update-icon-cache -f -t %{_iconsdir}/hicolor

%files
%{_datadir}/applications/%{appid}.desktop
%{_iconsdir}/hicolor/128x128/apps/%{appid}.png
%{_iconsdir}/hicolor/64x64/apps/%{appid}.png
%{_iconsdir}/hicolor/48x48/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32/apps/%{appid}.png
%{_iconsdir}/hicolor/16x16/apps/%{appid}.png
%{_bindir}/%{appid}
/opt/%{app_name}

%changelog
%autochangelog
