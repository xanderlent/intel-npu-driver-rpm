Name:		intel-npu-compiler-in-driver
Version:	UD2025.04
Release:	1%{?dist}
Summary:	Intel NPU Compiler-In-Driver component

%define version_tag npu_ud_2025_04_rc2
%define npu_llvm_commit 0d1145010d6d2ba48a945c824ed0ca03254b94ed
%define npu_elf_commit 2184e3a0c768e970916435405cd0a80809823673
%define npu_nn_cost_model_commit 483447ff4de0f1818fe3794a716b356400c7b369
%define openvino_commit 99d7cd4bc4492b81a99bc41e2d2469da1a929491
%define openvino_version 2024.6.0^20241204git99d7cd4

# TODO: Thoroughly audit included licenses!
License:	Apache-2.0
URL:		https://github.com/openvinotoolkit/npu_compiler
Source0:	%{url}/archive/refs/tags/%{version_tag}.tar.gz
Source1:	https://github.com/openvinotoolkit/npu_plugin_elf/archive/%{npu_elf_commit}.tar.gz
Source2:	https://github.com/intel/npu-nn-cost-model/archive/%{npu_nn_cost_model_commit}.tar.gz
Source3:	https://github.com/openvinotoolkit/openvino/archive/%{openvino_commit}.tar.gz
# Patch out the yaml-cpp and flatbuffers dependencies in the npu_compiler
Patch0:		0001-Disable-third-party-flatbuffers-yaml-cpp.patch
Patch1:		0002-Remove-Git-commands-not-useful-in-tarball.patch
# Patch out a bug in the system level zero detection in OpenVINO
Patch2:		0001-Fix-detection-of-level-zero-when-ENABLE_SYSTEM_LEVEL.patch
# Patch out the vendored gflags and patch out bad install-s
Patch3:		0002-Use-system-gflags-and-disable-spurious-install-s.patch
# Patch out the vendored gtest
Patch4:		0003-Swap-vendored-gtest-for-official.patch

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
# NPU Compiler Dependencies
BuildRequires:	flatbuffers-compiler
BuildRequires:	flatbuffers-devel
BuildRequires:	yaml-cpp-devel
%if 0%{fedora} < 41
BuildRequires:	mlir-devel < 19.1
BuildRequires:	llvm-devel < 19.1
%else
BuildRequires:	mlir-devel
BuildRequires:	llvm18-devel
%endif
Provides:	bundled(openvino) = %{openvino_version}

%description
TODO

%prep
%autosetup -N -n npu_compiler-%{version_tag}
# Patch out the yaml-cpp and flatbuffers dependencies in the npu_compiler
%patch -P 0 -p1
%patch -P 1 -p1
# Stitch in npu_plugin_elf subtree
%setup -q -D -T -a 1 -n npu_compiler-%{version_tag}
rmdir thirdparty/elf
mv npu_plugin_elf-%{npu_elf_commit}/ thirdparty/elf
# Note that we do not vendor the NPU LLVM tree, we can use stock LLVM 18,
# when we turn ON the config option ENABLE_PREBUILT_LLVM_MLIR_LIBS
# Stitch in npu-nn-cost-model subtree
# This download includes all of the files stored in Git LFS, thankfully.
%setup -q -D -T -a 2 -n npu_compiler-%{version_tag}
rmdir thirdparty/vpucostmodel
mv npu-nn-cost-model-%{npu_nn_cost_model_commit}/ thirdparty/vpucostmodel
# Create OpenVINO subtree as a separate directory from the NPU sources
# OpenVINO should be the final source so that we build with it
%setup -q -D -T -b 3 -n openvino-%{openvino_commit}
# Patch out a bug in the system level zero detection in OpenVINO
%patch -P 2 -p1
# Patch out the vendored gflags and patch out bad install-s
%patch -P 3 -p1
# Patch out the vendored gtest
%patch -P 4 -p1
# ONLY on Fedora 40, xbyak-devel doesn't ship with cmake files
%if 0%{fedora} < 41
sed -i "s/add_subdirectory(thirdparty\/xbyak EXCLUDE_FROM_ALL)//" thirdparty/dependencies.cmake
%endif

%build
# The CMake options come from these locations:
# https://github.com/intel/linux-npu-driver/blob/main/compiler/npu_compiler_build.cmake
# https://github.com/openvinotoolkit/npu_compiler/blob/develop/src/vpux_driver_compiler/docs/how_to_build_driver_compiler_on_linux.md
# Note that the CMake command to build the npu_compiler must come from the OpenVINO sources.
%cmake \
	-DCMAKE_C_COMPILER=gcc \
	-DCMAKE_CXX_COMPILER=g++ \
	-DBUILD_COMPILER_FOR_DRIVER=ON \
	-DENABLE_PREBUILT_LLVM_MLIR_LIBS=ON \
	-DOPENVINO_EXTRA_MODULES=../npu_compiler-npu_ud_2025_04_rc2 \
	-DTHREADING="TBB" \
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
# TODO: I think we need to specify the targets to the build step?
%cmake_build

%install
# TODO: I think we need to specify the targets to the install step?
%cmake_install

# TODO: are there any tests we can run?

%changelog

