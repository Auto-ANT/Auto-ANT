"""
run_analysis.py 
This file is called for each .abf file, and based on the users selections it evaluates which tables and charts to create.
It then calls other functions in other files to create said tables and charts, and saves them.

Input: Class of information from the GUI,
Output: Status on success or fail for all files.
"""
import os
import pyabf
import pandas as pd
import openpyxl
from tkinter import END

import matplotlib.pyplot as plt


from main.analysis.create_plots import create_plot_firing_current, \
                                create_plot_recording, \
                                create_plot_protocol, \
                                create_plot_current_voltage

from main.analysis.create_tables import create_ap_table,\
                                    create_membrane_table,\
                                    create_neuronal_overview_table

from utils import get_resource_path

#! Saving
def create_and_add_sheet_to_excel(file_name, iterator_number, cell_file_name, table, cols_to_export:False): 
    # Name the sheet 
    sheetname = f'cell {cell_file_name[:-4]}'

    # Convert the file name to an excel file
    full_file_name = get_resource_path(file_name + '.xlsx')

    # If the user has subset columns
    if cols_to_export:
        table = table[cols_to_export]

    # If its the first cell, create the file
    if iterator_number == 0:
        table.to_excel(full_file_name, sheet_name= sheetname, index=False) 
          
    # If the file already exists, add a new sheet to it
    else:
        if os.path.exists(full_file_name):
            # Maybe check if the file exists first? If so 
            with pd.ExcelWriter(full_file_name, mode = 'a') as writer:
                table.to_excel(writer, sheet_name = sheetname, index=False) 

        else:
            # Maybe check if the file exists first? If so 
            with pd.ExcelWriter(full_file_name, mode = 'w') as writer:
                table.to_excel(writer, sheet_name = sheetname, index=False)             

#! Need new function - create_and_add_row_to_excel (so only 1 sheet)
def create_and_add_row_to_excel(file_name, iterator_number, cell_name,  table, cols_to_export:False): 
    
    # Name the sheet 
    sheetname = 'Cell Overview'
    full_file_name = get_resource_path(file_name + '.xlsx')

    # The first column should be the cell name
    table.insert(0, 'Cell name', [cell_name[:-4]])

    # If the user has subset columns
    if cols_to_export:
        table = table[cols_to_export]

    # If its the first cell, create the file
    if iterator_number == 0:
        table.to_excel(full_file_name, sheet_name = sheetname, index=False) 
          
    # If the file already exists, add a new sheet to it
    else:
        # Load the existing workbook
        if os.path.exists(full_file_name):
            current_table = pd.read_excel(full_file_name, sheet_name=sheetname, engine='openpyxl')
            # Append the new data to the current table
            updated_table = pd.concat([current_table, table], ignore_index=True)
        else:
            # If the file somehow doesn't exist, initialize it with the current table
            updated_table = table
       
        # Save the updated data to the Excel file
        with pd.ExcelWriter(full_file_name, mode='w',  engine='openpyxl') as writer:
            updated_table.to_excel(writer, sheet_name=sheetname, index=False)


def get_cols_to_export(file_name):
    # Final step - convert selected fields to list of columns. maybe do this in other code. 
    try:
        cols_to_export_path = get_resource_path(file_name)
        cols_to_export = pd.read_csv(cols_to_export_path)           
        # cols_to_export = pd.read_csv(file_name)
        cols_to_export = cols_to_export[cols_to_export["to_include"] == 1]["column"].tolist()
        
    except Exception as e:
        cols_to_export = False 
    
    return cols_to_export



def update_gui_status_table(status_list, file, results_output_text, root) -> bool:
    """ 
    Now, we check the status output from all files.
    If all created files were successful - Report total succeess and print it in the tree, return all_successful = True
    If any one failed, show all fails statuses and return all_successful = False
    """
    
    def update_error_status_individual_files(target_file, results_output_text, e, root):
        """Update status in the status treeview for individual files"""
        if e:
            cross_mark = "\u2716"  # ✖
            warning_sign = "\u26A0"  
            output_text = f"{cross_mark} {target_file} failed because:"
            
            # Status of file
            display_status_message(output_text, results_output_text,root)
            # The returned error message
            display_status_message(f"{warning_sign} {e}", results_output_text,root)

        else:
            tick_mark = "\u2714"  # ✔
            output_text = f"{tick_mark} {target_file}"
            
            # Status update
            display_status_message(output_text, results_output_text,root)

    if not all(x.get("file_was_created") for x in status_list):
        # Some files failed
        all_successful = False

        # Status update
        output_text = f"{file[1][:-4]} - Contained errors"
        display_status_message(output_text,results_output_text, root)

        # Display status for each individual file that was attempted to be created
        for file in status_list:
            update_error_status_individual_files(file['file'], results_output_text, file['error_text'], root)
        
        # Add an empty row in the end if theres an error to make it easier to read
        display_status_message("",results_output_text, root)
    else:
        # No errors - all files were successful
        all_successful = True
        
        tick_mark = "\u2714"  # ✔
        output_text = f"{tick_mark} {file[1][:-4]} -- Success"
        display_status_message(output_text,results_output_text, root)

    return all_successful

def display_status_message(status_update: str, results_output_text, root):
    """Add elements to the treeview"""
    results_output_text.insert("",END, text = status_update)
    results_output_text.see(results_output_text.get_children()[-1]) 


#! MAIN
def run_analysis(data, file, results_output_text, root):

    # ------------------------ Inputs ------------------------
    # Set channels
    channel = int(data.channel_1) #for recording
    channel_c = int(data.channel_2) #for current

    # Current steps 
    #! These are  set to 600 and 601 as that always works
    # t1_c = float(data.start_current)
    # t2_c = float(data.end_current)
    t1_c = 600
    t2_c = 601

    # Start and end of stimulation (ms)
    # When does your current injection start and end
    stim_start = float(data.start_stimulation)
    stim_end = float(data.end_stimulation)
        
    # ------------------------ For Output ------------------------
    # Establishes location for new folder  (same name as the excel file name)
    output_file_name_AP = str(data.ap_table_file_name)
    output_file_name_MB = str(data.membrane_table_file_name)
    output_file_name_NO = str(data.neuronal_overview_file_name)

    # Prepare Output
    folder_path = f'{data.input_folder_name}/Auto ANT output/{data.output_folder_name}' 
    final_output_file_name_AP = folder_path + '/' + output_file_name_AP
    final_output_file_name_MB = folder_path + '/' + output_file_name_MB
    final_output_file_name_NO = folder_path + '/' + output_file_name_NO

    # Checks if the folder exists, otherwise creates it
    if not os.path.exists(folder_path): 
        os.makedirs(folder_path)

    # ------------------------ Status Trackers ------------------------
    # All_succesful tracks the total status - i.e. if all files were successful - it returns true.
    # If any one file, for any abf file failed, Returns false
    all_files_were_successful = True
    # Status list logs each file that was created, the status (success or fail) and any error text if it failed 
    status_list = []


    # ------------------------ Analysis and File Creation ------------------------
    # Only attempt analysis of a file if it is an abf file (just incase there's some other file there)
    if file[1].endswith('.abf'):
        
        # Define the full file path
        data_path = data.input_folder_name + '/' + file[1]
        
        # Ingest data 
        abf = pyabf.ABF(data_path)
        abf_c = pyabf.ABF(data_path)
        
        # In file names, the [:-4] is included to remove '.abf' from the filename
        # Manipulate Data, Generate and Save Plots
        if data.graph_1_state:
            try:
                firing_currents = create_plot_firing_current(abf, abf_c, channel_c, t1_c, t2_c, stim_start, stim_end)
                firing_currents.savefig(folder_path + f"/{file[1][:-4]}_firing_current.png", dpi=300)
                plt.close()

                file_was_created = True
                error_text = False

            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": "Firing Currents plot", "file_was_created": file_was_created, "error_text":error_text})

        if data.graph_2_state:
            try:
                input_resistance = create_plot_recording(abf, abf_c)
                input_resistance.savefig(folder_path + f"/{file[1][:-4]}_recording.png", dpi=300)
                plt.close()

                file_was_created = True
                error_text = False

            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": "Recording plot", "file_was_created": file_was_created, "error_text":error_text})

        if data.graph_3_state:
            try:
                input_resistance_currents = create_plot_protocol(abf, abf_c, channel_c)
                input_resistance_currents.savefig(folder_path + f"/{file[1][:-4]}_protocol.png", dpi=300)
                plt.close()
                
                file_was_created = True
                error_text = False
            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": "Protocol plot", "file_was_created": file_was_created, "error_text":error_text})

        if data.graph_4_state:
            try:
                current_voltage = create_plot_current_voltage(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                current_voltage.savefig(folder_path + f"/{file[1][:-4]}_current_voltage_linear_regression.png", dpi=300)
                plt.close()

                file_was_created = True
                error_text = False
            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": "Current voltage linear regression plot", "file_was_created": file_was_created, "error_text": error_text})

        # ---------------------- Generate tables ----------------------
        if data.ap_table:
            try:
                # Generate table with all columns
                complete_ap_table = create_ap_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/firing_properties_config.csv')
                # Export table data into new excel sheet
                create_and_add_sheet_to_excel(final_output_file_name_AP, file[0], file[1], complete_ap_table, cols_to_export)
                
                file_was_created = True
                error_text = False
            
            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": output_file_name_AP, "file_was_created": file_was_created, "error_text":error_text})

        if data.membrane_table:
            try:
                # Generate table
                complete_table_membrane_properties = create_membrane_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/passive_membrane_properties_config.csv')
                # Export table data into new excel sheet
                create_and_add_sheet_to_excel(final_output_file_name_MB, file[0], file[1], complete_table_membrane_properties, cols_to_export)
                # Load the workbook and immediately - this prevents a buggy behaviour
                workbook = openpyxl.load_workbook(f"{final_output_file_name_MB}.xlsx")
                workbook.close() 
                
                file_was_created = True
                error_text = False

            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": output_file_name_MB, "file_was_created": file_was_created, "error_text":error_text})

        if data.neuronal_overview_table:
            try:
                # Generate table with all columns
                complete_neuronal_overview_table = create_neuronal_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/neuronal_overview_config.csv')
                # Export table data into excel
                create_and_add_row_to_excel(final_output_file_name_NO, file[0], file[1],complete_neuronal_overview_table, cols_to_export)

                file_was_created = True
                error_text = False

            except Exception as e:
                file_was_created = False
                error_text = e

            status_list.append({"file": output_file_name_NO, "file_was_created": file_was_created, "error_text":error_text})

        # Verify the outcome of each file.
        # If any file failed, list all fails with their respective status
        all_files_were_successful = update_gui_status_table(status_list, file, results_output_text, root)
  
    return all_files_were_successful
    