Name:		intel-npu-compiler-in-driver
Version:	UD2025.28
Release:	1%{?dist}
Summary:	Intel NPU Compiler-In-Driver component

%define version_tag npu_ud_2025_28_rc1
%define npu_llvm_commit 544ee1a56b5ef5dd252e5e71f4582b630e1a9fc8
%define npu_elf_commit 7e8651735be77a877d2bfa04c7355136836def0f
%define npu_nn_cost_model_commit 338a471d7db8d71a9db1dd214d23f38e01a782f8

%define openvino_commit dd611339928e5637b1ea43d9557a88ac1b938060
%define openvino_version 2025.2.0^20250616gitdd61133

# TODO: Thoroughly audit included licenses!
License:	Apache-2.0
URL:		https://github.com/openvinotoolkit/npu_compiler
Source0:	%{url}/archive/refs/tags/%{version_tag}.tar.gz
Source1:	https://github.com/openvinotoolkit/npu_plugin_elf/archive/%{npu_elf_commit}.tar.gz
Source2:	https://github.com/intel/npu-nn-cost-model/archive/%{npu_nn_cost_model_commit}.tar.gz
Source3:	https://github.com/intel/npu-plugin-llvm/archive/%{npu_llvm_commit}.tar.gz
Source4:	https://github.com/openvinotoolkit/openvino/archive/%{openvino_commit}.tar.gz
# npu_compiler Patches
# Patch out the yaml-cpp and flatbuffers dependencies in the npu_compiler
Patch0:		0001-Disable-third-party-flatbuffers-yaml-cpp.patch
# Don't run git commands when working with the cost model, since we use the tarball
# (which thankfully includes all of the LFS artifacts)
Patch1:		0002-Remove-Git-commands-not-useful-in-tarball.patch
# OpenVINO Patches
# Patch out the vendored gflags and patch out bad install-s
Patch10:	0001-Use-system-gflags-and-disable-spurious-install-s.patch
# Patch out the vendored gtest
Patch11:	0002-Swap-vendored-gtest-for-official.patch
# Patch out vendored json-devel
Patch12:	0003-Replace-nlohmann_json-with-Fedora-s-json-devel.patch

# Common dependencies
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
# OpenVINO dependencies
BuildRequires:	tbb-devel
BuildRequires:	xbyak-devel
BuildRequires:	oneapi-level-zero-devel
BuildRequires:	gflags-devel
BuildRequires:	gtest-devel
BuildRequires:	pkgconfig(pugixml)
BuildRequires:	pybind11-devel
BuildRequires:	json-devel
# NPU Compiler Dependencies
BuildRequires:	flatbuffers-compiler
BuildRequires:	flatbuffers-devel
BuildRequires:	yaml-cpp-devel
BuildRequires:	zlib-devel

Provides:	bundled(openvino) = %{openvino_version}

%description
Compiler-in-Driver component of the Intel NPU Driver for Linux

%prep
%autosetup -N -n npu_compiler-%{version_tag}
# Apply npu_compiler Patches
%patch -P 0 -p1
%patch -P 1 -p1
# Stitch in npu_plugin_elf subtree
%setup -q -D -T -a 1 -n npu_compiler-%{version_tag}
rmdir thirdparty/elf
mv npu_plugin_elf-%{npu_elf_commit}/ thirdparty/elf
# Stitch in npu-nn-cost-model subtree
# This download includes all of the files stored in Git LFS, thankfully.
%setup -q -D -T -a 2 -n npu_compiler-%{version_tag}
rmdir thirdparty/vpucostmodel
mv npu-nn-cost-model-%{npu_nn_cost_model_commit}/ thirdparty/vpucostmodel
# Stitch in the custom LLVM subtree
%setup -q -D -T -a 3 -n npu_compiler-%{version_tag}
rmdir thirdparty/llvm-project
mv npu-plugin-llvm-%{npu_llvm_commit}/ thirdparty/llvm-project
# Create OpenVINO subtree as a separate directory from the NPU sources
# OpenVINO should be the final source so that we build with it
%setup -q -D -T -b 4 -n openvino-%{openvino_commit}
# Apply OpenVINO patches
%patch -P 10 -p1
%patch -P 11 -p1
%patch -P 12 -p1

%build
# The CMake options come from these locations:
# https://github.com/intel/linux-npu-driver/blob/main/compiler/npu_compiler_build.cmake
# https://github.com/openvinotoolkit/npu_compiler/blob/develop/src/vpux_driver_compiler/docs/how_to_build_driver_compiler_on_linux.md
# Note that the CMake command to build the npu_compiler must come from the OpenVINO sources.
%cmake \
	-DBUILD_COMPILER_FOR_DRIVER=ON \
	-DENABLE_PREBUILT_LLVM_MLIR_LIBS=OFF \
	-DOPENVINO_EXTRA_MODULES=../npu_compiler-%{version_tag} \
	-DTHREADING="TBB" \
	-DENABLE_INTEL_NPU=ON \
	-DENABLE_SYSTEM_TBB=ON \
	-DENABLE_SYSTEM_PUGIXML=ON \
	-DENABLE_SYSTEM_FLATBUFFERS=ON \
	-DENABLE_SYSTEM_OPENCL=ON \
	-DENABLE_SYSTEM_PROTOBUF=ON \
	-DENABLE_SYSTEM_SNAPPY=ON \
	-DENABLE_SYSTEM_LEVEL_ZERO=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DENABLE_CLANG_FORMAT=OFF \
	-DENABLE_NCC_STYLE=OFF \
	-DENABLE_AUTO=OFF \
	-DENABLE_AUTO_BATCH=OFF \
	-DENABLE_BLOB_DUMP=OFF \
	-DENABLE_FUNCTIONAL_TESTS=OFF \
	-DENABLE_HETERO=OFF \
	-DENABLE_INTEL_CPU=OFF \
	-DENABLE_INTEL_GPU=OFF \
	-DENABLE_JS=OFF \
	-DENABLE_MULTI=OFF \
	-DENABLE_INTEL_NPU_PROTOPIPE=OFF \
	-DENABLE_OV_IR_FRONTEND=ON \
	-DENABLE_OV_JAX_FRONTEND=OFF \
	-DENABLE_OV_ONNX_FRONTEND=OFF \
	-DENABLE_OV_PADDLE_FRONTEND=OFF \
	-DENABLE_OV_PYTORCH_FRONTEND=OFF \
	-DENABLE_OV_TF_FRONTEND=OFF \
	-DENABLE_OV_TF_LITE_FRONTEND=OFF \
	-DENABLE_PROXY=OFF \
	-DENABLE_SAMPLES=OFF \
	-DENABLE_TBBBIND_2_5=OFF \
	-DENABLE_TEMPLATE=OFF \
	-DENABLE_TESTS=OFF
%cmake_build -j1 --target npu_driver_compiler compilerTest profilingTest vpuxCompilerL0Test loaderTest

%install
# TODO: I think we need to specify the targets to the install step?
%cmake_install

# TODO: are there any tests we can run?

%changelog

