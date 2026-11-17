# Signing key from https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
%global appid com.mitchellh.ghostty
%global zig_version 0.17.1
%global zig_x86_64_sha256 3581863e3cbcfd0fce0efc682ce7e9e93da96668a977791d356a26d2a7e9b17a
%global zig_aarch64_sha256 a1546d5646eb184437918d6635ca6b762a0e889eac09cef720ee7a1ed3fe7795

# Zig does not emit the GNU build IDs required by Fedora's debug extractor.
%global debug_package %{nil}
# Zig does not emit GNU LTO objects; its transient cache objects should not be
# processed by Fedora's GNU LTO stripping pass.
%global __brp_strip_lto %{nil}

Name:           ghostty
Version:        1.4.0
Release:        1%{?dist}
Summary:        A fast, native terminal emulator written in Zig.
License:        MIT AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0) AND Apache-2.0
URL:            https://ghostty.org/
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig
Source2:        https://ziglang.org/download/%{zig_version}/zig-x86_64-linux-%{zig_version}.tar.xz
Source3:        https://ziglang.org/download/%{zig_version}/zig-aarch64-linux-%{zig_version}.tar.xz

ExclusiveArch: x86_64 aarch64

BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libadwaita-devel
BuildRequires:  minisign
BuildRequires:  pandoc-cli
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(egl)
BuildRequires:  wayland-protocols-devel

%description
👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

%package        devel
Summary:        Development files for libghostty-vt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package provides the development files for libghostty-vt.


%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%setup -q -n ghostty-%{version}
%ifarch x86_64
zig_archive=%{SOURCE2}
zig_sha256=%{zig_x86_64_sha256}
%elifarch aarch64
zig_archive=%{SOURCE3}
zig_sha256=%{zig_aarch64_sha256}
%endif
printf '%s  %s\n' "$zig_sha256" "$zig_archive" | sha256sum --check --strict -
mkdir .zig
tar -xf "$zig_archive" --strip-components=1 -C .zig
export PATH="$PWD/.zig:$PATH"
export ZIG_GLOBAL_CACHE_DIR="%{_builddir}/%{name}-zig-cache"
mkdir -p "$ZIG_GLOBAL_CACHE_DIR"
# Ghostty's lazy Zig downloads are unreliable during parallel compilation.
# Fetch the complete upstream cache first, retrying transient network resets.
for attempt in 1 2 3; do
    if ./nix/build-support/fetch-zig-cache.sh; then
        break
    fi
    if [ "$attempt" -eq 3 ]; then
        exit 1
    fi
    echo "Retrying Zig dependency fetch ($attempt/3)"
    sleep "$attempt"
done


%build
# Ghostty's GTK frontend dynamically loads Fedora's Fontconfig, FreeType, and
# HarfBuzz. Link Ghostty against those same libraries instead of exporting
# symbols from bundled static copies into the process.
rm -rf "%{_builddir}/%{name}-install"
PATH="$PWD/.zig:$PATH" \
    ZIG_GLOBAL_CACHE_DIR="%{_builddir}/%{name}-zig-cache" \
    DESTDIR="%{_builddir}/%{name}-install" zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -fsys=fontconfig \
    -fsys=freetype \
    -fsys=harfbuzz \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Dstrip=false \
    -Demit-docs \
    -Demit-themes=true

%if 0%{?fedora} >= 42
    rm -f "%{_builddir}/%{name}-install%{_datadir}/terminfo/g/ghostty"
%endif

%install
cp -a "%{_builddir}/%{name}-install/." "%{buildroot}/"

# libghostty-vt is architecture-specific. Ghostty currently installs it below
# /usr/lib and puts its pkg-config metadata in /usr/share, so move both into
# Fedora's architecture-specific library directory.
install -d "%{buildroot}%{_libdir}/pkgconfig"
mv "%{buildroot}%{_prefix}/lib/libghostty-vt.so"* \
    "%{buildroot}%{_libdir}/"
mv "%{buildroot}%{_datadir}/pkgconfig/libghostty-vt.pc" \
    "%{buildroot}%{_libdir}/pkgconfig/"
sed -i 's|^libdir=.*|libdir=%{_libdir}|' \
    "%{buildroot}%{_libdir}/pkgconfig/libghostty-vt.pc"

%find_lang %{appid}

%check
%{buildroot}%{_bindir}/ghostty --version
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{appid}.desktop
appstreamcli validate --no-net \
    %{buildroot}%{_datadir}/metainfo/%{appid}.metainfo.xml
! ldd %{buildroot}%{_bindir}/ghostty | grep -F 'not found'

%files -f %{appid}.lang
%license LICENSE
%{_bindir}/ghostty
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty
%{_iconsdir}/hicolor/1024x1024/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128@2/apps/%{appid}.png
%{_iconsdir}/hicolor/16x16/apps/%{appid}.png
%{_iconsdir}/hicolor/16x16@2/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256@2/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32@2/apps/%{appid}.png
%{_iconsdir}/hicolor/512x512/apps/%{appid}.png
%{_datadir}/kio/servicemenus/%{appid}.desktop
%{_mandir}/man1/ghostty.1*
%{_mandir}/man5/ghostty.5*
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/compiler/ghostty.vim
%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim
%{_datadir}/vim/vimfiles/compiler/ghostty.vim
%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/systemd/user/app-%{appid}.service
%{_libdir}/libghostty-vt.so.0
%{_libdir}/libghostty-vt.so.0.1.0

%{_datadir}/terminfo/x/xterm-ghostty
%if 0%{?fedora} < 42
    %{_datadir}/terminfo/g/ghostty
%endif

%files devel
%{_prefix}/include/ghostty/vt.h
%{_prefix}/include/ghostty/vt/
%{_libdir}/libghostty-vt.so
%{_libdir}/pkgconfig/libghostty-vt.pc

%changelog
%autochangelog
