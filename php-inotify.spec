%define modname inotify
%define soname %{modname}.so
%define inifile A82_%{modname}.ini

Summary:	Provides inotify functions for PHP
Name:		php-%{modname}
Version:	0.1.3
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/inotify/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:  php-devel >= 3:5.2.0
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The inotify extension allows to use inotify functions in a PHP script.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv -f ../package*.xml .

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc tests CREDITS README inotify.php tail.php package.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}