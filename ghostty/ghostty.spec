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

BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  minisign
BuildRequires:  libadwaita-devel
BuildRequires:  libX11-devel
BuildRequires:  pandoc-cli
BuildRequires:  systemd-rpm-macros
BuildRequires:  zig >= 0.14.0
BuildRequires:  zig-rpm-macros
BuildRequires:  pkgconfig(blueprint-compiler)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(zlib)
Requires: gtk4
Requires: gtk4-layer-shell
Requires: libadwaita
Conflicts: ghostty-nightly

%description
👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

%package devel
Summary: Development files for libghostty-vt
Requires: %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package includes the development files for Ghostty.

%package        shell-integration
Summary:        Ghostty shell integration
Supplements:    %{name}
BuildArch:      noarch

%description    shell-integration
This package contains files allowing Ghostty to integrate with various shells.

%package -n     libghostty-vt
Summary:        The libghostty-vt libraries

%description -n libghostty-vt
This package contains the libghostty-vt libraries, the first of many libghostty libaries in development.

%package -n     libghostty-vt-devel
Summary:        Development files for libghostty-vt
Requires:       libghostty-vt = %{version}-%{release}

%description -n libghostty-vt-devel
This package contains the libraries and header files that are needed for developing with libghostty-vt.

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%autosetup -n ghostty-%{version}

ZIG_GLOBAL_CACHE_DIR="%{_zig_cache_dir}" ./nix/build-support/fetch-zig-cache.sh

%build

%install
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" --prefix-lib-dir "%{_libdir}" \
    --prefix-exe-dir "%{_bindir}" --prefix-include-dir "%{_includedir}" \
    -Dversion-string="%{version}-%{release}" \
    -Dstrip=false \
    -Doptimize=ReleaseFast \
    -Dpie=true \
    -Demit-docs \
    -Demit-themes=false

# Don't conflict with ncurses-term on F42 and up
%if 0%{?fedora} >= 42
    rm -rf %{buildroot}%{_datadir}/terminfo/g/%{name}
%endif

%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_iconsdir}/hicolor/16x16/apps/%{appid}.png
%{_iconsdir}/hicolor/16x16@2/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32/apps/%{appid}.png
%{_iconsdir}/hicolor/32x32@2/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128/apps/%{appid}.png
%{_iconsdir}/hicolor/128x128@2/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256/apps/%{appid}.png
%{_iconsdir}/hicolor/256x256@2/apps/%{appid}.png
%{_iconsdir}/hicolor/512x512/apps/%{appid}.png
%{_iconsdir}/hicolor/1024x1024/apps/%{appid}.png
%{_datadir}/kio/servicemenus/%{appid}.desktop
%{_mandir}/man1/%{name}.1
%{_mandir}/man5/%{name}.5
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
%{_datadir}/locale/*/LC_MESSAGES/%{appid}.mo
%{_datadir}/systemd/user/app-%{appid}.service

%files devel
%{_includedir}/ghostty/

%files shell-integration
%{_datadir}/%{name}/shell-integration/

%if 0%{?fedora} < 42
    %{_datadir}/terminfo/g/%{name}
%endif
%{_datadir}/terminfo/x/xterm-ghostty

%files -n libghostty-vt
%{_libdir}/libghostty-vt.so.*

%files -n libghostty-vt-devel
%{_libdir}/libghostty-vt.so
%{_datadir}/pkgconfig/libghostty-vt.pc

%changelog
%autochangelog
