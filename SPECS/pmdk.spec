
# rpmbuild options:
#   --with | --without fabric
#   --with | --without ndctl
#   --define _testconfig <path to custom testconfig.sh>

# do not terminate build if files in the $RPM_BUILD_ROOT
# directory are not found in %%files (without fabric case)
%define _unpackaged_files_terminate_build 0

%bcond_without fabric

# by default build w/ ndctl, unless explicitly disabled
%bcond_without ndctl

%define min_libfabric_ver 1.4.2
%define min_ndctl_ver 60.1

Name:		pmdk
Version:	1.12.1
Release:	1%{?dist}
Summary:	Persistent Memory Development Kit (former NVML)
License:	BSD
URL:		http://pmem.io/pmdk

Source0:	https://github.com/pmem/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:		pmdk-use-platform-python.patch
Patch1:		Makefile-bypass-check-doc-in-check.patch

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	man
BuildRequires:	pkgconfig
BuildRequires:	pandoc
BuildRequires:	groff

%if %{with ndctl}
BuildRequires:	ndctl-devel >= %{min_ndctl_ver}
BuildRequires:	daxctl-devel >= %{min_ndctl_ver}
%endif

%if %{with fabric}
BuildRequires:	libfabric-devel >= %{min_libfabric_ver}
%endif


# Debug variants of the libraries should be filtered out of the provides.
%global __provides_exclude_from ^%{_libdir}/pmdk_debug/.*\\.so.*$

# By design, PMDK does not support any 32-bit architecture.
# Due to dependency on some inline assembly, PMDK can be compiled only
# on these architectures:
# - x86_64
# - ppc64le (experimental)
# - aarch64 (unmaintained, supporting hardware doesn't exist?)
#
# Other 64-bit architectures could also be supported, if only there is
# a request for that, and if somebody provides the arch-specific
# implementation of the low-level routines for flushing to persistent
# memory.

# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637

ExclusiveArch: x86_64 ppc64le

%description
The Persistent Memory Development Kit is a collection of libraries for
using memory-mapped persistence, optimized specifically for persistent memory.


%package -n libpmem
Summary: Low-level persistent memory support library
Group: System Environment/Libraries
%description -n libpmem
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

%files -n libpmem
%defattr(-,root,root,-)
%dir %{_datadir}/pmdk
%{_libdir}/libpmem.so.*
%{_datadir}/pmdk/pmdk.magic
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-devel
Summary: Development files for the low-level persistent memory library
Group: Development/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmem-devel
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This library is provided for software which tracks every store to
pmem and needs to flush those changes to durability. Most developers
will find higher level libraries like libpmemobj to be much more
convenient.

%files -n libpmem-devel
%defattr(-,root,root,-)
%{_libdir}/libpmem.so
%{_libdir}/pkgconfig/libpmem.pc
%{_includedir}/libpmem.h
%{_mandir}/man7/libpmem.7.gz
%{_mandir}/man3/pmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-debug
Summary: Debug variant of the low-level persistent memory library
Group: Development/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmem-debug
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmem-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmem.so
%{_libdir}/pmdk_debug/libpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk
Summary: Persistent Memory Resident Array of Blocks library
Group: System Environment/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmemblk
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

%files -n libpmemblk
%defattr(-,root,root,-)
%{_libdir}/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-devel
Summary: Development files for the Persistent Memory Resident Array of Blocks library
Group: Development/Libraries
Requires: libpmemblk = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemblk-devel
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

For example, a program keeping a cache of fixed-size objects in pmem
might find this library useful. This library is provided for cases
requiring large arrays of objects at least 512 bytes each. Most
developers will find higher level libraries like libpmemobj to be
more generally useful.

%files -n libpmemblk-devel
%defattr(-,root,root,-)
%{_libdir}/libpmemblk.so
%{_libdir}/pkgconfig/libpmemblk.pc
%{_includedir}/libpmemblk.h
%{_mandir}/man7/libpmemblk.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemblk_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-debug
Summary: Debug variant of the Persistent Memory Resident Array of Blocks library
Group: Development/Libraries
Requires: libpmemblk = %{version}-%{release}
Requires: libpmem = %{version}-%{release}
%description -n libpmemblk-debug
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemblk-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemblk.so
%{_libdir}/pmdk_debug/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog
Summary: Persistent Memory Resident Log File library
Group: System Environment/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmemlog
The libpmemlog library provides a pmem-resident log file. This is
useful for programs like databases that append frequently to a log
file.

%files -n libpmemlog
%defattr(-,root,root,-)
%{_libdir}/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-devel
Summary: Development files for the Persistent Memory Resident Log File library
Group: Development/Libraries
Requires: libpmemlog = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemlog-devel
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

%files -n libpmemlog-devel
%defattr(-,root,root,-)
%{_libdir}/libpmemlog.so
%{_libdir}/pkgconfig/libpmemlog.pc
%{_includedir}/libpmemlog.h
%{_mandir}/man7/libpmemlog.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemlog_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-debug
Summary: Debug variant of the Persistent Memory Resident Log File library
Group: Development/Libraries
Requires: libpmemlog = %{version}-%{release}
Requires: libpmem = %{version}-%{release}
%description -n libpmemlog-debug
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemlog-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemlog.so
%{_libdir}/pmdk_debug/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj
Summary: Persistent Memory Transactional Object Store library
Group: System Environment/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmemobj
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj
%defattr(-,root,root,-)
%{_libdir}/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-devel
Summary: Development files for the Persistent Memory Transactional Object Store library
Group: Development/Libraries
Requires: libpmemobj = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemobj-devel
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

%files -n libpmemobj-devel
%defattr(-,root,root,-)
%{_libdir}/libpmemobj.so
%{_libdir}/pkgconfig/libpmemobj.pc
%{_includedir}/libpmemobj.h
%{_includedir}/libpmemobj/*.h
%{_mandir}/man7/libpmemobj.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemobj_*.3.gz
%{_mandir}/man3/pobj_*.3.gz
%{_mandir}/man3/oid_*.3.gz
%{_mandir}/man3/toid*.3.gz
%{_mandir}/man3/direct_*.3.gz
%{_mandir}/man3/d_r*.3.gz
%{_mandir}/man3/tx_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-debug
Summary: Debug variant of the Persistent Memory Transactional Object Store library
Group: Development/Libraries
Requires: libpmemobj = %{version}-%{release}
Requires: libpmem = %{version}-%{release}
%description -n libpmemobj-debug
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemobj-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemobj.so
%{_libdir}/pmdk_debug/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool
Summary: Persistent Memory pool management library
Group: System Environment/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmempool
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%files -n libpmempool
%defattr(-,root,root,-)
%{_libdir}/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-devel
Summary: Development files for Persistent Memory pool management library
Group: Development/Libraries
Requires: libpmempool = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmempool-devel
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%files -n libpmempool-devel
%defattr(-,root,root,-)
%{_libdir}/libpmempool.so
%{_libdir}/pkgconfig/libpmempool.pc
%{_includedir}/libpmempool.h
%{_mandir}/man7/libpmempool.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmempool_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-debug
Summary: Debug variant of the Persistent Memory pool management library
Group: Development/Libraries
Requires: libpmempool = %{version}-%{release}
Requires: libpmem = %{version}-%{release}
%description -n libpmempool-debug
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmempool-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmempool.so
%{_libdir}/pmdk_debug/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%if %{with fabric}

%package -n librpmem
Summary: Remote Access to Persistent Memory library
Group: System Environment/Libraries
Requires: libfabric >= %{min_libfabric_ver}
Requires: openssh-clients
%description -n librpmem
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

%files -n librpmem
%defattr(-,root,root,-)
%{_libdir}/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n librpmem-devel
Summary: Development files for the Remote Access to Persistent Memory library
Group: Development/Libraries
Requires: librpmem = %{version}-%{release}
%description -n librpmem-devel
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

This sub-package contains libraries and header files for developing
applications that want to specifically make use of librpmem.

%files -n librpmem-devel
%defattr(-,root,root,-)
%{_libdir}/librpmem.so
%{_libdir}/pkgconfig/librpmem.pc
%{_includedir}/librpmem.h
%{_mandir}/man7/librpmem.7.gz
%{_mandir}/man3/rpmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n librpmem-debug
Summary: Debug variant of the Remote Access to Persistent Memory library
Group: Development/Libraries
Requires: librpmem = %{version}-%{release}
%description -n librpmem-debug
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n librpmem-debug
%defattr(-,root,root,-)
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/librpmem.so
%{_libdir}/pmdk_debug/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n rpmemd
Group: System Environment/Base
Summary: Target node process executed by librpmem
Requires: libfabric >= %{min_libfabric_ver}
Requires: libpmem = %{version}-%{release}
%description -n rpmemd
The rpmemd process is executed on a target node by librpmem library
and facilitates access to persistent memory over RDMA.

%files -n rpmemd
%{_bindir}/rpmemd
%{_mandir}/man1/rpmemd.1.gz

# _with_fabric
%endif

%package -n pmempool
Summary: Utilities for Persistent Memory
Group: System Environment/Base
Requires: libpmem = %{version}-%{release}
Requires: libpmemlog = %{version}-%{release}
Requires: libpmemblk = %{version}-%{release}
Requires: libpmemobj = %{version}-%{release}
Requires: libpmempool = %{version}-%{release}
Obsoletes: nvml-tools < %{version}-%{release}
%description -n pmempool
The pmempool is a standalone utility for management and off-line analysis
of Persistent Memory pools created by PMDK libraries. It provides a set
of utilities for administration and diagnostics of Persistent Memory pools.
The pmempool may be useful for troubleshooting by system administrators
and users of the applications based on PMDK libraries.

%files -n pmempool
%{_bindir}/pmempool
%{_mandir}/man1/pmempool.1.gz
%{_mandir}/man1/pmempool-*.1.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/pmempool
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n pmreorder
Summary: Consistency Checker for Persistent Memory
Group: __GROUP_SYS_BASE__
Requires: /usr/libexec/platform-python
%description -n pmreorder
The pmreorder tool is a collection of python scripts designed to parse
and replay operations logged by pmemcheck - a persistent memory checking tool.
Pmreorder performs the store reordering between persistent memory barriers -
a sequence of flush-fence operations. It uses a consistency checking routine
provided in the command line options to check whether files are in a consistent state.

%files -n pmreorder
%{_bindir}/pmreorder
%{_datadir}/pmreorder/*.py
%{_mandir}/man1/pmreorder.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%if %{with ndctl}

%package -n daxio
Summary: Perform I/O on Device DAX devices or zero a Device DAX device
Group: System Environment/Base
Requires: libpmem = %{version}-%{release}
%description -n daxio
The daxio utility performs I/O on Device DAX devices or zero
a Device DAX device.  Since the standard I/O APIs (read/write) cannot be used
with Device DAX, data transfer is performed on a memory-mapped device.
The daxio may be used to dump Device DAX data to a file, restore data from
a backup copy, move/copy data to another device or to erase data from
a device.

%files -n daxio
%{_bindir}/daxio
%{_mandir}/man1/daxio.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

# _with_ndctl
%endif


%prep
%autosetup -p1 -n %{name}-%{version}

%build
# For debug build default flags may be overriden to disable compiler
# optimizations.
%set_build_flags
NDCTL_ENABLE=y make %{?_smp_mflags} NORPATH=1


# Override LIB_AR with empty string to skip installation of static libraries
%install
NDCTL_ENABLE=y make install DESTDIR=%{buildroot} \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	docdir=%{_docdir}
mkdir -p %{buildroot}%{_datadir}/pmdk
cp utils/pmdk.magic %{buildroot}%{_datadir}/pmdk/


%post   -n libpmem -p /sbin/ldconfig
%postun -n libpmem -p /sbin/ldconfig
%post   -n libpmemblk -p /sbin/ldconfig
%postun -n libpmemblk -p /sbin/ldconfig
%post   -n libpmemlog -p /sbin/ldconfig
%postun -n libpmemlog -p /sbin/ldconfig
%post   -n libpmemobj -p /sbin/ldconfig
%postun -n libpmemobj -p /sbin/ldconfig
%post   -n libpmempool -p /sbin/ldconfig
%postun -n libpmempool -p /sbin/ldconfig

%if %{with fabric}
%post   -n librpmem -p /sbin/ldconfig
%postun -n librpmem -p /sbin/ldconfig
%endif

%if 0%{?__debug_package} == 0
%debug_package
%endif


%changelog
* Mon Nov 21 2022 Bryan Gurney <bgurney@redhat.com> - 1.12.1-1.el8
- Update to pmdk version 1.12.1
- Related: rhbz#2111428

* Tue Jan 25 2022 Bryan Gurney <bgurney@redhat.com> - 1.11.1-1.el8
- Update to pmdk version 1.11.1
- Related: rhbz#2009889

* Wed Jan  6 2021 Jeff Moyer <jmoyer@redhat.com> - 1.9.2-1.el8
- Package pmdk version 1.9.2 for stream 1-fileformat-v6-rhel-8.3.1
- libvmem is no longer packaged as part of pmdk.
- ppc64le packages are now built
- Related: rhbz#1524652, rhbz#1780388, rhbz#1854812, rhbz#1860860

* Fri Nov  1 2019 Jeff Moyer <jmoyer@redhat.com> - 1.6.1-1.el8
- Update to pmdk bugfix relase 1.6.1.
- Resolves: rhbz#1730675

* Mon Jun 24 2019 Jeff Moyer <jmoyer@redhat.com> - 1.6-2.el8
- Add explicit version dependencies
- Fix up broken link line in build system
- Related: rhbz#1598527

* Tue May 28 2019 Jeff Moyer <jmoyer@redhat.com> - 1.6-1.el8
- Add pmdk 1.6 to the distro.
- Resolves: rhbz#1598527

* Wed Oct 31 2018 Jeff Moyer <jmoyer@redhat.com> - 1.5-2.el8
- Fix up python3 uses to instead use platform-python (Jeff Moyer)
- related: rhbz#1488828

* Wed Oct 31 2018 Jeff Moyer <jmoyer@redhat.com> - 1.5-1.el8
- rebase to pmdk-1.5, and rename to nvml (Jeff Moyer)
- broken libpmemcto was removed
- c++ bindings were moved to a separate project/package
- Fix library requires to be =n-v-r instead of >= (Jeff Moyer)
- resolves: rhbz#1488828

* Mon Oct 08 2018 Jeff Moyer <jmoyer@redhat.com> - 1.4-6.el8
- default to building daxio (Jeff Moyer)
- Resolves: rhbz#1637168

* Wed Sep 26 2018 Jeff Moyer <jmoyer@redhat.com> - 1.4-5.el8
- use %set_build_flags instead of %{optflags}
- Resolves: rhbz#1630611

* Tue May 22 2018 Jeff Moyer <jmoyer@redhat.com> - 1.4-4
- Get rid of SuSe conditionals (Jeff Moyer)
- Remove the %check section. (Jeff Moyer)
- Resolves: rhbz#1580829

* Fri Mar 30 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-3
- Revert package name change
- Re-enable check

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-2
- Fix issues found by rpmlint

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-1
- Rename NVML project to PMDK
- Update to PMDK version 1.4 (RHBZ #1480578, #1539562, #1539564)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3.1-1
- Update to NVML version 1.3.1 (RHBZ #1480578)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3-1
- Update to NVML version 1.3 (RHBZ #1451741, RHBZ #1455216)
- Add librpmem and rpmemd sub-packages
- Force file system to appear as PMEM for make check

* Fri Jun 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.3-2
- Update to NVML version 1.2.3 (RHBZ #1451741)

* Sat Apr 15 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.2-1
- Update to NVML version 1.2.2 (RHBZ #1436820, RHBZ #1425038)

* Thu Mar 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.1-1
- Update to NVML version 1.2.1 (RHBZ #1425038)

* Tue Feb 21 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-3
- Fix compilation under gcc 7.0.x (RHBZ #1424004)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-1
- Update to NVML version 1.2 (RHBZ #1383467)
- Add libpmemobj C++ bindings

* Thu Jul 14 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-3
- Add missing package version requirements

* Mon Jul 11 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-2
- Move debug variants of the libraries to -debug subpackages

* Sun Jun 26 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-1
- NVML 1.1 release
- Update link to source tarball
- Add libpmempool subpackage
- Remove obsolete patches

* Wed Jun 01 2016 Dan Horák <dan[at]danny.cz> - 1.0-3
- switch to ExclusiveArch

* Sun May 29 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-2
- Exclude PPC architecture
- Add bug numbers for excluded architectures

* Tue May 24 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-1
- Initial RPM release
