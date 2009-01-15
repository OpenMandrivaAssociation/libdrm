%define major 2
%define libname %mklibname drm %{major}
%define develname %mklibname drm -d
%define staticdevelname %mklibname drm -d -s

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.4
Release:	%mkrel 1
Group:		Development/X11
License:	MIT/X11
URL:		http://xorg.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source1: 91-drm-modeset.rules
Source2: i915modeset

Patch0001:  0001-RH-libdrm-make-dri-perms-okay-v1.1.patch
Patch0002:  0002-RH-libdrm-2.4.0-no-bc-v1.3.patch
Patch0003:  0003-RH-libdrm-radeon-v1.3.patch

BuildRequires:	kernel-headers >= 1:2.6.27.4-3mnb2
BuildRequires:	libpthread-stubs
BuildRequires:	x11-util-macros >= 1.0.1
Conflicts:	kernel-headers <= 1:2.6.27.4-2mnb2
BuildRoot:	%{_tmppath}/%{name}-root

%description
Userspace interface to kernel DRM services

%package common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		Development/X11

%description common
Common files for the userspace interface to kernel DRM services

%package -n	%{libname}
Summary:	Userspace interface to kernel DRM services
Group:		Development/X11
Provides:	%{name} = %{version}
Requires: %{name}-common

%description -n	%{libname}
Userspace interface to kernel DRM services

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{name} >= %{version}
Requires:	%{libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{mklibname drm 2 -d}

%description -n	%{develname}
Development files for %{name}

%package -n	%{staticdevelname}
Summary:	Static development files for %{name}
Group:		Development/X11
Requires:	%{name}-devel >= %{version}
Requires:	%{libname} = %{version}
Provides:       %{name}-static-devel = %{version}-%{release}
Obsoletes:      %{mklibname drm 2 -d -s}

%description -n	%{staticdevelname}
Static development files for %{name}

%prep

%setup -q
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

%build
# (cg) Needed for radeon stuff
autoreconf -v --install || exit 1
%configure2_5x \
    --enable-udev \
    --enable-static

%make

%install
rm -rf %{buildroot}

%makeinstall_std 
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/modprobe.d/

find %{buildroot} -type f -name '*.la' -exec rm -f {} \;

# (cg) Note that RH remove drm.h drm_mode.h drm_sarea.h r300_reg.h via_3d_reg.h
# and we should perhaps do the same? (previous attempts have not gone well :)

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files common
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/91-drm-modeset.rules
%{_sysconfdir}/modprobe.d/i915modeset

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/drm/*.h
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/*.a
