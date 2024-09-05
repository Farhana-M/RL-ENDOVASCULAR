# Setup Guide for SOFA Framework with Python Virtual Environment

## Introduction
This guide details the setup process for a Python virtual environment tailored for the SOFA framework, including environment creation, dependency installation, and cloning of the SOFA repository.

## Requirements
- Python (preferably 3.8 or higher)
- Git

## Installation Steps

### Step 1: Create a Python Virtual Environment

You can use tools like venv, conda, or pyenv to create a virtual environment. Here is the method using Python's venv:

```bash
# Create the virtual environment
python -m venv myenv
```

### Step 2: Activate the Virtual Environment
```bash
# On Windows
myenv\Scripts\activate
```

### Step 3: Install Dependencies

Install the necessary Python packages in your virtual environment:

```bash
pip install numpy scipy pybind11
```

### Step 4: Create Directory Structure

Set up the appropriate directory structure for the SOFA framework:

```bash
mkdir mySofa
cd mySofa
mkdir build src
```

### Step 4: Clone the SOFA Framework

Clone the SOFA framework repository into the 'src' directory using Git. Adjust the version tag (-b) to the version you need:

```bash
git clone -b v23.12.00 --depth 1 https://github.com/sofa-framework/sofa.git ./src
```




### Step 5: Visit the SOFA Documentation and Configure CMake

1. **Visit the SOFA Documentation**
   - Before proceeding with configuration and building, visit the [SOFA documentation page]((https://www.sofa-framework.org/community/doc/). The documentation provides comprehensive guidance on installing prerequisite tools like CMake and other necessary dependencies such as Qt and Boost.
   - Follow the instructions to install CMake if you haven’t done so already.

2. **When You Reach the CMake Configuration Section**

   Once you have installed CMake and other necessary dependencies from the SOFA documentation, follow these detailed steps to configure CMake for the SOFA framework:

   - **Open CMake GUI**
     - Launch the CMake GUI application from your applications or programs folder.

   - **Specify the Source and Build Directories**
     - In the 'Where is the source code:' field, browse and select the directory where you have the SOFA source code (e.g., `path/to/sofa/src`).
     - In the 'Where to build the binaries:' field, specify the build directory (e.g., `path/to/sofa/build`).

   - **Configure CMake Options**
     - Click on the 'Configure' button. You may need to specify the generator for the project; choose "CodeBlocks - Unix Makefiles" if you are following the setup from the command line.
     - A dialog will prompt you to choose the compiler; select the appropriate compiler installed on your system.

   - **Set CMake Variables**
     - Once CMake has processed the initial configuration, you'll need to set several variables to match the environment setup required:
       - `CMAKE_PREFIX_PATH`: Set this to the path where Qt and other dependencies are located.
       - `SOFA_FETCH_SOFAPYTHON3`: Set to `True` to automatically fetch and build SofaPython3.
       - `SOFA_FETCH_BEAMADAPTER`: Set to `True` if you are using the BeamAdapter plugin.
       - `Python_EXECUTABLE`: Point this to your Python executable.
       - `Python_LIBRARY`: Provide the path to the Python library.
       - `Python_INCLUDE_DIR`: Set this to the directory where Python includes are located.
       - `pybind11_DIR`: Set this to the directory containing `pybind11Config.cmake`.
       - `SP3_LINK_TO_USER_SITE`: Set to `True` to link SofaPython3 against the user site packages.
       - `SP3_PYTHON_PACKAGES_LINK_DIRECTORY`: Set this to Python's site-packages directory if specific linking is required.
     - Adjust any additional paths and options as necessary.

   - **Generate and Build**
     - Click on the 'Generate' button in CMake GUI to generate the Makefiles.
     - After generating the Makefiles, you can proceed to build the project:
       ```bash
       cd path/to/build/directory
       make
       ```





