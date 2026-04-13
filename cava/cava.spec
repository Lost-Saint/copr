Name:           cava
Version:        0.10.7
Release:        1%{?dist}
Summary:        Console-based audio visualizer for ALSA/PulseAudio/PipeWire

License:        MIT
URL:            https://github.com/karlstav/cava
Source0:        %{url}/archive/%{version}/cava-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build

BuildRequires:  fftw-devel
BuildRequires:  ncurses-devel
BuildRequires:  iniparser-devel
BuildRequires:  libconfig-devel

BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel

%description
CAVA (Console-based Audio Visualizer for ALSA/PulseAudio/PipeWire)
is a terminal-based spectrum visualizer using FFT audio analysis.

%prep
%autosetup -n cava-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/cava
%{_datadir}/cava/
%{_mandir}/man1/cava.1*

%changelog
%autochangelog
