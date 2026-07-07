# Moonlight nightly COPR package

This is a source-only Fedora RPM package for the `master` branch of
[moonlight-stream/moonlight-qt](https://github.com/moonlight-stream/moonlight-qt).

`make-source.sh` clones the source recursively, preserving the four upstream
submodules, and produces two files in the output directory:

- `moonlight-nightly.spec`
- `moonlight-nightly-<commit>.tar.gz`

The generated spec builds the release target with Qt 6/qmake and installs only:

- `/usr/bin/moonlight`
- `/usr/share/applications/com.moonlight_stream.Moonlight.desktop`
- `/usr/share/icons/hicolor/scalable/apps/moonlight.svg`
- `/usr/share/metainfo/com.moonlight_stream.Moonlight.appdata.xml`
- License and README documentation through RPM metadata

No cache-update scriptlets are included; Fedora file triggers handle desktop,
icon, and AppStream cache updates.

## Generate a nightly source bundle

```bash
cd /copr/moonlight
./make-source.sh ./out
```

The generated source archive includes pinned submodule contents, so the RPM
build itself does not access the network.

## Build locally, then submit the SRPM to COPR

```bash
mkdir -p ~/rpmbuild/{SOURCES,SPECS}
cp out/moonlight-nightly-*.tar.gz ~/rpmbuild/SOURCES/
cp out/moonlight-nightly.spec ~/rpmbuild/SPECS/
rpmbuild -bs ~/rpmbuild/SPECS/moonlight-nightly.spec
copr-cli build <owner>/<project> ~/rpmbuild/SRPMS/moonlight-nightly-*.src.rpm
```

The COPR buildroot must make the listed `pkgconfig(libav*)` capabilities
available. Moonlight upstream explicitly notes that Fedora builds need RPM
Fusion for `ffmpeg-devel`; enable the appropriate additional repository for
your COPR project before building.
