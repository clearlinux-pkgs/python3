Name:           python3
Version:        3.11.4
Release:        299
License:        Python-2.0
Summary:        The Python Programming Language
Url:            https://www.python.org
Group:          devel/python
Source0:        https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tar.xz
Source1:        usrlocal.pth
Patch1:         0001-Fix-python-path-for-linux.patch
Patch2:         0002-Skip-tests-TODO-fix-skips.patch
Patch6:         0006-test_socket.py-remove-testPeek-test.test_socket.RDST.patch
Patch7:         0007-Force-config-to-always-be-shared.patch

# Suppress stripping binaries
%define __strip /bin/true
%define debug_package %{nil}



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
BuildRequires:  tk-extras
BuildRequires:  tk-staticdev
BuildRequires:  tcl-dev
BuildRequires:  tcl-staticdev
BuildRequires:  libX11-dev
BuildRequires:  pypi-pip
BuildRequires:  util-linux-dev
Requires: python3-core
Requires: python3-lib
Requires: usrbinpython
Requires: pypi-pip

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
# few fake provides for ease of integration with autospec
Provides:       pypi(enum34)
Provides:	pypi(pywin32)
Provides:       pypi(typing)
Requires:       pypi(setuptools)


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

%define python_configure_flags --with-threads --with-pymalloc  --without-cxx-main --with-signal-module --enable-ipv6=yes  --libdir=/usr/lib  ac_cv_header_bluetooth_bluetooth_h=no  ac_cv_header_bluetooth_h=no  --with-system-ffi --with-system-expat --with-lto --with-computed-gotos --without-ensurepip


%description dev
The Python Programming Language.

%description tcl
The Python Programming Language.

%prep
%setup -q -n Python-%{version}
%patch1 -p1
%patch2 -p1
%patch6 -p1
%patch7 -p1

pushd ..
cp -a Python-%{version} Python-avx2
cd Python-avx2
popd

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export LANG=C
export CFLAGS="$CFLAGS -O3 -fno-semantic-interposition -g1 -gno-column-info -gno-variable-location-views -gz"
export CXXFLAGS="$CXXFLAGS -O3 -fno-semantic-interposition -g1 -gno-column-info -gno-variable-location-views -gz"
%configure %python_configure_flags --enable-shared
SETUPTOOLS_USE_DISTUTILS=stdlib make %{?_smp_mflags}

pushd ../Python-avx2
export CFLAGS="$CFLAGS -march=x86-64-v3  "
export CXXFLAGS="$CXXFLAGS -march=x86-64-v3  "
%configure %python_configure_flags --enable-shared
SETUPTOOLS_USE_DISTUTILS=stdlib make %{?_smp_mflags} 
popd

%check
## NOTE: test timeouts are still occurring, so do not enable by default
#export LANG=C.UTF-8
#LD_LIBRARY_PATH=`pwd` ./python -Wd -E -tt  Lib/test/regrtest.py -v -x test_asyncio test_uuid test_subprocess || :

%install
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -fno-semantic-interposition -g1 -gno-column-info -gno-variable-location-views -gz "
export CXXFLAGS="$CXXFLAGS -O3 -fno-semantic-interposition -g1 -gno-column-info -gno-variable-location-views -gz "
export LDFLAGS="$LDFLAGS -g1 -gz"


pushd ../Python-avx2
%make_install_v3
popd

%make_install
mkdir -p  %{buildroot}/usr/lib64/  %{buildroot}-v3/usr/lib64/
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/
mv %{buildroot}-v3/usr/lib/libpython*.so* %{buildroot}-v3/usr/lib64/

export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export LANG=C
export CFLAGS="$CFLAGS -O3 -fno-semantic-interposition"

# --enable-optimizations does not work with --enable-shared
# https://bugs.python.org/issue29712

make clean
%configure %python_configure_flags --enable-optimizations
SETUPTOOLS_USE_DISTUTILS=stdlib make profile-opt %{?_smp_mflags}
%make_install

pushd ../Python-avx2
make clean
export CFLAGS="$CFLAGS -march=x86-64-v3  "
export CXXFLAGS="$CXXFLAGS -march=x86-64-v3  "
%configure %python_configure_flags --enable-optimizations
SETUPTOOLS_USE_DISTUTILS=stdlib make profile-opt %{?_smp_mflags}
%make_install_v3
popd

# Add /usr/local/lib/python*/site-packages to the python path
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/python3.11/site-packages/usrlocal.pth
# static library archives need to be writable for strip to work
install -m 0755 %{buildroot}/usr/lib/libpython3.11.a %{buildroot}/usr/lib64/
rm %{buildroot}*/usr/lib/libpython3.11.a

ln -s python%{version} %{buildroot}/usr/share/man/man1/python3
ln -s python%{version} %{buildroot}/usr/share/man/man1/python

/usr/bin/elf-move.py avx2 %{buildroot}-v3 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name}


%files

%files lib
/usr/lib64/libpython3.11.so.1.0
/V3/usr/lib64/libpython3.11.so.1.0

%files staticdev
/usr/lib/python3.11/config-3.11-x86_64-linux-gnu/libpython3.11.a
/usr/lib64/libpython3.11.a

%files core
/usr/bin/2to3
/usr/bin/2to3-3.11
#/usr/bin/easy_install-3.11
/usr/bin/pydoc3
/usr/bin/pydoc3.11
/usr/bin/python3
/usr/bin/python3-config
/usr/bin/python3.11
/usr/bin/python3.11-config
/usr/lib/python3.11
/V3/usr/lib/python3.11
/V3/usr/bin/python3.11
/V3/usr/lib/python3.11/config-3.11-x86_64-linux-gnu/python.o
/V3/usr/lib64/libpython3.so
/usr/share/man/man1/*
%exclude /usr/lib/python3.11/lib-dynload/_tkinter.cpython-311-x86_64-linux-gnu.so
%exclude /usr/lib/python3.11/tkinter
%exclude /usr/lib/python3.11/config-3.11-x86_64-linux-gnu/libpython3.11.a
%exclude /V3/usr/lib/python3.11/lib-dynload/_tkinter.cpython-311-x86_64-linux-gnu.so

%files dev
/usr/include/python3.11/*.h
/usr/include/python3.11/cpython/*.h
/usr/include/python3.11/internal/*.h
/usr/lib64/libpython3.11.so
/usr/lib64/libpython3.so
/usr/lib64/pkgconfig/python-3.11.pc
/usr/lib64/pkgconfig/python-3.11-embed.pc
/usr/lib64/pkgconfig/python3.pc
/usr/lib64/pkgconfig/python3-embed.pc


%files tcl
/usr/bin/idle3
/usr/bin/idle3.11
/usr/lib/python3.11/tkinter
/usr/lib/python3.11/lib-dynload/_tkinter.cpython-311-x86_64-linux-gnu.*
/V3/usr/lib/python3.11/lib-dynload/_tkinter.cpython-311-x86_64-linux-gnu.*
