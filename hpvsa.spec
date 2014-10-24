#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel package
%bcond_with	verbose		# verbose build (V=1)

%define	basever	3.13.0
%define	basedebrel	32
%define	debrel	%{basedebrel}.57
%define	localversion	%{basedebrel}-generic
%define	localver_str	%(echo %{localversion} | tr - _)

# binary driver. redefine macros
%define	alt_kernel	ubuntu
%define	kernel_name kernel%{_alt_kernel}
%define	kernel_version	%{basever}-%{localver_str}
%define	kernel_release	%{_kernel_ver}
%define	_kernel_ver %{basever}-%{localversion}
%define	_kernel_ver_str %(echo %{_kernel_ver} | tr - _)

%define		rel	1
%define		pname	hpvsa
Summary:	HP storage controller support
Name:		%{pname}%{_alt_kernel}
Version:	1.2.10
Release:	%{rel}
License:	HP Proprietary
Group:		Base/Kernel
Source0:	http://ppa.launchpad.net/hp-iss-team/hpvsa-update/ubuntu/pool/main/h/hpvsa/%{pname}_%{version}-121ubuntu18.tar.gz
# NoSource0-md5:	aa9d593d461d05e503b781c54174d777
NoSource:	0
Source1:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-image-%{_kernel_ver}_%{basever}-%{debrel}_amd64.deb
# NoSource1-md5:	51f5f700d35c4c05a6d195195a9d9ff1
NoSource:	1
Source2:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-image-extra-%{_kernel_ver}_%{basever}-%{debrel}_amd64.deb
# NoSource2-md5:	fe9dd9951ad3b1b8de3d650bb33d4e8f
NoSource:	2
URL:		https://launchpad.net/~hp-iss-team/+archive/hpvsa-update
BuildRequires:	rpmbuild(macros) >= 1.379
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		initrd_dir	/boot

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%description
Driver for HP Smart Array B120i/B320i SATA RAID controller.

%package -n kernel%{_alt_kernel}
Summary:	The Linux kernel (the core of the Linux operating system)
Version:	%{basever}
Release:	%{localver_str}
License:	GPL v2
Group:		Base/Kernel
Requires(post):	coreutils
Requires(post):	geninitrd >= 10000-3
Requires(post):	kmod >= 12-2
Requires:	/sbin/depmod
Requires:	coreutils
Requires:	geninitrd >= 10000-3
Requires:	kmod >= 12-2
Suggests:	crda
Suggests:	dracut
Suggests:	keyutils
Suggests:	linux-firmware
AutoReqProv:	no

%description -n kernel%{_alt_kernel}
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

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
mv hp-iss/* .

%if %{with kernel}
# kernel itself
ar xf %{SOURCE1}
tar xf data.tar.bz2

ar xf %{SOURCE2}
tar xf data.tar.bz2

# hardlink, and pld doesn't use that dir
rm -rv lib/modules/%{_kernel_ver}/initrd
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/scsi
cp -p hpvsa.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/scsi

%if %{with kernel}
install -d $RPM_BUILD_ROOT{/boot,/lib/{modules,firmware}}
# copy base kernel
cp -a boot/* $RPM_BUILD_ROOT/boot
cp -a lib/modules/* $RPM_BUILD_ROOT/lib/modules
cp -a lib/firmware/* $RPM_BUILD_ROOT/lib/firmware
touch $RPM_BUILD_ROOT%{initrd_dir}/initrd-%{_kernel_ver}.gz
touch $RPM_BUILD_ROOT%{initrd_dir}/initramfs-%{_kernel_ver}.img

# ghosted depmod files
for a in \
	dep{,.bin} \
	alias{,.bin} \
	devname \
	softdep \
	symbols{,.bin} \
	builtin.bin \
; do
	> $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/modules.$a
done
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}
[ -f /etc/sysconfig/kernel ] && . /etc/sysconfig/kernel
if [[ "$CREATE_SYMLINKS" != [Nn][Oo] ]]; then
%ifarch ia64
	mv -f /boot/efi/vmlinuz{,.old} 2> /dev/null
	ln -sf vmlinuz-%{_kernel_ver} /boot/efi/vmlinuz
%if 0%{?alt_kernel:1}
	mv -f /boot/efi/vmlinuz%{_alt_kernel}{,.old} 2> /dev/null
	ln -sf vmlinuz-%{_kernel_ver} /boot/efi/vmlinuz%{_alt_kernel}
%endif
%endif
	mv -f /boot/vmlinuz{,.old} 2> /dev/null
	mv -f /boot/System.map{,.old} 2> /dev/null
	ln -sf vmlinuz-%{_kernel_ver} /boot/vmlinuz
	ln -sf System.map-%{_kernel_ver} /boot/System.map
%if 0%{?alt_kernel:1}
	mv -f /boot/vmlinuz%{_alt_kernel}{,.old} 2> /dev/null
	mv -f /boot/System%{_alt_kernel}.map{,.old} 2> /dev/null
	ln -sf vmlinuz-%{_kernel_ver} /boot/vmlinuz%{_alt_kernel}
	ln -sf System.map-%{_kernel_ver} /boot/System.map%{_alt_kernel}
%endif
fi

%depmod %{_kernel_ver}

%posttrans	-n kernel%{_alt_kernel}
# use posttrans to generate initrd after all dependant module packages (-drm, etc) are installed
[ -f /etc/sysconfig/kernel ] && . /etc/sysconfig/kernel
initrd_file=""
if [[ "$USE_GENINITRD" != [Nn][Oo] ]]; then
	/sbin/geninitrd -f --initrdfs=initramfs %{initrd_dir}/initrd-%{_kernel_ver}.gz %{_kernel_ver} || :
	initrd_file="initrd-%{_kernel_ver}.gz"
fi

# if dracut is present then generate full-featured initramfs
if [[ "$USE_DRACUT" != [Nn][Oo] ]] && [ -x /sbin/dracut ]; then
	/sbin/dracut --force --quiet /boot/initramfs-%{_kernel_ver}.img %{_kernel_ver}
	[ -n "$initrd_file" ] || initrd_file="initramfs-%{_kernel_ver}.img"
fi

if [[ "$CREATE_SYMLINKS" != [Nn][Oo] ]]; then
	mv -f %{initrd_dir}/initrd{,.old} 2> /dev/null
	if [ -n "$initrd_file" ] ; then
		ln -sf "$initrd_file" %{initrd_dir}/initrd
	fi
%if 0%{?alt_kernel:1}
	mv -f %{initrd_dir}/initrd%{_alt_kernel}{,.old} 2> /dev/null
	if [ -n "$initrd_file" ] ; then
		ln -sf "$initrd_file" %{initrd_dir}/initrd%{_alt_kernel}
	fi
%endif
fi

# update boot loaders when old package files are gone from filesystem
if [ -x /sbin/update-grub -a -f /etc/sysconfig/grub ]; then
	if [ "$(. /etc/sysconfig/grub; echo ${UPDATE_GRUB:-no})" = "yes" ]; then
		/sbin/update-grub >/dev/null
	fi
fi
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{_kernel_ver}.gz --install %{_kernel_ver} --banner "PLD Linux (%{pld_release})%{?alt_kernel: / %{alt_kernel}}"
fi
if [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi
if [ -x /sbin/efi-boot-update ]; then
	/sbin/efi-boot-update --auto || :
fi

%post	-n kernel%{_alt_kernel}-scsi-hpvsa
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-scsi-hpvsa
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}
%defattr(644,root,root,755)
/boot/System.map-%{_kernel_ver}
/boot/abi-%{_kernel_ver}
/boot/config-%{_kernel_ver}
/boot/vmlinuz-%{_kernel_ver}
%ghost %{initrd_dir}/initrd-%{_kernel_ver}.gz
%ghost %{initrd_dir}/initramfs-%{_kernel_ver}.img

/lib/firmware/%{_kernel_ver}
%dir /lib/modules/%{_kernel_ver}
/lib/modules/%{_kernel_ver}/kernel
/lib/modules/%{_kernel_ver}/vdso
%exclude /lib/modules/%{_kernel_ver}/kernel/scsi/*.ko*

/lib/modules/%{_kernel_ver}/modules.builtin
/lib/modules/%{_kernel_ver}/modules.order

# rest modules.* are ghost (regenerated by post depmod -a invocation)
%ghost /lib/modules/%{_kernel_ver}/modules.alias
%ghost /lib/modules/%{_kernel_ver}/modules.alias.bin
%ghost /lib/modules/%{_kernel_ver}/modules.builtin.bin
%ghost /lib/modules/%{_kernel_ver}/modules.dep
%ghost /lib/modules/%{_kernel_ver}/modules.dep.bin
%ghost /lib/modules/%{_kernel_ver}/modules.devname
%ghost /lib/modules/%{_kernel_ver}/modules.softdep
%ghost /lib/modules/%{_kernel_ver}/modules.symbols
%ghost /lib/modules/%{_kernel_ver}/modules.symbols.bin
%endif

%files -n kernel%{_alt_kernel}-scsi-hpvsa
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/scsi/*.ko*
