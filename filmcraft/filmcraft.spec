%global debug_package %{nil}

Name:           filmcraft
Version:        0.5.0
Release:        1%{?dist}
Summary:        Native video editor

License:        (MIT OR Apache-2.0) AND OFL-1.1
URL:            https://getartcraft.com/apps/filmcraft
Source0:        https://github.com/storytold/filmcraft/releases/download/v%{version}/filmcraft-%{version}-linux-x86_64.tar.gz
Source1:        https://github.com/storytold/filmcraft/releases/download/v%{version}/filmcraft-%{version}-linux-aarch64.tar.gz
Source2:        https://github.com/storytold/filmcraft/releases/download/v%{version}/SHA256SUMS.txt

ExclusiveArch:  x86_64 aarch64

BuildRequires:  appstream
BuildRequires:  desktop-file-utils

%global appid ai.storyteller.%{name}
%global app_root %{name}-%{version}-linux-%{_arch}
%global with_font_licenses 1
%global with_notice 0

%description
FilmCraft is a native video editor from the ArtCraft team.

%prep
%setup -q -c -T -n %{name}-%{version}

%ifarch x86_64
archive=%{name}-%{version}-linux-x86_64.tar.gz
binary_archive=%{SOURCE0}
%elifarch aarch64
archive=%{name}-%{version}-linux-aarch64.tar.gz
binary_archive=%{SOURCE1}
%endif
expected_checksum=$(awk -v filename="$archive" '$2 == filename { print $1 }' "%{SOURCE2}")
if [ -z "$expected_checksum" ]; then
    echo "No checksum found for $archive" >&2
    exit 1
fi
printf '%s  %s\n' "$expected_checksum" "$binary_archive" | sha256sum --check --strict -
tar -xzf "$binary_archive" --no-same-owner --no-same-permissions

%build
# Upstream provides prebuilt Linux binaries.

%install
install -D -m 0755 %{app_root}/bin/%{name} \
    %{buildroot}%{_bindir}/%{name}
install -D -m 0755 %{app_root}/bin/%{name}-cli \
    %{buildroot}%{_bindir}/%{name}-cli
install -d %{buildroot}%{_datadir}
cp -a %{app_root}/share/. %{buildroot}%{_datadir}/

install -d %{buildroot}%{_licensedir}/%{name}
mv %{buildroot}%{_docdir}/%{name}/LICENSE-APACHE \
    %{buildroot}%{_licensedir}/%{name}/
mv %{buildroot}%{_docdir}/%{name}/LICENSE-MIT \
    %{buildroot}%{_licensedir}/%{name}/
mv %{buildroot}%{_datadir}/icons/hicolor/*/apps/%{appid}*.attribution \
    %{buildroot}%{_licensedir}/%{name}/
%if %{with_font_licenses}
mv %{buildroot}%{_docdir}/%{name}/OFL-*.txt \
    %{buildroot}%{_licensedir}/%{name}/
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
appstreamcli validate --no-net \
    %{buildroot}%{_metainfodir}/%{appid}.metainfo.xml

%files
%license %{_licensedir}/%{name}/LICENSE-APACHE
%license %{_licensedir}/%{name}/LICENSE-MIT
%license %{_licensedir}/%{name}/*.attribution
%if %{with_font_licenses}
%license %{_licensedir}/%{name}/OFL-*.txt
%endif
%doc %{_docdir}/%{name}/README.md
%if %{with_notice}
%doc %{_docdir}/%{name}/NOTICE
%endif
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_datadir}/applications/%{appid}.desktop
%{_metainfodir}/%{appid}.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/%{appid}.png
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/mime/packages/%{appid}.xml

%changelog
%autochangelog
