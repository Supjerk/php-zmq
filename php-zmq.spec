# Define version and release number
%global version @PACKAGE_VERSION@

Name:          php-zmq
Version:       %{version}
Release:       7%{?dist}
Summary:       PHP 0MQ/zmq/zeromq extension
# See https://github.com/mkoppanen/php-zmq/pull/58 for discussion
License:       BSD
Group:         Development/Libraries
URL:           http://github.com/mkoppanen/php-zmq
# Get the source files from https://github.com/mkoppanen/php-zmq/tags
Source:        %{name}-%{version}.tar.gz
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: php-devel
BuildRequires: php-cli
BuildRequires: zeromq-devel >= 2.0.7

Requires:      zeromq >= 2.0.7

%{?filter_setup:
%filter_from_provides /^zmq.so/d
%filter_setup
}

%description
PHP extension for the 0MQ/zmq/zeromq messaging system

%prep
%setup -q -n %{name}-%{version}

%build
/usr/bin/phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__make} install INSTALL_ROOT=%{buildroot}

# Create the ini location
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/php.d

# Preliminary extension ini
echo "extension=zmq.so" > %{buildroot}/%{_sysconfdir}/php.d/zmq.ini

%check
echo "n" | make test

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%doc README LICENSE
%{_libdir}/php/modules/zmq.so
%config(noreplace) %{_sysconfdir}/php.d/zmq.ini

%changelog
* Thu Dec 20 2012 Adrian Siminiceanu <adrian.siminiceanu@gmail.com>
 - Fixed the %filter_from_provides and %filter_setup macros error in EPEL5.
 - Use the version define globally in all the places.
 - Fixed the release number match the number of changes the spec file suffered.
 - Fixed the source to work with the archive files from https://github.com/mkoppanen/php-zmq/tags
 - Added back the cleanup section
 - Added back the buildroot since it does not build anymore on a RH system
* Mon Jul 09 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-5.20120613git516bd6f
 - Fixed the license field back to just "BSD".  The files thought to be
   PHP-licensed were in fact generated by "phpize" in the %%build section.
* Thu Jun 14 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-4.20120613git516bd6f
 - Fixed the private-shared-object-provides for reals with John Ciesla's help.
* Wed Jun 13 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-3.20120613git516bd6f
 - Updated License to BSD and PHP.
 - Removed spurious gcc BuildRequires.
 - Fixed private-shared-object-provides.
* Wed Jun 13 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-2.20120613git516bd6f
 - Using tarball of git checkout since the 0.6.0 release won't build anymore.
 - Using valid shortname for BSD license.
 - Added README and LICENSE to the doc
 - Use %%global instead of %%define.
 - Changed 0MQ to 0MQ/zmq/zeromq in Summary and Description to help with
   search.
 - Fully qualified Source URL.
 - Updated to modern BuildRequires.
 - Separated %%build out into %%build and %%install.
 - Removed unnecessary references to buildroot.
 - Removed unnecessary %%defattr.
 - Changed Group from Web/Applications to Development/Libraries.
 - Removed hardcoded Packager tag.
 - Added %%check section.
 - Marked /etc/php.d/zmq.ini as a config file.
* Wed Jun 15 2011 Rick Moran <moran@morangroup.org>
 - Minor Changes.
* Thu Apr 8 2010 Mikko Koppanen <mkoppanen@php.net>
 - Initial spec file
