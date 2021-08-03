# https://github.com/louisbraun/softhddevice-openglosd/commit/569fde5dce6750eabcd889d07b3298d5764fce34 
%global commit  569fde5dce6750eabcd889d07b3298d5764fce34
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20160717

%if 0%{?fedora} > 27
%bcond_without  compat_ffmpeg
%else
%bcond_with     compat_ffmpeg
%endif

Name:           vdr-softhddevice-openglosd
Version:        0.6.1
Release:        31.%{gitdate}git%{shortcommit}%{?dist}
Summary:        A software and GPU emulated HD output device plugin for VDR

License:        AGPLv3
URL:            http://projects.vdr-developer.org/projects/plg-softhddevice
Source0:        https://github.com/louisbraun/softhddevice-openglosd/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Configuration files for plugin parameters. These are Fedora specific and not in upstream.
Source1:        %{name}.conf
# http://projects.vdr-developer.org/issues/1417
Patch0:         exit-crash.patch
# http://projects.vdr-developer.org/issues/1916
Patch1:         chartype.patch
# https://projects.vdr-developer.org/issues/2424
Patch2:         ffmpeg_2.9.patch

BuildRequires:  gcc-c++
BuildRequires:  vdr-devel >= 1.7.22
BuildRequires:  gettext
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  alsa-lib-devel
%if %{with compat_ffmpeg}
BuildRequires: compat-ffmpeg28-devel
%else
BuildRequires:  ffmpeg-devel
%endif
BuildRequires:  freeglut-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  glm-devel >= 0.9.8.4-5
BuildRequires:  glew-devel
BuildRequires:  freetype-devel
Requires:       vdr(abi)%{?_isa} = %{vdr_apiversion}
Requires:       xorg-x11-server-Xorg

%description
A software and GPU emulated HD output device plugin for VDR.
With this version of the plugin softhddevice an OpenGL accelerated
OSD output was added. That works only with VDPAU output on NVidia cards.

    Video decoder CPU / VDPAU
    Video output VDPAU
    Audio FFMpeg / Alsa / Analog
    Audio FFMpeg / Alsa / Digital
    Audio FFMpeg / OSS / Analog
    HDMI/SPDIF pass-through
    Software volume, compression, normalize and channel resample
    VDR ScaleVideo API
    Software deinterlacer Bob (VA-API only)
    Autocrop
    Grab image (VDPAU only)
    Suspend / Dettach
    Letterbox, Stretch and Center cut-out video display modes
    atmo light support with plugin http://github.com/durchflieger/DFAtmo
    PIP (Picture-in-Picture) (VDPAU only)


%prep
%setup -qn softhddevice-openglosd-%{commit}
%patch0 -p1
%patch1 -p0
%if ! %{with compat_ffmpeg}
%patch2 -p1
%endif

# remove .git files and Gentoo files
rm -f .indent.pro .gitignore .gitattributes
rm -f vdr-softhddevice-9999.ebuild vdr-softhddevice-9999-pre1.7.36.ebuild

for f in ChangeLog README.txt; do
  iconv -f iso8859-1 -t utf-8 $f >$f.conv
  touch -r $f $f.conv
  mv $f.conv $f
done
mv README.txt README

%build
%if %{with compat_ffmpeg}
export PKG_CONFIG_PATH=%{_libdir}/compat-ffmpeg28/pkgconfig
%endif
make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" %{?_smp_mflags}

%install
%make_install
install -Dpm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/softhddevice.conf
%find_lang vdr-softhddevice

%files -f vdr-softhddevice.lang
%{vdr_plugindir}/libvdr-softhddevice.so.%{vdr_apiversion}
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/softhddevice.conf
%doc ChangeLog README
%license AGPL-3.0.txt

%changelog
* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-31.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-30.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-29.20160717git569fde5
- Rebuilt for new VDR API version

* Wed Oct 21 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-28.20160717git569fde5
- Rebuilt for new VDR API version

* Fri Aug 28 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-27.20160717git569fde5
- Rebuilt for new VDR API version

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-26.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-25.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-24.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-23.20160717git569fde5
- Rebuilt for new VDR API version 2.4.1

* Tue Jun 18 2019 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-22.20160717git569fde5
- Rebuilt for new VDR API version

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-21.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 0.6.1-20.20160717git569fde5
- Add BuildRequires: gcc-c++

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 0.6.1-19.20160717git569fde5
- Rebuild for glew 2.1.0

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-18.20160717git569fde5
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.6.1-17.20160717git569fde5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-16.20160717git569fde5
- Rebuilt for vdr-2.4.0

* Mon Feb 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-15.20160717git569fde5
- Use compat-ffmpeg28 for F28

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-14.20160717git569fde5
- Rebuilt for ffmpeg-3.5 git

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.6.1-13.20160717git569fde5
- Rebuilt for VA-API 1.0.0

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-12.20160717git569fde5
- Rebuild for ffmpeg update

* Tue Jul 19 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-11.20160717git569fde5
- update for new git snapshot

* Tue Jun 28 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-10.20160607gitdc8740b
- Added ffmpeg_2.9.patch

* Fri Jun 10 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-9.20160607gitdc8740b
- update for new git snapshot

* Tue Mar 29 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-8.20160327gitfd3db0b
- update for new git snapshot

* Sun Jan 31 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-7.20160131gitefd60c8
- first build of softhddevice-openglosd version
