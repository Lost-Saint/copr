%global commit 9a29a956b0eb199e495c72b54003f638829a70b7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20260429T204116Z
%global tag v0.5.22
%global clean_tag %(echo %{tag} | sed 's/^v//')

%define debug_package %{nil}
Name:           lutris
Version:        %{clean_tag}^%{git_date}.g%{shortcommit}
Release:        %autorelease
Summary:        Install and play any video game easily

# Automatically converted from old format: GPLv3 - review is highly recommended.
License:        GPL-3.0-only
URL:            https://github.com/lutris/lutris
Source0:        %{url}/archive/%{commit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  gobject-introspection
BuildRequires:  gtk3-devel
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  python3-cairo-devel
BuildRequires:  python3-gobject
BuildRequires:  fdupes, libappstream-glib
BuildRequires:  meson, gettext

Requires:       cabextract
Requires:       gtk3, psmisc
Requires:       hicolor-icon-theme
# According to the INSTALL.rst upstream docs, lutris requires either (xorg-x11-server-Xephyr, xrandr)
# or gnome-desktop3. Considering we are mainly using Wayland now, gnome-desktop3 should be sufficient.
Requires:       gnome-desktop3
Requires:       python3-distro
Requires:       python3-cairo

%ifarch x86_64
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader(x86-32)
Requires:       mesa-libGL(x86-32)
Recommends:     pipewire(x86-32)
Recommends:     libFAudio(x86-32)
Recommends:     wine-pulseaudio(x86-32)
Recommends:     wine-core(x86-32)
%endif

Requires:       mesa-vulkan-drivers
Requires:       mesa-dri-drivers
Requires:       vulkan-loader
Requires:       mesa-libGL
Requires:       glx-utils, gvfs
Requires:       webkit2gtk4.1
Recommends:     p7zip, curl
Recommends:     fluid-soundfont-gs
Recommends:     wine-core
Recommends:     p7zip-plugins
Recommends:     gamemode
Recommends:     libFAudio
Recommends:     gamescope

%description
Lutris is a gaming platform for GNU/Linux. Its goal is to make
gaming on Linux as easy as possible by taking care of installing
and setting up the game for the user. The only thing you have to
do is play the game. It aims to support every game that is playable
on Linux.

%prep
%autosetup -n %{name}-%{commit} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
%meson
%meson_build

%install
%pyproject_install
%pyproject_save_files lutris
%meson_install
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/net.%{name}.Lutris.metainfo.xml
%fdupes %{buildroot}%{python3_sitelib}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications share/applications/net.%{name}.Lutris.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications share/applications/net.%{name}.Lutris1.desktop
%find_lang %{name} --with-man

%check
# Python tests: Disabled because either they are querying hardware (Don't work in mock) or they're
# trying to spawn processes, which is also blocked.
# %pytest --ignore=tests/test_dialogs.py --ignore=tests/test_installer.py --ignore=tests/test_api.py -k "not GetNvidiaDriverInfo and not GetNvidiaGpuInfo and not import_module and not options"

%files -f %{pyproject_files} -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/net.%{name}.Lutris.desktop
%{_datadir}/applications/net.%{name}.Lutris1.desktop
%{_iconsdir}/hicolor/*/apps/net.lutris.Lutris.png
%{_iconsdir}/hicolor/*/mimetypes/application-x-lutris.svg
%{_mandir}/man1/%{name}.1.gz
# Some files being missed by the Python macros
%{python3_sitelib}/%{name}/__pycache__/optional_settings.*.pyc
%{python3_sitelib}/%{name}/optional_settings.py
# ---
%{_datadir}/mime/packages/application-x-lutris.xml
%{_datadir}/metainfo/
%{_datadir}/locale/

%changelog
%autochangelog
