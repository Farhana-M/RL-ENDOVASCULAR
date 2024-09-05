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

### Step 2: Install Dependencies

Install the necessary Python packages in your virtual environment:

bash
pip install numpy scipy pybind11


### Step 3: Create Directory Structure

Set up the appropriate directory structure for the SOFA framework:

bash
mkdir mySofa
cd mySofa
mkdir build src


### Step 4: Clone the SOFA Framework

Clone the SOFA framework repository into the 'src' directory using Git. Adjust the version tag (-b) to the version you need:

bash
git clone -b v23.12.00 --depth 1 https://github.com/sofa-framework/sofa.git ./src
