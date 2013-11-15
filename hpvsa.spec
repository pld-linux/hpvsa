#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

# binary driver. redefine
%define	_kernel_ver 3.8.0-33-generic
%define	_kernel_ver_str %(echo %{_kernel_ver} | tr - _)

%define		rel	0.1
%define		pname	hpvsa
Summary:	HP storage controller support
Name:		%{pname}%{_alt_kernel}
Version:	1.2.8
Release:	%{rel}
License:	HP Proprietary
Group:		Base/Kernel
Source0:	http://ppa.launchpad.net/hp-iss-team/hpvsa-update/ubuntu/pool/main/h/hpvsa/hpvsa_%{version}-0~12~ubuntu13.04.1.tar.gz
# NoSource0-md5:	1699424136da8b4098c9589f5494e477
NoSource:	0
URL:		https://launchpad.net/~hp-iss-team/+archive/hpvsa-update
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Driver for HP Smart Array B120i/B320i SATA RAID controller.

%package -n kernel%{_alt_kernel}-scsi-hpvsa
Summary:	Linux driver for hpvsa
Summary(pl.UTF-8):	Sterownik dla Linuksa do hpvsa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-scsi-hpvsa
Driver for HP Smart Array B120i/B320i SATA RAID controller.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-scsi-hpvsa -l pl.UTF-8
Sterownik dla Linuksa do hpvsa.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -qc
mv recipe-*/* .

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m hpvsa -d kernel/scsi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-scsi-hpvsa
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-scsi-hpvsa
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-scsi-hpvsa
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/scsi/*.ko*
%endif
