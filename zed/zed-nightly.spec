Name:           zed-nightly
Version:        nightly
Release:        1%{?dist}
Summary:        Zed – a fast, collaborative code editor (nightly build)

License:        GPL-3.0-only AND Apache-2.0
URL:            https://github.com/zed-industries/zed

# Source is the nightly tag tarball from GitHub
Source0:        https://github.com/zed-industries/zed/archive/refs/tags/nightly.tar.gz#/zed-%{version}.tar.gz

# Zed is Rust-only — no debug package, no automatic dependency provides from C
%define debug_package %{nil}

BuildArch:      x86_64 aarch64

# ── Build-time dependencies ──────────────────────────────────────────────────
BuildRequires:  rust cargo
BuildRequires:  gcc gcc-c++ clang cmake make lld
BuildRequires:  musl-libc-static musl-gcc
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  vulkan-loader-devel
BuildRequires:  gettext
BuildRequires:  git

# ── Runtime dependencies ─────────────────────────────────────────────────────
Requires:       vulkan-loader
Requires:       libva
Requires:       fontconfig
Requires:       alsa-lib
Requires:       wayland-devel
Requires:       pipewire
Requires:       xdg-desktop-portal

# Can't co-exist with the stable zed package
Conflicts:      zed

%description
Zed is a high-performance, multiplayer code editor built in Rust.
This package tracks the nightly release channel and is built from source.


# ── Prep ─────────────────────────────────────────────────────────────────────
%prep
%autosetup -n zed-%{version}

# Mark this build as nightly (no trailing newline, as Zed requires)
printf 'nightly' > crates/zed/RELEASE_CHANNEL

# Tell Zed not to offer auto-updates (the package manager handles that)
export ZED_UPDATE_EXPLANATION="Use your package manager to update Zed Nightly."


# ── Build ─────────────────────────────────────────────────────────────────────
%build
# Point cargo output to a local dir so rpmbuild doesn't try to write to HOME
export CARGO_HOME="%{_builddir}/cargo-home"

# Use lld for faster linking
export RUSTFLAGS="-C link-arg=-fuse-ld=lld"

# Build the CLI wrapper (goes in $PATH as 'zed')
cargo build --release -p cli

# Build the actual editor binary (goes in libexec)
cargo build --release -p zed


# ── Install ──────────────────────────────────────────────────────────────────
%install
rm -rf %{buildroot}

# CLI wrapper — this is what the user runs
install -Dm755 target/release/cli \
    %{buildroot}%{_bindir}/zed-nightly

# Real editor binary — must live at ../../libexec relative to the CLI binary
# i.e. /usr/libexec/zed-editor-nightly when CLI is at /usr/bin/zed-nightly
install -Dm755 target/release/zed \
    %{buildroot}%{_libexecdir}/zed-editor-nightly

# .desktop file — populate the template with nightly values, then install
APP_NAME="Zed Nightly" \
APP_CLI=zed-nightly \
APP_ICON=dev.zed.Zed-Nightly \
APP_ARGS="%U" \
DO_STARTUP_NOTIFY=true \
envsubst < crates/zed/resources/zed.desktop.in \
    > %{_builddir}/dev.zed.Zed-Nightly.desktop

install -Dm755 %{_builddir}/dev.zed.Zed-Nightly.desktop \
    %{buildroot}%{_datadir}/applications/dev.zed.Zed-Nightly.desktop

# App icon (use the nightly-specific one from resources)
install -Dm644 crates/zed/resources/app-icon-nightly.png \
    %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/dev.zed.Zed-Nightly.png

# Licence
install -Dm644 LICENSE-GPL %{buildroot}%{_datadir}/licenses/%{name}/LICENSE-GPL
install -Dm644 LICENSE-APACHE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE-APACHE


# ── Post-install / post-uninstall hooks ──────────────────────────────────────
%post
/usr/bin/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :


# ── File manifest ─────────────────────────────────────────────────────────────
%files
%license %{_datadir}/licenses/%{name}/LICENSE-GPL
%license %{_datadir}/licenses/%{name}/LICENSE-APACHE
%{_bindir}/zed-nightly
%{_libexecdir}/zed-editor-nightly
%{_datadir}/applications/dev.zed.Zed-Nightly.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/dev.zed.Zed-Nightly.png


# ── Changelog ────────────────────────────────────────────────────────────────
%changelog
%autochangelog
