%define tdbmajor	1
%define version		1.2.9
%define epoch 1

%define libtdb %mklibname tdb %tdbmajor
%define tdbdevel %mklibname -d tdb

%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} \
rm -Rf $GNUPGHOME \


Name: tdb
Version: %version
# We shipped it in samba3 versioned with the samba3 version
Epoch: %epoch
Release: %mkrel 2
Group: System/Libraries
License: GPLv2
URL: http://tdb.samba.org/
Summary: Library implementing Samba's embedded database
Source: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
Source1: http://samba.org/ftp/tdb/tdb-%{version}.tar.asc
Source2: tridge.asc
BuildRequires: python-devel xsltproc docbook-style-xsl
BuildRoot: %{_tmppath}/%{name}-root

%description
Library implementing Samba's embedded database and utilities for backing up,
restoring and manipulating the database.

%package -n %libtdb
Group: System/Libraries
Summary: Library implementing Samba's embedded database

%description -n %libtdb
Library implementing Samba's embedded database

%package -n tdb-utils
Group: Databases
Summary: Tools for backing up, restoring, and manipulating Samba's embedded database
Conflicts: samba-server < 3.3.2-2

%description -n tdb-utils
Tools for backing up, restoring, and manipulating Samba's embedded database

%package -n %tdbdevel
Group: Development/C
Summary: Library implementing Samba's embedded database
Provides: tdb-devel = %{epoch}:%{version}-%{release}
#Version: %version
Requires: %libtdb = %{epoch}:%{version}-%{release}
# because /usr/include/tdb.h was moved from libsmbclient0-devel to libtdb-devel
Conflicts: %{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %tdbdevel
Library implementing Samba's embedded database

%package -n python-tdb
Group: Development/Python
Summary: Python bindings to Samba's tdb embedded database

%description -n python-tdb
Pyhton bindings to Samba's tdb embedded database

%prep
#Try and validate signatures on source:
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE

%check_sig %{SOURCE2} %{SOURCE1} $VERIFYSOURCE

rm -f $VERIFYSOURCE

%setup -q

%build
export PYTHONDIR=%{py_platsitedir}
%configure2_5x	--disable-rpath
%make

%install
rm -Rf %{buildroot}
%makeinstall_std
#ln -s libtdb.so.%{tallocmajor} %{buildroot}/%{_libdir}/libtdb.so

%clean
rm -Rf %{buildroot}

%files -n %libtdb
%defattr(-,root,root)
%{_libdir}/libtdb.so.%{tdbmajor}*

%files -n %tdbdevel
%defattr(-,root,root)
%{_libdir}/libtdb.so
#{_libdir}/libtdb.a
%{_includedir}/tdb.h
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-utils
%defattr(-,root,root)
%{_bindir}/tdb*
%{_mandir}/man8/tdb*.8*

%files -n python-tdb
%defattr(-,root,root)
%{py_platsitedir}/tdb.so
