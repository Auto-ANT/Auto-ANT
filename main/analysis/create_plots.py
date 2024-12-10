
#! FILE 1 - CREATE PLOTS
# Pupose: Creates charts 
# Input ABF file, 
# Outputs Charts. 
# Returns three plots
 
from ipfx.feature_extractor import SpikeFeatureExtractor, SpikeTrainFeatureExtractor
import pandas as pd
from efel import getFeatureValues
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def create_plot_firing_current(abf, abf_c, channel_c, t1_c, t2_c, stim_start, stim_end):
    # Set the dataframe for the table
    table_2 = pd.DataFrame()

    # Loop function to analyze each voltage and current trace of the file
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        abf_c.setSweep(sweep, channel = channel_c)

        time = abf.sweepX
        voltage = abf.sweepY
        current = abf_c.sweepC

        currents = [] # Current value between t1 and t2 (ms) for each step
        t1 = int(t1_c*abf.dataPointsPerMs) 
        t2 = int(t2_c*abf.dataPointsPerMs)
        current_mean = np.average(abf_c.sweepC[t1:t2])

        sfx = SpikeFeatureExtractor(start=stim_start/1000, end=stim_end/1000, filter=None)
        sfx_results = sfx.process(time, voltage, current)
        stfx = SpikeTrainFeatureExtractor (start=stim_start/1000, end=stim_end/1000)
        stfx_results = stfx.process(time, voltage, current, sfx_results)

        length = len(table_2)
        table_2.loc[length, 'current_step'] = current_mean
        table_2.loc[length, 'avg_rate'] = stfx_results["avg_rate"]
        
    fig = plt.figure(figsize=(15, 5))

    # Input-output curve
    currents = []
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        abf_c.setSweep(sweep, channel = channel_c)
        currents.append(np.average(abf_c.sweepC[t1:t2]))
    plt.plot(currents, table_2.loc[:,'avg_rate'])
    plt.xlabel('Current step (pA)', fontsize=16)
    plt.ylabel('Firing Rate (Hz)', fontsize=16)
    plt.tick_params(axis='both', labelsize=12)

    #plt.title('Firing Rate vs Current')
    
    return(fig)


def create_plot_recording(abf, abf_c):
    # All traces
    fig = plt.figure(figsize=(15, 5))
    
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        plt.plot(abf.sweepX, abf.sweepY, alpha=.6, label="Sweep %d" % (sweep))
    plt.ylabel('Membrane voltage (mV)', fontsize=16)
    plt.xlabel('Time (s)', fontsize=16)
    plt.tick_params(axis='both', labelsize=12)
    
    # To highlight one trace
    abf.setSweep(0) 
    plt.plot(abf.sweepX, abf.sweepY, linewidth=1, color='black')

    return(fig)

def create_plot_protocol(abf, abf_c, channel_c):
    # All current steps
    fig = plt.figure(figsize=(15, 5))
    
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        abf_c.setSweep(sweep, channel = channel_c)
        current = abf_c.sweepC
        plt.plot(abf.sweepX, current, alpha=.6, label="Sweep %d" % (sweep))
        
    plt.ylabel("Current (pA)", fontsize=16)
    plt.xlabel("Time (s)", fontsize=16)
    plt.tick_params(axis='both', labelsize=12)
    
    return(fig)


def create_plot_current_voltage (abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    
    table_m = pd.DataFrame(columns=['Sweep', 
                                    'current_pA', 
                                    'steady_state_voltage_stimend'])  
    
    # Loop function
    for sweep in abf.sweepList:  # To select a range of traces
        abf.setSweep(sweep, channel = channel)
        abf_c.setSweep(sweep, channel = channel_c)
        # Defines a trace and region of analysis
        trace = {'T': abf.sweepX*1000, # convert to ms
                 'V': abf.sweepY,
                 'I': abf_c.sweepC,
                 'stim_start' : [stim_start],
                 'stim_end' : [stim_end]}
        traces = [trace]
        
        currents = [] # Current value between t1 and t2 (ms) for each step
        t1 = int(t1_c*abf.dataPointsPerMs) 
        t2 = int(t2_c*abf.dataPointsPerMs)
        current_mean = np.average(abf_c.sweepC[t1:t2])

        # Output features
        feature_values = getFeatureValues(traces,
                                               ['voltage', 'steady_state_voltage_stimend', 
                                                'current', 'time_constant', 
                                                'sag_amplitude', 
                                                'sag_ratio1', 'AP_amplitude'],
                                               raise_warnings=None)[0] # If true, returns warnings

        # Optional: create table from the results
        # Use [0] to extract the values from the Spikecount array
        length = len(table_m)
        if feature_values["AP_amplitude"] is None and current_mean <100:
            table_m.loc[length, 'Sweep'] = sweep
            table_m.loc[length, 'steady_state_voltage_stimend'] = feature_values['steady_state_voltage_stimend'][0]
            table_m.loc[length, 'current_pA'] = current_mean # [] to select the rows of current step
        elif feature_values["AP_amplitude"] is not None:
            if len(feature_values['AP_amplitude']) <1:
                table_m.loc[length, 'Sweep'] = sweep
                table_m.loc[length, 'steady_state_voltage_stimend'] = feature_values['steady_state_voltage_stimend'][0]
                table_m.loc[length, 'current_pA'] = current_mean # [] to select the rows of current step


    fig = plt.figure(figsize=(10, 5))
    current = table_m["current_pA"].to_list()
    voltage = table_m["steady_state_voltage_stimend"].to_list()
    
    # I-V graph
    fig.tight_layout()
    fig.set_canvas(plt.gcf().canvas)

    ax = fig.add_subplot()
    ax.scatter(current, voltage)
    ax.set_xlabel('Current (pA)', fontsize=16)
    ax.set_ylabel('Voltage (mV)', fontsize=16)
    ax.tick_params(axis='both', labelsize=12)
    
    # Linear regression using the function polyfit (degree 1)
    m, b = np.polyfit(current, voltage, 1)
    # Plot regression line
    line = np.polyval([m, b], current)
    plt.plot(current, line, color='r')
    ax.set_title(f'Input resistance (GOhm) = {m}')

    return(fig)
