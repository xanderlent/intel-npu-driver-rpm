Name:		intel-npu-level-zero
Version:	1.5.0
Release:	3%{?dist}
Summary:	Intel Neural Processing Unit Driver for Linux

# MIT license for linux-npu-driver (except firmware and Linux uapi headers)
# MIT license for level-zero-npu-extensions
# Apache 2.0 license for npu_plugin_elf
License:	MIT AND Apache-2.0
URL:		https://github.com/intel/linux-npu-driver
Source:		%{url}/archive/refs/tags/v%{version}.tar.gz
# TODO: Long-term it would be nice to untangle these vendored dependencies
%define lz_npu_exts_version e748c51f87fbe8bdcf9dec9e6f14827be4188599
# v1.5.0 vendors commit 202d62313d776fa13fa14dea7c7ef7bd671c9e74 which does not correspond to any tag or release
Source:		https://github.com/intel/level-zero-npu-extensions/archive/%{lz_npu_exts_version}.tar.gz
%define npu_elf_version npu_ud_2024_24_rc1
# v1.5.0 vendors commit 202d62313d776fa13fa14dea7c7ef7bd671c9e74 which is tagged npu_ud_2024_24_rc1
Source:		https://github.com/openvinotoolkit/npu_plugin_elf/archive/refs/tags/%{npu_elf_version}.tar.gz
Source:		https://github.com/intel/linux-npu-driver/raw/v%{version}/firmware/bin/vpu_37xx_v0.0.bin
Patch:		0001-Fix-the-compilation-issues-from-gcc-14.patch
Patch:		0002-Disable-third-party-googletest-and-yaml-cpp.patch
Patch:		0003-Always-install-firmware-to-lib-fimrware.patch

# TODO: Can this build on non-x86?
ExclusiveArch:	i686 x86_64

# NOTE: This project vendors the drm/ivpu_accel.h header and the DMA-BUF headers
# TODO: Compare vendored headers and switch to using kernel-headers as needed, since the kernel side is upstream.
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	glibc-devel
BuildRequires:	gmock-devel >= 1.13.0
BuildRequires:	gtest-devel >= 1.13.0
BuildRequires:	libudev-devel
# TODO: Only rawhide ships 1.17.2 right now, but that's what upstream has tested against
#BuildRequires:	oneapi-level-zero-devel >= 1.17.2
BuildRequires:	oneapi-level-zero-devel >= 1.16.1
# TODO: maybe higher requirement, but definitely 3.0+
BuildRequires:	openssl-devel >= 3.0.0
BuildRequires:	yaml-cpp-devel >= 0.7.0
# Meteor Lake requires kernel v6.5 or later, Lunar Lake and Arrow Lake require kernel v6.8.12 or later
# TODO: Requires at runtime? Recommends?
#Recommends:	intel-npu-firmware = #{version}
#Requires:	oneapi-level-zero >= 1.16.1

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

%package -n intel-npu-firmware
License:	Redistributable, no modification permitted
Summary:	Intel Neural Processing Unit Firmware
BuildArch:	noarch
# NOTE: Keep the description of the firmware in sync with the main package
# TODO: Do what the upstream package does and auto-reload the NPU kernel module on firmware install?
%description -n intel-npu-firmware
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

%prep
%setup -q -n linux-npu-driver-%{version}
# Now, stitch the two vendored projects that we need into the source tree
%setup -q -n linux-npu-driver-%{version} -T -D -a 1
rmdir third_party/level-zero-vpu-extensions/
mv level-zero-npu-extensions-%{lz_npu_exts_version} third_party/level-zero-vpu-extensions/
cp third_party/level-zero-vpu-extensions/LICENSE.txt LICENSE-level-zero-vpu-extensions.txt
%setup -q -n linux-npu-driver-%{version} -T -D -a 2
rmdir third_party/vpux_elf/
mv npu_plugin_elf-%{npu_elf_version} third_party/vpux_elf
cp third_party/vpux_elf/LICENSE LICENSE-vpux_elf
rm firmware/bin/vpu_37xx_v0.0.bin
cp %{_sourcedir}/vpu_37xx_v0.0.bin firmware/bin/vpu_37xx_v0.0.bin
# Upstream commit ffdc049ca41ad7d8c9555fa95760b7a9f44494a5
# Should appear in the next release, fixes bugs revealed by gcc 14
%patch -P 0 -p1
# Patch out the vendored googletest and yaml-cpp directories
# (these are git submodules and so are empty in the tarball)
# TODO: Work with upstream to handle detecting these libraries in CMake
%patch -P 1 -p1
# Patch CMAKE_INSTALL_LIBDIR to lib/ for firmware
# TODO: Propose this patch to upstream; normally the usage is good but firmware is noarch and so lives with 32-bit code in the 'default' location
%patch -P 2 -p1

%build
%cmake
%cmake_build


%install
%cmake_install

%files
%license LICENSE.md third-party-programs.txt LICENSE-level-zero-vpu-extensions.txt LICENSE-vpux_elf
# TODO: Also include the RPM repo readme?
%doc README.md docs/overview.md security.md
# TODO: Does the unversioned library belong in a -devel package?
%{_libdir}/libze_intel_vpu.so
%{_libdir}/libze_intel_vpu.so.1
%{_libdir}/libze_intel_vpu.so.%{version}

%files tests
%{_bindir}/vpu-kmd-test
%{_bindir}/vpu-umd-test

%files -n intel-npu-firmware
%license firmware/bin/COPYRIGHT
/usr/lib/firmware/updates/intel/vpu/*.bin

%check
%ctest


%changelog
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-3
- Fix vpu_37xx_v0.0.bin being a Git LFS pointer, replace it with the real blob
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-2
- Fix build broken by incorrect paths in various last-minute additions
* Sun Jun 30 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-1
- Intial Release
