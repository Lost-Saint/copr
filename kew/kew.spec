%global debug_package %{nil}

Name:           kew
Version:        4.0.0
Release:        1%{?dist}
Summary:        A terminal music player for Linux

License:        GPL-2.0-only
URL:            https://codeberg.org/ravachol/kew
Source0:        https://codeberg.org/ravachol/kew/archive/v%{version}.tar.gz

Patch0:         kew-no-setcap.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  taglib-devel
BuildRequires:  fftw-devel
BuildRequires:  opus-devel
BuildRequires:  opusfile-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libogg-devel
BuildRequires:  chafa-devel
BuildRequires:  freeimage-devel
BuildRequires:  libnotify-devel
BuildRequires:  glib2-devel
BuildRequires:  libatomic

# Add: AAC/M4A support via faad2 (auto-detected at build time)
BuildRequires:  faad2-devel

Requires:       chafa
Requires:       libnotify

%description
kew is a terminal music player that searches your music library
by partial title and builds a playlist automatically. It supports
MP3, FLAC, AAC/M4A, Opus, OGG, WebM, WAV, and AIFF, with gapless
playback, full-color album art in sixel terminals, MPRIS integration,
lyrics via .lrc files or embedded tags, replay gain, and a spectrum
visualizer.

%prep
%autosetup -p1 -n kew

%build
%make_build PREFIX=%{_prefix} KEW_VERSION=v%{version}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%files
%license LICENSE
%doc README.md
%{_bindir}/kew
%{_datadir}/kew/
%{_datadir}/locale/*/LC_MESSAGES/kew.mo
%{_mandir}/man1/kew.1*

%changelog
%autochangelog
