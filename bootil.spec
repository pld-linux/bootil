Summary:	Garry Newman's utility library
Summary(pl.UTF-8):	Biblioteka narzędziowa Garry'ego Newmana
Name:		bootil
Version:	0
%define	snap	20140109
Release:	0.%{snap}.1
# URL says: "My personal utility library, feel free to steal :)"
License:	unknown (free)
Group:		Libraries
# git clone https://github.com/garrynewman/bootil
# tar cJ --exclude=.git -f bootil.tar.xz
Source0:	%{name}.tar.xz
# Source0-md5:	fcbf821466349cc3d91f362fea8bd9de
Patch0:		%{name}-includes.patch
URL:		https://github.com/garrynewman/bootil
BuildRequires:	libstdc++-devel
BuildRequires:	premake >= 4
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Garry Newman's utility library.

%description -l pl.UTF-8
Biblioteka narzędziowa Garry'ego Newmana.

%package devel
Summary:	Header files for Bootil library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Bootil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Bootil library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Bootil.

%prep
%setup -q -n bootil
%patch -P0 -p1

%{__sed} -i -e 's/bootil_static/bootil/;s/StaticLib/SharedLib/' projects/bootil.lua

%build
cd projects
premake4 gmake
LDFLAGS="%{rpmldflags}" \
%{__make} -C linux/gmake \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS='%{rpmcflags} %{rpmcppflags} $(CPPFLAGS) $(ARCH) -ffast-math -fPIC' \
	verbose=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

install -D lib/linux/gmake/libbootil.so $RPM_BUILD_ROOT%{_libdir}/libbootil.so
cp -pr include/Bootil $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbootil.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/Bootil
