%global blender_api 5.2
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global _without_bundled_deps 1

# Build conditionals
%bcond clang      0   # Use Clang compiler
%bcond draco      1   # Draco mesh compression support
%bcond fribidi    1   # Fribidi support
%bcond harfbuzz   1   # Harfbuzz support
%bcond llvm       1   # Required for OSL support
%bcond manifold   1   # Manifold support
%bcond manpage    1   # Generate manpage
%bcond materialx  1   # MaterialX support
%bcond nanovdb    1   # NanoVDB support
%bcond ninja      1   # Use Ninja build system
%bcond openvdb    1   # OpenVDB support
%bcond vulkan     1   # Vulkan rendering support

# Architecture-specific features
%ifarch x86_64 aarch64 ppc64le
%global cyclesflag ON
    # x86_64/aarch64 specific features
    %ifarch x86_64 aarch64
    %bcond embree 1   # Intel Embree ray tracing
    %bcond hidapi 1   # HIDAPI support

    # x86_64 exclusive features
    %ifarch x86_64
    %bcond hip   1    # AMD HIP support
    %bcond hiprt 0    # HIP ray tracing (requires Fedora 42+)
    %bcond oidn  1    # OpenImageDenoise
    %bcond oneapi 1   # Intel OneAPI support
    %bcond openshading 1  # OpenShadingLanguage support
    %bcond opgl  1    # OpenPGL
    %global llvm_compat 20
    %endif
    %bcond usd   1    # Universal Scene Description
%else
    %bcond embree 0
    %bcond hidapi 0
    %bcond oidn  0
    %bcond opgl  0
    %bcond usd   0
%endif
%else
%global cyclesflag OFF
%endif

Name:           blender
Epoch:          1
Version:        5.2.0
Release:        %autorelease

Summary:        3D modeling, animation, rendering and post-production
# Blender source is under GPL-2.0-or-later by default
# Apache-2.0 for Blender Cycles rendering engine
# BSD License for Open Shading Language
# Zlib License for Bullets
# GPL-3.0-or-later for the whole project
# https://www.blender.org/about/license/
License:	%{shrink:
		Apache-2.0 AND
  		BSD-3-Clause AND
  		GPL-2.0-or-later AND
  		GPL-3.0-or-later AND
  		Zlib
		}
URL:            https://www.blender.org

Source0:        https://download.%{name}.org/source/%{name}-%{version}.tar.xz
# Custom RPM macros
Source1:        %{name}-macros-source

# Build requirements
BuildRequires:  boost-devel
BuildRequires:  ccache
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  libharu-devel
BuildRequires:  subversion-devel

# Conditional build deps
%if %{with clang}
BuildRequires:  clang%{?llvm_compat}-devel
%endif
%if %{with llvm}
BuildRequires:  llvm%{?llvm_compat}-devel
%endif
%if %{with ninja}
BuildRequires:  ninja-build
%endif

# System libraries
BuildRequires:  mold
BuildRequires:  pkgconfig(blosc)
BuildRequires:  pkgconfig(eigen3)
BuildRequires:  pkgconfig(epoxy) >= 1.5.10
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(gmp)
%if %{with hidapi}
BuildRequires:  pkgconfig(hidapi-hidraw)
%endif
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libpcre2-32)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  pkgconfig(python3) >= 3.7
%if %{with vulkan}
BuildRequires:  pkgconfig(shaderc)
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xxf86vm)
# Required only for aarch64 architecture
%ifarch aarch64
BuildRequires:  sse2neon-devel
%endif

# Python stuff
BuildRequires:  python3dist(setuptools)
# In build_files/utils/make_bpy_wheel.py, the call to setuptools.setup has
# install_requires=["cython", "numpy", "requests", "zstandard"]; these are
# therefore both build-time and runtime dependencies.
BuildRequires:  python3dist(cattrs)
Requires:       python3dist(cattrs)
BuildRequires:  python3dist(cython)
Requires:       python3dist(cython)
BuildRequires:  python3dist(numpy)
Requires:       python3dist(numpy)
BuildRequires:  python3dist(requests)
Requires:       python3dist(requests)
BuildRequires:  python3dist(zstandard)
Requires:       python3dist(zstandard)
# In source/creator/CMakeLists.txt, an attempt is made to add direct
# dependencies on certifi, (chardet or charset_normalizer), idna, and urllib3,
# as indirect dependencies that enable necessary functionality in requests. As
# packaged, requests already has a hard dependency on charset_normalizer, idna,
# and urllib3 â€“ and it would depend on certifi, but this is correctly patched
# out in favor of explicitly and unconditional using the system certificate
# bundle. We therefore do not need to add direct dependencies on any of the
# above.
#
# Many Python scripts that are installed, especially from the add-ons, depend
# on various external Python packages. As far as we know, there is no clear
# listing of these that we can use as a reference to generate depdendencies
# automatically. A listing appears in PYTHON_SUBPACKAGES in
# build_files/build_environment/install_linux_packages.py, but the entries are
# redundant with those appearing above.
#
# Some dependencies can be found easily because they are required for testing;
# others may be less obvious. In general, each should be both a BuildRequires
# (even if not used in testing, to avoid accidentally building a Blender
# package that builds from source but fails to install due to an unsatisfied
# Requires) and a Requires (so users are not faced with â€œNo module named '...'â€
# errors).
#
# Something like this can help search for possible dependencies:
#
# rpm2cpio blender-4.1.1-1.fc40.x86_64.rpm | pax -r
# p='^[[:blank:]]*(from[[:blank:]]+[^[:blank:]]+[[:blank:]]+)?import\b'
# rg -I -g '*.py' "${p}" ./usr | awk '{print $2}' | grep -vE '^\.' | sort -u |
#   tee imports.txt
#
# This is an imperfect heuristic, but the result is generally a list of
# absolute imports that might reflect external dependencies. Some come from
# Blender; many come from the Python standard library. Those that remain are
# candidates for this list.
#
# The ant_landscape add-on has a weak dependency (used only if available) on
# numexpr; so does the mesh_tissue add-on.
BuildRequires:  python3dist(numexpr)
Recommends:     python3dist(numexpr)
# The ant_landscape add-on has a weak dependency on psutil.
BuildRequires:  python3dist(psutil)
Recommends:     python3dist(psutil)
#
# The mesh_tissue add-on has a weak dependency on numba. Numba is not packaged
# for Fedora, and probably never will be, because it is tied closely to the
# implementation details of a particular Python interpreter version, and can
# take six months to a year to support a new Python release.
# BuildRequires:  python3dist(numba)
# Recommends:     python3dist(numba)
# Only if numba is not available (see above), the mesh_tissue add-on falls back
# to using ensurepip to install pip, and then using pip to try to install numba
# from PyPI into the user site-packages. This *might* work. It is probably
# better if pip is already available.
BuildRequires:  python3dist(pip)
Recommends:     python3dist(pip)
#
# The io_mesh_uv_layout add-on has a weak dependency on OpenImageIO. Currently,
# the OpenImageIO package does not produce the necessary Python metadata for a
# dependency on python3dist(openimageio) to work.
BuildRequires:  python3-openimageio
Recommends:     python3-openimageio
#
# The io_export_dxf add-on requires pydevd (PyDev.Debugger,
# https://pypi.org/project/pydevd/) for debugging when the BLENDER_DEBUG
# environment variable is set. Since this is a debug-only dependency, we would
# choose not to add it even if it were packaged.
#
# The io_import_dxf add-on has a weak dependency on pyproj.
BuildRequires:  python3dist(pyproj)
Recommends:     python3dist(pyproj)
#
# %%{_datadir}/blender/%%{blender_api}/scripts/modules/bl_i18n_utils/utils_spell_check.py
# has "import enchant", but we judge that these scripts are really for people
# working on the translations, and should not be required in normal uses of the
# RPM package.

# Compression stuff
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(lzo2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)

# 3D modeling stuff
BuildRequires:  cmake(ceres)
BuildRequires:  flexiblas-devel
%if %{with embree}
BuildRequires:  embree-devel
%endif
%if %{with manifold}
BuildRequires:	pkgconfig(manifold)
BuildRequires:  polyclipping2-devel
%endif
%if %{with materialx}
BuildRequires:  cmake(materialx)
BuildRequires:  materialx-data
BuildRequires:  python3-materialx
%endif
BuildRequires:  metis-devel
BuildRequires:  opensubdiv-devel >= 3.4.4
%if %{with openshading}
# Use oslc compiler
BuildRequires:  OpenImageIO-plugin-osl
BuildRequires:  openshadinglanguage-common-headers >= 1.12.6.2
BuildRequires:  pkgconfig(oslcomp)
%endif
%if %{with oidn}
BuildRequires:  cmake(OpenImageDenoise)
%endif
%if %{with opgl}
BuildRequires:  openpgl-devel
%endif
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(ftgl)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  openxr-libs
BuildRequires:  pkgconfig(openxr)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(ode)
%if %{with usd}
BuildRequires:  usd-devel
%endif
BuildRequires:  pkgconfig(xproto)

# Picture/Video stuff
BuildRequires:  cmake(Alembic)
BuildRequires:  ffmpeg-free-devel >= 5.1.2
BuildRequires:  lame-devel
BuildRequires:  libspnav-devel
%if %{with nanovdb}
BuildRequires:  openvdb-nanovdb-devel
%endif
%if %{with openvdb}
BuildRequires:  openvdb-devel
%endif
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libheif)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(openjph)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(thorvg-1)
BuildRequires:  pkgconfig(vpx)
# OpenColorIO 2 and up required
BuildRequires:  cmake(OpenColorIO) > 1
BuildRequires:  cmake(Imath)
BuildRequires:  cmake(OpenEXR)
BuildRequires:  cmake(OpenImageIO) >= 2.5.0.0
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(tbb)
BuildRequires:  potrace-devel

# Audio stuff
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(freealut)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(vorbis)

# Typography stuff
BuildRequires:  fontpackages-devel
%if %{with fribidi}
BuildRequires:  pkgconfig(fribidi)
%endif
BuildRequires:  pkgconfig(freetype2)
%if %{with harfbuzz}
BuildRequires:  pkgconfig(harfbuzz)
%endif
BuildRequires:  pkgconfig(tinyxml)
# Appstream stuff
BuildRequires:  libappstream-glib

# HIP stuff
# https://developer.blender.org/docs/handbook/building_blender/cycles_gpu_binaries/#linux
%if %{with hip}
%if %{with hiprt}
BuildRequires:  hiprt-devel
%endif
BuildRequires:	hipcc
BuildRequires:  rocm-core
BuildRequires:  rocm-device-libs
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
%endif

# OneAPI stuff
%if %{with oneapi}
BuildRequires:  intel-level-zero-gpu-raytracing
BuildRequires:  pkgconfig(level-zero)
BuildRequires:  pkgconfig(vpl)
%endif

Requires:       hicolor-icon-theme
Requires:       rsms-inter-fonts
Requires:       shared-mime-info
Provides:       blender(ABI) = %{blender_api}

# Starting from 2.90, Blender supports only 64-bits architectures
# Starting from 5.0.0, Blender dropped big endian support impacting s390x arch
# https://projects.blender.org/blender/blender/commit/bc80ef136e8af0a355d234205ed6c7b0acaa84ab
ExcludeArch:	%{ix86} %{arm} s390x

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

%package rpm-macros
Summary:        RPM macros for third-party blender addons
BuildArch:      noarch

%description rpm-macros
Provides RPM macros for creating third-party addon packages for Blender.

%prep
%autosetup -p1

# System integration fixes
rm -f build_files/cmake/Modules/FindOpenJPEG.cmake
%py3_shebang_fix .
sed -i "s/date_time/date_time python%{python3_version_nodots}/" \
        build_files/cmake/platform/platform_unix.cmake

# Fix clog format
# Incorrect format from upstream 5.1 branch
# https://projects.blender.org/blender/blender/src/commit/b70da489d7f4eae7760cc0a50cc6c60cd5464205/source/blender/gpu/vulkan/vk_texture_pool.cc#L559
#
# Correct format from upstream main branch
# https://projects.blender.org/blender/blender/src/commit/402799c1d9706b1bced1008680ceace9a8434c68/source/blender/gpu/vulkan/vk_texture_pool.cc#L558
sed -i 's/CLOG_TRACE(&LOG, log_message\.c_str());/CLOG_TRACE(\&LOG, "%s", log_message.c_str());/' \
        source/blender/gpu/vulkan/vk_texture_pool.cc

%build
%if %{with hip}
export HIP_PATH=`hipconfig -p`
export HIP_CLANG_PATH=`hipconfig -l`
%endif

%cmake \
%if %{with ninja}
    -G Ninja \
%endif
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_SKIP_RPATH=ON \
    -DPYTHON_VERSION=%{python3_version} \
    -DWITH_COMPILER_CCACHE=ON \
    -DWITH_CYCLES=%{cyclesflag} \
    -DWITH_CYCLES_EMBREE=%{?with_embree:ON}%{!?with_embree:OFF} \
    -DWITH_INSTALL_PORTABLE=OFF \
    -DWITH_PYTHON_INSTALL=OFF \
%if %{with fribidi}
    -DWITH_FRIBIDI=ON \
%endif
%if %{with harfbuzz}
    -DWITH_HARFBUZZ=ON \
%endif
%if %{with manpage}
    -DWITH_DOC_MANPAGE=ON \
%endif
%if %{with materialx}
    -DWITH_MATERIALX=ON \
%else
    -DWITH_MATERIALX=OFF \
%endif
%if %{with openshading}
    -DOSL_COMPILER=%{_bindir}/oslc \
%endif
%if %{with usd}
    -DUSD_LIBRARY=%{_libdir}/libusd_ms.so \
%else
    -DWITH_USD=OFF \
%endif
    -D_ffmpeg_INCLUDE_DIR=$(pkg-config --variable=includedir libavformat) \
    -DEMBREE_INCLUDE_DIR=%{_includedir} \
    -DXR_OPENXR_SDK_LOADER_LIBRARY=%{_libdir}/libopenxr_loader.so.1 \
%if %{with hip}
    -DHIP_HIPCC_EXECUTABLE=%{_bindir}/hipcc \
    -DWITH_CYCLES_HIP_BINARIES=ON \
%if %{with hiprt}
    -DWITH_CYCLES_DEVICE_HIPRT=ON \
%endif
%endif
%if %{with oneapi}
    -DWITH_CYCLES_DEVICE_ONEAPI=ON \
    -DWITH_CYCLES_ONEAPI_BINARIES=ON \
%endif
    -DWITH_OPENCOLLADA=OFF \
    -DWITH_LIBS_PRECOMPILED=OFF \
    -DWITH_SYSTEM_GLOG=ON \
    -W no-dev

%cmake_build

%install
%cmake_install

# Additional installs
mkdir -p %{buildroot}%{macrosdir}
install -pm 644 %{SOURCE1} %{buildroot}%{macrosdir}/macros.%{name}
sed -i 's/@VERSION@/%{blender_api}/g' %{buildroot}%{macrosdir}/macros.%{name}

# Metainfo
install -p -m 644 -D release/freedesktop/org.%{name}.Blender.metainfo.xml \
          %{buildroot}%{_metainfodir}/org.%{name}.Blender.metainfo.xml

# Localization and cleanup
%fdupes %{buildroot}%{_datadir}/%{name}/%{blender_api}/
%find_lang %{name}
find %{buildroot}%{_datadir}/%{name}/%{blender_api}/scripts -name "*.py" -exec chmod 755 {} \;
rm -rf %{buildroot}%{_docdir}/%{name}/*

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.%{name}.Blender.metainfo.xml

%files -f %{name}.lang
%license COPYING doc/license/*-license.txt release/text/copyright.txt
%doc release/text/readme.html
%{_bindir}/%{name}{,-thumbnailer}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/%{blender_api}/
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_metainfodir}/org.%{name}.Blender.metainfo.xml
%{?with_manpage:%{_mandir}/man1/%{name}.*}

%files rpm-macros
%{macrosdir}/macros.%{name}

%changelog
%autochangelog
