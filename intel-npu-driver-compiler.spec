# So the way this works is it is just the driver build except we allow
# the compiler-in-driver build process to fetch code from the Internet
# and then delete the rest of the driver after building it
Name:           intel-npu-driver-compiler
Version:       	UD2025.24
# The "real" version needs to be the actual linux-npu-driver code
%define driver_version 1.19.0
%define lz_npu_exts_version d16f5d09fd695c1aac0c29524881fec7ccf7d27e
%define npu_elf_version 855ab36b6b2f0bcb34e0e9cd0d8862e963a6f412
Release:        1%{?dist}
Summary:        Intel NPU Driver Compiler component

%global toolchain clang

# TODO: Extract all the licenses?
License:        MIT AND Apache-2.0
# Same URL and sources as the main driver
# These will only be used for the main driver, since the code downloads its own stuff...
URL:            https://github.com/intel/linux-npu-driver
Source0:        %{url}/archive/refs/tags/v%{driver_version}.tar.gz
Source1:        https://github.com/intel/level-zero-npu-extensions/archive/%{lz_npu_exts_version}.tar.gz
Source2:        https://github.com/openvinotoolkit/npu_plugin_elf/archive/%{npu_elf_version}.tar.gz
Patch0:         0001-Add-USE_SYSTEM_LIBRARIES-option-for-distro-packagers.patch
# Extra patch to hack the npu_compiler build process to work on Fedora 41/42/43
Patch1:         0002-HACK-Patch-compiler-to-build-on-Fedora-41-42-43.patch

ExclusiveArch:	x86_64

# Same BuildRequires/Provides as the main driver!
BuildRequires:	cmake >= 3.22
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	glibc-devel
BuildRequires:	gmock-devel >= 1.14.0
BuildRequires:	gtest-devel >= 1.14.0
BuildRequires:	oneapi-level-zero-devel >= 1.18.4
BuildRequires:	yaml-cpp-devel >= 0.7.0
Provides: bundled(level-zero-npu-extensions)
Provides: bundled(openvino-npu_plugin_elf)
# We also need the following:
# Really big TODO: LFS pulls in prebuilt kernel binaries for the NPU. Can we eliminate them?
BuildRequires:  git-core
BuildRequires:  git-lfs
BuildRequires:	tbb-devel
# And now the rest... from npu_compiler and OpenVINO
# Intel bundled projects from the npu_compiler
Provides: bundled(vpucostmodel)
Provides: bundled(LLVM)
# Bundled code from the npu_compiler
Provides: bundled(flatbuffers)
Provides: bundled(gtest-parallel)
Provides: bundled(yaml-cpp)
# Provides from OpenVINO
Provides: bundled(OpenVINO)
Provides: bundled(ncc)
Provides: bundled(pybind11)
Provides: bundled(ARMComputeLibrary)
Provides: bundled(kleidiai)
Provides: bundled(libxsmm)
Provides: bundled(OneDNN)
Provides: bundled(shl)
Provides: bundled(xbyak_riscv)
Provides: bundled(gtest)
Provides: bundled(gflags)
Provides: bundled(ittapi)
Provides: bundled(json-devel)
Provides: bundled(oneapi-level-zero)
Provides: bundled(opencl-headers)
Provides: bundled(ocl-icd-loader)
Provides: bundled(onnx)
Provides: bundled(protobuf)
Provides: bundled(pugixml)
Provides: bundled(snappy)
Provides: bundled(telemetry)
Provides: bundled(xbyak)
Provides: bundled(zlib)

%description
Driver Compiler component of the Intel NPU Driver

%prep
%autosetup -p1 -n linux-npu-driver-%{driver_version}
%setup -q -T -D -a 1 -n linux-npu-driver-%{driver_version}
%setup -q -T -D -a 2 -n linux-npu-driver-%{driver_version}
rmdir third_party/level-zero-npu-extensions
mv level-zero-npu-extensions-%{lz_npu_exts_version} third_party/level-zero-npu-extensions
rmdir third_party/vpux_elf
mv npu_plugin_elf-%{npu_elf_version} third_party/vpux_elf


%build
# So the "solution" to building the compiler-in-driver correctly
# is just build it inside the normal build process, which means 
# allowing it to download all the deps and build the compiler
%cmake -DUSE_SYSTEM_LIBRARIES=ON -DENABLE_NPU_COMPILER_BUILD=ON
%cmake_build


%install
%cmake_install
tree .
# TODO: Remove everything except the target so file...


%files
#license TODO
#doc TODO



%changelog
* Wed Jul 09 2025 Alexander F. Lent <lx@xanderlent.com> - UD2025.24
- Initial Version (it's a giant hack!)
