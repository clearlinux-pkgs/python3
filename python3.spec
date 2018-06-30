Name:           python3
Version:        3.7.0
Release:        144
License:        Python-2.0
Summary:        The Python Programming Language
Url:            http://www.python.org
Group:          devel/python
Source0:        https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
Patch1:         0001-Fix-python-path-for-linux.patch
Patch2:         0002-Skip-tests-TODO-fix-skips.patch
Patch3:         0003-Use-pybench-to-optimize-python.patch
Patch4:         0004-Add-avx2-and-avx512-support.patch
Patch5:         0005-Build-avx2-and-avx512-versions-of-the-math-library.patch
Patch6:         0001-Add-pybench-for-pgo-optimization.patch
Patch7:		hashcompile.patch

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
Requires: python3-core
Requires: python3-lib
Requires: python3-lib-avx2
Requires: usrbinpython


%global __arch_install_post %{nil}

%description
The Python Programming Language.

%package lib
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description lib
The Python Programming Language.

%package lib-avx2
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python
Requires: 	python3-lib

%description lib-avx2
The Python Programming Language.

%package core
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python
Provides:       python3
Provides:       python3-modules
Provides:       /bin/python3

Requires:  	setuptools-python3
Requires:  	setuptools-bin


# evil evil compatibility hack for bootstrap purposes
Provides:       python(abi) = 3.6

%description core
The Python Programming Language.

%package dev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel
Requires:       python3-lib
Requires:       python3-core
Requires:	usrbinpython

%define python_configure_flags  --with-threads --with-pymalloc  --without-cxx-main --with-signal-module --enable-ipv6=yes  --libdir=/usr/lib  ac_cv_header_bluetooth_bluetooth_h=no  ac_cv_header_bluetooth_h=no  --with-system-ffi --with-system-expat --with-lto=8 --with-computed-gotos


%description dev
The Python Programming Language.

%package doc
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description doc
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

# pushd ..
# cp -a Python-%{version} Python-avx2
# cd Python-avx2
# popd

%build
export LANG=C

# Build with PGO for perf improvement
export CFLAGS="$CFLAGS -O3"
%configure %python_configure_flags --enable-shared
make %{?_smp_mflags}

# pushd ../Python-avx2
# export CFLAGS="$CFLAGS -march=haswell -mfma  "
# export CXXFLAGS="$CXXFLAGS -march=haswell -mfma"

# configure %python_configure_flags --enable-shared --bindir=/usr/bin/haswell
# make %{?_smp_mflags}
# popd

%install

# pushd ../Python-avx2
# make_install
# mkdir -p %{buildroot}/usr/lib64/haswell
# mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/haswell/
# rm -rf %{buildroot}/usr/lib/*
# rm -rf %{buildroot}/usr/bin/*
# popd


%make_install
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/

# --enable-optimizations does not work with --enable-shared
# https://bugs.python.org/issue29712
# pushd ../Python-avx2
# make clean
# configure %python_configure_flags --enable-optimizations
# make profile-opt %{?_smp_mflags}
# ./python Tools/pybench/pybench.py -n 20
# popd

# make clean
# configure %python_configure_flags --enable-optimizations
# make profile-opt %{?_smp_mflags}
# ./python Tools/pybench/pybench.py -n 20
#make_install

# check
# export LANG=C
# LD_LIBRARY_PATH=`pwd` ./python -Wd -E -tt  Lib/test/regrtest.py -v -x test_asyncio test_uuid test_subprocess || :


%files

%files lib
/usr/lib64/libpython3.7m.so.1.0

%files lib-avx2
#/usr/lib64/haswell/libpython3.7m.so.1.0

%files core
%exclude /usr/bin/2to3
/usr/bin/2to3-3.7
%exclude /usr/bin/easy_install-3.7
/usr/bin/idle3
/usr/bin/idle3.7
%exclude /usr/bin/pip3
%exclude /usr/bin/pip3.7
/usr/bin/pydoc3
/usr/bin/pydoc3.7
/usr/bin/python3
/usr/bin/python3-config
/usr/bin/python3.7
/usr/bin/python3.7-config
/usr/bin/python3.7m
/usr/bin/python3.7m-config
/usr/bin/pyvenv
/usr/bin/pyvenv-3.7
/usr/lib/python3.7
%exclude /usr/lib/python3.7/site-packages/setuptools-39.0.1.dist-info
%exclude /usr/lib/python3.7/site-packages/setuptools
%exclude /usr/lib/python3.7/ensurepip/_bundled/setuptools-39.0.1-py2.py3-none-any.whl
%exclude /usr/lib/python3.7/site-packages/pkg_resources
%exclude /usr/lib/python3.7/site-packages/pip/_internal/

%files dev
/usr/include/python3.7m/*.h
#/usr/lib64/haswell/libpython3.7m.so
/usr/lib64/libpython3.7m.so
/usr/lib64/libpython3.so
/usr/lib64/pkgconfig/python-3.7.pc
/usr/lib64/pkgconfig/python-3.7m.pc
/usr/lib64/pkgconfig/python3.pc

%files doc
%{_mandir}/man1/*
