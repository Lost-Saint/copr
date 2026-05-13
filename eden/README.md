# Eden

[![⚡️ Powered by COPR](https://img.shields.io/badge/⚡️_Powered_by-COPR-blue?style=flat-square)](https://copr.fedorainfracloud.org/)
[![Build Status](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/package/eden/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/)

## ⚠️ Special Note

This package depends on ffmpeg-devel, which is provided via the RPM Fusion repository configured in this COPR build environment.

## About the Application

This is a package of the Eden Emulator. Eden Emulator is derived from Yuzu and Sudachi - started by developer Camille LaVey. It's written in C++

- Bugs related to Eden should be reported directly to the Eden Emulator repo:
  <https://git.eden-emu.dev/eden-emu/eden/issues>

- Bugs related to this package should be reported at this Git project:
  <https://github.com/lost-saint/copr/issues>

## Installation

1. Enable copr repo

```bash
sudo dnf copr enable myriad-sun/eden
```

- Substitute `dnf` for `yum` if desired

2. Install

```bash
sudo dnf install eden --refresh
```
