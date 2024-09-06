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




### Step 5: Follow SOFA Instructions and Set CMake Variables

1. **Refer to SOFA Documentation**
   - Follow the [SOFA documentation](https://sofa-framework.github.io/doc/getting-started/build/windows/) for detailed steps on how to install dependencies (such as Visual Studio, CMake, Qt, Boost, etc.) and to set up the project structure.
   - Follow the instructions to generate the Visual Studio solution using CMake-GUI.

2. **Important: Set Additional CMake Variables**
   - When you reach the step to **launch CMake-GUI** as part of the SOFA build process, ensure you manually set the following CMake variables before clicking on **Generate**:
     - **CMAKE_PREFIX_PATH**: Path to your Qt and Boost installations.
       ```bash
       C:\path\to\qt;C:\path\to\boost
       ```
     - **SOFA_FETCH_SOFAPYTHON3**: Set to `True` to fetch and build SofaPython3.
       ```bash
       True
       ```
     - **SOFA_FETCH_BEAMADAPTER**: Set to `True` if using the BeamAdapter plugin.
       ```bash
       True
       ```
     - **Python_EXECUTABLE**: Full path to your Python executable.
       ```bash
       C:\path\to\Python310\python.exe
       ```
     - **Python_LIBRARY**: Path to the Python `.lib` file.
       ```bash
       C:\path\to\Python310\libs\python3.10.lib
       ```
     - **Python_INCLUDE_DIR**: Path to the Python include files.
       ```bash
       C:\path\to\Python310\include
       ```
     - **pybind11_DIR**: Path to `pybind11Config.cmake`.
       ```bash
       C:\path\to\pybind11\share\cmake\pybind11
       ```
     - **SP3_LINK_TO_USER_SITE**: Set to `True` to link SofaPython3 against user-installed Python packages.
       ```bash
       True
       ```
     - **SP3_PYTHON_PACKAGES_LINK_DIRECTORY**: Set to the Python `site-packages` directory.
       ```bash
       C:\path\to\Python310\Lib\site-packages
       ```

### Step 7: Install the dEVE Package

Once SOFA is set up, you can install the **dEVE** package within the same virtual environment. Follow these steps:

1. **Clone the dEVE Repository**
   - Clone the dEVE package repository using Git:
     ```bash
     git clone https://github.com/lkarstensen/deve.git
     cd deve
     ```

2. **Install the dEVE Package**
   - Install the dEVE package in editable mode (or regular mode) inside the virtual environment:
     ```bash
     python3 -m pip install -e .
     ```

3. **Verify the dEVE Installation**
   - To verify that dEVE is installed correctly, you can check the available commands:
     ```bash
     python -m deve --help
     ```






