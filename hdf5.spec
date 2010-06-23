%define snaprel %{nil}
Name: hdf5
Version: 1.8.5
Release: 3%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://www.hdfgroup.org/HDF5/
#Source0: ftp://ftp.hdfgroup.org/HDF5/current/src/%{name}-%{version}.tar.gz
Source0: http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-%{version}%{?snaprel}.tar.bz2
Source1: h5comp
Patch1: hdf5-1.8.5-longdouble.patch
Patch3: hdf5-1.8.0-multiarch.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: krb5-devel, openssl-devel, zlib-devel, gcc-gfortran, time

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is 
essentially a multidimensional array of data elements, and a group is a 
structure for organizing objects in an HDF5 file. Using these two basic 
objects, one can create and store almost any kind of scientific data 
structure, such as images, arrays of vectors, and structured and unstructured 
grids. You can also mix and match them in HDF5 files according to your needs.


%package devel
Summary: HDF5 development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
HDF5 development headers and libraries.


%package static
Summary: HDF5 static libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
HDF5 static libraries.


%prep
%setup -q -n %{name}-%{version}%{?snaprel}
%ifarch ppc64
%patch1 -p1 -b .longdouble
%endif
%patch3 -p1 -b .multiarch
find -name '*.[ch]' -o -name '*.f90' -exec chmod -x {} +


%build
export CC=gcc
export CXX=g++
export F9X=gfortran
export CFLAGS="${RPM_OPT_FLAGS/O2/O0}"
%configure \
  --disable-dependency-tracking \
  --enable-cxx \
  --enable-fortran \
  --enable-hl
# --enable-cxx/fortran and --enable-parallel flags are incompatible
#  --with-mpe=DIR          Use MPE instrumentation [default=no]
# --enable-cxx/fortran/parallel and --enable-threadsafe flags are incompatible
#Multiarch header
%ifarch x86_64 ppc64 ia64 s390x sparc64 alpha
cp src/H5pubconf.h \
   src/H5pubconf-64.h
%else
cp src/H5pubconf.h \
   src/H5pubconf-32.h
%endif
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
#Fortran modules
mkdir -p ${RPM_BUILD_ROOT}%{_fmoddir}
mv ${RPM_BUILD_ROOT}%{_includedir}/*.mod ${RPM_BUILD_ROOT}%{_fmoddir}

#Fixup headers and scripts for multiarch
%ifarch x86_64 ppc64 ia64 s390x sparc64 alpha
mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-64.h
for x in h5c++ h5cc h5fc
do
  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
     ${RPM_BUILD_ROOT}%{_bindir}/${x}-64
  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
done
%else
mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-32.h
for x in h5c++ h5cc h5fc
do
  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
     ${RPM_BUILD_ROOT}%{_bindir}/${x}-32
  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
done
%endif


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5copy
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5mkgrp
%{_bindir}/h5perf_serial
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5stat
%{_bindir}/h5unjam
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/h5c++
%{_bindir}/h5c++-*
%{_bindir}/h5cc
%{_bindir}/h5cc-*
%{_bindir}/h5fc
%{_bindir}/h5fc-*
%{_bindir}/h5redeploy
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.settings
%{_fmoddir}/*.mod
%{_datadir}/hdf5_examples/

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a


%changelog
* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-3
- Update longdouble patch for 1.8.5

* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-2
- Re-add longdouble patch on ppc64 for EPEL builds

* Mon Jun 21 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-1
- Update to 1.8.5
- Drop patches fixed upstream

* Mon Mar 1 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.4.patch1-1
- Update to 1.8.4-patch1

* Wed Jan 6 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.4-1
- Update to 1.8.4
- Must compile with -O0 due to gcc-4.4 incompatability
- No longer need -fno-strict-aliasing

* Thu Oct 1 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.3-3.snap12
- Update to 1.8.3-snap12
- Update signal patch
- Drop detect and filter-as-option patch fixed upstream
- Drop ppc only patch
- Add patch to skip tstlite test for now, problem reported upstream
- Fixup some source file permissions

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 2 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.3-1
- Update to 1.8.3
- Update signal and detect patches
- Drop open patch fixed upstream

* Sat Apr 18 2009 Karsten Hopp <karsten@redhat.com> 1.8.2-1.1
- fix s390x builds, s390x is 64bit, s390 is 32bit

* Mon Feb 23 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.2-1
- Update to 1.8.2
- Add patch to compile H5detect without optimization - make detection
  of datatype characteristics more robust - esp. long double
- Update signal patch
- Drop destdir patch fixed upstream
- Drop scaleoffset patch
- Re-add -fno-strict-aliasing
- Keep settings file needed for -showconfig (bug #481032)
- Wrapper script needs to pass arguments (bug #481032)

* Wed Oct 8 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-3
- Add sparc64 to 64-bit conditionals

* Fri Sep 26 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-2
- Add patch to filter -little as option used on sh arch (#464052)
 
* Thu Jun 5 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-1
- Update to 1.8.1

* Tue May 27 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-0.rc1.1
- Update to 1.8.1-rc1

* Tue May 13 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0.snap5-2
- Use new %%{_fmoddir} macro
- Re-enable ppc64, disable failing tests.  Failing tests are for 
  experimental long double support.

* Mon May 5 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0.snap5-1
- Update to 1.8.0-snap5
- Remove --enable-threadsafe, incompatible with --enable-cxx and 
  --enable-fortran
- ExcludeArch ppc64 until we can get it to build (bug #445423)

* Tue Mar 4 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0-2
- Remove failing test for now

* Fri Feb 29 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0-1
- Update to 1.8.0, drop upstreamed patches
- Update signal patch
- Move static libraries into -static sub-package
- Make -devel multiarch (bug #341501)

* Wed Feb  6 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-7
- Add patch to fix strict-aliasing
- Disable production mode to enable debuginfo

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-6
- Add patch to fix calling free() in H5PropList.cpp

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-5
- Add patch to support s390 (bug #431510)

* Mon Jan  7 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-4
- Add patches to support sparc (bug #427651)

* Tue Dec  4 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-3
- Rebuild against new openssl

* Fri Nov 23 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-2
- Add patch to build on alpha (bug #396391)

* Wed Oct 17 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-1
- Update to 1.6.6, drop upstreamed patches
- Explicitly set compilers

* Fri Aug 24 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-9
- Update license tag to BSD
- Rebuild for BuildID

* Wed Aug  8 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-8
- Fix memset typo
- Pass mode to open with O_CREAT

* Mon Feb 12 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-7
- New project URL
- Add patch to use POSIX sort key option
- Remove useless and multilib conflicting Makefiles from html docs
  (bug #228365)
- Make hdf5-devel own %%{_docdir}/%%{name}

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-6
- Rebuild for FC6

* Wed Mar 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-5
- Change rpath patch to not need autoconf
- Add patch for libtool on x86_64
- Fix shared lib permissions

* Mon Mar 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-4
- Add patch to avoid HDF setting the compiler flags

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-3
- Rebuild for gcc/glibc changes

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-2
- Don't ship h5perf with missing library

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-1
- Update to 1.6.5

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-9
- Rebuild

* Wed Nov 30 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-8
- Package fortran files properly
- Move compiler wrappers to devel

* Fri Nov 18 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-7
- Add patch for fortran compilation on ppc

* Wed Nov 16 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-6
- Bump for new openssl

* Tue Sep 20 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-5
- Enable fortran since the gcc bug is now fixed

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-4
- Make example scripts executable

* Wed Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-3
- Add --enable-threads --with-pthreads to configure
- Add %%check
- Add some %%docs
- Use %%makeinstall
- Add patch to fix test for h5repack
- Add patch to fix h5diff_attr.c

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-2
- remove szip from spec, since szip license doesn't meet Fedora standards

* Sun Apr 3 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-1
- inital package for Fedora Extras
