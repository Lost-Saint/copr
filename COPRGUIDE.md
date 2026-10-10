# COPR Guide

Quick reference for the `myriad-sun/lazarus` COPR repository.

## Current Status

- COPR project: <https://copr.fedorainfracloud.org/coprs/myriad-sun/lazarus/>
- Current published chroots: Fedora 43–45 and Rawhide
- CI/build target config in this repo: Fedora 43–45

## Install

Enable the COPR repository, then install the package.

```bash
sudo dnf install dnf-plugins-core
sudo dnf copr enable myriad-sun/lazarus
sudo dnf install <package-name> --refresh
```

## Packages

| Package               | What it is                                    | Notes                                                |
| --------------------- | --------------------------------------------- | ---------------------------------------------------- |
| `android-studio`      | Google's official IDE for Android development | `x86_64`                                             |
| `cava`                | Terminal audio visualizer                     |                                                      |
| `designcraft`         | Page layout and publishing app                 | `x86_64`, `aarch64`                                  |
| `easyeffects`         | Audio effects and equalizer for PipeWire      |                                                      |
| `eden`                | Nintendo Switch emulator                      |                                                      |
| `effectcraft`         | Motion graphics and visual effects app         | `x86_64`, `aarch64`                                  |
| `filmcraft`           | Video editor                                  | `x86_64`, `aarch64`                                  |
| `ghostty`             | Fast, feature-rich terminal emulator          |                                                      |
| `kew`                 | Terminal music player                         |                                                      |
| `lightcraft`          | Photo library and RAW developer                | `x86_64`, `aarch64`                                  |
| `lutris`              | Game manager built from the `lutris-git` spec | Install package name is `lutris`                     |
| `moonlight-nightly`   | Nightly Moonlight game-streaming client       |                                                      |
| `pdfcraft`            | PDF workbench                                 | `x86_64`, `aarch64`                                  |
| `photocraft`          | Raster image editor                           | `x86_64`, `aarch64`                                  |
| `vectorcraft`         | Vector illustration app                       | `x86_64`, `aarch64`                                  |
| `zed`                 | Zed editor for `x86_64`                       |                                                      |
| `zed-aarch64`         | Zed editor for `aarch64`                      | Architecture-specific package name                   |
| `zen-browser`         | Zen Browser for `x86_64`                      |                                                      |
| `zen-browser-aarch64` | Zen Browser for `aarch64`                     | Architecture-specific package name                   |

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
- Fedora release EOL list: <https://docs.fedoraproject.org/en-US/releases/eol/>
