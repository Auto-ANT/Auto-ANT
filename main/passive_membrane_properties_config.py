from tkinter import ttk , Toplevel, BooleanVar, Checkbutton
from idlelib.tooltip import Hovertip
import pandas as pd
from gui_style_definitions import init_gui_style
from utils import get_resource_path


#! ------------------------------ Menu for subsetting cols ------------------------------
# here
def passive_membrane_properities_table():
    top = Toplevel()
    init_gui_style(top)

    top.title("Configure passive membrane properties")
    title = ttk.Label(top, text="Configure passive membrane properties output columns", style = "TopHeader.TLabel")
    title.grid(row=0, column=1, sticky = 'w', pady = (5,3), padx=(10, 10), columnspan = 3)

    description_text = f"\
    Excel file containing the passive menmbrane properties of the analysed neurons. Each sheet is a recording, each\n\
    row is a sweep from that recording (only sweeps with no action potentials are included in this analysis)\n"
    description = ttk.Label(top, text=description_text, style = "pText.TLabel")
    description.grid(row = 1, column = 1, sticky = 'w', columnspan = 4)

    top.grid_columnconfigure(1, weight=2, uniform="sample")
    top.grid_columnconfigure(2, weight=1, uniform="sample")
    top.grid_columnconfigure(3, weight=2, uniform="sample")
    top.grid_columnconfigure(4, weight=1, uniform="sample")
    top.grid_columnconfigure(5, weight=2, uniform="sample")
    top.grid_columnconfigure(6, weight=1, uniform="sample")

    #? ---------------- Create buttons and check if required ----------------
    def save_values():
        def update_target_column(row):
            if row['updated_state']:
                return 1
            else:
                return 0
            
        # Fetch all values, create a dictionary, craete data frame, join and update original, save it to csv
        updated_values = []
        updated_values.append({'clean_name': cols_to_export.loc[0,'clean_name'], 'updated_state': 1 })
        
        updated_values.append({'clean_name': cols_to_export.loc[1,'clean_name'], 'updated_state': current.get()})
        updated_values.append({'clean_name': cols_to_export.loc[2,'clean_name'], 'updated_state': voltage_base.get()})
        updated_values.append({'clean_name': cols_to_export.loc[3,'clean_name'], 'updated_state': membrane_voltage.get()})
        updated_values.append({'clean_name': cols_to_export.loc[4,'clean_name'], 'updated_state': time_constant.get()})

        updated_values.append({'clean_name': cols_to_export.loc[5,'clean_name'], 'updated_state': input_resistance.get()})
        updated_values.append({'clean_name': cols_to_export.loc[6,'clean_name'], 'updated_state': capacitance.get() })
        updated_values.append({'clean_name': cols_to_export.loc[7,'clean_name'], 'updated_state': decay_time_constant.get() })
        updated_values.append({'clean_name': cols_to_export.loc[8,'clean_name'], 'updated_state': sag_amplitude.get() })

        updated_values.append({'clean_name': cols_to_export.loc[9,'clean_name'], 'updated_state': sag_ratio.get()})
        updated_values.append({'clean_name': cols_to_export.loc[10,'clean_name'], 'updated_state': sag_time_constant.get()})


        new_values = pd.DataFrame(updated_values)
        updated_df = cols_to_export.merge(new_values, on = 'clean_name', how = 'left')

        # Convert Tru/False to 1/0
        updated_df['to_include'] = updated_df.apply(update_target_column, axis = 1)

        # Now, just subset and save the excel with the same name
        finalized_df = updated_df[['clean_name','column', 'to_include']]
        save_path = get_resource_path("main/analysis/output_config/passive_membrane_properties_config.csv")
        finalized_df.to_csv(save_path, index=False)  
        # finalized_df.to_csv('main/analysis/output_config/passive_membrane_properties_config.csv', index=False)  

        top.destroy()

    def check_checkbutton(initial_state):
        if initial_state == 1:
            check_box.select()

    # Ingest the csv
    try:
        read_path = get_resource_path("main/analysis/output_config/passive_membrane_properties_config.csv")
        cols_to_export = pd.read_csv(read_path)
        # cols_to_export = pd.read_csv('main/analysis/output_config/passive_membrane_properties_config.csv')
        # print(cols_to_export)
    except FileNotFoundError as e:
        warning_text = ttk.Label(top, 
                                 text="Error - Configuration file not found. Make sure it's named 'passive_membrane_properties_config.csv'", 
                                 style = "Variable.TLabel")
        warning_text.grid(row=3, column=1, padx=(10, 10), sticky = 'w')


    # 0  ------------------------------------------------------------
    #! Sweep is always included, so not needed as an option

    #? Column 1 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index = 1
    current = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = current, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    current_tp_text = "Amount of current injected."
    current_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    current_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    current_tp_icon = Hovertip(current_tp, current_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    voltage_base = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = voltage_base, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    voltage_base_tp_text = "Membrane voltage before current is injected.\n\
It is calculated as the average voltage during the last 10% of time before current injection."
    voltage_base_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    voltage_base_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    voltage_base_tp_icon = Hovertip(voltage_base_tp, voltage_base_tp_text, hover_delay=50)

    # 3 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    membrane_voltage = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = membrane_voltage, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    membrane_voltage_tp_text = "Membrane voltage in response to the injected current.\n\
It is calculated as the average voltage for the last 10% of the current injection duration."
    membrane_voltage_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    membrane_voltage_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    membrane_voltage_tp_icon = Hovertip(membrane_voltage_tp, membrane_voltage_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    time_constant = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = time_constant, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    time_constant_tp_text = "The time it takes for the cell membrane's potential to fall to 63% of its final value\n\
after a small negative current pulse. It is calculated as the exponential fit of the membrane voltage\n\
during hyperpolarization. "
    time_constant_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    time_constant_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    time_constant_tp_icon = Hovertip(time_constant_tp, time_constant_tp_text, hover_delay=50)   

    #? Column 2 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index += 1
    input_resistance = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = input_resistance, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    input_resistance_tp_text = "It indicates how much a neuron depolarizes in response to a steady current.\n\
It is a measure of excitability, and it is calculated using Ohm's law as Steady membrane voltage/current\n\
step per sweep."
    input_resistance_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    input_resistance_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    input_resistance_tp_icon = Hovertip(input_resistance_tp, input_resistance_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    capacitance = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = capacitance, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    capacitance_tp_text = "The electrical capacitance of the membrane calculated as Membrane time constant/input resistance."
    capacitance_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    capacitance_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    capacitance_tp_icon = Hovertip(capacitance_tp, capacitance_tp_text, hover_delay=50)

    # 3 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    decay_time_constant = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = decay_time_constant, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    decay_time_constant_tp_text = "Time constant of the voltage decay after the injected current, calculated as specified for Membrane time constant."
    decay_time_constant_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    decay_time_constant_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    decay_time_constant_tp_icon = Hovertip(decay_time_constant_tp, decay_time_constant_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    sag_amplitude = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = sag_amplitude, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    sag_amplitude_tp_text = "Amplitude of the sag, calculated as the difference between the minimum membrane voltage\n\
reached during hyperpolarization and the steady membrane voltage."
    sag_amplitude_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    sag_amplitude_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    sag_amplitude_tp_icon = Hovertip(sag_amplitude_tp, sag_amplitude_tp_text, hover_delay=50)


    #? Column 3 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index += 1
    sag_ratio = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = sag_ratio, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    sag_ratio_tp_text = "Ratio between the Voltage delta and the Sag amplitude,\n\
calculated as (Voltage base - steady membrane voltage)/Sag amplitude."
    sag_ratio_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    sag_ratio_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    sag_ratio_tp_icon = Hovertip(sag_ratio_tp, sag_ratio_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    sag_time_constant = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = sag_time_constant, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    sag_time_constant_tp_text = "Time constant of the exponential voltage decay from the bottom\n\
of the sag to the steady membrane voltage."
    sag_time_constant_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    sag_time_constant_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    sag_time_constant_tp_icon = Hovertip(sag_time_constant_tp, sag_time_constant_tp_text, hover_delay=50)

    #? ---------------- Save button ----------------
    save_button = ttk.Button(top,
                             text="Save", 
                             command=save_values,
                             style = 'Save_settings.TButton')

    save_button.grid(row = 7, column=3, padx = (10,0), pady = (20,20), sticky = 'w')