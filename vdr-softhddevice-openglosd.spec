# https://github.com/louisbraun/softhddevice-openglosd/commit/569fde5dce6750eabcd889d07b3298d5764fce34 
%global commit  569fde5dce6750eabcd889d07b3298d5764fce34
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20160717

Name:           vdr-softhddevice-openglosd
Version:        0.6.1
Release:        11.%{gitdate}git%{shortcommit}%{?dist}
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

BuildRequires:  vdr-devel >= 1.7.22
BuildRequires:  gettext
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  freeglut-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  glm-devel
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
%patch2 -p1

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
