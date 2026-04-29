Name:           zed
Version:        0.232.2
Release:        1%{?dist}
Summary:        High-performance multiplayer code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-only
URL:            https://github.com/zed-industries/zed
Source0:        https://github.com/zed-industries/zed/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  protobuf-compiler
BuildRequires:  openssl-devel
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  fontconfig-devel
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-loader-devel
BuildRequires:  zlib-devel
BuildRequires:  gettext

Requires:       vulkan-loader
Requires:       libxkbcommon%{?_isa}
Requires:       fontconfig%{?_isa}
Requires:       openssl-libs%{?_isa}
Requires:       alsa-lib%{?_isa}

Suggests:       gnome-keyring

%description
Zed is a high-performance, multiplayer code editor written in Rust by the
creators of Atom and Tree-sitter. It renders via GPU (Vulkan), providing
sub-millisecond input latency and instant startup. Supports X11 and Wayland.

%prep
%autosetup -n zed-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
export ZED_UPDATE_EXPLANATION="Use your system package manager to update Zed."

cargo build --release --locked --package zed --package cli

export APP_ID="dev.zed.Zed"
export APP_CLI="%{_bindir}/zed"
export APP_ICON="%{_datadir}/icons/hicolor/512x512/apps/dev.zed.Zed.png"
export APP_NAME="Zed"
envsubst < crates/zed/resources/zed.desktop.in > zed.desktop

%install
# CLI wrapper → /usr/bin/zed
install -Dm755 target/release/cli %{buildroot}%{_bindir}/zed

# Editor binary → /usr/libexec/zed-editor (CLI finds it here via relative path)
install -Dm755 target/release/zed %{buildroot}%{_libexecdir}/zed-editor

# Icons
for size in 16 32 48 128 256 512 1024; do
    icon="crates/zed/resources/app-icon-${size}.png"
    [ -f "$icon" ] || continue
    install -Dm644 "$icon" \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/dev.zed.Zed.png
done

# Desktop entry
install -Dm644 zed.desktop %{buildroot}%{_datadir}/applications/dev.zed.Zed.desktop

# Licenses
install -Dm644 LICENSE-AGPL   %{buildroot}%{_licensedir}/%{name}/LICENSE-AGPL
install -Dm644 LICENSE-APACHE %{buildroot}%{_licensedir}/%{name}/LICENSE-APACHE
install -Dm644 LICENSE-GPL    %{buildroot}%{_licensedir}/%{name}/LICENSE-GPL

%post
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license %{_licensedir}/%{name}/LICENSE-AGPL
%license %{_licensedir}/%{name}/LICENSE-APACHE
%license %{_licensedir}/%{name}/LICENSE-GPL
%doc README.md
%{_bindir}/zed
%{_libexecdir}/zed-editor
%{_datadir}/applications/dev.zed.Zed.desktop
%{_datadir}/icons/hicolor/*/apps/dev.zed.Zed.png

%changelog
* Tue Apr 29 2026 Your Name <you@example.com> - 0.232.2-1
- Initial COPR build
