Name:           easyeffects
Version:        8.2.1
Release:        1%{?dist}
Summary:        Audio effects and filters for PipeWire applications

License:        GPL-3.0-only
URL:            https://github.com/wwmm/easyeffects
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Absorb the old PulseAudio-era name
Provides:       pulseeffects = 6.1.1-1
Obsoletes:      pulseeffects < 6.1.1-1

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils

# Qt6
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Graphs)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)

# KDE Frameworks 6
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6Kirigami)
BuildRequires:  cmake(KF6KirigamiAddons)
BuildRequires:  cmake(KF6QQC2DesktopStyle)

# QML module availability at build time
BuildRequires:  qt6qml(org.kde.kirigami)

# TBB (cmake find module, not pkgconfig)
BuildRequires:  cmake(TBB)

# Audio / DSP — versioned where upstream enforces minimums
BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.0.6
BuildRequires:  pkgconfig(lilv-0) >= 0.24
BuildRequires:  pkgconfig(libebur128) >= 1.2.6
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(rnnoise)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-qt6)
BuildRequires:  pkgconfig(webrtc-audio-processing-2)
BuildRequires:  pkgconfig(libmysofa)
BuildRequires:  zita-convolver-devel >= 3.1.0
BuildRequires:  ladspa-devel

# Runtime — QML modules must be declared explicitly for Fedora depsolving
Requires:       qt6qml(org.kde.kirigami)
Requires:       qt6qml(org.kde.kirigamiaddons.components)
Requires:       qt6qml(QtGraphs)

# Visual style
Requires:       breeze-icon-theme
Requires:       hicolor-icon-theme
# Default theme referenced directly in source
Requires:       kf6-qqc2-desktop-style%{?_isa}
# Upstream recommendation; non-fatal without it
Recommends:     plasma-breeze%{?_isa}

# D-Bus activation
Requires:       dbus-common

# PipeWire PulseAudio compatibility layer
Requires:       pipewire-pulseaudio

# Optional LV2/LADSPA plugin collections (provide the actual effects)
Recommends:     lv2-calf-plugins
Recommends:     lsp-plugins-lv2
Recommends:     lv2-mdala-plugins
Recommends:     lv2-zam-plugins

# In-app help requires yelp
Recommends:     yelp

%description
EasyEffects (formerly PulseEffects) is an audio effects and filters
application for PipeWire. It applies real-time DSP processing to both
playback and recording streams, with a modern Qt6/QML/Kirigami interface
and a system tray applet.

Supported effects include: parametric equalizer, compressor, limiter,
gate, expander, convolver (room correction / impulse response), bass
enhancer, exciter, RNNoise AI-based noise reduction, stereo tools,
pitch shifting, reverberation, echo canceller, and more.

Effect chains are fully configurable: plugins can be reordered
dynamically and saved as named presets that can be autoloaded per device.

%prep
%autosetup -p1

%conf
%cmake -GNinja

%build
%cmake_build

%install
%cmake_install

%find_lang %{name}

%check
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/com.github.wwmm.%{name}.metainfo.xml
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/com.github.wwmm.%{name}.desktop

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/com.github.wwmm.%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/com.github.wwmm.%{name}{,-symbolic}.svg
%{_datadir}/metainfo/com.github.wwmm.%{name}.metainfo.xml
%{_datadir}/dbus-1/services/com.github.wwmm.%{name}.service
%{_datadir}/%{name}/

%changelog
%autochangelog
