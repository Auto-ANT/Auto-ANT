#  Auto Analysis and Tables (Auto ANT)

# Running Auto ANT as an application
Running Auto ANT as an application does not require any programming expertise. After downloading the application, it can be run without any further installations.
1. Open the folder "Ready to use applications"
2. Select the relevant zip file depending on your operating system (mac or PC) and click it
3. In the upper right corner there are 3 dots ("..."). Click this, and download the .zip file
4. Unzip the file 
5. Right click the file and select open (if you double click it directly, a warning may prevent it from opening)
6. The application might take a minute to open. Once opened it's ready to be used.

# Running Auto ANT via code 
To run Auto ANT via code, the user will need to download the repo (either via cloning or downloading the zip).
To run the code, the user will need to use python 3.7.3.

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

#### If the use of this software supports a publication, make sure to reference the creators of the underlying packages.
- Instructions for how to cite the key packages are in their respective GitHub repositories:
    - EFEL package (https://github.com/BlueBrain/eFEL)
    - IPFX package (https://github.com/AllenInstitute/ipfx)

