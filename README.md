Intel AI Boost NPU Driver for Linux
===================================

This repository provides packages for the Linux user space driver and proprietary firmware for the Intel AI Boost NPU hardware found on Intel Core Ultra processors.

This driver supports the NPU hardware found in Intel Core Ultra (Series 1) and newer (Meteor Lake and newer) processors from Intel. Currently, the Meteor Lake, Arrow Lake, and Lunar Lake NPUs are supported.

It was formerly known as the Intel (Movidius) Versatile Processing Unit (VPU). The Linux kernel driver is upstream as `drivers/accel/ivpu`.

See the [upstream intel/linux-npu-driver repository](https://github.com/intel/linux-npu-driver) for more information about the hardware, firmware, and software.

### Sources

The patches to the source included in this repository can be found at [my downstream fork xanderlent/linux-npu-driver, in the fix-fedora-build-v1.16.0-2 tag](https://github.com/xanderlent/linux-npu-driver/tree/fix-fedora-build-v1.16.0-2).

Note that this RPM downloads two vendored source code modules for [intel/level-zero-npu-extensions](https://github.com/intel/level-zero-npu-extensions/) and [openvinotoolkit/npu\_plugin\_elf](https://github.com/openvinotoolkit/npu_plugin_elf/), and integrates them into the source tree to allow the driver to compile. All other vendored modules are either disabled by us or upstream was thoughtful enough to detect if they are already installed.

### Package Availability

[![Copr build status](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/)  
This package is available for use with Fedora Linux and other RPM-based distributions through my Fedora Copr repository, [xanderlent/intel-npu-driver](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver). See that page for information on how to install and use this software on Fedora Linux and other RPM-based distributions.

Given that I am maintaining this on a volunteer basis, I can only provide support as I have the time to do so. That said, I will prioritize support for current Fedora stable versions, as the below demonstrates. I will try to announce support decisions in the [discussion thread for the copr](https://discussion.fedoraproject.org/t/xanderlent-intel-npu-driver/124221) as they happen.

#### Support Status for Fedora

- Fedora 39 is not supported, because it has reached end-of-life. (It was initially supported.)
- Fedora 40 is supported.
  - The copr backports oneapi-level-zero from Fedora 41 to Fedora 40, as a newer version is required.
- Fedora 41 is supported.
- Fedora 42 is supported.
- Fedora Rawhide is supported on a best-effort basis, given that breakages frequently occur. It may take some time for me to fix the package.

#### Other Supported Distributions

- EPEL10 is supported on a best-effort basis, since EL10 (CentOS Stream 10) is based on Fedora between 40 and 41.
  - I am not proactively testing new releases on EPEL10; I only check that the package builds.
  - I am happy to troubleshoot issues, but I reserve the right to drop support if it becomes a burden.

### Installation instructions

To use the Intel NPU:

  - Enable this copr.
  - Install the `intel-npu-firmware-upstream` package.
    - You can also use the older firmware included in Fedora 40 and newer from `linux-firmware`.
    - If the kernel module has already been loaded, you must manually unload and reload it to pick up the new firmware.
    - If you are using a recent kernel dracut should automatically include the ivpu kernel module and associated firmware in your initramfs the next time that it is regenerated (usually when you get a new kernel version). Triggering this on firmware install is TODO.
  - Install the `intel-npu-level-zero` package to enable use of the NPU via OneAPI Level Zero.
    - Users of Fedora 40 need to install oneapi-level-zero from this copr as well, since it backports the latest version from Fedora 41, which is required by the upstream driver as of 1.13.0 and newer.
  - Optionally install and run the user-mode and kernel-mode driver tests from `intel-npu-level-zero-tests`.
  - Optionally install the `-debuginfo` and `-debugsource` packages for easier debugging.
  - Higher level programs that use this driver can be found in the [xanderlent/intel-npu-highlevel copr](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-highlevel/) [(Sources)](https://github.com/xanderlent/intel-npu-highlevel-rpms).
  - The -devel package, which contains the unversioned .so file.
    - Still TODO: Other devel parts of this driver; For example, should we ship the firmware API headers somewhere?
    - Still TODO: Fedora's `oneapi-level-zero-devel` package provides the common Level Zero headers, but the NPU extension headers are not yet packaged; we and the OpenVINO package vendor them.
  - Still TODO: This driver can be built with OpenVINO to get the compiler-in-driver component. It's modular but not really optional since many functions don't work without it. That's not yet available from this repo because it's complicated. I'm working on it.


### Project Homepage and Issue Reporting

This project is a downstream packaging project and **is not affiliated with Intel**. Please see [the homepage](https://github.com/xanderlent/intel-npu-driver-rpm) for more information and report any issues you find at the [issue tracker](https://github.com/xanderlent/intel-npu-driver-rpm/issues).
