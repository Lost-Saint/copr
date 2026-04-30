Name:           zed
Version:        1.0.0
Release:        1%{?dist}
Summary:        Zed is a high-performance, multiplayer code editor

License:        ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND ((MIT OR Apache-2.0) AND Unicode-3.0) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 AND ISC) AND AGPL.3.0-only AND AGPL-3.0-or-later AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception) AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR MIT OR Apache-2.0) AND BSD-2-Clause AND (CC0-1.0 OR Apache-2.0 OR Apache-2.0 WITH LLVM-exception) AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND CC0-1.0 AND GPL-3.0-or-later AND (ISC AND (Apache-2.0 OR ISC) AND OpenSSL) AND (ISC AND (Apache-2.0 OR ISC)) AND ISC AND (MIT AND (MIT OR Apache-2.0)) AND (MIT AND BSD-3-Clause) AND (MIT OR Apache-2.0 OR CC0-1.0) AND (MIT OR Apache-2.0 OR NCSA) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND MIT AND MPL-2.0 AND Unicode-3.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT) AND Zlib

URL:            https://zed.dev/
Source0:        https://github.com/zed-industries/zed/releases/download/v%{version}/zed-linux-x86_64.tar.gz

BuildRequires:  tar

ExclusiveArch:  x86_64

%global debug_package %{nil}

# Verified via ldd zed.app/libexec/zed-editor - these resolve from /lib64 (system)
# Everything else resolves from the bundled zed.app/lib/
Requires:       glibc%{?_isa}
Requires:       libgcc%{?_isa}
Requires:       libstdc++%{?_isa}
Requires:       alsa-lib%{?_isa}
# Loaded at runtime via dlopen, not visible in ldd
Requires:       vulkan-loader%{?_isa}

Suggests:       gnome-keyring

%description
Code at the speed of thought - Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.

This package installs the official prebuilt binary from the Zed project.

%prep
%autosetup -n zed.app -p1

%build
# nothing to build

%install
# CLI wrapper
install -Dm755 bin/zed %{buildroot}%{_bindir}/zed

# Editor binary (CLI finds it via relative path ../libexec/zed-editor)
install -Dm755 libexec/zed-editor %{buildroot}%{_libexecdir}/zed-editor

# Bundled libraries
install -dm755 %{buildroot}%{_libdir}/zed
cp -a lib/. %{buildroot}%{_libdir}/zed/

# Icons
install -Dm644 share/icons/hicolor/512x512/apps/zed.png \
               %{buildroot}%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed.png
install -Dm644 share/icons/hicolor/1024x1024/apps/zed.png \
               %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed.png

# Desktop entry
install -dm755 %{buildroot}%{_datadir}/applications
sed 's|Icon=zed|Icon=dev.zed.Zed|g' share/applications/dev.zed.Zed.desktop \
    > %{buildroot}%{_datadir}/applications/dev.zed.Zed.desktop

# License
install -Dm644 licenses.md %{buildroot}%{_licensedir}/%{name}/licenses.md

%post
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache -f -t %{_iconsdir}/hicolor &>/dev/null || :

%files
%license %{_licensedir}/%{name}/licenses.md
%{_bindir}/zed
%{_libexecdir}/zed-editor
%{_libdir}/zed/
%{_datadir}/applications/dev.zed.Zed.desktop
%{_iconsdir}/hicolor/512x512/apps/dev.zed.Zed.png
%{_iconsdir}/hicolor/1024x1024/apps/dev.zed.Zed.png

%changelog
%autochangelog
