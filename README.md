#  Auto Analysis and Tables (ANT) Version 1

Within this folder there are 3 things
- An Auto ANT application for Mac (AutoANT-Mac)
- An Auto ANT application for PC (AutoANT-PC)
- The code itself for running Auto ANT locally, which requires installation of Python 3.7.3 and the installation of python packages.

If possible, download, unzip and use one of the applications as it requires no installation process.

## Easiest Install: Via Conda 
1. Install Conda
    - Google Conda
2. In conda, select and activate Anaconda Prompt
3. Create VENV in Conda
    - In Anaconda Promt, write "conda create --name  env_name python=3.7.3"
    - It will ask the user if the proposed packages are OK to install, type 'y' and hit enter
4. Activate venv
    - In Anaconda Prompt, write "conda activate env_name"
5. Place the GUI folder in a convenient location (higher up the directory path is better), e.g., in the "users" folder
6. Write "pip install -r requirements.txt" - this installs all required packages for the GUI
    - A lot of text will run through the screen as all packages install. 
    - If  nothing happens with Pip, the environment might be missing Pip. If so, write "conda install pip", and write "y" when prompted.

## To Run via Conda
1. (If not already activated) In Conda, activate conda prompt
2. (If not already activated) Activate the VENV
3. Navigate to the folder with the GUI installed 
4. in Conda promt, write "python run_analysis.py".

## Useful Litterature 
- Conda - https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python 
- Virtual Environments in Conda - https://medium.com/swlh/setting-up-a-conda-environment-in-less-than-5-minutes-e64d8fc338e4 
- Pip (installing packages in Python) - https://medium.com/@pdx.lucasm/understanding-pip-the-package-installer-for-python-d3401de7072a 
- Using the terminal (CD is the key command - it allows navigation between directories) - https://medium.com/@roomee/command-line-essentials-a-beginners-guide-to-cmd-commands-6e2c327019d0 


#### If the use of this software supports a publication, make sure to reference the creators of the underlying packages.
- Instructions for how to cite the key packages are in their respective GitHub repositories:
    - EFEL package (https://github.com/BlueBrain/eFEL)
    - IPFX package (https://github.com/AllenInstitute/ipfx)

