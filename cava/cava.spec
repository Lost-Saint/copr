Name:           cava
Version:        0.10.7
Release:        1%{?dist}
Summary:        Console-based Audio Visualizer for Alsa

License:        MIT
URL:            https://github.com/karlstav/cava
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  alsa-lib-devel
BuildRequires:  fftw-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
BuildRequires:  iniparser-devel
BuildRequires: make

%description
C.A.V.A. is a bar spectrum analyzer for audio using ALSA for input.

%prep
%autosetup -p1
./autogen.sh


%build
%configure FONT_DIR=/lib/kbd/consolefonts LIBS=-lrt
make %{?_smp_mflags} \
    cava_LDFLAGS=


%install
%make_install
rm -f %{buildroot}%{_libdir}/libiniparser.{a,la,so}

%files
%license LICENSE
%doc README.md
%doc example_files
%{_bindir}/cava
/lib/kbd/consolefonts/cava.psf


%changelog
* Mon Apr 13 2026 Myriad Sun <lost-saint@users.noreply.github.com> - 0.10.7-1
- fixed various PipeWire issues (#688 #699)
- fixed device issues on Windows (#696 #713 #712)
- improved memory handling in config reloading (#698)
- added live config auto-reload (#718)
- adjusted default EQ and frequency bandwidth (commit 724c694)
