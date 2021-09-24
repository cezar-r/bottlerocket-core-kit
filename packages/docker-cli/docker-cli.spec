%global goproject github.com/docker
%global gorepo cli
%global goimport %{goproject}/%{gorepo}

%global gover 20.10.7
%global rpmver %{gover}
%global gitrev f0df35096d5f5e6b559b42c7fde6c65a2909f7c5

%global source_date_epoch 1492525740

%global _dwz_low_mem_die_limit 0

Name: %{_cross_os}docker-%{gorepo}
Version: %{rpmver}
Release: 1%{?dist}
Summary: Docker CLI
License: Apache-2.0
URL: https://%{goimport}
Source0: https://%{goimport}/archive/v%{gover}/cli-%{gover}.tar.gz
Source1000: clarify.toml

# CVE-2021-41092
Patch0001: 0001-registry-ensure-default-auth-config-has-address.patch

BuildRequires: git
BuildRequires: %{_cross_os}glibc-devel

%description
%{summary}.

%prep
%autosetup -Sgit -n %{gorepo}-%{gover} -p1
%cross_go_setup %{gorepo}-%{gover} %{goproject} %{goimport}

%build
%cross_go_configure %{goimport}
LD_VERSION="-X github.com/docker/cli/cli/version.Version=%{gover}"
LD_GIT_REV="-X github.com/docker/cli/cli/version.GitCommit=%{gitrev}"
LD_PLATFORM="-X \"github.com/docker/cli/cli/version.PlatformName=Docker Engine - Community\""
BUILDTIME=$(date -u -d "@%{source_date_epoch}" --rfc-3339 ns 2> /dev/null | sed -e 's/ /T/')
LD_BUILDTIME="-X github.com/docker/cli/cli/version.BuildTime=${BUILDTIME}"
go build \
  -buildmode=pie \
  -ldflags "-linkmode=external ${LD_VERSION} ${LD_GIT_REV} ${LD_PLATFORM} ${LD_BUILDTIME}" \
  -o docker \
  %{goimport}/cmd/docker

%install
install -d %{buildroot}%{_cross_bindir}
install -p -m 0755 docker %{buildroot}%{_cross_bindir}

%cross_scan_attribution --clarify %{S:1000} go-vendor vendor

%files
%license LICENSE NOTICE
%{_cross_attribution_file}
%{_cross_attribution_vendor_dir}
%{_cross_bindir}/docker

%changelog
