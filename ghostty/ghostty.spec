# Signing key from https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
%global appid com.mitchellh.ghostty

Name:           ghostty
Version:        1.3.1
Release:        1%{?dist}
Summary:        A fast, native terminal emulator written in Zig.
License:        MIT AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0) AND Apache-2.0
URL:            https://ghostty.org/
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig


ExclusiveArch: x86_64 aarch64


BuildRequires: blueprint-compiler
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: glib2-devel
BuildRequires: gtk4-devel
BuildRequires: minisign
BuildRequires: gtk4-layer-shell-devel
BuildRequires: harfbuzz-devel
BuildRequires: libadwaita-devel
BuildRequires: libpng-devel
BuildRequires: oniguruma-devel
BuildRequires: pandoc-cli
BuildRequires: pixman-devel
BuildRequires: pkg-config
BuildRequires: wayland-protocols-devel
BuildRequires: zig
BuildRequires: zlib-ng-devel


Requires: fontconfig
Requires: freetype
Requires: glib2
Requires: gtk4
Requires: harfbuzz
Requires: libadwaita
Requires: libpng
Requires: oniguruma
Requires: pixman
Requires: zlib-ng


%description
👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

%package        devel
Summary:        Development files for libghostty-vt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package provides the development files for libghostty-vt.


%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%setup -n ghostty-%{version}

%build
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs \
    -Demit-themes=true

%if 0%{?fedora} >= 42
    rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%files -f %{appid}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_prefix}/share/applications/%{appid}.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/128x128/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/16x16/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/256x256/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/32x32/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/%{appid}.png
%{_prefix}/share/icons/hicolor/512x512/apps/%{appid}.png
%{_prefix}/share/kio/servicemenus/%{appid}.desktop
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}.5.gz
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/dbus-1/services/%{appid}.service
%{_prefix}/share/locale/*/LC_MESSAGES/%{appid}.mo
%{_prefix}/share/metainfo/%{appid}.metainfo.xml
%{_prefix}/share/systemd/user/app-%{appid}.service
%{_prefix}/lib/libghostty-vt.so.0
%{_prefix}/lib/libghostty-vt.so.0.1.0

%{_prefix}/share/terminfo/x/xterm-ghostty
%if 0%{?fedora} < 42
    %{_prefix}/share/terminfo/g/ghostty
%endif

%files devel
%{_prefix}/include/ghostty/vt.h
%{_prefix}/include/ghostty/vt/
%{_prefix}/lib/libghostty-vt.so
%{_prefix}/share/pkgconfig/libghostty-vt.pc

%changelog
%autochangelog
