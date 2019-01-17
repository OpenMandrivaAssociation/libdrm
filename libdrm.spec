%define major 2
%define libname %mklibname drm %{major}
%define devname %mklibname drm -d

%define kms_major 1
%define libkms %mklibname kms %{kms_major}
%define intel_major 1
%define libintel %mklibname drm_intel %{intel_major}
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
# vc4
%define vc4_major 0
%define libvc4 %mklibname drm_vc4 %{vc4_major}
# etnaviv
%define etnaviv_major 1
%define libetnaviv %mklibname drm_etnaviv %{etnaviv_major}

%global optflags %{optflags} -O3

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.96
Release:	3
Group:		System/Libraries
License:	MIT/X11
Url:		http://dri.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source1:	91-drm-modeset.rules
# hardcode the 666 instead of 660 for device nodes
Patch3:		libdrm-make-dri-perms-okay.patch
Patch6:		drm-update-arm.patch

# For building man pages
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd42-xml
BuildRequires:	xsltproc
BuildRequires:	kernel-release-headers
BuildRequires:	pkgconfig(pthread-stubs)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xorg-macros)
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	meson

%description
Userspace interface to kernel DRM services.

%package	common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		System/Libraries
Requires:	coreutils

%description	common
Common files for the userspace interface to kernel DRM services.

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

%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries

%description -n	%{libintel}
Shared library for Intel kernel Direct Rendering Manager services.

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

# For now (2.4.70), VC4 is just a set of headers - no binary built
#
#vc4
#
%package -n	%{libvc4}
Summary:	Shared library for Broadcom VC4 kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libvc4}
Shared library for Broadcom VC4 kernel Direct Rendering Manager services.

#
#etnaviv
#
%package -n	%{libetnaviv}
Summary:	Shared library for Etnaviv kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libetnaviv}
Shared library for Etnaviv kernel Direct Rendering Manager services.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{version}
Requires:	%{libkms} = %{version}
%ifarch %{ix86} %{x86_64}
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
Requires:	%{libetnaviv} = %{version}
%if 0
Requires:	%{libvc4} = %{version}
%endif
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}drm-static-devel

%description -n	%{devname}
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson \
%ifarch %{ix86} %{x86_64}
	-Dintel=true \
%else
	-Dintel=false \
%endif
%ifarch %{armx}
	-Domap=true \
	-Dexynos=true \
	-Dfreedreno=true \
	-Dtegra=true \
	-Detnaviv=true \
	-Dvc4=true \
%else
	-Domap=false \
	-Dexynos=false \
	-Dfreedreno=false \
	-Dtegra=false \
	-Detnaviv=false \
	-Dvc4=false \
%endif
	-Dradeon=true \
	-Damdgpu=true \
	-Dnouveau=true \
	-Dlibkms=true

%meson_build

%install
%meson_install

install -m644 %{SOURCE1} -D %{buildroot}/lib/udev/rules.d/91-drm-modeset.rules

%files common
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.ids
/lib/udev/rules.d/91-drm-modeset.rules

%files -n %{libname}
%{_libdir}/libdrm.so.%{major}*

%files -n %{libkms}
%{_libdir}/libkms.so.%{kms_major}*

%ifarch %{ix86} %{x86_64}
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

%files -n %{libetnaviv}
%{_libdir}/libdrm_etnaviv.so.%{etnaviv_major}*

# No binary yet, but the headers are useful
%if 0
%files -n %{libvc4}
%{_libdir}/libdrm_vc4.so.%{vc4_major}*
%endif
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
