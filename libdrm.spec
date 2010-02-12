%define major 2
%define libname %mklibname drm %{major}
%define develname %mklibname drm -d
%define staticdevelname %mklibname drm -d -s

%define intel_major 1
%define libintel %mklibname drm_intel %{intel_major}
%define nouveau_major 1
%define libnouveau %mklibname drm_nouveau %{nouveau_major}
%define radeon_major 1
%define libradeon %mklibname drm_radeon %{radeon_major}

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.17
Release:	%mkrel 6
Group:		System/Libraries
License:	MIT/X11
URL:		http://xorg.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source1: 91-drm-modeset.rules

# Patches from upstream:
# 050 and 051 are from fd.o bug #25912 (reported on irc)
Patch0050: 0050-retry-getsources-if-hotplug.patch
Patch0051: 0051-retry-getconnector-if-hotplug.patch
# 052 should prevent gpu hangups
Patch0052: 0052-handle-resetting-of-input-params.patch
# 053 prevents oops and hangs
Patch0053: 0053-intel-account-for-potential-pinned-buffers.patch


Patch0100:  0100-RH-libdrm-make-dri-perms-okay-v1.1.patch
# Do not try proc for backward Linux compatibility:
Patch0101:  0101-RH-libdrm-2.4.0-no-bc-v1.3.patch

Patch0500:  0500-improve-waiting-for-dri-device-to-appear-when-system.patch

Patch1005:     libdrm_mips_drm_cas.patch
Patch1006:     libdrm_mips_sarea_max.patch

# nouveau commits from upstream
Patch2001:	0001-nouveau-Update-nouveau_class.h-with-new-renouveau.xm.patch
Patch2002:	0002-nouveau-Update-some-object-definitions-from-renouvea.patch
Patch2003:	0003-nouveau-Unreference-pushbuf-objects-on-channel-destr.patch
Patch2004:	0004-nouveau-add-BEGIN_RING_NI.patch
Patch2005:	0005-nouveau-Update-nouveau_class.h.patch
Patch2006:	0006-nouveau-fix-memory-leak-in-nouveau_channel_free.patch
Patch2007:	0007-nouveau-disable-flush_notify-on-channel_free.patch
Patch2008:	0008-nouveau-fail-channel-creation-if-pushbuf-init-fails.patch
Patch2009:	0009-nouveau-add-nouveau_resource_destroy.patch
Patch2010:	0010-nouveau-Regenerate-nouveau_class.h.patch

BuildRequires:	kernel-headers >= 1:2.6.27.4-3mnb2
BuildRequires:	libpthread-stubs
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires: udev-devel
Conflicts:	kernel-headers <= 1:2.6.27.4-2mnb2
BuildRoot:	%{_tmppath}/%{name}-root

%description
Userspace interface to kernel DRM services

%package common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		System/Libraries

%description common
Common files for the userspace interface to kernel DRM services

%package -n	%{libname}
Summary:	Userspace interface to kernel DRM services
Group:		System/Libraries
Provides:	%{name} = %{version}
Requires: %{name}-common

%description -n	%{libname}
Userspace interface to kernel DRM services

%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libintel}
Shared library for Intel kernel Direct Rendering Manager services.

%package -n	%{libnouveau}
Summary:	Shared library for Nouveau kernel DRM services
Group:		System/Libraries

%description -n %{libnouveau}
Shared library for Nouveau kernel Direct Rendering Manager services.

%package -n	%{libradeon}
Summary:	Shared library for Radeon kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libradeon}
Shared library for Radeon kernel Direct Rendering Manager services.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{version}
Requires:	%{libintel} = %{version}
Requires:	%{libnouveau} = %{version}
Requires:	%{libradeon} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{mklibname drm 2 -d}
Obsoletes:	drm-nouveau-devel < 2.3.0-2.20090111.2

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
%apply_patches

%build
# Needed for patch4
autoreconf -fv --install
%configure2_5x \
    --enable-udev \
    --enable-static \
    --enable-nouveau-experimental-api \
    --enable-radeon-experimental-api

%make

%install
rm -rf %{buildroot}

%makeinstall_std 
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/

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

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libdrm.so.%{major}*

%files -n %{libintel}
%defattr(-,root,root)
%{_libdir}/libdrm_intel.so.%{intel_major}*

%files -n %{libnouveau}
%defattr(-,root,root)
%{_libdir}/libdrm_nouveau.so.%{nouveau_major}*

%files -n %{libradeon}
%defattr(-,root,root)
%{_libdir}/libdrm_radeon.so.%{radeon_major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/drm
%{_includedir}/nouveau
%{_includedir}/*.h
%{_libdir}/libdrm*.so
%{_libdir}/pkgconfig/libdrm*.pc

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/*.a
