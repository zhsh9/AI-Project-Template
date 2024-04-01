import torch
import subprocess
import re
import os
import platform

# Function to find the cuDNN version from the header file on Linux
def find_cudnn_version_linux(header_paths):
    major_version, minor_version, patch_version = None, None, None
    for path in header_paths:
        if os.path.isfile(path):
            with open(path, 'r') as f:
                # Read the file line by line and search for version definitions
                for line in f:
                    if '#define CUDNN_MAJOR' in line:
                        major_version = line.split()[-1]
                    elif '#define CUDNN_MINOR' in line:
                        minor_version = line.split()[-1]
                    elif '#define CUDNN_PATCHLEVEL' in line:
                        patch_version = line.split()[-1]
                if major_version and minor_version and patch_version:
                    return f"{major_version}.{minor_version}.{patch_version}"
    return "Not Found"

# Function to find the cuDNN version on Windows
def find_cudnn_version_windows():
    try:
        # Assuming cuDNN is installed in the CUDA path, we search for the 'cudnn64_*.dll' file
        cuda_path = os.environ['CUDA_PATH']
        cudnn_dll_file = next((f for f in os.listdir(cuda_path + "\\bin") if re.match(r'cudnn64_\d+\.dll', f)), None)
        if cudnn_dll_file:
            cudnn_version_match = re.search(r'cudnn64_(\d+)', cudnn_dll_file)
            if cudnn_version_match:
                # We only get the major version from the DLL name
                return cudnn_version_match.group(1)
    except Exception as e:
        print("Could not determine cuDNN version on Windows:", e)
    return "Not Found"

# Check if CUDA is supported by the current PyTorch installation
cuda_available = torch.cuda.is_available()
print("Is CUDA supported by this system?", cuda_available)

# Get the number of GPUs available
gpu_count = torch.cuda.device_count()
print("Number of GPUs available:", gpu_count)

# Get the name of the current default CUDA device (GPU) if available
if cuda_available:
    for i in range(gpu_count):
        print(f"CUDA Device {i} name:", torch.cuda.get_device_name(i))

# Get the PyTorch version
print("PyTorch version:", torch.__version__)

# Retrieve the CUDA version if CUDA is available
if cuda_available:
    cudart_lib_version = torch.version.cuda
    print("CUDA Runtime version (from PyTorch):", cudart_lib_version)

    # Attempt to get the exact version of installed CUDA toolkit using nvcc
    try:
        nvcc_version = subprocess.check_output(["nvcc", "--version"]).decode("utf-8")
        cuda_version_match = re.search(r"release (\d+\.\d+)", nvcc_version)
        if cuda_version_match:
            cuda_toolkit_version = cuda_version_match.group(1)
            print("CUDA Toolkit version (from nvcc):", cuda_toolkit_version)
    except Exception as e:
        print("Could not retrieve CUDA Toolkit version. Make sure nvcc is in your PATH.")

# Get the cuDNN version if CUDA is available
if cuda_available:
    if platform.system() == "Windows":
        cudnn_version = find_cudnn_version_windows()
    elif platform.system() == "Linux":
        cudnn_header_paths = ['/usr/local/cuda/include/cudnn.h', '/usr/include/cudnn.h']
        cudnn_version = find_cudnn_version_linux(cudnn_header_paths)
    else:
        cudnn_version = "Unsupported platform for cuDNN version check."
    print("cuDNN version:", cudnn_version)
