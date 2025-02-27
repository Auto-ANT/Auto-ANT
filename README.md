#  Auto Analysis and Tables (Auto ANT)

# Downloading Auto ANT
The user can download a specific application (PC or Mac), the entire repository, or a release. The code and applications reflects the latest release.
If the user only wants the application:
- Download the relevant .zip file directly from the folder Ready_to_use_applications.
If the user wants the code and the applications:
- It is recommended to download the latest release. This zip file contains all content in the repository, including the .zip files for the applications and the code. 

# Running Auto ANT as an application
Running Auto ANT as an application does not require any programming expertise. After downloading the application, it can be run without any further installations.
1. Open the folder "Ready_to_use_applications"
2. Select the relevant zip file depending on your operating system (mac or PC) and click it
3. In the upper right corner there are 3 dots ("..."). Click this, and download the .zip file
4. Unzip the file 
5. Right click the file and select open (if you double click it directly, a warning may prevent it from opening)
    - On Mac computers the user may be warned not to open software from unknown developers. To open the application, users may need to navigate to Settings -> Privacy & Security to explicitly allow the use of the application
6. The application might take a minute to open. Once opened it's ready to be used.

# Running Auto ANT via code 
To run Auto ANT via code, the user will need to download the repo (either via cloning or downloading the zip).
To run the code, the user will need to use python 3.9.1.

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

## Error Handling
If an error is encountered, a short, summarizing error description is mentioned in the status window. Users can view a more detailed error message within the log.
- ⁠If the error affects all recordings in the dataset—such as an incorrect protocol or recording channel—no output will be produced. 
- ⁠If an error pertains to only some recordings (e.g. a recording acquired with a different protocol from the rest of the dataset), those specific recordings will be indicated in the status window and excluded from the output tables, while the rest of the dataset is analysed as usual.
- ⁠If an error affects only a specific output table or plot (e.g., selecting the firing table for recordings without action potentials), only that specific table will be blocked, while all other outputs will function normally.
Common errors to encounter are:
- ⁠NoFiringSweepsError
    - Raised when there are no sweeps fulfilling the requirement for firing properties
    - May affect the Firing properties table
- NoNegativeSweepsError
    - Raised when there are no sweeps fulfilling the requirement for membrane
    - May affect the Membrane table, the Neuronal Overview table, or the Current-Voltage linear regression plot
- WrongRecordingChannelError
    - Raised when the wrong recording channel is used
    - May affect all tables and plots
- ⁠WrongProtocolChannelError
    - Raised when the wrong protocol channel is used
    - May affect all tables and plots

## Detailed Logs
After a run is completed, a button called "Detailed Logs" will become visible. Clicking this button opens a new window with the logs from recent runs (since the application was opened).

The log shows general information about the files being created (tagged as Info), as well as Warnings (tagged as Warning) and errors (tagged as Errors).

## Citations
#### If the use of this software supports a publication, make sure to reference the creators of the underlying packages.
- Instructions for how to cite the key packages are in their respective GitHub repositories:
    - EFEL package (https://github.com/BlueBrain/eFEL)
    - IPFX package (https://github.com/AllenInstitute/ipfx)

