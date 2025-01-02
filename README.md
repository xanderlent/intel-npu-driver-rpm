RPM Packages for the Intel Neural Processing Unit Driver for Linux
==================================================================

This repository provides packages for the Linux user space driver and proprietary firmware for the Intel AI Boost NPU hardware found on Intel Core Ultra processors.

This driver supports the NPU hardware found in Intel Core Ultra (Series 1) and newer (Meteor Lake and newer) processors from Intel. Currently, the Meteor Lake, Arrow Lake, and Lunar Lake NPUs are supported.

It was formerly known as the Intel (Movidius) Versatile Processing Unit (VPU). The Linux kernel driver is upstream as `drivers/accel/ivpu`.

See the [upstream intel/linux-npu-driver repository](https://github.com/intel/linux-npu-driver) for more information about the hardware, firmware, and software.

### Sources

The patches to the source included in this repository can be found at [my downstream fork xanderlent/linux-npu-driver, in the fix-fedora-build-v1.10.1-f41+ tag](https://github.com/xanderlent/linux-npu-driver/tree/fix-fedora-build-v1.10.1-f41+). Also available is [a subset of patches for anyone building on Fedora 40](https://github.com/xanderlent/linux-npu-driver/tree/fix-fedora-build-v1.10.1-f40).

Note that this RPM downloads two vendored source code modules for [intel/level-zero-npu-extensions](https://github.com/intel/level-zero-npu-extensions/) and [openvinotoolkit/npu\_plugin\_elf](https://github.com/openvinotoolkit/npu_plugin_elf/), and integrates them into the source tree to allow the driver to compile. All other vendored modules are either disabled by us or upstream was thoughtful enough to detect if they are already installed.

### Package Availability

[![Copr build status](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/)  
This package is available for use with Fedora Linux and possibly other RPM-based distributions through my Fedora Copr repository, [xanderlent/intel-npu-driver](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver). See that page for information on how to install and use this software on Fedora Linux (and possibly other RPM-based distributions).

### Installation instructions

To use the Intel NPU:

  - Enable the Copr.
  - Install the `intel-npu-firmware` package.
    - If the kernel module has already been loaded, you must manually unload and reload it to pick up the new firmware. (According to [discussions upstream](https://github.com/intel/linux-npu-driver/issues/17#issuecomment-2278209529), using an unmatched firmware and driver version is not supported.)
    - If you are using Linux v6.12-rc1 or newer, including stable versions v6.6.55, v6.10.14, and v6.11.3 and newer, or your kernel tree includes [upstream commit 58b5618ba80a5e5a8d531a70eae12070e5bd713f (`accel/ivpu: Add missing MODULE_FIRMWARE metadata`)](https://github.com/torvalds/linux/commit/58b5618ba80a5e5a8d531a70eae12070e5bd713f), then dracut should automatically include the ivpu kernel module and associated firmware in your initramfs the next time that it is regenerated. On unpatched kernels, you will need to manually add the firmware to your initramfs.
  - Install the `intel-npu-level-zero` package to enable use of the NPU via OneAPI Level Zero.
  - Optionally install and run the user-mode and kernel-mode driver tests from `intel-npu-level-zero-tests`.
  - Optionally install the `-debuginfo` and `-debugsource` packages for easier debugging.
  - Still TODO: The devel parts of this driver; the headers and libraries that are required to build your own code against it.
    - Fedora's `oneapi-level-zero-devel` package provides the common Level Zero headers, but the NPU extension headers are not yet packaged.
  - Still TODO, possibly in another repo: Programs that acutally use this driver, like Intel's NPU Python library or GIMP Plugin.
  - Still TODO: This driver can be built with OpenVINO in some kind of tight integration?


### Project Homepage and Issue Reporting

This project is a downstream packaging project and **is not affiliated with Intel**. Please see [the homepage](https://github.com/xanderlent/intel-npu-driver-rpm) for more information and report any issues you find at the [issue tracker](https://github.com/xanderlent/intel-npu-driver-rpm/issues).
