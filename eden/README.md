````markdown
# Eden (COPR Build)

Eden is an experimental open-source Nintendo Switch emulator focused on performance and stability.

---

## ⚠️ Requirement

This build requires **RPM Fusion Free repository**.

---

## 📦 Install from COPR

Enable the COPR repository:

```bash
sudo dnf copr enable myriad-sun/eden
```
````

Install Eden:

```bash
sudo dnf install eden --refresh
```

---

## 🛠️ About

This package builds Eden Emulator using system libraries, Qt6, and Vulkan, with optional performance optimizations like LTO and PGO.

---

## 💡 Notes

- Works on Fedora and other RPM-based systems
- Supports x86_64 and aarch64
- Built with modern toolchain (CMake + Ninja + LLVM)
- Tests are disabled in this build
