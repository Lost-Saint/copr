# copr

A collection of Fedora COPR repositories for apps that aren't in the official Fedora repos, are out of date there, or just work better built fresh. Feel free to use any of them!

> [!WARNING]
> These repos are maintained primarily for personal use, so don't expect a strict release schedule. That said, if something breaks for you, feel free to open an issue!

## Packages

| Package | Description | Install |
|---------|-------------|---------|
| [android-studio](https://copr.fedorainfracloud.org/coprs/myriad-sun/android-studio/) | Google's official IDE for Android development | `dnf copr enable myriad-sun/android-studio` |
| [easyeffects](https://copr.fedorainfracloud.org/coprs/myriad-sun/easyeffects/) | Audio effects and equalizer for PipeWire | `dnf copr enable myriad-sun/easyeffects` |
| [eden](https://copr.fedorainfracloud.org/coprs/myriad-sun/eden/) | Nintendo Switch emulator | `dnf copr enable myriad-sun/eden` |
| [ghostty](https://copr.fedorainfracloud.org/coprs/myriad-sun/ghostty/) | Fast, feature-rich terminal emulator | `dnf copr enable myriad-sun/ghostty` |
| [lutris-git](https://copr.fedorainfracloud.org/coprs/myriad-sun/lutris-git/) | Latest git builds of the Lutris game manager | `dnf copr enable myriad-sun/lutris-git` |
| [zed](https://copr.fedorainfracloud.org/coprs/myriad-sun/zed/) | High-performance, multiplayer code editor | `dnf copr enable myriad-sun/zed` |
| [zen-browser](https://copr.fedorainfracloud.org/coprs/myriad-sun/zen-browser/) | Firefox-based browser focused on privacy and UX | `dnf copr enable myriad-sun/zen-browser` |

## Usage

Enabling a repo and installing a package is two commands:

```bash
sudo dnf copr enable myriad-sun/<repo-name>
sudo dnf install <package-name>
```

For example, to install Ghostty:

```bash
sudo dnf copr enable myriad-sun/ghostty
sudo dnf install ghostty
```

To disable a repo you no longer want:

```bash
sudo dnf copr disable myriad-sun/<repo-name>
```

## Supported Releases

Each repo targets recent Fedora releases. Check the individual repo pages on [COPR](https://copr.fedorainfracloud.org/coprs/myriad-sun/) for the exact list of supported versions.

## Issues

Something broken or out of date? [Open an issue](https://github.com/Lost-Saint/copr/issues) and I'll take a look when I can. Bug reports are always welcome!
