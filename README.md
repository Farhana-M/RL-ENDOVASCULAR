# Installation and Testing Guide for SOFA, dEVE, and dEVE_bench Frameworks

## Introduction

This guide provides step-by-step instructions to set up a Python virtual environment on Windows, install the necessary dependencies for the **SOFA**, **dEVE**, and **dEVE_bench** frameworks, clone the repositories, and test the installation of **dEVE** and **dEVE_bench** using a Python script.

## Requirements

- Python (preferably 3.8 or higher)
- Git

## Setup Process

### Step 1: Create a Python Virtual Environment

To isolate your project's dependencies, create a Python virtual environment. You can use tools like `venv`, `conda`, or `pyenv` to do this. Below is the method for creating a virtual environment using Python's built-in `venv` tool:

```bash
# Create the virtual environment
python -m venv myenv
```

### Step 2: Activate the Virtual Environment

Once the virtual environment is created, activate it with the following command:

```bash
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
   - Follow the [SOFA documentation](https://sofa-framework.github.io/doc/getting-started/build/windows/) for detailed steps on how to install dependencies (such as Visual Studio, CMake, Qt, Boost, etc.).
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
       C:\path\to\Python3x\python.exe
       ```
     - **Python_LIBRARY**: Path to the Python `.lib` file.
       ```bash
       C:\path\to\Python3x\libs\python3x.lib
       ```
     - **Python_INCLUDE_DIR**: Path to the Python include files.
       ```bash
       C:\path\to\Python3x\include
       ```
     - **pybind11_DIR**: Path to `pybind11Config.cmake`
       ```bash
       C:\path\to\pybind11\share\cmake\pybind11
       ```
     - **SP3_LINK_TO_USER_SITE**: Set to `True` to link SofaPython3 against user-installed Python packages.
       ```bash
       True
       ```
     - **SP3_PYTHON_PACKAGES_LINK_DIRECTORY**: Set to the Python `site-packages` directory.
       ```bash
       C:\path\to\Python3x\Lib\site-packages
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

3. **Test the dEVE Installation**
   - You can test your installation by running a Python script. Use the following steps:
   ```bash
   cd myenv
   myenv\Scripts\activate
   python C:\path\to\deve\examples\function_check.py
    ```

### Step 8: Install the dEVE_bench Package

Install the **dEVE_bench** package within the same virtual environment. Follow these steps:

1. **Clone the dEVE_bench Repository**
   - Clone the dEVE_bench package repository using Git:
     ```bash
     git clone https://github.com/lkarstensen/deve_bench.git
     cd deve_bench
     ```

2. **Install the dEVE_bench Package**
   - Install the dEVE_bench package in editable mode (or regular mode) inside the virtual environment:
     ```bash
     python3 -m pip install -e .
     ```
3. **Test the dEVE_ bench Installation**
   -You can test your installation by running a Python script. Use the following steps:
   ```bash
   cd myenv
   myenv\Scripts\activate
   python C:\path\to\deve_bench\example\function_check.py
    ```




