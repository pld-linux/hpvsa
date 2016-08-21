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
%define	_kernel_ver	%{_kernel_ver}
%define	_kernel_basever %{basever}-%{basedebrel}
%define	_kernel_ver %{basever}-%{localversion}
%define	_kernel_ver_str %(echo %{_kernel_ver} | tr - _)

# lynx -dump http://archive.ubuntu.com/ubuntu/pool/main/l/linux/ | grep 3.13.0-95 | grep -vE 'i386|diff|dsc|\.udeb|lowlatency|doc|source'

%define		rel	1
%define		pname	hpvsa
Summary:	HP storage controller support
Name:		%{pname}%{_alt_kernel}
Version:	1.2.12
Release:	%{rel}
License:	HP Proprietary
Group:		Base/Kernel
Source0:	http://ppa.launchpad.net/hp-iss-team/hp-storage/ubuntu/pool/main/h/hpvsa/%{pname}_%{version}-115-3.13ubuntu2.tar.gz
# NoSource0-md5:	7c6ee33ed10baf0ca61c3fa7353aad4e
NoSource:	0
Source1:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-image-%{_kernel_ver}_%{basever}-%{debrel}_amd64.deb
# NoSource1-md5:	51f5f700d35c4c05a6d195195a9d9ff1
NoSource:	1
Source2:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-image-extra-%{_kernel_ver}_%{basever}-%{debrel}_amd64.deb
# NoSource2-md5:	fe9dd9951ad3b1b8de3d650bb33d4e8f
NoSource:	2
Source3:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-headers-%{_kernel_ver}_%{basever}-%{debrel}_amd64.deb
# NoSource3-md5:	b83bd34df0107b8b208904be64ad3def
NoSource:	3
Source4:	http://archive.ubuntu.com/ubuntu/pool/main/l/linux/linux-headers-%{_kernel_basever}_%{basever}-%{debrel}_all.deb
# NoSource4-md5:	18fa458ad9dc6d2414f8f373f91ed45c
NoSource:	4
URL:		https://launchpad.net/~hp-iss-team/+archive/ubuntu/hp-storage
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		initrd_dir	/boot
# define this to '-%{basever}' for longterm branch
%define		versuffix	%{nil}

%define		_kernelbasesrcdir	/usr/src/linux-headers%{versuffix}-%{basever}-%{basedebrel}
%define		_kernelsrcdir	/usr/src/linux-headers%{versuffix}-%{basever}-%{localversion}

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%description
Driver for HP Smart Array B120i/B320i SATA RAID controller.

%package -n kernel%{_alt_kernel}
Summary:	The Linux kernel (the core of the Linux operating system)
Version:	%{basever}
Release:	%{localver_str}
Epoch:		3
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

%package -n kernel%{_alt_kernel}-headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Version:	%{basever}
Release:	%{localver_str}
Epoch:		3
Group:		Development/Building
AutoReqProv:	no

%description -n kernel%{_alt_kernel}-headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description -n kernel%{_alt_kernel}-headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten, die beim rekompilieren des
Kernels oder bei Kernel Modul kompilationen gebraucht werden.

%description -n kernel%{_alt_kernel}-headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package -n kernel%{_alt_kernel}-module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Version:	%{basever}
Release:	%{localver_str}
Epoch:		3
Group:		Development/Building
Requires:	kernel%{_alt_kernel}-headers = %{epoch}:%{basever}-%{localver_str}
Requires:	make
Conflicts:	rpmbuild(macros) < 1.652
AutoReqProv:	no

%description -n kernel%{_alt_kernel}-module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description -n kernel%{_alt_kernel}-module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description -n kernel%{_alt_kernel}-module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package -n kernel%{_alt_kernel}-scsi-hpvsa
Summary:	Linux driver for hpvsa
Summary(pl.UTF-8):	Sterownik dla Linuksa do hpvsa
Version:	%{basever}
Release:	%{rel}@%{_kernel_ver_str}
Epoch:		3
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
tar xf data.tar.bz2 && rm data.tar.bz2

ar xf %{SOURCE2}
tar xf data.tar.bz2 && rm data.tar.bz2

ar xf %{SOURCE3}
tar xf data.tar.xz && rm data.tar.xz

ar xf %{SOURCE4}
tar xf data.tar.xz && rm data.tar.xz

# hardlink, and pld doesn't use that dir
rm -rv lib/modules/%{_kernel_ver}/initrd
%endif

%build
v=$(modinfo -F vermagic ./hpvsa.ko | awk '{print $1}')
# 3.13.0-32-generic
test "$v" = "%{basever}-%{localversion}"

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

# rpm obeys filelinkto checks for ghosted symlinks, convert to files
rm -f $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/{build,source}
touch $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/{build,source}

# install headers
install -d $RPM_BUILD_ROOT%{_usrsrc}
cp -a usr/src/* $RPM_BUILD_ROOT%{_usrsrc}

# gcc5 hack
ln -s compiler-gcc4.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/compiler-gcc5.h
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

%post -n kernel%{_alt_kernel}-headers
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux%{versuffix}%{_alt_kernel}

%postun -n kernel%{_alt_kernel}-headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux%{versuffix}%{_alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux%{versuffix}%{_alt_kernel})" = "linux%{versuffix}%{_alt_kernel}-%{version}" ]; then
			rm -f %{_prefix}/src/linux%{versuffix}%{_alt_kernel}
		fi
	fi
fi

%triggerin -n kernel%{_alt_kernel}-module-build -- kernel%{_alt_kernel} = %{version}-%{release}
ln -sfn %{_kernelsrcdir} /lib/modules/%{_kernel_ver}/build
ln -sfn %{_kernelsrcdir} /lib/modules/%{_kernel_ver}/source

%triggerun -n kernel%{_alt_kernel}-module-build -- kernel%{_alt_kernel} = %{version}-%{release}
if [ "$1" = 0 ]; then
	rm -f /lib/modules/%{_kernel_ver}/{build,source}
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

# symlinks pointing to kernelsrcdir
%ghost /lib/modules/%{_kernel_ver}/build
%ghost /lib/modules/%{_kernel_ver}/source

%files -n kernel%{_alt_kernel}-headers
%defattr(644,root,root,755)
%defattr(-,root,root,-)
%{_kernelsrcdir}

%files -n kernel%{_alt_kernel}-module-build
%defattr(644,root,root,755)
%defattr(-,root,root,-)
%{_kernelbasesrcdir}
%endif

%files -n kernel%{_alt_kernel}-scsi-hpvsa
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/scsi/*.ko*
