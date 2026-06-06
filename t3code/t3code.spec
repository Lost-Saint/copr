Name:           t3code
Version:        0.0.25
Release:        1%{?dist}
Summary:        Minimal web GUI for AI coding agents (Claude, Codex, OpenCode)
License:        MIT
URL:            https://github.com/pingdotgg/t3code

# Upstream ships a prebuilt AppImage; we repackage the extracted contents.
# A source build is not feasible: electron-builder downloads a ~100 MB Electron
# binary at build time and the pnpm/turbo toolchain is not in Fedora repos.
Source0:        https://github.com/pingdotgg/t3code/releases/download/v%{version}/T3-Code-%{version}.AppImage
# Source tarball used only for the LICENSE file
Source1:        https://github.com/pingdotgg/t3code/archive/refs/tags/v%{version}.tar.gz#/t3code-%{version}.tar.gz

ExclusiveArch:  x86_64

# Bundled Electron requires these at runtime
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXrandr
Requires:       mesa-libgbm
Requires:       nss
Requires:       alsa-lib
Requires:       at-spi2-atk
Requires:       cups-libs
Requires:       gtk3
Requires:       libdrm
Requires:       libxcb
Requires:       libxkbcommon

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
# For extracting the AppImage squashfs
BuildRequires:  squashfs-tools

# Nothing to compile — we repackage a prebuilt binary
%global debug_package %{nil}

%description
T3 Code is a minimal desktop GUI for AI coding agents.
It supports Claude Code, Codex CLI, and OpenCode, providing
a unified interface to interact with those agents.

Install and authenticate at least one provider before use:
  - Claude:   claude auth login
  - Codex:    codex login
  - OpenCode: opencode auth login

%prep
# Unpack source tarball for the LICENSE file only
%autosetup -n t3code-%{version} -b 1 -T

# Make the AppImage executable so we can extract it
install -m 0755 %{SOURCE0} %{_builddir}/T3-Code.AppImage

%build
# Extract the AppImage without FUSE (--appimage-extract is built into every AppImage)
cd %{_builddir}
./T3-Code.AppImage --appimage-extract
# Contents are now at %{_builddir}/squashfs-root/

%install
# Application files
install -d %{buildroot}%{_libdir}/%{name}
cp -a %{_builddir}/squashfs-root/. %{buildroot}%{_libdir}/%{name}/
# Remove AppImage-specific stub; we provide our own launcher
rm -f %{buildroot}%{_libdir}/%{name}/AppRun
rm -f %{buildroot}%{_libdir}/%{name}/.DirIcon

# Launcher wrapper
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/sh
exec %{_libdir}/%{name}/t3code "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Icons — AppImage ships them under usr/share/icons
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
for size in 16 32 48 64 128 256 512; do
    src="%{_builddir}/squashfs-root/usr/share/icons/hicolor/${size}x${size}/apps/t3code.png"
    if [ -f "$src" ]; then
        install -Dm 0644 "$src" \
            %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
    fi
done
# Fallback: use the .DirIcon as a 256px icon if present
if [ -f "%{_builddir}/squashfs-root/t3code.png" ]; then
    install -Dm 0644 "%{_builddir}/squashfs-root/t3code.png" \
        %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
fi

# Desktop entry
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=T3 Code
Comment=Minimal GUI for AI coding agents
Exec=t3code %U
Icon=t3code
Terminal=false
Type=Application
Categories=Development;IDE;
Keywords=AI;coding;agent;claude;codex;opencode;
StartupWMClass=t3code
EOF
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# AppStream metainfo
install -d %{buildroot}%{_datadir}/metainfo
cat > %{buildroot}%{_datadir}/metainfo/%{name}.metainfo.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.pingdotgg.t3code</id>
  <name>T3 Code</name>
  <summary>Minimal GUI for AI coding agents</summary>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <description>
    <p>
      T3 Code is a minimal desktop GUI for AI coding agents.
      It supports Claude Code, Codex CLI, and OpenCode, providing
      a unified chat interface to interact with those agents.
    </p>
  </description>
  <url type="homepage">https://t3.codes</url>
  <url type="bugtracker">https://github.com/pingdotgg/t3code/issues</url>
  <releases>
    <release version="0.0.25" date="2026-06-04"/>
  </releases>
  <content_rating type="oars-1.1"/>
</component>
EOF
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/%{name}.metainfo.xml

%files
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}.metainfo.xml

%changelog
* Wed Jun 04 2026 Your Name <you@example.com> - 0.0.25-1
- Initial COPR package (prebuilt AppImage repackage)
