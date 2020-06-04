%ifarch %{x86_64}
%bcond_without compat32
%endif

# For python modules
%global _disable_ld_no_undefined 1

%define major   1
%define libname %mklibname tdb %{major}
%define devname %mklibname -d tdb
%define lib32name %mklib32name tdb %{major}
%define dev32name %mklib32name -d tdb
%define beta %nil

# beta releases are taken from the samba4 tarball using
# mkdir -p tdb-1.2.11/lib
# cp -a buildtools lib/tdb/* tdb-1.2.11/
# cp -a lib/replace tdb-1.2.11/lib/
# tar cf tdb-1.2.11.tar tdb-1.2.11

%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} \
rm -Rf $GNUPGHOME \

Name:           tdb
Version:        1.4.3
%if "%beta" != ""
Release:	0.%beta.1
%else
Release:        2
Source1:        https://talloc.samba.org/ftp/tdb/tdb-%{version}.tar.asc
Source2:        samba-pubkey.asc
%endif
Group:          System/Libraries
License:        GPLv2
URL:            https://tdb.samba.org/
Summary:        Library implementing Samba's embedded database
Source0:        https://talloc.samba.org/ftp/tdb/tdb-%{version}.tar.gz
Source100:	tdb-1.4.3-python32.patch
BuildRequires:  pkgconfig(python3)
BuildRequires:  xsltproc
BuildRequires:  docbook-style-xsl
%if %{with compat32}
BuildRequires:	devel(libpython3.8)
BuildRequires:	devel(libintl)
%endif

%description
Library implementing Samba's embedded database and utilities for backing up,
restoring and manipulating the database.

%package -n     %{libname}
Group:          System/Libraries
Summary:        Library implementing Samba's embedded database

%description -n %{libname}
Library implementing Samba's embedded database

%package -n     tdb-utils
Group:          Databases
Summary:        Tools for backing up, restoring, and manipulating Samba's embedded database
Conflicts:      samba-server < 3.3.2-2

%description -n tdb-utils
Tools for backing up, restoring, and manipulating Samba's embedded database

%package -n     %{devname}
Group:          Development/C
Summary:        Library implementing Samba's embedded database
Provides:       tdb-devel = %{EVRD}
Requires:       %{libname} = %{EVRD}
# because /usr/include/tdb.h was moved from libsmbclient0-devel to libname-devel
Conflicts:      %{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %{devname}
Library implementing Samba's embedded database

%package -n     python-tdb
Group:          Development/Python
Summary:        Python bindings to Samba's tdb embedded database

%description -n python-tdb
Pyhton bindings to Samba's tdb embedded database

%if %{with compat32}
%package -n     %{lib32name}
Group:          System/Libraries
Summary:        Library implementing Samba's embedded database (32-bit)

%description -n %{lib32name}
Library implementing Samba's embedded database

%package -n     %{dev32name}
Group:          Development/C
Summary:        Library implementing Samba's embedded database (32-bit)
Requires:       %{devname} = %{EVRD}
Requires:       %{lib32name} = %{EVRD}

%description -n %{dev32name}
Library implementing Samba's embedded database
%endif

%prep
%if "%beta" == ""
#Try and validate signatures on source:
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE

#check_sig %{SOURCE2} %{SOURCE1} $VERIFYSOURCE

rm -f $VERIFYSOURCE
%endif

%autosetup -p1

%build
%if %{with compat32}
mkdir build32
cp -a $(ls -1 |grep -v build32) build32/
cd build32
patch -p1 -z .omv32~ -b <%{S:100}
export CC="gcc -m32"
export CPP="g++ -m32"
cat >python3-config <<'EOF'
#!/bin/sh
/usr/bin/python3-config "$@" |sed -e 's,-m64,-m32,g;s,lib64,lib,g;s,-lintl,,g'
EOF
chmod +x python3-config
export PYTHON_CONFIG="$(pwd)/python3-config"
./configure --prefix=%{_prefix} --libdir=%{_prefix}/lib
%make_build
rm -f python3-config
cd ..
%endif

%setup_compile_flags
export CC=%{__cc}
export CPP=%{__cxx}
if ! ./configure --prefix=%{_prefix} --libdir=%{_libdir}; then
	echo "Configure failed -- log:"
	cat bin/config.log
	exit 1
fi
%make

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install
chmod 755 %{buildroot}%{_libdir}/libtdb.so.%{major}*

%files -n %{libname}
%{_libdir}/libtdb.so.%{major}*

%files -n %{devname}
%{_libdir}/libtdb.so
#{_libdir}/libname.a
%{_includedir}/tdb.h
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-utils
%{_bindir}/tdb*
%{_mandir}/man8/tdb*.8*

%files -n python-tdb
%{py_platsitedir}/tdb*.so
%{_libdir}/python*/site-packages/*.py*
%{_libdir}/python*/site-packages/__pycache__/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libtdb.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libtdb.so
%{_prefix}/lib/pkgconfig/tdb.pc
%endif
