#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	LibGSSH - friendly GIO wrapper for libssh
Summary(pl.UTF-8):	LibGSSH - przyjazne obudowanie GIO dla libssh
Name:		libgssh
Version:	2014.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgssh/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	8aac1b015961682287bbf37ae324d66a
URL:		https://wiki.gnome.org/Projects/LibGSSH
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	libssh-devel >= 0.6
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.34.0
Requires:	libssh >= 0.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibGSSH wraps libssh (0.6 or newer) with GIO-like friendly
asynchronous API.

%description -l pl.UTF-8
LibGSSH obudowuje libssh (w wersji 0.6 lub nowszej) w przyjazne,
asynchroniczne API w stylu GIO.

%package devel
Summary:	Header files for LibGSSH library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibGSSH
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0

%description devel
Header files for LibGSSH library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibGSSH.

%package static
Summary:	Static LibGSSH library
Summary(pl.UTF-8):	Statyczna biblioteka LibGSSH
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibGSSH library.

%description static -l pl.UTF-8
Statyczna biblioteka LibGSSH.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgssh-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgssh-1.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgssh-1.so
%{_includedir}/libgssh-1
%{_pkgconfigdir}/libgssh-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgssh-1.a
%endif
