RPM Packages for the Intel Neural Processing Unit Driver for Linux
==================================================================

This repository provides packages for the Linux user space driver and proprietary firmware for the Intel Neural Processing Unit (NPU) hardware found on Intel Core Ultra Series 1 and newer (Meteor Lake and newer) Intel processors. It was formerly known as the Intel Versatile Processing Unit (VPU). The Linux kernel driver is already upstream as `drivers/accel/ivpu`.

See the [upstream intel/linux-npu-driver repository](https://github.com/intel/linux-npu-driver) for more information about the hardware, firmware, and software.

### Sources

The patches to the source included in this repository can be found at [my downstream fork xanderlent/linux-npu-driver, in the fix-fedora-build-v1.8.0-2 branch](https://github.com/xanderlent/linux-npu-driver/tree/fix-fedora-build-v1.8.0-2).

Note that this RPM downloads two vendored source code modules for [intel/level-zero-npu-extensions](https://github.com/intel/level-zero-npu-extensions/) and [openvinotoolkit/npu\_plugin\_elf](https://github.com/openvinotoolkit/npu_plugin_elf/), and integrates them into the source tree to allow the driver to compile. All other vendored modules are either disabled by us or upstream was thoughtful enough to detect if they are already installed.

### Package Availability

[![Copr build status](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver/package/intel-npu-level-zero/)  
This package is available for use with Fedora Linux and possibly other RPM-based distributions through my Fedora Copr repository, [xanderlent/intel-npu-driver](https://copr.fedorainfracloud.org/coprs/xanderlent/intel-npu-driver). See that page for information on how to install and use this software on Fedora Linux (and possibly other RPM-based distributions).

### Installation instructions

To use the Intel NPU:

  - Enable the Copr.
  - Install the `intel-npu-firmware` package.
    - If the kernel module has already been loaded, you must manually unload and reload it to pick up the new firmware.
    - If you want to include the firmware in all of your initramfses, make sure to also run `sudo dracut --regenerate-all --force --install /usr/lib/firmware/updates/intel/vpu/vpu_37xx_v0.0.bin --install /usr/lib/firmware/updates/intel/vpu/vpu_40xx_v0.0.bin`. The install lines are only necessary until the kernel includes the firmware metadata in modinfo, which should happen soon. See [bug #1](https://github.com/xanderlent/intel-npu-driver-rpm/issues/1).
  - Install the `intel-npu-level-zero` package to enable use of the NPU via OneAPI Level Zero.
  - Optionally install and run the user-mode and kernel-mode driver tests from `intel-npu-level-zero-tests`.
  - Still TODO: The devel parts of this driver; the headers and libraries that are required to build your own code against it.
  - Still TODO, possibly in another repo: Programs that acutally use this driver, like Intel's NPU Python library or GIMP Plugin.
  - Still TODO: The parts of the driver where it can be tightly integrated with OpenVINO.


### Project Homepage and Issue Reporting

This project is a downstream packaging project and **is not affiliated with Intel**. Please see [the homepage](https://github.com/xanderlent/intel-npu-driver-rpm) for more information and report any issues you find at the [issue tracker](https://github.com/xanderlent/intel-npu-driver-rpm/issues).
