# Python Project Boiler Plate
The Python project boiler plate supports test driven development of custom Python packages and Jupyter notebooks. This includes a series of batch scripts to expedite set up and development.

# Note
The parent directory for the project should not contain any spaces for the batch scripts to work as expected.

# Directory Overview
* jupyter: Jupyter notebooks can be stored alongside a quick launch script of starting the Jupyter UI
* package: Development of a custom Python package should occur within this directory and can be renamed
* test_package: Stores the pytest unit testing code for test driven development of custom Python packages
* UtilityScripts: Stores a collection of batch scripts for expediting development
* requirements.txt: Python package list
* quick_reqs.txt: Common list of Python packages for quick development
* setup.py: Installation instructions for the custom Python package

# Quick Set Up

## Setting Up the Virtual Environment
* Run the Python Virtual Environment Initialization.bat script to set up the Python virtual environment
* Run the Python Packages Load Quick Reqs.bat script to load common Python libraries into the virtual environment

## Adding Additional Python Packages
* Run the Command Prompt Vir Env.bat script to load the virtual environment in the command prompt
* Use pip to install additional Python packages to the virtual environment
    * python -m pip install <package>

## Testing the Custom Python Package
* Run the Python Package Editable Install.bat script to set up the custom Python package within the virtual environment
* The custom Python package can continue to be modified, but can be referenced elsewhere within the virtual environment

## Running Pytest
* If the package name was changed, modify the Example Python Pytest.bat script to point to the test_<package> directory
* Run the modified batch script to perform all tests within the test directory

## Using Jupyter Notebooks
* Run the Python Jupyter Initialization.bat script to set up Jupyter with the virtual environment
* Run the Python Jupyter Start.bat script to start the Jupyter UI in the default browser
