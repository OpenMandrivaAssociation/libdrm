%define major 2
%define libname %mklibname drm %{major}
%define devname %mklibname drm -d

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
# amdgpu
%define amdgpu_major 1
%define libamdgpu %mklibname drm_amdgpu %{amdgpu_major}
# exynos
%define exynos_major 1
%define libexynos %mklibname drm_exynos %{exynos_major}
# adreno
%define freedreno_major 1
%define libfreedreno %mklibname drm_freedreno %{freedreno_major}
# omap
%define omap_major 1
%define libomap %mklibname drm_omap %{omap_major}
# tegra
%define tegra_major 0
%define libtegra %mklibname drm_tegra %{tegra_major}

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.67
Release:	2
Group:		System/Libraries
License:	MIT/X11
Url:		http://dri.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source1:	91-drm-modeset.rules
# Backports from git:
# hardcode the 666 instead of 660 for device nodes
Patch3:		libdrm-make-dri-perms-okay.patch
# remove backwards compat not needed on Fedora
Patch4:		libdrm-2.4.0-no-bc.patch
Patch6:		drm-update-arm.patch

# For building man pages
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	kernel-headers
BuildRequires:	pkgconfig(pthread-stubs)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xorg-macros)

%description
Userspace interface to kernel DRM services.

%package	common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		System/Libraries

%description	common
Common files for the userspace interface to kernel DRM services.

%package -n	%{libname}
Summary:	Userspace interface to kernel DRM services
Group:		System/Libraries
Provides:	%{name} = %{version}
Requires:	%{name}-common

%package -n	%{libkms}
Summary:	Shared library for KMS
Group:		System/Libraries

%description -n	%{libkms}
Shared library for kernel mode setting.

%ifarch %{ix86} x86_64
%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries

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

%package -n	%{libamdgpu}
Summary:	Shared library for AMD GPU kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libamdgpu}
Shared library for AMD GPU kernel Direct Rendering Manager services.

# ARM stuff
%ifarch %{armx}

#
#Samsung Exynos video
#
%package -n	%{libexynos}
Summary:	Shared library for Exynos kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libexynos}
Shared library for Radeon kernel Direct Rendering Manager services.

#
#Free Adreno
#
%package -n	%{libfreedreno}
Summary:	Shared library for Adreno kernel DRM services
Group:		System/Libraries

%description -n %{libfreedreno}
Shared library for Adreno kernel Direct Rendering Manager services.

#
#Omap
#
%package -n	%{libomap}
Summary:	Shared library for OMAP kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libomap}
Shared library for OMAP kernel Direct Rendering Manager services.

#
#tegra
#
%package -n	%{libtegra}
Summary:	Shared library for Tegra kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libtegra}
Shared library for Tegra kernel Direct Rendering Manager services.
%endif

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{version}
Requires:	%{libkms} = %{version}
%ifarch %{ix86} x86_64
Requires:	%{libintel} = %{version}
%endif
Requires:	%{libnouveau} = %{version}
Requires:	%{libradeon} = %{version}
Requires:	%{libamdgpu} = %{version}
%ifarch %{armx}
Requires:	%{libexynos} = %{version}
Requires:	%{libfreedreno} = %{version}
Requires:	%{libomap} = %{version}
Requires:	%{libtegra} = %{version}
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}drm-static-devel

%description -n	%{devname}
Development files for %{name}.

%track
prog %{name} = {
	url = http://dri.freedesktop.org/libdrm/
	regex = %{name}-(__VER__)\.tar\.bz2
	version = %{version}
}

%prep
%setup -q
%apply_patches
# Needed for patch4
autoreconf -fv --install

%build
%configure \
	--enable-udev \
%ifnarch %{ix86} x86_64
	--disable-intel \
%endif
%ifarch %{armx}
	--enable-exynos-experimental-api \
	--enable-freedreno-experimental-api \
	--enable-tegra-experimental-api \
	--enable-omap-experimental-api \
%endif
	--enable-udev

%make

%install
%makeinstall_std

install -m644 %{SOURCE1} -D %{buildroot}/lib/udev/rules.d/91-drm-modeset.rules

# (cg) Note that RH remove drm.h drm_mode.h drm_sarea.h r300_reg.h via_3d_reg.h
# and we should perhaps do the same? (previous attempts have not gone well :)

%files common
/lib/udev/rules.d/91-drm-modeset.rules

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

%files -n %{libamdgpu}
%{_libdir}/libdrm_amdgpu.so.%{amdgpu_major}*

%ifarch %{armx}
%files -n %{libexynos}
%{_libdir}/libdrm_exynos.so.%{exynos_major}*

%files -n %{libfreedreno}
%{_libdir}/libdrm_freedreno.so.%{freedreno_major}*

%files -n %{libomap}
%{_libdir}/libdrm_omap.so.%{omap_major}*

%files -n %{libtegra}
%{_libdir}/libdrm_tegra.so.%{tegra_major}*
%endif

%files -n %{devname}
%{_includedir}/libdrm
%{_includedir}/libkms
%{_includedir}/*.h
%ifarch %{armx}
%{_includedir}/exynos/
%{_includedir}/freedreno/
%{_includedir}/omap/
%endif
%{_libdir}/libdrm*.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm*.pc
%{_libdir}/pkgconfig/libkms*.pc
%{_mandir}/man3/*
%{_mandir}/man7/*
