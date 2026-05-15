# Eden

[![⚡ Powered by COPR](https://img.shields.io/badge/Powered%20by-COPR-blue?style=flat-square)](https://copr.fedorainfracloud.org/)
[![Build Status](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/package/eden/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/)

[![Latest Version](https://img.shields.io/badge/dynamic/json?color=blue&label=Version&query=builds.latest.source_package.version&url=https%3A%2F%2Fcopr.fedorainfracloud.org%2Fapi_3%2Fpackage%3Fownername%3Dmyriad-sun%26projectname%3Deden%26packagename%3Deden%26with_latest_build%3DTrue&style=flat-square&logoColor=blue)](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/package/eden/)

## About Eden

Eden Emulator is a Nintendo Switch emulator derived from Yuzu and Sudachi, originally started by developer Camille LaVey.

This repository provides RPM packaging and distribution for Fedora systems through COPR.

## ⚠ Special Note

This package depends on `ffmpeg-devel`, which is provided through RPM Fusion in the COPR build environment.

If you encounter dependency-related issues, ensure RPM Fusion is enabled on your system.

## Bug Reports

Issues related to the emulator itself should be reported directly to the Eden Emulator project:

<https://git.eden-emu.dev/eden-emu/eden/issues>

Issues related to installation, dependencies, COPR builds, or RPM packaging should be reported here:

<https://github.com/lost-saint/copr/issues>

## Installation

### 1. Enable the COPR Repository

```bash
sudo dnf copr enable myriad-sun/eden
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

## Links

- COPR Repository
  [https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/)

- Eden Emulator
  [https://git.eden-emu.dev/eden-emu/eden](https://git.eden-emu.dev/eden-emu/eden)
