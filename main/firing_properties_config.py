from tkinter import ttk , Toplevel, BooleanVar, Checkbutton
from idlelib.tooltip import Hovertip
import pandas as pd
from gui_style_definitions import init_gui_style
from utils import get_resource_path


#! ------------------------------ Menu for subsetting cols ------------------------------
# here
def config_firing_properities_table():
    top = Toplevel()
    init_gui_style(top)
    top.title("Config firing properties")
    
    title = ttk.Label(top, text="Configure firing properties output columns", style = "TopHeader.TLabel")
    title.grid(row=0, column=1, sticky ='w', pady = (5,3), padx=(10, 10), columnspan = 3)

    description_text = "\
    The excel file contains the firing properties of the analysed neurons. Each sheet is a recording, each\n\
    row is a sweep from that recording (only sweeps with at least one action potential are included in this analysis)\n"
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

        updated_values.append({'clean_name': cols_to_export.loc[1,'clean_name'], 'updated_state': first_isi.get()})
        updated_values.append({'clean_name': cols_to_export.loc[2,'clean_name'], 'updated_state': mean_isi.get()})
        updated_values.append({'clean_name': cols_to_export.loc[3,'clean_name'], 'updated_state': isi_cv.get()})
        updated_values.append({'clean_name': cols_to_export.loc[4,'clean_name'], 'updated_state': current_step.get()})
        updated_values.append({'clean_name': cols_to_export.loc[5,'clean_name'], 'updated_state': membrane_voltage.get()})
        updated_values.append({'clean_name': cols_to_export.loc[6,'clean_name'], 'updated_state': n_of_spikes.get() })
        updated_values.append({'clean_name': cols_to_export.loc[7,'clean_name'], 'updated_state': latency.get() })
        updated_values.append({'clean_name': cols_to_export.loc[8,'clean_name'], 'updated_state': frequency.get() })
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
        updated_values.append({'clean_name': cols_to_export.loc[79,'clean_name'], 'updated_state': amplitude_ap1_apl.get()})
        updated_values.append({'clean_name': cols_to_export.loc[80,'clean_name'], 'updated_state': peak_ap1_apl.get() })
        updated_values.append({'clean_name': cols_to_export.loc[81,'clean_name'], 'updated_state': halfwidth_ap1_apl.get() })

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
        save_path = get_resource_path("main/analysis/output_config/firing_properties_config.csv")
        finalized_df.to_csv(save_path, index=False)  
        # finalized_df.to_csv('main/analysis/output_config/firing_properties_config.csv', index=False)  

        top.destroy()

    def check_checkbutton(initial_state):
        if initial_state == 1:
            check_box.select()

    # Ingest the csv
    try:
        read_path = get_resource_path("main/analysis/output_config/firing_properties_config.csv")
        cols_to_export = pd.read_csv(read_path)
        # cols_to_export = pd.read_csv('main/analysis/output_config/firing_properties_config.csv')
    except FileNotFoundError as e:
        warning_text = ttk.Label(top, 
                                 text="Error - Configuration file not found. Make sure it's named 'firing_properties_config.csv'", 
                                 style = "Variable.TLabel")
        warning_text.grid(row=3, column=1, padx=(10, 10), sticky ='w')

    # 0  ------------------------------------------------------------
    #! Sweep is always included, so not needed as an option

    #? Column 1 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
    data_index = 1
    first_isi = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = first_isi, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    first_isi_tp_text = "Firing frequency calculated and N of spikes/Current injection duration (ms) * 1000 ."
    first_isi_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    first_isi_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    first_isi_tp_icon = Hovertip(first_isi_tp, first_isi_tp_text, hover_delay=50)

    # 2 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    mean_isi = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = mean_isi, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    mean_isi_tp_text = "Average ISI of all the APs of the sweep."
    mean_isi_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    mean_isi_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    mean_isi_tp_icon = Hovertip(mean_isi_tp, mean_isi_tp_text, hover_delay=50)

    # 3 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    isi_cv = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = isi_cv, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    isi_cv_tp_text = "Coefficient of variation (CV) of the ISI, calculated as ISI standard deviation/Mean ISI.\n\
It is a measure of rhythmicity."
    isi_cv_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    isi_cv_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    isi_cv_tp_icon = Hovertip(isi_cv_tp, isi_cv_tp_text, hover_delay=50)

    # 4 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    current_step = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = current_step, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    current_step_tp_text = "Amount of current injected."
    current_step_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    current_step_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    current_step_tp_icon = Hovertip(current_step_tp, current_step_tp_text, hover_delay=50)

    # 5 ------------------------------------------------------------
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

    # 6 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    n_of_spikes = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = n_of_spikes, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    n_of_spikes_tp_text = "Number of action potentials (AP) that are detected during the current injection.\n\
If spikes happen before or after the current injection, they are automatically excluded."
    n_of_spikes_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    n_of_spikes_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    n_of_spikes_tp_icon = Hovertip(n_of_spikes_tp, n_of_spikes_tp_text, hover_delay=50)

    # 7 ------------------------------------------------------------
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

    # 8 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    frequency = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = frequency, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    frequency_tp_text = "Firing frequency calculated ad N of spikes/Current injection duration (ms) * 1000."
    frequency_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    frequency_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    frequency_tp_icon = Hovertip(frequency_tp, frequency_tp_text, hover_delay=50)

    # 9 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_amplitude = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_amplitude, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=1, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_amplitude_tp_text = "Height of the AP from firing threshold to peak."
    ap_amplitude_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_amplitude_tp.grid(row=placement_index, column=2, padx=(0, 10), sticky ='w')
    ap_amplitude_tp_icon = Hovertip(ap_amplitude_tp, ap_amplitude_tp_text, hover_delay=50)


    #? Column 2 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
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

    # 2 ------------------------------------------------------------
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

    # 3 ------------------------------------------------------------
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

    # 4 ------------------------------------------------------------
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

    # 5 ------------------------------------------------------------
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

    # 6 ------------------------------------------------------------
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

    # 7 ------------------------------------------------------------
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

    # 8 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_fall_rate = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_fall_rate, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_fall_rate_tp_text = "Rate of change of voltage over time,\n\
calculated as dV/dt from AP threshold to AP peak (rise) and AP peak to AHP voltage (fall)."
    ap_fall_rate_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_fall_rate_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_fall_rate_tp_icon = Hovertip(ap_fall_rate_tp, ap_fall_rate_tp_text, hover_delay=50)

    # 9 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    ap_rise_time = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = ap_rise_time, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=3, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    ap_rise_time_tp_text = "Time between AP threshold and peak in the depolarization phase (rise)\n\
and repolarization phase (fall) of the AP."
    ap_rise_time_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    ap_rise_time_tp.grid(row=placement_index, column=4, padx=(0, 10), sticky ='w')
    ap_rise_time_tp_icon = Hovertip(ap_rise_time_tp, ap_rise_time_tp_text, hover_delay=50)


    #? Column 3 ------------------------------------------------------------
    # 1 ------------------------------------------------------------
    placement_index = 3
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

    # 2 ------------------------------------------------------------
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

    # 3 ------------------------------------------------------------
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

    # 4 ------------------------------------------------------------
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

    # 5 ------------------------------------------------------------
    #! These are at the bottom of the table, so the index jumps heaps
    placement_index += 1
    data_index = 79
    amplitude_ap1_apl = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = amplitude_ap1_apl, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])
    
    # Tooltip
    amplitude_ap1_apl_tp_text = "Ratio between the amplitude of the first and the last action potential."
    amplitude_ap1_apl_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    amplitude_ap1_apl_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    amplitude_ap1_apl_tp_icon = Hovertip(amplitude_ap1_apl_tp, amplitude_ap1_apl_tp_text, hover_delay=50)

    # 6 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    peak_ap1_apl = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = peak_ap1_apl, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    peak_ap1_apl_tp_text = "Ratio between the peak of the first and the last action potential."
    peak_ap1_apl_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    peak_ap1_apl_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    peak_ap1_apl_tp_icon = Hovertip(peak_ap1_apl_tp, peak_ap1_apl_tp_text, hover_delay=50)

    # 7 ------------------------------------------------------------
    placement_index += 1
    data_index += 1
    halfwidth_ap1_apl = BooleanVar()
    check_box = Checkbutton(top, text = cols_to_export.loc[data_index,'clean_name'], variable = halfwidth_ap1_apl, 
                            onvalue = 1, offvalue = 0,anchor = 'w', width=200, font = ('calibri', 13), background = 'white') 

    check_box.grid(row=placement_index, column=5, padx = (10,0))
    check_checkbutton(cols_to_export.loc[data_index,'to_include'])

    # Tooltip
    halfwidth_ap1_apl_tp_text = "Ratio between the half width of the first and the last action potential."
    halfwidth_ap1_apl_tp = ttk.Label(top, text="(?)", style  = 'Hover.TLabel')
    halfwidth_ap1_apl_tp.grid(row=placement_index, column=6, padx=(0, 10), sticky ='w')
    halfwidth_ap1_apl_tp_icon = Hovertip(halfwidth_ap1_apl_tp, halfwidth_ap1_apl_tp_text, hover_delay=50)


    #? ---------------- Save button ----------------
    save_button = ttk.Button(top,
                             text="Save", 
                             command=save_values,
                             style = 'Save_settings.TButton')

    save_button.grid(row= 15, column=3, padx = (10,0), pady = (20,20), sticky = 'w')