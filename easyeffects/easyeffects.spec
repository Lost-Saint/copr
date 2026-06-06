Name:           easyeffects
Version:        8.2.4
Release:        1%{?dist}
Summary:        Audio effects and filters for PipeWire applications

License:        GPL-3.0-or-later
URL:            https://github.com/wwmm/easyeffects
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Preserve upgrade path from the historical PulseEffects package.
Provides:       pulseeffects = 6.1.1-1
Obsoletes:      pulseeffects < 6.1.1-1

# Base build requirements
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  itstool

# Qt 6 framework
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Graphs)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6WebEngineQuick)

# KDE Frameworks 6 integration
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6Kirigami)
BuildRequires:  cmake(KF6KirigamiAddons)
BuildRequires:  cmake(KF6QQC2DesktopStyle)

# QML modules not detected automatically
BuildRequires:  qt6qml(org.kde.kirigami)

# Core libraries and DSP dependencies
BuildRequires:  cmake(TBB)

BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.0.6
BuildRequires:  pkgconfig(lilv-0) >= 0.24
BuildRequires:  pkgconfig(libebur128) >= 1.2.6
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(rnnoise)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-qt6)
BuildRequires:  pkgconfig(webrtc-audio-processing-2)

# Convolution engine
BuildRequires:  zita-convolver-devel >= 3.1.0

# Plugin and filter support
BuildRequires:  ladspa-devel
BuildRequires:  pkgconfig(libmysofa)

# Runtime integration and desktop styling
Requires:       breeze-icon-theme

# Default QQC2 desktop style selected by upstream
Requires:       kf6-qqc2-desktop-style%{?_isa}

# Recommended Breeze Plasma styling
Recommends:     plasma-breeze%{?_isa}

# Runtime QML modules required by the UI
Requires:       qt6qml(org.kde.kirigami)
Requires:       qt6qml(org.kde.kirigamiaddons.components)
Requires:       qt6qml(QtGraphs)
Requires:       qt6qml(QtWebEngine)

# Runtime system integration
Requires:       hicolor-icon-theme
Requires:       dbus-common

# Optional LV2 plugin collections
Recommends:     lv2-calf-plugins
Recommends:     lv2-mdala-plugins
Recommends:     lsp-plugins-lv2
Recommends:     lv2-zam-plugins

# QtWebEngine limits supported architectures
ExclusiveArch:  %{qt6_qtwebengine_arches}

%description
Limiters, compressor, reverberation, high-pass filter, low pass filter,
equalizer many more effects for PipeWire applications.

%prep
%autosetup

%conf
%cmake

%build
%cmake_build

%install
%cmake_install

%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/com.github.wwmm.%{name}.metainfo.xml


%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/com.github.wwmm.%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.github.wwmm.%{name}{,-symbolic}.svg
%{_datadir}/icons/hicolor/scalable/apps/com.github.wwmm.easyeffects-off-symbolic.svg
%{_datadir}/metainfo/com.github.wwmm.%{name}.metainfo.xml

%changelog
%autochangelog
