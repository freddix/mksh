Summary:	MirBSD Korn Shell
Name:		mksh
Version:	46
Release:	1
License:	BSD
Group:		Applications/Shells
Source0:	http://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-R%{version}.tgz
# Source0-md5:	77c108d8143a6e7670954d77517d216d
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
mksh is the MirBSD enhanced version of the Public Domain Korn shell
(pdksh), a Bourne-compatible shell which is largely similar to the
original AT&T Korn shell. It includes bug fixes and feature
improvements in order to produce a modern, robust shell good for
interactive and especially script use. It has UTF-8 support in the
emacs command line editing mode; corresponds to OpenBSD 4.2-current
ksh sans GNU bash-like $PS1; the build environment requirements are
autoconfigured; throughout code simplification/bugfix/enhancement has
been done, and the shell has extended compatibility to other modern
shells.

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

# skip some tests if not on terminal
if ! tty -s; then
	skip_tests="-C regress:no-ctty"
fi

%check
#./test.sh -v $skip_tests

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_mandir}/man1}
install -p mksh $RPM_BUILD_ROOT%{_bindir}

cp -a mksh.1 $RPM_BUILD_ROOT%{_mandir}/man1/mksh.1
echo ".so mksh.1" > $RPM_BUILD_ROOT%{_mandir}/man1/sh.1

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mkshrc

#ln -sf /usr/bin/mksh $RPM_BUILD_ROOT/bin/sh
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
#%attr(755,root,root) /bin/sh
%{_mandir}/man1/mksh.1*
%{_mandir}/man1/sh.1*

