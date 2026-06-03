# myriad-sun/lazarus

A personal COPR repository providing up-to-date and community-maintained packages for Fedora.

## Packages

| Package         | Description                                                 |
| --------------- | ----------------------------------------------------------- |
| **eden**        | A Switch Emulator                                           |
| **ghostty**     | A fast, feature-rich terminal emulator                      |
| **kew**         | A terminal music player                                     |
| **lutris**      | Open gaming platform for Linux                              |
| **zed**         | High-performance code editor (x86_64 & aarch64)             |
| **zen-browser** | Privacy-focused browser based on Firefox (x86_64 & aarch64) |

---

## Installation

### 1. Enable the repository

```bash
sudo dnf copr enable myriad-sun/lazarus
```

### 2. Install a package

```bash
sudo dnf install <package-name>
```

For example:

```bash
sudo dnf install ghostty
sudo dnf install zed
sudo dnf install lutris
```

---

## Uninstallation

### 1. Remove a package

```bash
sudo dnf remove <package-name>
```

For example:

```bash
sudo dnf remove ghostty
sudo dnf remove zed
sudo dnf remove lutris
```

### 2. Disable or remove the repository

```bash
# Disable (keeps repo file but won't pull updates)
sudo dnf copr disable myriad-sun/lazarus

# Remove entirely
sudo dnf copr remove myriad-sun/lazarus
```
