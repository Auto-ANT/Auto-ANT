from tkinter import ttk , Toplevel, BooleanVar, Checkbutton
from idlelib.tooltip import Hovertip
import pandas as pd
from gui_style_definitions import init_gui_style

from utils import get_resource_path


#! ------------------------------ Menu for subsetting cols ------------------------------
# here
def config_neuronal_overview_table():
    top = Toplevel()
    init_gui_style(top)
    top.title("Config neuronal overview")
    title = ttk.Label(top, text="Configure neuronal overview output columns", style = "TopHeader.TLabel")
    title.grid(row=0, column=1, sticky ='w', pady = (5,3), padx=(10, 10), columnspan = 3)

    description_text = "\
    The excel file contains a summary table containing an overview of the properties of each recording in the\n\
    input folder. The file consists of a single sheet, where each row corresponds to a recording.\n"
    description = ttk.Label(top, text=description_text, style = "pText.TLabel")
    description.grid(row = 1, column = 1, sticky ='w', columnspan = 4)

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

        updated_values.append({'clean_name': cols_to_export.loc[1,'clean_name'], 'updated_state': resting_membrane_potential.get()})
        updated_values.append({'clean_name': cols_to_export.loc[2,'clean_name'], 'updated_state': sag_amplitude.get()})
        updated_values.append({'clean_name': cols_to_export.loc[3,'clean_name'], 'updated_state': sag_ratio.get()})
        updated_values.append({'clean_name': cols_to_export.loc[4,'clean_name'], 'updated_state': membrane_input_resistance.get()})
        updated_values.append({'clean_name': cols_to_export.loc[5,'clean_name'], 'updated_state': membrane_time_constant.get()})
        updated_values.append({'clean_name': cols_to_export.loc[6,'clean_name'], 'updated_state': membrane_capacitance.get() })
        updated_values.append({'clean_name': cols_to_export.loc[7,'clean_name'], 'updated_state': rheobase.get() })
        updated_values.append({'clean_name': cols_to_export.loc[8,'clean_name'], 'updated_state': latency.get() })
        
        updated_values.append({'clean_name': cols_to_export.loc[9,'clean_name'], 'updated_state': ap_amplitude.get() })
        updated_values.append({'clean_name': cols_to_export.loc[10,'clean_name'], 'updated_state': ap_peak.get()})
        updated_values.append({'clean_name': cols_to_export.loc[11,'clean_name'], 'updated_state': ap_width.get()})
        updated_values.append({'clean_name': cols_to_export.loc[12,'clean_name'], 'updated_state': ap_half_width.get()})
        updated_values.append({'clean_name': cols_to_export.loc[13,'clean_name'], 'updated_state': ap_threshold.get()})
        updated_values.append({'clean_name': cols_to_export.loc[14,'clean_name'], 'updated_state': ap_peak_upstroke.get()})
        updated_values.append({'clean_name': cols_to_export.loc[15,'clean_name'], 'updated_state': ap_peak_downstroke.get() })
        updated_values.append({'clean_name': cols_to_export.loc[16,'clean_name'], 'updated_state': ap_rise_rate.get() })

        updated_values.append({'clean_name': cols_to_export.loc[17,'clean_name'], 'updated_state': ap_fall_rate.get() })
        updated_values.append({'clean_name': cols_to_export.loc[18,'clean_name'], 'updated_state': ap_rise_time.get() })
        updated_values.append({'clean_name': cols_to_export.loc[19,'clean_name'], 'updated_state': ap_fall_time.get()})
        updated_values.append({'clean_name': cols_to_export.loc[20,'clean_name'], 'updated_state': ap_abs_depth.get()})
        updated_values.append({'clean_name': cols_to_export.loc[21,'clean_name'], 'updated_state': ap_time_from_peak.get()})
        updated_values.append({'clean_name': cols_to_export.loc[22,'clean_name'], 'updated_state': ap_depth_from_threshold.get()})

        #! NOTE
        #! So, there are some variables that repat. EG APamplitude 1, 2 , 3 etc.
        #! Users sjould only select AP_Amplitude, not each number
        #! the solution is - They all share the same "show name" but they have different technical names
        #! That way, when it is joined in the next step, it becomes a many-to-one join.
        #? Conclusion - If you selecct AP_amplitude, you get all ap_amplitudes (1,2,3 etc)

        new_values = pd.DataFrame(updated_values)
        updated_df = cols_to_export.merge(new_values, on = 'clean_name', how = 'left')

        # Convert Tru/False to 1/0
        updated_df['to_include'] = updated_df.apply(update_target_column, axis = 1)

        # Now, just subset and save the excel with the same name
        finalized_df = updated_df[['clean_name','column', 'to_include']]

        save_path = get_resource_path("main/analysis/output_config/neuronal_overview_config.csv")
        finalized_df.to_csv(save_path, index=False)  
        # finalized_df.to_csv('main/analysis/output_config/neuronal_overview_config.csv', index=False)  

        top.destroy()

    def check_checkbutton(initial_state):
        if initial_state == 1:
            check_box.select()

    # Ingest the csv
    try:
        read_path = get_resource_path("main/analysis/output_config/neuronal_overview_config.csv")
        cols_to_export = pd.read_csv(read_path)
        # cols_to_export = pd.read_csv('main/analysis/output_config/neuronal_overview_config.csv')
    except FileNotFoundError as e:
        warning_text = ttk.Label(top, 
                                 text="Error - Configuration file not found. Make sure it's named 'neuronal_overview_config.csv'", 
                                 style = "Variable.TLabel")
        warning_text.grid(row=3, column=1, padx=(10, 10), sticky ='w')

    # 0  ------------------------------------------------------------
    #! Sweep is always included, so not needed as an option

    #? Column 1 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index = 1
    resting_membrane_potential = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = resting_membrane_potential, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    resting_membrane_potential_tp_text = "Membrane voltage when the neuron is in a resting state. It is caluclated as the average voltage during\n\
the last 10% of time before the first current step of the protocol is deleivered to the neuron. "
    resting_membrane_potential_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    resting_membrane_potential_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    resting_membrane_potential_tp_icon = Hovertip(resting_membrane_potential_tp, resting_membrane_potential_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    sag_amplitude = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = sag_amplitude, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    sag_amplitude_tp_text = "Amplitude of the sag, calculated as the difference between the minimum membrane voltage\n\
reached during hyperpolarization and the steady membrane voltage. This value is caluclated on the most hyperpolarized step of the protocol."
    sag_amplitude_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    sag_amplitude_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    sag_amplitude_tp_icon = Hovertip(sag_amplitude_tp, sag_amplitude_tp_text, hover_delay=50)


    # 3 ------------------------------------------------------------
    placement_index +=1
    data_index += 1
    sag_ratio = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = sag_ratio, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    sag_ratio_tp_text = "Ratio between the Voltage delta and the Sag amplitude,\n\
calculated as (Voltage base - steady membrane voltage)/Sag amplitude. This value is caluclated on the most hyperpolarized step of the protocol."
    sag_ratio_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    sag_ratio_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    sag_ratio_tp_icon = Hovertip(sag_ratio_tp, sag_ratio_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    membrane_input_resistance = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = membrane_input_resistance, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    membrane_input_resistance_tp_text = "It indicates how much a neuron depolarizes in response to a steady current.\n\
It is a measure of excitability, and it is calculated as the slope of the linear regression of the\n\
membrane voltage on the injected current."
    membrane_input_resistance_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    membrane_input_resistance_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    membrane_input_resistance_tp_icon = Hovertip(membrane_input_resistance_tp, membrane_input_resistance_tp_text, hover_delay=50)


    # 5 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    membrane_time_constant = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = membrane_time_constant, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    membrane_time_constant_tp_text = "The time it takes for the cell membrane's potential to fall to 63% of its final value\n\
after a small negative current pulse. It is calculated as the average exponential decay of the the membrane voltage \n\
in response to the injection of hyperpolarizing current steps beetween -50pA and -40pA, in absense of AP. "
    membrane_time_constant_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    membrane_time_constant_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    membrane_time_constant_tp_icon = Hovertip(membrane_time_constant_tp, membrane_time_constant_tp_text, hover_delay=50)   


    # 6 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    membrane_capacitance = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = membrane_capacitance, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    membrane_capacitance_tp_text = "The electrical membrane capacitance of the membrane calculated as Membrane time constant/Membrane input resistance."
    membrane_capacitance_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    membrane_capacitance_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    membrane_capacitance_tp_icon = Hovertip(membrane_capacitance_tp, membrane_capacitance_tp_text, hover_delay=50)

    # 7 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    rheobase = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = rheobase, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    rheobase_tp_text = "It is the amount of current necessary to induce the first AP."
    rheobase_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    rheobase_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    rheobase_tp_icon = Hovertip(rheobase_tp, rheobase_tp_text, hover_delay=50)

    # 8 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    latency = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = latency, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    latency_tp_text = "Time from the start of the current injection to the peak of the first AP."
    latency_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    latency_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    latency_tp_icon = Hovertip(latency_tp, latency_tp_text, hover_delay=50)


    #? Column 2 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index += 1
    ap_amplitude = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_amplitude, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_amplitude_tp_text = "Height of the AP from firing threshold to peak."
    ap_amplitude_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_amplitude_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_amplitude_tp_icon = Hovertip(ap_amplitude_tp, ap_amplitude_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_peak = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_peak, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_peak_tp_text = "Maximum voltage reached by the AP."
    ap_peak_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_peak_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_peak_tp_icon = Hovertip(ap_peak_tp, ap_peak_tp_text, hover_delay=50)

    # 3 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_width = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_width, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_width_tp_text = "Width of the AP at the firing threshold."
    ap_width_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_width_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_width_tp_icon = Hovertip(ap_width_tp, ap_width_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_half_width = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_half_width, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_half_width_tp_text = "Width of the AP at half the AP amplitude."
    ap_half_width_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_half_width_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_half_width_tp_icon = Hovertip(ap_half_width_tp, ap_half_width_tp_text, hover_delay=50)

    # 5 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_threshold = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_threshold, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_threshold_tp_text = "Voltage at the AP start.  "
    ap_threshold_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_threshold_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_threshold_tp_icon = Hovertip(ap_threshold_tp, ap_threshold_tp_text, hover_delay=50)

    # 6 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_peak_upstroke = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_peak_upstroke, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])
    
    # Tooltip
    ap_peak_upstroke_tp_text = "Maximum rise rate of the AP (positive number)."
    ap_peak_upstroke_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_peak_upstroke_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_peak_upstroke_tp_icon = Hovertip(ap_peak_upstroke_tp, ap_peak_upstroke_tp_text, hover_delay=50)


    # 7 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_peak_downstroke = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_peak_downstroke, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_peak_downstroke_tp_text = "Minimum fall rate of the AP (negative number)."
    ap_peak_downstroke_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_peak_downstroke_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_peak_downstroke_tp_icon = Hovertip(ap_peak_downstroke_tp, ap_peak_downstroke_tp_text, hover_delay=50)

    # 8 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_rise_rate = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_rise_rate, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_rise_rate_tp_text = "Rate of change of voltage over time,\n\
calculated as dV/dt from AP threshold to AP peak (rise) and AP peak to AHP voltage (fall)."
    ap_rise_rate_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_rise_rate_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_rise_rate_tp_icon = Hovertip(ap_rise_rate_tp, ap_rise_rate_tp_text, hover_delay=50)

    #? Column 3 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index += 1
    ap_fall_rate = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_fall_rate, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_fall_rate_tp_text = "Rate of change of voltage over time,\n\
calculated as dV/dt from AP threshold to AP peak (rise) and AP peak to AHP voltage (fall)."
    ap_fall_rate_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_fall_rate_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_fall_rate_tp_icon = Hovertip(ap_fall_rate_tp, ap_fall_rate_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_rise_time = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_rise_time, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_rise_time_tp_text = "Time between AP threshold and peak in the depolarization phase (rise)\n\
and repolarization phase (fall) of the AP."
    ap_rise_time_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_rise_time_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_rise_time_tp_icon = Hovertip(ap_rise_time_tp, ap_rise_time_tp_text, hover_delay=50)

    # 3 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_fall_time = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_fall_time, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_fall_time_tp_text = "Time between AP threshold and peak in the depolarization phase (rise)\n\
and repolarization phase (fall) of the AP."
    ap_fall_time_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_fall_time_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_fall_time_tp_icon = Hovertip(ap_fall_time_tp, ap_fall_time_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_abs_depth = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_abs_depth, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_abs_depth_tp_text = "Minimum voltage reached during after hyperpolarization (AHP)."
    ap_abs_depth_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_abs_depth_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_abs_depth_tp_icon = Hovertip(ap_abs_depth_tp, ap_abs_depth_tp_text, hover_delay=50)

    # 5 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_time_from_peak = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_time_from_peak, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_time_from_peak_tp_text = "Time from AP peak to AHP."
    ap_time_from_peak_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_time_from_peak_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_time_from_peak_tp_icon = Hovertip(ap_time_from_peak_tp, ap_time_from_peak_tp_text, hover_delay=50)

    # 6 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_depth_from_threshold = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_depth_from_threshold, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_depth_from_threshold_tp_text = "Voltage delta between AP threshold and AHP."
    ap_depth_from_threshold_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_depth_from_threshold_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    ap_depth_from_threshold_tp_icon = Hovertip(ap_depth_from_threshold_tp, ap_depth_from_threshold_tp_text, hover_delay=50)


    #? ---------------- Save button ----------------
    save_button = ttk.Button(top,
                             text="Save", 
                             command=save_values,
                             style = 'Save_settings.TButton')

    save_button.grid(row= 15, column=3, padx = (10,0), pady = (20,20), sticky = 'w')