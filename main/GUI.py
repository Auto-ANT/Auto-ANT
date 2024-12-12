"""
GUI.py 
This file contains all logic for the main GUI

Input: User provides input
Output: Calls other functions to create files
"""
import os
import sys
from tkinter import ttk, Tk, PhotoImage, Menu, Checkbutton, BooleanVar, filedialog, END
from idlelib.tooltip import Hovertip
import threading
import signal 

# Only for writing to file, cannot show plots
from matplotlib import use as use_plotting_engine
use_plotting_engine('Agg')

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)


# Add the top-level directory to the sys.path, to enable function imports
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gui_style_definitions import init_gui_style

from main.analysis.run_model import run_analysis

from firing_properties_config import config_firing_properities_table
from passive_membrane_properties_config import passive_membrane_properities_table
from neuronal_overview_config import config_neuronal_overview_table
from to_reference_info import  to_reference

from utils import get_resource_path

# To enable cancelling analysis runs early
exit_event =  threading.Event()


#! ------------------------------ Create data class ------------------------------
class data_to_use:
    # When Called the first Time  - Configures init values
    def __init__(self, input_folder_name, output_folder_name,
                 start_stimulation, end_stimulation, 
                 channel_1, channel_2, 
                 graph_1_state, graph_2_state, graph_3_state, graph_4_state,
                 ap_table, membrane_table, neuronal_overview_table,
                 ap_table_file_name, membrane_table_file_name, neuronal_overview_file_name):
        
        
        self.input_folder_name = input_folder_name
        self.output_folder_name = output_folder_name
        
        self.channel_1 = channel_1
        self.channel_2 = channel_2
        
        self.start_stimulation = start_stimulation
        self.end_stimulation = end_stimulation

        self.graph_1_state = graph_1_state
        self.graph_2_state = graph_2_state
        self.graph_3_state = graph_3_state
        self.graph_4_state = graph_4_state

        self.ap_table = ap_table
        self.ap_table_file_name = ap_table_file_name
        self.membrane_table = membrane_table
        self.membrane_table_file_name = membrane_table_file_name
        self.neuronal_overview_table = neuronal_overview_table
        self.neuronal_overview_file_name = neuronal_overview_file_name

    # For Debugging
    def present_data(self):
        print(f'Input Folder Name: {self.input_folder_name}')
        print(f'Output Folder name: {self.output_folder_name}')

        print(f'Channel 1: {self.channel_1}')
        print(f'Channel 2: {self.channel_2}')

        print(f'Start Stimulation: {self.start_stimulation}')
        print(f'End Stimulation: {self.end_stimulation}')

        print(f'Graph_1: {self.graph_1_state}')
        print(f'Graph_2: {self.graph_2_state}')
        print(f'Graph_3: {self.graph_3_state}')
        print(f'Graph_3: {self.graph_4_state}')

        print(f'AP Table: {self.ap_table}')
        print(f'AP Table file name: {self.ap_table_file_name}')

        print(f'Membrane Table: {self.ap_table}')
        print(f'Membrane Table file name: {self.membrane_table_file_name}')

        print(f'Membrane Table: {self.neuronal_overview_table}')
        print(f'Membrane Table file name: {self.neuronal_overview_file_name}')

    # For v6
    def run_electro_analysis(self):
        
        # Hide and present stop/start buttons
        trigger_calculations_button.grid_forget()
        stop_button.grid(row=25, column=4, pady = (0,10),padx=(10,0), sticky = 'w')
        
        # Set input folder, output folder, file name
        # ---------- Files Processed Heading ------------------------------------------
        files_processed_titles.config(text = "File status:")
        # ---------- Files Processed List------------------------------------------
        frame = ttk.Frame(root)
        frame.grid(row=3, column=4, padx=(0, 20), sticky="nwe", rowspan=17)

        # Create the Treeview widget inside the frame
        gui_status_table = ttk.Treeview(frame, column=("File status"), show="tree", height = 16)
        gui_status_table.grid(row=0, column=0, sticky="nswe")
        gui_status_table.column("#0", width=500, stretch=True)

        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=gui_status_table.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a horizontal scrollbar inside the frame and attach it to the Treeview
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=gui_status_table.xview)
        h_scroll.grid(row=1, column=0, sticky="we")  # Place it directly below the Treeview

        # Configure the Treeview to use the scrollbar
        gui_status_table.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scroll.set)

        # Configure column and row weights to allow resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # ------------------------------------------------------------------------

        # ------------------------ For Input ------------------------
        # Automatic Input - Get the list of all files in the directory
        dir_list = os.listdir(self.input_folder_name)
        # Ensures files are handled in alphabetical order
        dir_list.sort()
        # Here, file[0] is the iterator number, file[1] is the actual value
        list_outcomes = []
        for file in enumerate(dir_list):

            # If its been stopped - Break the loop
            if exit_event.is_set():
                break
            
            #! Need to store all returns here, and if ANY of them is False, then stop with errors
            #! Not fixed yet?
            outcome = run_analysis(self,file,gui_status_table, root)
            list_outcomes.append(outcome)

        # Need to swtich the  "Running" for "Stopping"
        if exit_event.is_set():
            status_title.config(text = 'Stopped early',foreground='red')
        elif all(list_outcomes):
            status_title.config(text = 'Success! ',foreground='green')
        else:
            status_title.config(text = 'Completed with errors',foreground='red')

        # Remove the exit event, so the analysis can be re-run
        exit_event.clear()

        # Hide and present stop/start buttons
        stop_button.grid_forget()
        trigger_calculations_button.grid(row=25, column=4, pady = (0,10),padx=(10,0), sticky = 'w')


#! Stop run
def stop_run():
    try:
        # Need to switch the start button to become a stop button and vice-versa
        status_title.config(text = 'Stopping..', foreground='red')
        exit_event.set()
    except:
        print("Need to start a run before cancelling it.")

#! ------------------------------ Custom functions for image hovertip ------------------------------
class ImageHovertip(Hovertip):
    def __init__(self, anchor_widget, image_path, hover_delay=50):
        super().__init__(anchor_widget, "", hover_delay=hover_delay)
        self.image_path = image_path
        
        modified_image_path = get_resource_path(image_path)
        self.image = PhotoImage(file=modified_image_path)
    
    def showcontents(self):
        label = ttk.Label(self.tipwindow, image=self.image)
        # label = ttk.Label(self.tipwindow, image=self.image, bg="white")
        label.image = self.image  # Keep a reference to prevent garbage collection
        label.pack()

#! ------------------------------ Support functions ------------------------------
#! Trigger Calculation
def populate_data():
    """
    Populate the class
    """
    data_for_analysis = data_to_use(input_folder_name = root.input_folder_name, output_folder_name = output_folder_name.get(), 
                                    start_stimulation = start_stimulation_text.get(), end_stimulation = end_stimulation_text.get(),
                                    channel_1 = channel_1.get(), channel_2 = channel_2.get(),
                                    graph_1_state = graph_1_state.get(), graph_2_state = graph_2_state.get(),
                                    graph_3_state = graph_3_state.get(), graph_4_state = graph_4_state.get(),
                                    ap_table = ap_table_state.get(), 
                                    membrane_table = membrane_table_state.get(),
                                    neuronal_overview_table = neuronal_overview_table_state.get(),
                                    ap_table_file_name = ap_table_file_name.get(), 
                                    membrane_table_file_name = membrane_table_file_name.get(),
                                    neuronal_overview_file_name = neuronal_overview_file_name.get())
    return data_for_analysis

def trigger_calculations():
    """ 
    Validate Input, remove status and error messages, populate data, (print full input in the back)
    Update status finally, activate the calculations
    """
    try:        
        # Validate inputs
        if not validate_and_update_inputs():
            raise TypeError        
        
        # if data passes validity checks, remove the errors and past resulsts
        remove_status_and_errors()

        # Populate the class        
        data_for_analysis = populate_data()

        # Class method, to view the data in cmd , for debugging
        # data_for_analysis.present_data()
                
        # Update status
        status_title.config(text = 'Running..', foreground='blue')

        # Run analysis - Can include arguments in thread via  args = []. Explained in docs, (for Daemon add - daemon=True)
        t = threading.Thread(target = data_for_analysis.run_electro_analysis)
        t.start()

    #? If not all configuration is done and Validation failed
    except TypeError:
        ##! fix this - if you reset values, and run again, you cant see the verify message because
        #! Its blocked by "Verify etc". Fix 
        # If there is a title, it needs to be removed first. Else do nothing
        try:
            files_processed_titles.config(text = "")
        except Exception as e:
            pass
        error_text.config(text = 'Verify highligthed fields', font=(8))
        error_text.grid(row=error_text_row, column=4, padx=(0,10), sticky = 'w')

    except:
        # If there is a title, it needs to be removed first. Else do nothing
        try:
            files_processed_titles.config(text = "")
        except Exception as e:
            pass

        error_text.config(text = 'Verify data selection', font=(8))
        error_text.grid(row=error_text_row, column=4, padx=(0,10), sticky = 'w')

#! Data Fetch and validation
def get_and_validate_file_path():
    """
    Supports button for input folder selection
    Select folder, and validate it
    The first folder is where the code resides, but it remembers the last used location
    """   
    # Starting directory - where the code lives
    # Starts at home, but if  someone is running  it again it saves the last folder
    try:
        current_directory = root.input_folder_name
    except:
        current_directory = os.getcwd()


    root.input_folder_name = filedialog.askdirectory(initialdir = current_directory,
                                                     title = 'Select Folder...')

    validate_input_folder()

#! Validations
def validate_and_update_inputs() -> bool:
    '''
    Validate Entry fields 
    Validate Combobox fields 
    Validate input field
    Return True/False (if validation passes/fails) and change style depending on results'''
    # TODO - These can be harmonized. Use a 'type check' on the widget to find the right name

    def is_float(value):
        try:
            val = float(value)
            return True
        except:
            return False
    
    def is_valid_entry(element):
        # if  tthe value is populated
        if element.get():
            # If the value is a float or an integer
            if is_float(element.get()):
            # if element.get().isdigit() or element.get().isnumeric():
                return True
            else:
                return False
        else:
            return False 

    def update_entry_color(element_state, element):
        style_choice = 'Approved.TEntry' if element_state else 'Failed.TEntry'
        element.configure(style = style_choice) 

    def is_valid_combo(element):
        if element.get():
            if element.get().isdigit():
                return True
            else:
                return False
        else:
            return False 

    def update_combo_color(element_state, element):
        style_choice = 'Approved.TCombobox' if element_state else 'Failed.TCombobox'
        element.configure(style = style_choice) 

    free_text_elements = [start_stimulation_text, end_stimulation_text]
    
    # ---------- Check if all entryies are valid
    element_status = [is_valid_entry(entry) for entry in free_text_elements]
    # Update colors based on validity
    [update_entry_color(status, entry) for status, entry in zip(element_status, free_text_elements)]

    # ---------- Validate comboboxes
    combo_elements = [channel_1,  channel_2]
    # Check if all elements are valid
    combo_status = [is_valid_combo(combo) for combo in combo_elements]
    # Update colors based on validity
    [update_combo_color(status, combo) for status, combo in zip(combo_status, combo_elements)]
            
    # ---------- Validate input folder 
    input_folder_validity = validate_input_folder()

    # if any failed validation, fail the whole process
    return False if (False in element_status) | (False in combo_status)| (input_folder_validity == False) else True

def validate_input_folder()-> bool:
    """
    1. Verify a folder was actually selected, if not fail
    2. Verify that something real was selected (i.e. if the dialog was opened and cancelled)
    3. Verify foldercontains  .abf files
    If all 3  conditions are met - green flag
    Else, fail validation
    """
    
    def has_abf_in_folder(directory:str) -> bool: 
        """Check if there are .abf files in the chosen directory"""

        # Get directory content and check if any files end in .abf
        dir_list = os.listdir(directory)
        has_abf = [x.endswith('abf') for x in dir_list]
        if True in has_abf:
            return True
        else:
            return False
    
    # Verify folder dialog was activated 
    if hasattr(root, 'input_folder_name'):
        # If the dialog is opened and closed, the value is populated but empty. Hence this layer of check
        if len(root.input_folder_name) > 0:
            # Check if there are .abf files in the chosen directory
            if has_abf_in_folder(root.input_folder_name):
                # If yes - show name of folder and turn green
                directory_path_list = root.input_folder_name.split('/')[-1]
                final_directory_display_name = f".../{directory_path_list}"
                select_input_path.config(text = final_directory_display_name,                
                                         style = 'FolderValid.TButton')
                return True
            else:
                # Otherwise request new folder and turn red
                select_input_path.config(text = 'No .abf file found',                
                                         style = 'FolderFail.TButton')
                
        # If the directroy button was clicked, but no folder was selected, delete it
        else:
            delattr(root, "input_folder_name")
            
    # If the dialog wasn't even opened
    else:
        select_input_path.config(text = 'Select a folder',                
                                style = 'FolderFail.TButton')        
    return False

#!  Reset Data
# Reset statuses and errors, in parts
def remove_status_and_errors() -> None:
    """
    Remove Error messages and switches to last run
    """
    # Remove any remaining errors
    error_text.grid_forget()

    if status_title.cget("text") != "":
        # Remove Process update
        status_title.config(text = 'Last run:', foreground='black')

def reset_input_output_folders() -> None:
    """
    Reset Input folder style and content
    """
    # Reset Input folder style and content
    select_input_path.config(text = 'Select Folder...',                
                            style = 'FolderNeutral.TButton')  
    
    # If the attribute exists, delete it 
    if hasattr(root, 'input_folder_name'):
        delattr(root, "input_folder_name") 

    # Reset Output folder style and content (no need for style)
    output_folder_name.delete(0, END)
    output_folder_name.config(style = 'Default.TEntry')   

def reset_combo_elements() -> None:
    """
    Reset Combo Styles and content
    """
    combo_elements = [channel_1,  channel_2]
    for combo_element in combo_elements:
        combo_element.configure(style = 'Default.TCombobox') 
        combo_element.set('')

def reset_entry_elements() -> None:
    # Reset input Styles and content
    free_text_elements = [start_stimulation_text, end_stimulation_text]
    
    for entry_element in free_text_elements:
        entry_element.configure(style = 'Default.TEntry') 
        entry_element.delete(0, END)

def reset_file_image_selections() -> None:
    check_boxes = [graph_1_button, graph_2_button, graph_3_button, 
                   graph_4_button, membrane_table_button, ap_table_button, 
                   neuronal_overview_table_button ]

    for selection in check_boxes:
        selection.select()

def reset_output_table_names() -> None:
    ap_table_file_name.delete(0,'')
    membrane_table_file_name.delete(0,'')
    neuronal_overview_file_name.delete(0,'')

    ap_table_file_name.insert(0,'Firing properties table')
    membrane_table_file_name.insert(0,'Passive membrane properties')
    neuronal_overview_file_name.insert(0,'Neuronal overview table')

def reset_all_data() -> None:
    """Full reset of all configuration variables,
        selections,
        and output table names"""
    
    reset_input_output_folders()
    reset_combo_elements()
    reset_entry_elements()
    remove_status_and_errors() 
    reset_file_image_selections()
    reset_output_table_names()
    
    
#! ------------------------------ Create the Frame of the GUI ------------------------------
root = Tk()

#? Attempt of fixing the scailing
# ----------------------------------------------------------------------------------------------------
def get_dpi():
    screen = Tk()
    dpi = screen.winfo_fpixels('1i')  # Get pixels per inch
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    screen.destroy()
    return dpi, screen_width, screen_height

# Calculate scale based on the target DPI
def calculate_scale(target_dpi):
    current_dpi, screen_width, screen_height = get_dpi()
    # Calculate scale factor based on DPI, but also consider screen resolution
    dpi_scale = current_dpi / target_dpi
    resolution_scale = min(screen_width / 1920, screen_height / 1080)  # Adjust for 1080p as a baseline resolution
    return dpi_scale * resolution_scale  # Combine both scaling factors for consistency

def scaled(original_width):
    return round(original_width * scale)

# Define a target DPI for a more consistent cross-platform scale (typically 96 DPI on PC)
target_dpi = 96
# Adjust dimension scaling
scale = calculate_scale(target_dpi)

#! ------------------------------ Page Size and Top Info ------------------------------

root.title("Auto ANT")
# Initialize the styles in the app. 
init_gui_style(root)
root.grid_columnconfigure(0, weight=3, uniform="sample")
root.grid_columnconfigure(1, weight=2, uniform="sample")
root.grid_columnconfigure(2, weight=3, uniform="sample")
root.grid_columnconfigure(3, weight=1, uniform="sample")
root.grid_columnconfigure(4, weight=3, uniform="sample")

# Add the Logo
logo_image_path = get_resource_path("main/images/auto_ant_logo_2_rbg.png")
logo_image = PhotoImage(file = logo_image_path) 
logo = ttk.Label(root,
                 image = logo_image,    
                 style = "Logo.TLabel")
logo.grid(row = 3, column=2, rowspan = 6, sticky = 'ne', pady=(0,0))

#? ------------------------------ Menu bar -----------------------------------------
def browser_open_url(url):
    from webbrowser import open as open_link
    open_link(url, new=0, autoraise=True)

# For adding Links via the menu bar
menubar = Menu(root)

more_info_menu = Menu(menubar, tearoff=0)
# more_info_menu.add_command(label="Link to paper", command= lambda: browser_open_url('https://www.aftonbladet.se/'))
more_info_menu.add_command(label="Link to repo", command= lambda: browser_open_url('https://github.com/Auto-ANT/Auto-ANT'))

menubar.add_cascade(label="More Info...", menu=more_info_menu)
root.config(menu=menubar)

#! ------------------------------ Populate the GUI ------------------------------

#? Inputs and  Outputs ------------------------------------------------------------------------
input_output_title = ttk.Label(root, text="Input and Output", style = "MidHeader.TLabel")
input_output_title.grid(row=1, column=0, pady = 5, padx=(10, 10), sticky = 'w')

# --------------- Design Interface and place Buttons ---------------
input_row = 2
data_set_label = ttk.Label(root, text="Input Folder*", style = "Variable.TLabel")
data_set_label.grid(row=input_row, column=0, padx=(10, 10), sticky = 'w')
# Folder containing data 
select_input_path = ttk.Button(root, 
                               text='Select Folder...', 
                               command=lambda: get_and_validate_file_path(), 
                               style = 'FolderNeutral.TButton')
select_input_path.grid(row=input_row, column=1)
# Tooltip
select_input_path_tp_text = "\
Select the folder where you have stored\n\
your recordings for analysis.\n\
NB: the folder should containing abf files\n\
recorded using IDENTICAL settings"
select_input_path_tp = ttk.Label(root, text=" (?)", style = 'Hover.TLabel')
select_input_path_tp.grid(row=input_row, column=2, padx=(0, 10), sticky = 'w')
select_input_path_tp_icon = Hovertip(select_input_path_tp, select_input_path_tp_text, hover_delay=50)

# --------------- Output Folder name Check Buttons ---------------
output_row = 3
output_folder_title = ttk.Label(root, text="Output",style = "Variable.TLabel")
output_folder_title.grid(row=output_row, column=0, padx=(10, 10), sticky = 'w', pady = 5)
# Entry field
output_folder_name_label = ttk.Label(root, text="Output folder name", style = "Variable.TLabel")
output_folder_name_label.grid(row=3, column=0, padx=(10, 10), sticky = 'w')
output_folder_name = ttk.Entry(root, style = 'Default.TEntry')
output_folder_name.grid(row = output_row, column = 1)

#? Configure Analysis ------------------------------------------------------------------------
configure_analysis_title = ttk.Label(root, text="\nConfigure Analysis settings", style = "MidHeader.TLabel")
configure_analysis_title.grid(row=4, column=0, padx=(10, 10), sticky = 'w', pady = 10, columnspan = 2)

#  Channel 1
channel_1_row = 5
channel_1_label = ttk.Label(root, text="Recording channel*", style = "Variable.TLabel")
channel_1_label.grid(row=channel_1_row, column=0, padx=(10, 10), sticky = 'w')
# Combo read only - so the user cant add their own thing - no need for this
channel_1 = ttk.Combobox(
                    state="readonly", 
                    values=[0, 1, 2, 3],
                    style = 'Default.TCombobox'
                    )
channel_1.grid(row=channel_1_row, column=1)
# Tooltip
channel_1_tp_text = "\
Choose the channel where your recording\n\
is stored (usually 0)"
channel_1_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
channel_1_tp.grid(row=channel_1_row, column=2, padx=(0, 10), sticky = 'w')
channel_1_tp_icon = Hovertip(channel_1_tp, channel_1_tp_text, hover_delay=50)


# Channel 2
channel_2_row = 6
channel_2_label = ttk.Label(root, text="Protocol channel*", style = "Variable.TLabel")
channel_2_label.grid(row=channel_2_row, column=0, padx=(10, 10), sticky = 'w')
# Combo read only - so the user cant add their own thing
channel_2 = ttk.Combobox(
                    state="readonly", 
                    values=[0, 1, 2, 3],
                    style = 'Default.TCombobox'
                    )
channel_2.grid(row=channel_2_row, column=1)
# Tooltip
channel_2_tp_text = "\
Choose the channel where your current steps\n\
are stored. (It can be 0, 1, 2 or 3)"
channel_2_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
channel_2_tp.grid(row=channel_2_row, column=2, padx=(0, 10), sticky = 'w')
channel_2_tp_icon = Hovertip(channel_2_tp, channel_2_tp_text, hover_delay=50)


#--------- Stimulation start and end Measure ---------
# Free Text (for Stimulation)
start_stimulation_row = 7
start_stimulation_label = ttk.Label(root, text="Protocol starts (ms)*", style = "Variable.TLabel")
start_stimulation_label.grid(row=start_stimulation_row, column=0, padx=(10, 10), sticky = 'w')
# Entry field
start_stimulation_text = ttk.Entry(root, style = 'Default.TEntry')
start_stimulation_text.grid(row = start_stimulation_row, column = 1)
# Tooltip
start_stimulation_tp_text = "\
Integers or decimal.\n\
when do you start injecting current?"
start_stimulation_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
start_stimulation_tp.grid(row=start_stimulation_row, column=2, padx=(0, 10), sticky = 'w')
start_stimulation_tp_icon = Hovertip(start_stimulation_tp, start_stimulation_tp_text, hover_delay=50)


# Free Text (for stimulation)
end_stimulation_row = 8
end_stimulation_label = ttk.Label(root, text="Protocol ends (ms)*", style = "Variable.TLabel")
end_stimulation_label.grid(row=end_stimulation_row, column=0, padx=(10, 10), sticky = 'w')
# Entry field
end_stimulation_text = ttk.Entry(root, style = 'Default.TEntry')
end_stimulation_text.grid(row = end_stimulation_row, column = 1)
# Tooltip
end_stimulation_tp_text = "\
Integers or decimal.\n\
When do you finish injecting current?"
end_stimulation_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
end_stimulation_tp.grid(row=end_stimulation_row, column=2, padx=(0, 10), sticky = 'w')
end_stimulation_tp_icon = Hovertip(end_stimulation_tp, end_stimulation_tp_text, hover_delay=50)

#--------- Dataset Check Buttons ---------
data_rows = 9
dataset_title = ttk.Label(root, text="\nDatasets to generate", style = "MidHeader.TLabel")
dataset_title.grid(row=data_rows, column=0, padx=(10, 10), sticky = 'w', pady = 10)
 
# Standard Settings
# Create Checkbutton, make it boolean, Default to Selected
ap_table_state = BooleanVar() 
membrane_table_state = BooleanVar() 
neuronal_overview_table_state = BooleanVar() 


settings_image_path = get_resource_path("main/images/cog.png")
settings_image = PhotoImage(file = settings_image_path) 
# settings_image = PhotoImage(file = "main/images/cog.png") 


#! ------------ Neuronal Overview Table   ---------------
#? Checkbutton
neuronal_overview_table_button = Checkbutton(root, text = "Neuronal overview table", 
                            variable = neuronal_overview_table_state, 
                            onvalue = True, 
                            offvalue = False,
                            anchor = 'w', 
                            width=200,
                            font = ('calibri', 13),
                            background = 'white')
 
neuronal_overview_table_button.grid(row= data_rows + 1, column=0, padx = (10,0))
neuronal_overview_table_button.select()
#! ------------ Neuronal Overview Table config Button  ---------------
# Create the stop button, but hide it immediately. It shows up when a run has been triggrered
no_window_config = ttk.Button(image = settings_image, 
                          command=config_neuronal_overview_table,
                          style ='Gear.TButton')

no_window_config.grid(row=data_rows + 1, column=1, sticky = 'w')

#? Tooltip Checkbutton
no_tp_text = "Configure the output columns for the neuronal overview table"
no_table_tp_icon = Hovertip(no_window_config, no_tp_text, hover_delay=50)


#? File name
neuronal_overview_file_name = ttk.Entry(root, style = 'FileName.TEntry')
neuronal_overview_file_name.grid(row = data_rows + 2, column=0, padx=(30, 0), sticky = 'w')
neuronal_overview_file_name.insert(0,'Neuronal overview table')

#? File name tp
neuronal_overview_file_name_text = '\
Name of the neuronal overview table file.\n\
If not specified - "Neuronal overview table".'
neuronal_overview_file_name_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
neuronal_overview_file_name_tp.grid(row=data_rows + 2, column=1, padx=(0, 10), sticky = 'w')
neuronal_overview_file_name_icon = Hovertip(neuronal_overview_file_name_tp, neuronal_overview_file_name_text, hover_delay=50)



#! ------------ AP Table   ---------------
#? Checkbutton
ap_table_button = Checkbutton(root, text = "Firing properties table", 
                            variable = ap_table_state, 
                            onvalue = True, 
                            offvalue = False,
                            anchor = 'w', 
                            width=200,
                            font = ('calibri', 13),
                            background = 'white')
 
ap_table_button.grid(row= data_rows + 3, column=0, padx = (10,0))
ap_table_button.select()


#! ------------ AP Table config Button  ---------------
ap_window_config = ttk.Button(image = settings_image, 
                                command=config_firing_properities_table,
                                style ='Gear.TButton')

ap_window_config.grid(row=data_rows + 3, column=1, sticky = 'w')

#? Tooltip Checkbutton
fp_tp_text = "Configure the output columns for the firing properties table"
fp_table_tp_icon = Hovertip(ap_window_config, fp_tp_text, hover_delay=50)

#? File name
ap_table_file_name = ttk.Entry(root, style = 'FileName.TEntry')
ap_table_file_name.grid(row= data_rows + 4, column=0, padx=(30, 0), sticky = 'w')
ap_table_file_name.insert(0,'Firing properties table')

#? File name tp
ap_table_file_name_text = '\
Name of the firing properties table file.\n\
If not specified - "Firing properties table"'
ap_table_file_name_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
ap_table_file_name_tp.grid(row=data_rows + 4, column=1, padx=(0, 10), sticky = 'w')
ap_table_file_name_icon = Hovertip(ap_table_file_name_tp, ap_table_file_name_text, hover_delay=50)

#! ------------ Membrane Table   ---------------
#? Checkbutton
membrane_table_button = Checkbutton(root, text = "Passive membrane properties table", 
                            variable = membrane_table_state, 
                            onvalue = True, 
                            offvalue = False,
                            anchor = 'w',
                            width=200,
                            font = ('calibri', 13),
                            background = 'white')
membrane_table_button.grid(row= data_rows + 5, column=0,padx = (10,0))
membrane_table_button.select()

#! ------------ Memebrane Table config Button  ---------------
# Create the stop button, but hide it immediately. It shows up when a run has been triggrered
pm_window_config = ttk.Button(image = settings_image, 
                          command=passive_membrane_properities_table,
                          style ='Gear.TButton')

pm_window_config.grid(row=data_rows + 5, column=1, sticky = 'w')

#? Tooltip Checkbutton
pm_tp_text = "Configure the output columns for the passive membrane properties table"
pm_table_tp_icon = Hovertip(pm_window_config, pm_tp_text, hover_delay=50)


#? File name
membrane_table_file_name = ttk.Entry(root, style = 'FileName.TEntry')
membrane_table_file_name.grid(row = data_rows + 6, column=0, padx=(30, 0), sticky = 'w')
membrane_table_file_name.insert(0,'Passive membrane properties')

#? File name tp
membrane_table_file_name_text = '\
Name of the passive membrane properties table file.\n\
If not specified - "Passive membrane properties".'
membrane_table_file_name_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
membrane_table_file_name_tp.grid(row=data_rows + 6, column=1, padx=(0, 10), sticky = 'w')
membrane_table_file_name_icon = Hovertip(membrane_table_file_name_tp, membrane_table_file_name_text, hover_delay=50)

#--------- Graph Check Buttons ---------
graph_rows = 9
graph_title = ttk.Label(root, text="\nGraphs to generate", style = "MidHeader.TLabel")
graph_title.grid(row=graph_rows, column=2, padx=(10, 10), sticky = 'w', pady = 10)
 
# Standard Settings - Create Checkbutton, make it boolean, Default to Selected
graph_1_state = BooleanVar() 
graph_2_state = BooleanVar() 
graph_3_state = BooleanVar() 
graph_4_state = BooleanVar() 

graph_1_button = Checkbutton(root, text = "Firing-current plot", 
                            variable = graph_1_state, 
                            onvalue = True, offvalue = False,
                            anchor = 'w', width=200,
                            font = ('calibri', 13),
                            background = 'white')
graph_1_button.grid(row=graph_rows+1, column=2, padx = (10,0)) 
graph_1_button.select()
#? Graph sample in tooltip
graph_1_sample_image = "main/images/firing_current_sample.png"
graph_1_sample_image_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
graph_1_sample_image_tp.grid(row=graph_rows + 1, column=3, padx=(0, 10), sticky = 'w')
graph_1_sample_image_icon = ImageHovertip(graph_1_sample_image_tp, graph_1_sample_image)



graph_2_button = Checkbutton(root, text = "Recording plot", 
                            variable = graph_2_state, 
                            onvalue = True, offvalue = False,
                            anchor = 'w',width=200,
                            font = ('calibri', 13),
                            background = 'white')
graph_2_button.grid(row=graph_rows+2, column=2, padx = (10,0))
graph_2_button.select()
#? Graph sample in tooltip
graph_2_sample_image = "main/images/recording_sample.png"
graph_2_sample_image_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
graph_2_sample_image_tp.grid(row=graph_rows + 2, column=3, padx=(0, 10), sticky = 'w')
graph_2_sample_image_icon = ImageHovertip(graph_2_sample_image_tp, graph_2_sample_image)



graph_3_button = Checkbutton(root, text = "Protocol plot", 
                            variable = graph_3_state, 
                            onvalue = True, offvalue = False,
                            anchor = 'w',width=200,
                            font = ('calibri', 13),
                            background = 'white')
graph_3_button.grid(row=graph_rows+3, column=2, padx = (10,0))
graph_3_button.select()
#? Graph sample in tooltip
graph_3_sample_image = "main/images/protocol_sample.png"
graph_3_sample_image_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
graph_3_sample_image_tp.grid(row=graph_rows + 3, column=3, padx=(0, 10), sticky = 'w')
graph_3_sample_image_icon = ImageHovertip(graph_3_sample_image_tp, graph_3_sample_image)



graph_4_button = Checkbutton(root, text = "Current-voltage linear regression plot", 
                            variable = graph_4_state, 
                            onvalue = True, offvalue = False,
                            anchor = 'w',width=200,
                            font = ('calibri', 13),
                            background = 'white')
graph_4_button.grid(row=graph_rows+4, column=2, padx = (10,0))
graph_4_button.select()
#? Graph sample in tooltip
graph_4_sample_image = "main/images/current_voltage_linear_regression_sample.png"
graph_4_sample_image_tp = ttk.Label(root, text=" (?)", style  = 'Hover.TLabel')
graph_4_sample_image_tp.grid(row=graph_rows + 4, column=3, padx=(0, 10), sticky = 'w')
graph_4_sample_image_icon = ImageHovertip(graph_4_sample_image_tp, graph_4_sample_image)


#?  Triggering the actual calculations ---------------------------------------
# Trigger calculation - for populating selections and initializing the class
trigger_calculations_button = ttk.Button(text="Run Analysis", 
                                  command=trigger_calculations,
                                  style = 'Trigger.TButton')
trigger_calculations_button.grid(row=25, column=4, pady = (0,10),padx=(10,0), sticky = 'w')

# ------------ Clear Button  ---------------
# Deleting selected values and the class
reset_button = ttk.Button(text="Reset Values", 
                          command=reset_all_data,
                          style ='Reset.TButton')
reset_button.grid(row=25, column=4, pady = (0,10), padx=(0,15), sticky = 'e')


# ------------ Stop Button  ---------------
# Create the stop button, but hide it immediately. It shows up when a run has been triggrered
stop_button = ttk.Button(text="Stop Analysis", 
                          command=stop_run,
                          style ='Stop.TButton')
stop_button.grid_forget()

# ------------ Citation Button  ---------------
citation_button_2 = ttk.Button(text="Citation Info" ,
                          command=to_reference,
                          style ='Cite.TButton')
citation_button_2.grid(row=26, column=4, pady = (0,5), padx=(10,15), sticky = 'e')

#?  File process Output ---------------------------------------
# ---------- Status Update ---------
status_title = ttk.Label(root, text="", style = 'StatusTitle.TLabel')
status_title.grid(row=1, column=4, padx=(0,10), sticky = 'w')

files_processed_titles = ttk.Label(root, text="", style = 'MidHeader.TLabel')
files_processed_titles.grid(row=2, column=4, padx=(0,10), sticky = 'w')

#?  Errors ---------------------------------------
# ---------- Error text placeholder---------
error_text_row = 2
error_text = ttk.Label(root, text="", style = 'Error.TLabel')
error_text.grid(row=error_text_row, column=4, padx=(0,10), sticky = 'w')

#? 'w'indow ---------------------------------------\

# Shenanigans for exiting all threads when main ends
def signal_handler(signum, frame):
    exit_event.set()

signal.signal(signal.SIGINT, signal_handler)
# Event Loop
if __name__ == '__main__':
    # This window now has the same size across all monitors. 
    root.geometry(f'{round(root.winfo_screenwidth() * 4 / 5)}x{round(root.winfo_screenheight() * 3.5 / 5)}')
    root.mainloop()