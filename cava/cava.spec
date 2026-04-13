Name:           cava
Version:        0.10.7
Release:        1%{?dist}
Summary:        Console-based audio visualizer for ALSA/PulseAudio/PipeWire

License:        MIT
URL:            https://github.com/karlstav/cava
Source0:        %{url}/archive/%{version}/cava-%{version}.tar.gz

ExclusiveArch: x86_64 aarch64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  iniparser-devel
BuildRequires:  pkgconfig(libconfig)

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpipewire-0.3)

%description
%{summary}.

%prep
%autosetup -n cava-%{version}
./autogen.sh

%build
%configure
%make_build

%install
%make_install

%files
%license LICENSE
%doc README.md
%{_bindir}/cava
%{_datadir}/cava/
%{_mandir}/man1/cava.1*
%{_datadir}/consolefonts/cava.psf

%changelog
%autochangelog
