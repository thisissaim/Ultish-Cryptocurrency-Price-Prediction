###First, check the versions of Python and Pip you have by running 
`python3 --version and pip3 --version`
Make sure it's >= to 3.9.0

## Install a virtual environment
`python3 -m pip install --user virtualenv (For Mac/UNIX)`
`py -m pip install --user virtualenv (For Windows)`

## Create a virtual environment
`python3 -m venv env (For MAC)`
`py -m venv env (Windows)`

### Once setup run the following command

`python3 -m pip install -r requirements.txt(Unix/MacOS)`
`py -m pip install -r requirements.txt (Windows)`



## Incase you are not able to activate your virtual environment, run the libraries in the requirements file separately by:


``python3 -m pip install library_name (Mac) or library_name==version (if present)``
`py -m pip install library_name (Windows) or library_name==version (if present)`


Once installed, open your terminal and run

`streamlit run model.py`



