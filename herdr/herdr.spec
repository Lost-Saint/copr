Name:           herdr
Version:        0.8.0
Release:        1%{?dist}
Summary:        Terminal workspace manager for AI coding agents

License:        Apache-2.0
URL:            https://herdr.dev/

Source0:        https://github.com/herdrdev/herdr/releases/download/v%{version}/herdr-linux-x86_64
Source1:        https://github.com/herdrdev/herdr/releases/download/v%{version}/herdr-linux-aarch64

ExclusiveArch:  x86_64 aarch64

%global debug_package %{nil}

%description
Herdr is a terminal workspace manager and runtime for coding agents.

%prep

%build

%install
%ifarch x86_64
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_bindir}/herdr
%endif

%ifarch aarch64
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_bindir}/herdr
%endif

%check
%{buildroot}%{_bindir}/herdr --version

%files
%{_bindir}/herdr
