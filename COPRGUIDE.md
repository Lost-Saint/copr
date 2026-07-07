# COPR Guide

Quick reference for the `myriad-sun/lazarus` COPR repository.

## Current Status

- COPR project: <https://copr.fedorainfracloud.org/coprs/myriad-sun/lazarus/>
- Current published chroots: Fedora 44 `x86_64` and `aarch64`
- CI/build target config in this repo: Fedora 43 and Fedora 44
- Build dependency note: the COPR project has RPM Fusion Free configured as an additional build repository.

## Install

Enable the COPR repository, then install the package.

```bash
sudo dnf install dnf-plugins-core
sudo dnf copr enable myriad-sun/lazarus
sudo dnf install <package-name> --refresh
```

## Packages

| Package | What it is | Notes |
| --- | --- | --- |
| `android-studio` | Google's official IDE for Android development | `x86_64` |
| `cava` | Terminal audio visualizer |  |
| `easyeffects` | Audio effects and equalizer for PipeWire |  |
| `eden` | Nintendo Switch emulator | Needs RPM Fusion Free available on the client system |
| `ghostty` | Fast, feature-rich terminal emulator |  |
| `kew` | Terminal music player |  |
| `lutris` | Game manager built from the `lutris-git` spec | Install package name is `lutris` |
| `moonlight-nightly` | Nightly Moonlight game-streaming client | Needs RPM Fusion Free available on the client system |
| `zed` | Zed editor for `x86_64` |  |
| `zed-aarch64` | Zed editor for `aarch64` | Architecture-specific package name |
| `zen-browser` | Zen Browser for `x86_64` |  |
| `zen-browser-aarch64` | Zen Browser for `aarch64` | Architecture-specific package name |

`gtk4-layer-shell` is also published in the COPR project, but it is a support
package used by Ghostty rather than a normal end-user app.

## Examples

Install Ghostty:

```bash
sudo dnf copr enable myriad-sun/lazarus
sudo dnf install ghostty --refresh
```

Install Zed on `aarch64`:

```bash
sudo dnf copr enable myriad-sun/lazarus
sudo dnf install zed-aarch64 --refresh
```

Install Moonlight nightly:

```bash
sudo dnf copr enable myriad-sun/lazarus
sudo dnf install moonlight-nightly --refresh
```

## RPM Fusion

Eden and Moonlight need RPM Fusion Free for FFmpeg-related packages. If those
dependencies do not resolve, enable RPM Fusion Free on the client system:

```bash
sudo dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
```

## Update

Update packages normally with the rest of the system:

```bash
sudo dnf upgrade --refresh
```

## Uninstall

Remove packages first, then disable or remove the COPR repository.

```bash
sudo dnf remove <package-name>
sudo dnf copr disable myriad-sun/lazarus
```

To remove the repo file entirely:

```bash
sudo dnf copr remove myriad-sun/lazarus
```

## References

- COPR enable command: <https://docs.pagure.org/copr.copr/how_to_enable_repo.html>
- COPR project API: <https://copr.fedorainfracloud.org/api_3/project?ownername=myriad-sun&projectname=lazarus>
- COPR package API: <https://copr.fedorainfracloud.org/api_3/package/list?ownername=myriad-sun&projectname=lazarus>
- RPM Fusion setup: <https://docs.fedoraproject.org/en-US/quick-docs/rpmfusion-setup/>
- Fedora release EOL list: <https://docs.fedoraproject.org/en-US/releases/eol/>
