
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

#! MAIN?
def run_analysis(data, file, results_output_text, root):

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

    all_successful = True

    # Only attempt analysis of a file if it is an abf file (just incase there's some other file there)
    if file[1].endswith('.abf'):
        
        # Define the full file path
        data_path = data.input_folder_name + '/' + file[1]
        
        # Ingest data 
        abf = pyabf.ABF(data_path)
        abf_c = pyabf.ABF(data_path)
        
        try: 
            # In file names, the [:-4] is included to remove '.abf' from the filename
            # Manipulate Data, Generate and Save Plots
            if data.graph_1_state:
                firing_currents = create_plot_firing_current(abf, abf_c, channel_c, t1_c, t2_c, stim_start, stim_end)
                firing_currents.savefig(folder_path + f"/{file[1][:-4]}_firing_current.png", dpi=300)
                plt.close()

            if data.graph_2_state:
                input_resistance = create_plot_recording(abf, abf_c)
                input_resistance.savefig(folder_path + f"/{file[1][:-4]}_recording.png", dpi=300)
                plt.close()

            if data.graph_3_state:
                input_resistance_currents = create_plot_protocol(abf, abf_c, channel_c)
                input_resistance_currents.savefig(folder_path + f"/{file[1][:-4]}_protocol.png", dpi=300)
                plt.close()

            if data.graph_4_state:
                current_voltage = create_plot_current_voltage(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                current_voltage.savefig(folder_path + f"/{file[1][:-4]}_current_voltage_linear_regression.png", dpi=300)
                plt.close()

            # Generate tables
            if data.ap_table:
                # Generate table with all columns
                complete_ap_table = create_ap_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/firing_properties_config.csv')
                # Export table data into new excel sheet
                create_and_add_sheet_to_excel(final_output_file_name_AP, file[0], file[1], complete_ap_table, cols_to_export)

            if data.membrane_table:
                # Generate table
                complete_table_membrane_properties = create_membrane_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/passive_membrane_properties_config.csv')
        
                # Export table data into new excel sheet
                create_and_add_sheet_to_excel(final_output_file_name_MB, file[0], file[1], complete_table_membrane_properties, cols_to_export)
                
                # Load the workbook and print the sheet names - this prevents a buggy behaviour
                workbook = openpyxl.load_workbook(f"{final_output_file_name_MB}.xlsx")
                workbook.close() 

            # Generate tables
            if data.neuronal_overview_table:
                # Generate table with all columns
                complete_neuronal_overview_table = create_neuronal_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
                # Convert selected fields from config to list of columns. 
                cols_to_export = get_cols_to_export('main/analysis/output_config/neuronal_overview_config.csv')
                # Export table data into excel
                create_and_add_row_to_excel(final_output_file_name_NO, file[0], file[1],complete_neuronal_overview_table, cols_to_export)

            output_text = f"{file[1][:-4]}"

            # Status update
            display_most_recent_processed_file(output_text,results_output_text, root)
            display_most_recent_processed_file("--Completed successfully",results_output_text, root)
        
        except Warning as w:
            output_text = f"{file[1][:-4]} received a warning because:"
            print(output_text)
            print(w)

            # Status update
            display_most_recent_processed_file(output_text, results_output_text,root)
            display_most_recent_processed_file(f"--{w}", results_output_text,root)

        # Maybe rephrase "Failed becase...to something less harsh"
        except Exception as e:
            output_text = f"{file[1][:-4]} failed because:"
            print(output_text)
            print(e)

            # Status update
            display_most_recent_processed_file(output_text, results_output_text,root)
            display_most_recent_processed_file(f"--{e}", results_output_text,root)

            all_successful = False

    return all_successful
    
def display_most_recent_processed_file(status_update: str, results_output_text, root):
    results_output_text.insert("",END, text = status_update)

