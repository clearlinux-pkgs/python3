Name:           python3
Version:        3.9.6
Release:        230
License:        Python-2.0
Summary:        The Python Programming Language
Url:            http://www.python.org
Group:          devel/python
Source0:        https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tar.xz
Source1:        usrlocal.pth
Patch1:         0001-Fix-python-path-for-linux.patch
Patch2:         0002-Skip-tests-TODO-fix-skips.patch
Patch3:         0003-AVX2-and-AVX512-support.patch
Patch4:         0004-Build-avx2-and-avx512-versions-of-the-math-library.patch
Patch5:         0005-pythonrun.c-telemetry-patch.patch
Patch6:         0006-test_socket.py-remove-testPeek-test.test_socket.RDST.patch
Patch7:         0007-Force-config-to-always-be-shared.patch

BuildRequires:  bzip2
BuildRequires:  db
BuildRequires:  grep
BuildRequires:  bzip2-dev
BuildRequires:  xz-dev
BuildRequires:  gdbm-dev
BuildRequires:  readline-dev
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  sqlite-autoconf
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  ncurses-dev
BuildRequires:  expat-dev
BuildRequires:  libffi-dev
BuildRequires:  procps-ng-bin
BuildRequires:  netbase
BuildRequires:  tk-dev
BuildRequires:  tcl-dev
BuildRequires:  libX11-dev
BuildRequires:  pip
Requires: python3-core
Requires: python3-lib
Requires: usrbinpython

%define keepstatic 1
%global __arch_install_post %{nil}

%description
The Python Programming Language.

%package lib
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description lib
The Python Programming Language.
%package staticdev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description staticdev
The Python Programming Language.

%package core
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python
Provides:       python3-modules
Provides:       /bin/python3
Requires:       setuptools-python3


# evil evil compatibility hack for bootstrap purposes
#Provides:       python(abi) = 3.7

%description core
The Python Programming Language.

%package dev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel
Requires:       python3-lib
Requires:       python3-core
Requires:       usrbinpython

%package tcl
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel
Requires:       python3-lib
Requires:       python3-core
Requires:       usrbinpython

%define python_configure_flags  LDFLAGS="-Wa,-mbranches-within-32B-boundaries"  --with-threads --with-pymalloc  --without-cxx-main --with-signal-module --enable-ipv6=yes  --libdir=/usr/lib  ac_cv_header_bluetooth_bluetooth_h=no  ac_cv_header_bluetooth_h=no  --with-system-ffi --with-system-expat --with-lto=8 --with-computed-gotos --without-ensurepip


%description dev
The Python Programming Language.

%description tcl
The Python Programming Language.

%prep
%setup -q -n Python-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

pushd ..
cp -a Python-%{version} Python-avx2
cd Python-avx2
popd

%build
export LANG=C
export CFLAGS="$CFLAGS -O3"
%configure %python_configure_flags --enable-shared
make %{?_smp_mflags}

pushd ../Python-avx2
export CFLAGS="$CFLAGS -march=haswell -mfma  "
export CXXFLAGS="$CXXFLAGS -march=haswell -mfma"
%configure %python_configure_flags --enable-shared --bindir=/usr/bin/haswell
make %{?_smp_mflags}
popd

%install

pushd ../Python-avx2
%make_install

mkdir -p %{buildroot}/usr/lib64/haswell
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/haswell/
rm -rf %{buildroot}/usr/lib/*
rm -rf %{buildroot}/usr/bin/*
popd


%make_install
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/

# --enable-optimizations does not work with --enable-shared
# https://bugs.python.org/issue29712
pushd ../Python-avx2
make clean
%configure %python_configure_flags --enable-optimizations
make profile-opt %{?_smp_mflags}
popd

make clean
%configure %python_configure_flags --enable-optimizations
make profile-opt %{?_smp_mflags}
%make_install
# Add /usr/local/lib/python*/site-packages to the python path
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/python3.9/site-packages/usrlocal.pth
# static library archives need to be writable for strip to work
install -m 0755 %{buildroot}/usr/lib/libpython3.9.a %{buildroot}/usr/lib64/
rm %{buildroot}/usr/lib/libpython3.9.a

ln -s python%{version} %{buildroot}/usr/share/man/man1/python3
ln -s python%{version} %{buildroot}/usr/share/man/man1/python

# NOTE: test timeouts are still occurring, so do not enable by default
# check
# export LANG=C.UTF-8
# LD_LIBRARY_PATH=`pwd` ./python -Wd -E -tt  Lib/test/regrtest.py -v -x test_asyncio test_uuid test_subprocess || :


%files

%files lib
/usr/lib64/haswell/libpython3.9.so.1.0
/usr/lib64/libpython3.9.so.1.0

%files staticdev
/usr/lib/python3.9/config-3.9-x86_64-linux-gnu/libpython3.9.a
/usr/lib64/libpython3.9.a

%files core
/usr/bin/2to3
/usr/bin/2to3-3.9
#/usr/bin/easy_install-3.9
/usr/bin/pydoc3
/usr/bin/pydoc3.9
/usr/bin/python3
/usr/bin/python3-config
/usr/bin/python3.9
/usr/bin/python3.9-config
/usr/lib/python3.9
/usr/share/man/man1/*

%files dev
/usr/include/python3.9/*.h
/usr/include/python3.9/cpython/*.h
/usr/include/python3.9/internal/*.h
/usr/lib64/haswell/libpython3.9.so
/usr/lib64/libpython3.9.so
/usr/lib64/libpython3.so
/usr/lib64/pkgconfig/python-3.9.pc
/usr/lib64/pkgconfig/python-3.9-embed.pc
/usr/lib64/pkgconfig/python3.pc
/usr/lib64/pkgconfig/python3-embed.pc

%files tcl
/usr/bin/idle3
/usr/bin/idle3.9
/usr/lib/python3.9/tkinter
/usr/lib/python3.9/lib-dynload/_tkinter.cpython-39-x86_64-linux-gnu.*
