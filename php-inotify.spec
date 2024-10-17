%define modname inotify
%define soname %{modname}.so
%define inifile A82_%{modname}.ini

Summary:	Provides inotify functions for PHP
Name:		php-%{modname}
Version:	0.1.6
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/inotify/
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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.6-1mdv2012.0
+ Revision: 797148
- 0.1.6
- rebuild for php-5.4.x
- remove broken source
- 0.1.5

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-14
+ Revision: 761261
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-13
+ Revision: 696437
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-12
+ Revision: 695412
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-11
+ Revision: 646654
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-10mdv2011.0
+ Revision: 629816
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-9mdv2011.0
+ Revision: 628137
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-8mdv2011.0
+ Revision: 600501
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-7mdv2011.0
+ Revision: 588839
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-6mdv2010.1
+ Revision: 514564
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-5mdv2010.1
+ Revision: 485398
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-4mdv2010.1
+ Revision: 468180
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-3mdv2010.0
+ Revision: 451284
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1.4-2mdv2010.0
+ Revision: 397542
- Rebuild

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-1mdv2010.0
+ Revision: 377658
- 0.1.4 (fixes build with php-5.3.x)
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-5mdv2009.1
+ Revision: 346508
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-4mdv2009.1
+ Revision: 341770
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-3mdv2009.1
+ Revision: 321811
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-2mdv2009.1
+ Revision: 310280
- rebuilt against php-5.2.7

* Thu Nov 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-1mdv2009.1
+ Revision: 300262
- 0.1.3

* Tue Oct 28 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2009.1
+ Revision: 297808
- import php-inotify


* Tue Oct 28 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2009.0
- initial Mandriva package
