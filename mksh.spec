Summary:	Free implementation of the Korn Shell
Name:		mksh
Version:	49
Release:	2
License:	BSD
Group:		Core/Shells
Source0:	http://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-R%{version}.tgz
# Source0-md5:	e8c205cac72c3dc8540bbc3897421422
Source1:	%{name}-mkshrc
Patch0:		%{name}-mkshrc_support.patch
Patch1:		%{name}-no_stop_alias.patch
URL:		https://www.mirbsd.org/mksh.htm
BuildRequires:	perl-base
BuildRequires:	sed
Requires(pre):	FHS
# compat links
Provides:	/bin/sh
Provides:	/bin/mksh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mksh is a command interpreter intended for both interactive and shell
script use. Its command language is a superset of the sh(C) shell
language and largely compatible to the original Korn shell.

%prep
%setup -qcT
gzip -dc %{SOURCE0} | cpio -mid
mv mksh/* .; rmdir mksh

%patch0 -p0
%patch1 -p1

%build
install -d out

CC="%{__cc}" \
CFLAGS="%{rpmcflags} -DMKSH_GCC55009" \
LDFLAGS="%{rpmldflags}" \
CPPFLAGS="%{rpmcppflags}" \
sh ./Build.sh -Q -r -j -c lto

%check
#./test.sh -v $skip_tests

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_mandir}/man1}
install -p mksh $RPM_BUILD_ROOT%{_bindir}

cp -a mksh.1 $RPM_BUILD_ROOT%{_mandir}/man1/mksh.1
echo ".so mksh.1" > $RPM_BUILD_ROOT%{_mandir}/man1/sh.1

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mkshrc

ln -sf mksh $RPM_BUILD_ROOT%{_bindir}/sh

# some pdksh scripts used that
ln -sf mksh $RPM_BUILD_ROOT%{_bindir}/ksh

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p %add_etc_shells -p /bin/sh /usr/bin/sh /usr/bin/ksh /usr/bin/mksh
%preun  -p %remove_etc_shells -p /bin/sh /usr/bin/sh /usr/bin/ksh /usr/bin/mksh

%posttrans -p %add_etc_shells -p /bin/sh /usr/bin/sh /usr/bin/ksh

%files
%defattr(644,root,root,755)
%doc dot.mkshrc
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mkshrc
%attr(755,root,root) %{_bindir}/mksh
%attr(755,root,root) %{_bindir}/ksh
%attr(755,root,root) %{_bindir}/sh
%{_mandir}/man1/mksh.1*
%{_mandir}/man1/sh.1*

