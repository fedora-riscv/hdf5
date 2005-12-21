Name: hdf5
Version: 1.6.5
Release: 1%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD-ish
Group: System Environment/Libraries
URL: http://hdf.ncsa.uiuc.edu/HDF5/
Source0: ftp://ftp.ncsa.uiuc.edu/HDF/HDF5/current/src/%{name}-%{version}.tar.gz
Patch0: hdf5-1.6.4-gcc4.patch
Patch1: hdf5-1.6.4-destdir.patch
Patch2: hdf5-1.6.4-norpath.patch
Patch3: hdf5-1.6.4-testh5repack.patch
Patch4: hdf5-1.6.5-h5diff_attr.patch
Patch5: hdf5-1.6.4-ppc.patch
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
autoconf
%configure --with-ssl --enable-cxx --enable-fortran \
           --enable-threadsafe --with-pthread
make

%install
rm -rf $RPM_BUILD_ROOT
find doc/html -type f | xargs chmod -x
find doc/html -name '*.sh*' | xargs chmod +x
%makeinstall docdir=${RPM_BUILD_ROOT}%{_docdir}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la $RPM_BUILD_ROOT/%{_libdir}/*.settings

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY.txt doc/html
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5perf
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5unjam
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,0755)
%{_bindir}/h5c++
%{_bindir}/h5cc
%{_bindir}/h5fc
%{_bindir}/h5redeploy
%{_docdir}/%{name}/examples/
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.mod

%changelog
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
- Add %check
- Add some %docs
- Use %makeinstall
- Add patch to fix test for h5repack
- Add patch to fix h5diff_attr.c

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-2
- remove szip from spec, since szip license doesn't meet Fedora standards

* Sun Apr 3 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-1
- inital package for Fedora Extras
