%define libdrm %mklibname drm 2
Name: libdrm
Summary: Userspace interface to kernel DRM services
Version: 2.3.0
Release: %mkrel 2
Group: Development/X11
License: MIT/X11
URL: http://xorg.freedesktop.org
Source0: http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
# (fc) do not change permission if not requested
Patch0: libdrm-2.3.0-perm.patch
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros >= 1.0.1

%description
Userspace interface to kernel DRM services

#-----------------------------------------------------------
%package -n %{libdrm}
Summary: Userspace interface to kernel DRM services
Group: Development/X11
Provides: %{name} = %{version}

%description -n %{libdrm}
Userspace interface to kernel DRM services

#-----------------------------------------------------------

%package -n %{libdrm}-devel
Summary: Development files for %{name}
Group: Development/X11
Provides: libdrm-devel = %{version}-%{release}
Requires: %{name} >= %{version}

%description -n %{libdrm}-devel
Development files for %{name}

%files -n %{libdrm}-devel
%defattr(-,root,root)
%dir %{_includedir}/drm
%{_includedir}/drm/drm.h
%{_includedir}/drm/drm_sarea.h
%{_includedir}/drm/i915_drm.h
%{_includedir}/drm/mach64_drm.h
%{_includedir}/drm/mga_drm.h
%{_includedir}/drm/r128_drm.h
%{_includedir}/drm/r300_reg.h
%{_includedir}/drm/radeon_drm.h
%{_includedir}/drm/savage_drm.h
%{_includedir}/drm/sis_drm.h
%{_includedir}/drm/via_3d_reg.h
%{_includedir}/drm/via_drm.h
%{_includedir}/xf86drm.h
%{_includedir}/xf86mm.h
%{_libdir}/libdrm.la
%{_libdir}/libdrm.so
%{_libdir}/pkgconfig/libdrm.pc
 
#-----------------------------------------------------------

%package -n %{libdrm}-static-devel
Summary: Static development files for %{name}
Group: Development/X11
Requires: %{name}-devel >= %{version}
Provides: libdrm-static-devel = %{version}-%{release}

%description -n %{libdrm}-static-devel
Static development files for %{name}

%files -n %{libdrm}-static-devel
%defattr(-,root,root)
%{_libdir}/libdrm.a

#-----------------------------------------------------------

%prep
%setup -q -n libdrm-%{version}
%patch0 -p1 -b .perm

%build
%configure2_5x	--x-includes=%{_includedir}\
		--x-libraries=%{_libdir} \
		--enable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std 

%clean
rm -rf %{buildroot}

%post -n %{libdrm} -p /sbin/ldconfig

%postun -n %{libdrm} -p /sbin/ldconfig

%files -n %{libdrm}
%defattr(-,root,root)
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.*


