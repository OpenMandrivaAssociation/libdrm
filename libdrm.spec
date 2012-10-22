%define major 2
%define libname %mklibname drm %{major}
%define develname %mklibname drm -d

%define kms_major 1
%define libkms %mklibname kms %{kms_major}
%ifarch %{ix86} x86_64
%define intel_major 1
%define libintel %mklibname drm_intel %{intel_major}
%endif
%define nouveau_major 2
%define libnouveau %mklibname drm_nouveau %{nouveau_major}
%define radeon_major 1
%define libradeon %mklibname drm_radeon %{radeon_major}

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.39
Release:	1
Group:		System/Libraries
License:	MIT/X11
URL:		http://xorg.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source1:	91-drm-modeset.rules

# Revert nouveau api so mesa 7.10.1 can build:
# Patch0050: 0050-revert-nouveau-split-pushbuf-macros.patch

# Backports from git:

# (from mageia) Revert nouveau merge to allow mesa build.
Patch0900:	0900-Revert-nouveau-silence-some-remaining-valgrind-warni.patch
Patch0901:	0901-Revert-nouveau-fix-channel-closing.patch
Patch0902:	0902-Revert-nouveau-expose-notifier-handle-on-nvc0-as-wel.patch
Patch0903:	0903-Revert-nouveau-remove-unnecessary-EAGAIN-loops.patch
Patch0904:	0904-Revert-nouveau-init-nvc0-channel-alloc-req-structure.patch



Patch0100:	0100-RH-libdrm-make-dri-perms-okay-v1.1.patch
# Do not try proc for backward Linux compatibility:
Patch0101:	0101-RH-libdrm-2.4.0-no-bc-v1.3.patch

Patch0500:	0500-improve-waiting-for-dri-device-to-appear-when-system.patch

Patch1005:	libdrm_mips_drm_cas.patch
Patch1006:	libdrm_mips_sarea_max.patch

Patch3000:	libdrm-2.4.19-fix-linking.patch

BuildRequires:	kernel-headers >= 1:2.6.27.4-3mnb2
BuildRequires:	libpthread-stubs
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	udev-devel
BuildRequires:	libpciaccess-devel
Conflicts:	kernel-headers <= 1:2.6.27.4-2mnb2

%description
Userspace interface to kernel DRM services

%package	common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		System/Libraries

%description	common
Common files for the userspace interface to kernel DRM services

%package -n	%{libname}
Summary:	Userspace interface to kernel DRM services
Group:		System/Libraries
Provides:	%{name} = %{version}
Requires:	%{name}-common

%description -n	%{libname}
Userspace interface to kernel DRM services

%package -n	%{libkms}
Summary:	Shared library for KMS
Group:		System/Libraries

%description -n	%{libkms}
Shared library for kernel mode setting.

%ifarch %{ix86} x86_64
%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n	%{libintel}
Shared library for Intel kernel Direct Rendering Manager services.
%endif

%package -n	%{libnouveau}
Summary:	Shared library for Nouveau kernel DRM services
Group:		System/Libraries

%description -n	%{libnouveau}
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
Requires:	%{libkms} = %{version}
%ifarch %{ix86} x86_64
Requires:	%{libintel} = %{version}
%endif
Requires:	%{libnouveau} = %{version}
Requires:	%{libradeon} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}drm2-devel
Obsoletes:	%{_lib}drm-static-devel
Obsoletes:	drm-nouveau-devel < 2.3.0-2.20090111.2

%description -n	%{develname}
Development files for %{name}

%prep
%setup -q
%apply_patches
# Needed for patch4
autoreconf -fv --install

%build
%configure2_5x \
    --enable-udev \
%ifnarch %{ix86} x86_64
    --disable-intel \
%endif
    --enable-nouveau-experimental-api

%make

%install
%makeinstall_std 
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/

# (cg) Note that RH remove drm.h drm_mode.h drm_sarea.h r300_reg.h via_3d_reg.h
# and we should perhaps do the same? (previous attempts have not gone well :)

%files common
%{_sysconfdir}/udev/rules.d/91-drm-modeset.rules

%files -n %{libname}
%{_libdir}/libdrm.so.%{major}*

%files -n %{libkms}
%{_libdir}/libkms.so.%{kms_major}*

%ifarch %{ix86} x86_64
%files -n %{libintel}
%{_libdir}/libdrm_intel.so.%{intel_major}*
%endif

%files -n %{libnouveau}
%{_libdir}/libdrm_nouveau.so.%{nouveau_major}*

%files -n %{libradeon}
%{_libdir}/libdrm_radeon.so.%{radeon_major}*

%files -n %{develname}
%{_includedir}/libdrm
%{_includedir}/libkms
%{_includedir}/*.h
%{_libdir}/libdrm*.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm*.pc
%{_libdir}/pkgconfig/libkms*.pc
