%global release_prefix          101

Name:                           ices
Version:                        2.0.3
Release:                        %{release_prefix}%{?dist}
Summary:                        Source streaming for Icecast
License:                        GPLv2
URL:                            https://www.icecast.org
Vendor:                         Package Store <https://pkgstore.github.io>
Packager:                       Kitsune Solar <kitsune.solar@gmail.com>

Source0:                        https://downloads.xiph.org/releases/ices/ices-%{version}.tar.bz2
Source1:                        ices.service
Source2:                        ices.logrotate

BuildRequires:                  gcc
BuildRequires:                  libxml2-devel, libshout-devel >= 2.0, libvorbis-devel
BuildRequires:                  alsa-lib-devel, pkgconfig, zlib-devel, libogg-devel
BuildRequires:                  libtheora-devel, speex-devel, systemd-units
Requires(post):                 systemd-units
Requires(preun):                systemd-units
Requires(postun):               systemd-units

%description
IceS is a source client for a streaming server. The purpose of this client is
to provide an audio stream to a streaming server such that one or more
listeners can access the stream. With this layout, this source client can be
situated remotely from the icecast server.

The primary example of a streaming server used is Icecast 2, although others
could be used if certain conditions are met.

# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------------< SCRIPT >----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

%prep
%setup -q
%{__perl} -pi -e 's|<background>0</background>|<background>1</background>|' conf/*.xml


%build
%configure    \
  --with-ogg  \
  --with-vorbis

%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}

%{__install} -D -m 755 src/ices %{buildroot}%{_bindir}/ices
%{__install} -D -m 644 conf/ices-playlist.xml %{buildroot}%{_sysconfdir}/ices.conf
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ices.service
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/ices
%{__install} -d -m 755 %{buildroot}%{_var}/log/ices


%pre
/usr/sbin/useradd -c "IceS Shoutcast source" \
  -s /sbin/nologin -r -d / ices 2> /dev/null || :


%post
if [[ ${1} -eq 1 ]]; then
  # Initial installation.
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [[ ${1} -eq 0 ]]; then
  # Package removal, not upgrade.
  /bin/systemctl --no-reload disable ices.service > /dev/null 2>&1 || :
  /bin/systemctl stop ices.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [[ ${1} -ge 1 ]]; then
  # Package upgrade, not uninstall.
  /bin/systemctl try-restart ices.service >/dev/null 2>&1 || :
fi

%triggerun -- ices < 2.0.1-13
# Save the current service runlevel info.
# User must manually run systemd-sysv-convert --apply ices
# to migrate them to systemd targets.
/usr/bin/systemd-sysv-convert --save ices >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them.
/sbin/chkconfig --del ices >/dev/null 2>&1 || :
/bin/systemctl try-restart ices.service >/dev/null 2>&1 || :


%files
%doc AUTHORS COPYING doc/*.html doc/*.css conf/*.xml
%{_bindir}/ices
%config(noreplace) %{_sysconfdir}/ices.conf
%config %{_sysconfdir}/logrotate.d/ices
%{_unitdir}/ices.service
%attr(0755,root,ices) %{_var}/log/ices


%changelog
* Fri Jun 18 2021 Package Store <kitsune.solar@gmail.com> - 2.0.3-100
- UPD: Move to Package Store.
- UPD: License.

* Sat Jun 29 2019 MARKETPLACE <uid.marketplace@gmail.com> - 2.0.2-100
- Update from MARKETPLACE.

* Sun Mar 31 2019 Kitsune Solar <kitsune.solar@gmail.com> - 2.0.2-3
- Remove MP3.

* Sun Mar 31 2019 Kitsune Solar <kitsune.solar@gmail.com> - 2.0.2-2
- Enable MP3.

* Tue Jan 15 2019 Kitsune Solar <kitsune.solar@gmail.com> - 2.0.2-1
- New version: 2.0.2.
- Update from MARKETPLACE.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 2.0.1-18
- BR: systemd-units for %%_unitdir (#992560, #1106791)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Jon Ciesla <limburgher@gmail.com> - 2.0.1-13
- Migrate to systemd, BZ 789710.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 23 2010 Paulo Roma <roma@lcg.ufrj.br> - 2.0.1-10
- Removed the non sense serial test.
- Removed service-default-enabled warning.
- Removed non-standard-dir-perm /var/log/ices 0770 warning.
- Removed use-tmp-in-%%pre (changed /tpm for /).
- Fixed %%postun scriptlet failed.
- Fixed status in ices.init.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.1-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.1-6
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Andreas Thienemann <athienem@redhat.com> - 2.0.1-5
- Rebuilt against gcc43

* Wed Mar 07 2007 Andreas Thienemann <andreas@bawue.net> - 2.0.1-4
- Fixed logrotation script to point to the correct file

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.0.1-3
- FE6 Rebuild

* Tue Mar 28 2006 Andreas Thienemann <andreas@bawue.net> 2.0.1-2
- Cleaned up the specfile for FE

* Thu Nov 17 2005 Matt Domsch <Matt_Domsch@dell.com> 2.0.1-1
- add dist tag
- rebuild for FC4

* Mon Jan 31 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:2.0.1-0.iva.0
- Upstream update

* Fri Jan  7 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:2.0.0-0.iva.0
- Retooled for Fedora Core 3
