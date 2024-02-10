#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Free, simple and portable asynchronous resolver library
Summary(pl.UTF-8):	Wolnodostępna, prosta i przenośna biblioteka asynchronicznego rozwiązywania nazw
Name:		libasr
Version:	1.0.4
Release:	1
License:	ISC, BSD
Group:		Libraries
Source0:	https://www.opensmtpd.org/archives/%{name}-%{version}.tar.gz
# Source0-md5:	ad76b488a19de962efd2e1c57e45a13a
URL:		https://github.com/OpenSMTPD/libasr
# <openssl/opensslv.h> used in openbsd-compat layer
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libasr allows to run DNS queries and perform hostname resolutions in a
fully asynchronous fashion. The implementation is thread-less,
fork-less, and does not make use of signals or other "tricks" that
might get in the developer's way. The API was initially developed for
the OpenBSD operating system, where it is natively supported.

This library is intended to bring this interface to other systems. It
is originally provided as a support library for the portable version
of the OpenSMTPD daemon, but it can be used in any other contexts.

%description -l pl.UTF-8
Libasr pozwala na wykonywanie zapytań DNS i rozwiązywanie nazw hostów
w sposób całkowicie asynchroniczny. Implementacja jest bezwątkowa, nie
tworzy nowych procesów i nie wykorzystuje sygnałów ani innych
"sztuczek", mogących przeszkadzać programistom. API było początkowo
projektowane dla systemu OpenBSD i tam jest obsługiwane natywnie.

Biblitoteka ma na celu dostarczenie tego interfejsu dla innych
systemów. Pierwotnie powstała jako biblioteka wspierająca dla
przenośnej wersji demona OpenSMTPD, ale może być używana także w
innych zastosowaniach.

%package devel
Summary:	Development files for libasr library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libasr
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file for developing with libasr.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia programów z
wykorzystaniem libasr.

%package static
Summary:	Static libasr library
Summary(pl.UTF-8):	Statyczna biblioteka libasr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libasr library.

%description static -l pl.UTF-8
Statyczna biblioteka libasr.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-mantype=man

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libasr.la

# not installed as of 1.0.4
install -d $RPM_BUILD_ROOT%{_mandir}/man3
cp -p src/asr_run.3 $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENCE README.md
%attr(755,root,root) %{_libdir}/libasr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libasr.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasr.so
%{_includedir}/asr.h
%{_mandir}/man3/asr_run.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libasr.a
%endif
