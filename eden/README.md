# Eden

[![⚡ Powered by COPR](https://img.shields.io/badge/⚡Powered%20by-COPR-blue?style=flat-square)](https://copr.fedorainfracloud.org/)
[![Copr build status](https://copr.fedorainfracloud.org/coprs/myriad-sun/lazarus/package/eden/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/myriad-sun/lazarus/package/eden/)

[![Latest Version](https://img.shields.io/badge/dynamic/json?color=blue&label=Version&query=builds.latest.source_package.version&url=https%3A%2F%2Fcopr.fedorainfracloud.org%2Fapi_3%2Fpackage%3Fownername%3Dmyriad-sun%26projectname%3Dlazarus%26packagename%3Deden%26with_latest_build%3DTrue&style=flat-square&logoColor=blue)](https://copr.fedorainfracloud.org/coprs/myriad-sun/lazarus/package/eden/)

## About Eden

Eden Emulator is a Nintendo Switch emulator derived from Yuzu and Sudachi, originally started by developer Camille LaVey.

This repository provides RPM packaging and distribution for Fedora systems through COPR.

## ⚠ Special Note

The build uses `ffmpeg-devel` from RPM Fusion Free. RPM Fusion Free must be enabled for the Fedora 44 COPR build chroots.

If installation reports missing FFmpeg dependencies, enable RPM Fusion Free on your system.

## Bug Reports

Issues related to the emulator itself should be reported directly to the Eden Emulator project:

<https://git.eden-emu.dev/eden-emu/eden/issues>

Issues related to installation, dependencies, COPR builds, or RPM packaging should be reported here:

<https://github.com/lost-saint/copr/issues>

## Installation

### 1. Enable the COPR Repository

```bash
sudo dnf copr enable myriad-sun/lazarus
```

### 2. Install Eden

```bash
sudo dnf install eden --refresh
```

## Updating

To update Eden alongside your normal system updates:

```bash
sudo dnf upgrade
```

## Uninstall

To remove Eden:

```bash
sudo dnf remove eden
```
