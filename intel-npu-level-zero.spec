Name:		intel-npu-level-zero
Version:	1.16.0
Release:	1%{?dist}
Summary:	Intel Neural Processing Unit Driver for Linux

# MIT license for linux-npu-driver (except firmware and Linux uapi headers)
# MIT license for level-zero-npu-extensions
# Apache 2.0 license for npu_plugin_elf
# TODO: Thoroughly search other files for licenses/headers
License:	MIT AND Apache-2.0
URL:		https://github.com/intel/linux-npu-driver
Source:		%{url}/archive/refs/tags/v%{version}.tar.gz
# this version vendors the below commit which does not correspond to any tag or release in the secondary repo
%define lz_npu_exts_version c0156a3390ae39671ff8f2a6f5471f04bb65bb12
Source:		https://github.com/intel/level-zero-npu-extensions/archive/%{lz_npu_exts_version}.tar.gz
# this version vendors the below commit which should be tagged except Intel forgot to push them for recent releases
%define npu_elf_version ce501d3059c81fd6bd0ad7165ab823838fa5d851
Source:		https://github.com/openvinotoolkit/npu_plugin_elf/archive/%{npu_elf_version}.tar.gz
# Patch out the vendored deps
Patch:		0001-Add-USE_SYSTEM_LIBRARIES-option-for-distro-packagers.patch
# Fix firmware install path to be relative
Patch:		0002-Make-firmware-respect-CMAKE_INSTALL_PREFIX.patch


# TODO: Can this build on non-x86? Can this even build 32-bit? I haven't tested!
ExclusiveArch:	x86_64

BuildRequires:	cmake >= 3.22
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	glibc-devel
BuildRequires:	gmock-devel >= 1.14.0
BuildRequires:	gtest-devel >= 1.14.0
BuildRequires:	oneapi-level-zero-devel >= 1.18.4
# Upstream is using 0.8.0 as of v1.5.1, but with no meaningful updates to upstream code
BuildRequires:	yaml-cpp-devel >= 0.7.0
Provides: bundled(level-zero-npu-extensions)
Provides: bundled(openvino-npu_plugin_elf)

# Tweaked from the upstream README.md.
%description
This is the user space driver for the Intel NPU device. It allows the use
of the Intel NPU via the Level Zero API.

The Intel NPU device is an AI inference accelerator integrated with Intel
client CPUs, starting from the Intel Core Ultra generation of CPUs (CPUs
formerly known as Meteor Lake). It enables energy-efficient execution of
artificial neural network tasks.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).

%package -n intel-npu-firmware-upstream
License:	Redistributable, no modification permitted
Summary:	Intel Neural Processing Unit Firmware
BuildArch:	noarch
Obsoletes:	intel-npu-firmware <= 1.13.0
# NOTE: Keep the description of the firmware in sync with the main package
# TODO: Do what the upstream package does and auto-reload the NPU kernel module on firmware install?
# TODO: Trigger regeneration of initramfs since firmware needs to be included there?
%description -n intel-npu-firmware-upstream
This is the firmware for the Intel NPU device.

The Intel NPU device is an AI inference accelerator integrated with Intel
client CPUs, starting from the Intel Core Ultra generation of CPUs (CPUs
formerly known as Meteor Lake). It enables energy-efficient execution of
artificial neural network tasks.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).


%package tests
License:	MIT AND Apache-2.0
Summary:	Tests for the Intel Neural Processing Unit Driver for Linux
# TODO: Do the tests actually require any of the other parts? Or any deps?
%description tests
Tests for the Intel NPU Driver for Linux.

These programs exercise the kernel-mode (kmd) and user-mode (umd) parts of
the driver.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).

%package devel
License:	MIT AND Apache-2.0
Summary:	Development files for the Intel Neural Processing Unit Driver for Linux
%description devel
Development files for the Intel NPU Driver for Linux.

At present, this is just the unversioned .so file.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).


%prep
%autosetup -p1 -n linux-npu-driver-%{version}
# Now, stitch the two vendored projects that we need into the source tree
%setup -q -n linux-npu-driver-%{version} -T -D -a 1
rmdir third_party/level-zero-npu-extensions/
mv level-zero-npu-extensions-%{lz_npu_exts_version} third_party/level-zero-npu-extensions/
cp third_party/level-zero-npu-extensions/LICENSE.txt LICENSE-level-zero-npu-extensions.txt
cp validation/umd-test/configs/README.md README-umd-test-configs.md
%setup -q -n linux-npu-driver-%{version} -T -D -a 2
rmdir third_party/vpux_elf/
mv npu_plugin_elf-%{npu_elf_version} third_party/vpux_elf
cp third_party/vpux_elf/LICENSE LICENSE-vpux_elf
# Make extension headers reference system headers
# for some reason this worked without changes prior to v1.16.0
sed -i "s/#include \"ze_api.h\"/#include <level_zero\/ze_api.h>/" third_party/level-zero-npu-extensions/ze_graph_ext.h

%build
%cmake -DUSE_SYSTEM_LIBRARIES=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE.md third-party-programs.txt LICENSE-level-zero-npu-extensions.txt LICENSE-vpux_elf
# TODO: Also include the RPM repo readme?
%doc README.md docs/overview.md security.md README-umd-test-configs.md validation/umd-test/configs/basic.yaml
%{_libdir}/libze_intel_npu.so.1
%{_libdir}/libze_intel_npu.so.%{version}

%files devel
%{_libdir}/libze_intel_npu.so

%files tests
%{_bindir}/npu-kmd-test
%{_bindir}/npu-umd-test

%files -n intel-npu-firmware-upstream
%license firmware/bin/COPYRIGHT
/usr/lib/firmware/updates/intel

%check
%ctest


%changelog
* Mon Apr 7 2025 Alexander F. Lent <lx@xanderlent.com> - 1.16.0-1
- Upgrade to latest version
- Rename the intel-npu-firmware package to intel-npu-firmware-upstream
* Sun Mar 9 2025 Alexander F. Lent <lx@xanderlent.com> - 1.13.0-2
- Tweak patches based on upstream feedback.
* Fri Jan 31 2025 Alexander F. Lent <lx@xanderlent.com> - 1.13.0-1
- Uprev to latest upstream version.
- Require new oneapi-level-zero to build, backports available in copr.
- Split unversioned .so into -devel package per fedora review script.
- Modernize setup macro to autosetup now that patches are simpler.
* Wed Jan 1 2025 Alexander F. Lent <lx@xanderlent.com> - 1.10.1-1
- Uprev to latest upstream version.
- Upstream moved firmware file from LFS into repo, so that eliminates some workarounds.
* Sat Nov 9 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-3
- Fix copr import (build should be fine) by unconditionally specifying patchfiles.
* Fri Nov 8 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-2
- Whoops, need to patch the extension headers if building against OneAPI Level Zero >= 1.8
- Apparently they have not tested this since GCC correctly errors out with a type mismatch
  because of the change, so patch the driver to fix the bug.
* Fri Nov 8 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-1
- Update package to the latest released version.
- Allows us to drop a substantial number of patches, including one downstream, yay!
- Requires us to uprev bundled packages and some dependencies.
* Wed Sep 25 2024 Alexander F. Lent <lx@xanderlent.com> - 1.8.0-2
- Update the package to the latest upstream patch, not yet in any release.
- It is just a fix to a documented option we aren't using, but still.
* Wed Sep 18 2024 Alexander F. Lent <lx@xanderlent.com> - 1.8.0-1
- Add some additional documentation files to the package.
- Update the package to the latest upstream release & patch.
* Wed Aug 14 2024 Alexander F. Lent <lx@xanderlent.com> - 1.6.0-2
- Whoops, sources file has special semantics.
* Wed Aug 14 2024 Alexander F. Lent <lx@xanderlent.com> - 1.6.0-1
- Update package to latest upstream release.
- Bump minimum dependency versions where upstream's preferred version is now in Fedora.
* Tue Jul 9 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.1-1
- Update to latest upstream release.
* Thu Jul 4 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-5
- Revert firmware location change, it seems like a deeper bug
- Attempt to also own the other directories that we install like /lib/firmware/updates/intel (etc)
* Thu Jul 4 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-4
- Fix dracut not picking up the NPU/VPU firmware
- Fix a typo in the firmware patch name
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-3
- Fix vpu_37xx_v0.0.bin being a Git LFS pointer, replace it with the real blob
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-2
- Fix build broken by incorrect paths in various last-minute additions
* Sun Jun 30 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-1
- Intial Release
