Name:           cava
Version:        0.10.7
Release:        1%{?dist}
Summary:        Cross-platform Audio Visualizer for terminal or desktop
License:        MIT
URL:            https://github.com/karlstav/cava
Source0:        %{url}/archive/%{version}/cava-%{version}.tar.gz

%global _lto_cflags %nil

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  autoconf-archive
BuildRequires:  fftw-devel
BuildRequires:  ncurses-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  iniparser-devel
BuildRequires:  libglvnd-devel
BuildRequires:  SDL2-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel
BuildRequires:  pipewire-jack-audio-connection-kit-devel

Requires:       fftw
Requires:       ncurses
Requires:       alsa-lib
Requires:       iniparser
Requires:       libglvnd
Requires:       SDL2
Requires:       portaudio
Requires:       sndio
Requires:       pulseaudio-libs
Requires:       pipewire
Requires:       pipewire-jack-audio-connection-kit

%description
Cava is a bar spectrum audio visualizer for terminal or desktop (SDL).

Supports the following audio backends: PipeWire, PulseAudio, ALSA,
JACK, PortAudio, and FIFO input.

%prep
%autosetup -n cava-%{version}

%build
./autogen.sh
%configure
%make_build

%install
%make_install
install -Dm644 LICENSE -t %{buildroot}%{_datadir}/licenses/%{name}/

%files
%license LICENSE
%doc README.md
%{_bindir}/cava
%{_mandir}/man1/cava.1*
%{_datadir}/consolefonts/cava.psf

%changelog
* Mon Apr 13 2026 Your Name <you@example.com> - 0.10.7-1
- Update to latest upstream release 0.10.7
- Disable GLSL output to avoid AX_CHECK_GL macro incompatibility
