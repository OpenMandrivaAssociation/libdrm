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
# exynos
%define exynos_major 1
%define libexynos %mklibname drm_exynos %{exynos_major}
# adreno
%define freedreno_major 1
%define libfreedreno %mklibname drm_freedreno %{freedreno_major}
# omap
%define omap_major 1
%define libomap %mklibname drm_omap %{omap_major}

%bcond_without	uclibc

Summary:	Userspace interface to kernel DRM services
Name:		libdrm
Version:	2.4.60
Release:	1
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
# make rule to print the list of test programs
Patch5:		libdrm-2.4.25-check-programs.patch
Patch6:		drm-update-arm.patch

# For building man pages
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	kernel-headers
BuildRequires:	pkgconfig(pthread-stubs)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xorg-macros)
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

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

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	Userspace interface to kernel DRM services (uClibc build)
Group:		System/Libraries
Requires:	%{name}-common

%description -n	uclibc-%{libname}
Userspace interface to kernel DRM services
%endif

%package -n	%{libkms}
Summary:	Shared library for KMS
Group:		System/Libraries

%description -n	%{libkms}
Shared library for kernel mode setting.

%if %{with uclibc}
%package -n	uclibc-%{libkms}
Summary:	Shared library for KMS (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libkms}
Shared library for kernel mode setting.
%endif

%ifarch %{ix86} x86_64
%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries

%description -n	%{libintel}
Shared library for Intel kernel Direct Rendering Manager services.

%if %{with uclibc}
%package -n	uclibc-%{libintel}
Summary:	Shared library for Intel kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libintel}
Shared library for Intel kernel Direct Rendering Manager services.
%endif
%endif

%package -n	%{libnouveau}
Summary:	Shared library for Nouveau kernel DRM services
Group:		System/Libraries

%description -n	%{libnouveau}
Shared library for Nouveau kernel Direct Rendering Manager services.

%if %{with uclibc}
%package -n	uclibc-%{libnouveau}
Summary:	Shared library for Nouveau kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libnouveau}
Shared library for Nouveau kernel Direct Rendering Manager services.
%endif

%package -n	%{libradeon}
Summary:	Shared library for Radeon kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libradeon}
Shared library for Radeon kernel Direct Rendering Manager services.

%if %{with uclibc}
%package -n	uclibc-%{libradeon}
Summary:	Shared library for Radeon kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libradeon}
Shared library for Radeon kernel Direct Rendering Manager services.
%endif

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

%if %{with uclibc}
%package -n	uclibc-%{libexynos}
Summary:	Shared library for Exynos kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libexynos}
Shared library for Exynos kernel Direct Rendering Manager services.
%endif

#
#Free Adreno
#
%package -n	%{libfreedreno}
Summary:	Shared library for Adreno kernel DRM services
Group:		System/Libraries

%description -n %{libfreedreno}
Shared library for Adreno kernel Direct Rendering Manager services.

%if %{with uclibc}
%package -n	uclibc-%{libfreedreno}
Summary:	Shared library for Adreno kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libfreedreno}
Shared library for Adreno kernel Direct Rendering Manager services.
%endif

#
#Omap
#
%package -n	%{libomap}
Summary:	Shared library for OMAP kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libomap}
Shared library for OMAP kernel Direct Rendering Manager services.

%if %{with uclibc}
%package -n	uclibc-%{libomap}
Summary:	Shared library for OMAP kernel DRM services (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libomap}
Shared library for OMAP kernel Direct Rendering Manager services.
%endif
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
%ifarch %{armx}
Requires:	%{libexynos} = %{version}
Requires:	%{libfreedreno} = %{version}
Requires:	%{libomap} = %{version}
%endif

%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
Requires:	uclibc-%{libkms} = %{version}
%ifarch %{ix86} x86_64
Requires:	uclibc-%{libintel} = %{version}
%endif
Requires:	uclibc-%{libnouveau} = %{version}
Requires:	uclibc-%{libradeon} = %{version}
%ifarch %{armx}
Requires:	uclibc-%{libexynos} = %{version}
Requires:	uclibc-%{libfreedreno} = %{version}
Requires:	uclibc-%{libomap} = %{version}
%endif
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
export CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-shared \
	--disable-static \
	--disable-manpages \
	--enable-udev \
%ifnarch %{ix86} x86_64
	--disable-intel \
%endif
%ifarch %{armx}
	--enable-exynos-experimental-api \
	--enable-freedreno-experimental-api \
	--enable-omap-experimental-api \
%endif
	--enable-udev

%make
popd
%endif

mkdir -p system
pushd system
%configure \
	--enable-udev \
%ifnarch %{ix86} x86_64
	--disable-intel \
%endif
%ifarch %{armx}
	--enable-exynos-experimental-api \
	--enable-freedreno-experimental-api \
	--enable-omap-experimental-api \
%endif
	--enable-udev

%make

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
%endif
%makeinstall_std -C system

install -m644 %{SOURCE1} -D %{buildroot}/lib/udev/rules.d/91-drm-modeset.rules

# (cg) Note that RH remove drm.h drm_mode.h drm_sarea.h r300_reg.h via_3d_reg.h
# and we should perhaps do the same? (previous attempts have not gone well :)

%files common
/lib/udev/rules.d/91-drm-modeset.rules

%files -n %{libname}
%{_libdir}/libdrm.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libdrm.so.%{major}*
%endif

%files -n %{libkms}
%{_libdir}/libkms.so.%{kms_major}*

%if %{with uclibc}
%files -n uclibc-%{libkms}
%{uclibc_root}%{_libdir}/libkms.so.%{kms_major}*
%endif

%ifarch %{ix86} x86_64
%files -n %{libintel}
%{_libdir}/libdrm_intel.so.%{intel_major}*

%if %{with uclibc}
%files -n uclibc-%{libintel}
%{uclibc_root}%{_libdir}/libdrm_intel.so.%{intel_major}*
%endif
%endif

%files -n %{libnouveau}
%{_libdir}/libdrm_nouveau.so.%{nouveau_major}*

%if %{with uclibc}
%files -n uclibc-%{libnouveau}
%{uclibc_root}%{_libdir}/libdrm_nouveau.so.%{nouveau_major}*
%endif

%files -n %{libradeon}
%{_libdir}/libdrm_radeon.so.%{radeon_major}*

%if %{with uclibc}
%files -n uclibc-%{libradeon}
%{uclibc_root}%{_libdir}/libdrm_radeon.so.%{radeon_major}*
%endif

%ifarch %{armx}
%files -n %{libexynos}
%{_libdir}/libdrm_exynos.so.%{exynos_major}*

%files -n %{libfreedreno}
%{_libdir}/libdrm_freedreno.so.%{exynos_major}*

%files -n %{libomap}
%{_libdir}/libdrm_omap.so.%{exynos_major}*

%if %{with uclibc}
%files -n uclibc-%{libexynos}
%{uclibc_root}%{_libdir}/libdrm_exynos.so.%{exynos_major}*

%files -n uclibc-%{libomap}
%{uclibc_root}%{_libdir}/libdrm_omap.so.%{omap_major}*

%files -n uclibc-%{libfreedreno}
%{uclibc_root}%{_libdir}/libdrm_freedreno.so.%{freedreno_major}*
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
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libdrm*.so
%{uclibc_root}%{_libdir}/libkms.so
%endif
%{_libdir}/pkgconfig/libdrm*.pc
%{_libdir}/pkgconfig/libkms*.pc
%{_mandir}/man3/*
%{_mandir}/man7/*
