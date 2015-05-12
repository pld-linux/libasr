Summary:	Free, simple and portable asynchronous resolver library
Name:		libasr
Version:	1.0.1
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://www.opensmtpd.org/archives/%{name}-%{version}.tar.gz
# Source0-md5:	ca46c5f24846598f9fd2322c265f5313
URL:		https://github.com/OpenSMTPD/libasr
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

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files and libraries for developing
with %{name}.

%prep
%setup -q

%build
%configure \
	--enable-shared \
	--disable-static \
	--with-mantype=man

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libasr.la

# FIXME: somehow libtool installs this with -m 644
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libasr.so.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENCE README.md
%attr(755,root,root) %{_libdir}/libasr.so.*.*.*
%ghost %{_libdir}/libasr.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/asr.h
%{_libdir}/libasr.so
