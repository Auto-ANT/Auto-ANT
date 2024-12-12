"""
create_tables.py 
Houses all functions used to create table, i.e.,
Neuronal overview table, Action Potential table, and membrane potential table

Input: ABF files,
Output: Tables (pandas dataframes)
"""

import pandas as pd
from ipfx.feature_extractor import SpikeFeatureExtractor, SpikeTrainFeatureExtractor
from efel import getFeatureValues
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

#! ----- Action Potential Table - Combination of IPFX and AP table
# IPFX TABLE
def generate_ipfx_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    
    table_1 = pd.DataFrame()

    # Loop function to analyze each voltage and current trace of the file
    for sweep in abf.sweepList:
        # abf.setSweep(sweep)
        abf.setSweep(sweep, channel = channel)
        abf_c.setSweep(sweep, channel = channel_c)

        time = abf.sweepX
        voltage = abf.sweepY
        current = abf_c.sweepC

        currents = [] # Current value between t1 and t2 (ms) for each step
        t1 = int(t1_c*abf.dataPointsPerMs) 
        t2 = int(t2_c*abf.dataPointsPerMs)
        current_mean = np.average(abf_c.sweepC[t1:t2])

        sfx = SpikeFeatureExtractor(start=(stim_start/1000), end=(stim_end/1000), filter=None)
        sfx_results = sfx.process(time, voltage, current)
        stfx = SpikeTrainFeatureExtractor (start=(stim_start/1000), end=(stim_end/1000))
        stfx_results = stfx.process(time, voltage, current, sfx_results)

        # Create a table with the stfx results
        length = len(table_1)

        if stfx_results ['avg_rate'] > 0:
            table_1.loc[length, 'Sweep'] = sweep
            table_1.loc[length, 'First ISI (ms)'] = stfx_results ["first_isi"]*1000
            table_1.loc[length, 'Mean ISI (ms)'] = stfx_results ["mean_isi"]*1000
            table_1.loc[length, 'ISI CV'] = stfx_results ["isi_cv"] #Coefficient of variation
    
    return(table_1)


#! FILE 3
# AP table
def generate_AP_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):

    # Define the variables
    for sweep in abf.sweepList:
        # abf.setSweep(sweep)
        abf.setSweep(sweep, channel = channel)
        abf_c.setSweep(sweep, channel = channel_c)
        time = abf.sweepX*1000 # in miliseconds
        voltage = abf.sweepY
        current = abf_c.sweepC

    # Define the variables and region of analysis
    trace = {'T': abf.sweepX*1000, 
             'V': abf.sweepY,
             'stim_start': [stim_start],
             'stim_end': [stim_end]} 
    traces = [trace]

    # Optional: Current step values
    currents = [] # Current value between t1 and t2 (ms) for each step
    t1 = int(t1_c*abf.dataPointsPerMs) 
    t2 = int(t2_c*abf.dataPointsPerMs)
    current_mean = np.average(abf_c.sweepC[t1:t2])

    # OptionaL Create a table with the results-> what you want to display
    table = pd.DataFrame(columns=[#general
                                 'Sweep', 'Current step (pA)', 'Membrane voltage (mV)', 'N of spikes', 'Latency (ms)','Frequency (Hz)',

                                #Average
                                'Average amplitude (mV)', 'Average peak (mV)', 'Average width (ms)', 'Average half width (ms)','Average threshold (mV)',
                                'Average peak upstroke (V/s)', 'Average peak downstroke (V/s)', 'Average rise rate', 'Average fall rate',
                                'Average rise time (ms)', 'Average fall time (ms)', 'Average AHP abs depth', 'Average AHP time from peak (ms)', 'Average AHP depth from threshold (mV)',

                                 #AP1
                                'AP1 amplitude (mV)', 'AP1 peak (mV)', 'AP1 width (ms)', 'AP1 half width (ms)','AP1 threshold (mV)',
                                'AP1 peak upstroke (V/s)', 'AP1 peak downstroke (V/s)', 'AP1 rise rate', 'AP1 fall rate',
                                'AP1 rise time (ms)', 'AP1 fall time (ms)', 'AHP1 abs depth', 'AHP1 time from peak (ms)', 'AHP1 depth from threshold (mV)',
                
                                #AP2
                                'AP2 amplitude (mV)', 'AP2 peak (mV)', 'AP2 width (ms)', 'AP2 half width (ms)','AP2 threshold (mV)',
                                'AP2 peak upstroke (V/s)', 'AP2 peak downstroke (V/s)', 'AP2 rise rate', 'AP2 fall rate',
                                'AP2 rise time (ms)', 'AP2 fall time (ms)', 'AHP2 abs depth', 'AHP2 time from peak (ms)', 'AHP2 depth from threshold (mV)',
                                    
                                #APsL
                                'APsL amplitude (mV)', 'APsL peak (mV)', 'APsL width (ms)', 'APsL half width (ms)','APsL threshold (mV)',
                                'APsL peak upstroke (V/s)', 'APsL peak downstroke (V/s)', 'APsL rise rate', 'APsL fall rate',
                                'APsL rise time (ms)', 'APsL fall time (ms)', 'AHPsL abs depth', 'AHPsL time from peak (ms)', 'AHPsL depth from threshold (mV)',
                                    
                                #APL
                                'APL amplitude (mV)', 'APL peak (mV)', 'APL width (ms)', 'APL half width (ms)','APL threshold (mV)',
                                'APL peak upstroke (V/s)', 'APL peak downstroke (V/s)', 'APL rise rate', 'APL fall rate',
                                'APL rise time (ms)', 'APL fall time (ms)', 'AHPL abs depth', 'AHPL time from peak (ms)', 'AHPL depth from threshold (mV)',
                                # # AP1/APL    
                                'Amplitude AP1/APL', 'Peak AP1/APL', 'Half width AP1/APL'])

    for sweep in abf.sweepList:
        # abf.setSweep(sweep)
        abf.setSweep(sweep, channel = channel)
        abf_c.setSweep(sweep, channel = channel_c)

        # Defines a trace and region of analysis
        trace = {'T': abf.sweepX*1000, # convert to ms
                 'V': abf.sweepY,
                 'I': abf_c.sweepC,
                 'stim_start' : [stim_start],
                 'stim_end' : [stim_end]}
        traces = [trace]

        # Optional: Current step values
        currents = [] # Current value between t1 and t2 (ms) for each step
        t1 = int(t1_c*abf.dataPointsPerMs) 
        t2 = int(t2_c*abf.dataPointsPerMs)
        current_mean = np.average(abf_c.sweepC[t1:t2])

        # Define the output features
        # Or use instead efel.getMeanFeatureValues() to get mean values

        feature_values = getFeatureValues(traces,
                                           ['AP_amplitude', 'peak_voltage', 'AP_width', 'AP_duration_half_width',
                                            'spike_half_width', 'AP_fall_time',
                                            'AP_begin_voltage', 'AP_peak_upstroke', 'AP_peak_downstroke',
                                            'AP_rise_rate', 'AP_begin_indices','AHP_time_from_peak',
                                            'AP_fall_rate','AP_rise_time','AP_phaseslope','AHP_depth_abs',
                                            'AHP_depth','AP_duration_half_width', 
                                            'Spikecount', 'AHP_depth_abs_slow',
                                            'time_to_first_spike', 'AP2_AP1_diff', 'AP2_AP1_peak_diff', 'min_AHP_values', 
                                            'min_voltage_between_spikes', 'mean_frequency', 'mean_AP_amplitude', 
                                             'peak_indices', 'steady_state_voltage_stimend'],
                                             raise_warnings=None)[0] # If true, returns warnings (e.g. no spikes in trace)
        
        if feature_values["AP_amplitude"] is not None: 

            length = len(table)
            table.loc[length, 'Sweep'] = sweep # if you want only one put =1, 2 ...
            table.loc[length, 'Current step (pA)'] = current_mean
            table.loc[length, 'N of spikes'] = feature_values['Spikecount']
            table.loc[length, 'Latency (ms)'] = feature_values['time_to_first_spike']
            table.loc[length, 'Frequency (Hz)'] =  (table.loc[length, 'N of spikes']/(stim_end-stim_start)*1000)
            table.loc[length, 'Membrane voltage (mV)'] = feature_values['steady_state_voltage_stimend']
    

            #AP1
            if len(feature_values['AP_amplitude']) > 0:

                #AP average
                table.loc[length, 'Average amplitude (mV)'] = feature_values['AP_amplitude'].mean() # [0] returns values of first action potential, [1], for 2nd, etc. 
                table.loc[length, 'Average peak (mV)'] = feature_values['peak_voltage'].mean()
                table.loc[length, 'Average width (ms)'] = feature_values['AP_width'].mean()   
                table.loc[length, 'Average half width (ms)'] = feature_values['spike_half_width'].mean()
                table.loc[length, 'Average threshold (mV)'] = feature_values['AP_begin_voltage'].mean()
                table.loc[length, 'Average peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'].mean()
                table.loc[length, 'Average peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'].mean()
                table.loc[length, 'Average rise rate'] = feature_values['AP_rise_rate'].mean()
                table.loc[length, 'Average fall rate'] = feature_values['AP_fall_rate'].mean()
                table.loc[length, 'Average rise time (ms)'] = feature_values['AP_rise_time'].mean()
                table.loc[length, 'Average fall time (ms)'] = feature_values['AP_fall_time'].mean()
                table.loc[length, 'Average AHP abs depth'] = feature_values['AHP_depth_abs'].mean()
                table.loc[length, 'Average AHP time from peak (ms)'] = feature_values['AHP_time_from_peak'].mean()
                table.loc[length, 'Average AHP depth from threshold (mV)'] = (feature_values['AHP_depth_abs'].mean() - feature_values['AP_begin_voltage'].mean()) 
                
                # AP1
                table.loc[length, 'AP1 amplitude (mV)'] = list(feature_values['AP_amplitude'])[0] # [0] returns values of first action potential, [1], for 2nd, etc. 
                table.loc[length, 'AP1 peak (mV)'] = feature_values['peak_voltage'][0]
                table.loc[length, 'AP1 width (ms)'] = feature_values['AP_width'][0]                    
                table.loc[length, 'AP1 half width (ms)'] = feature_values['spike_half_width'][0]
                table.loc[length, 'AP1 threshold (mV)'] = feature_values['AP_begin_voltage'][0]
                table.loc[length, 'AP1 peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'][0]
                table.loc[length, 'AP1 peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'][0]
                table.loc[length, 'AP1 rise rate'] = feature_values['AP_rise_rate'][0]
                table.loc[length, 'AP1 fall rate'] = feature_values['AP_fall_rate'][0]
                table.loc[length, 'AP1 rise time (ms)'] = feature_values['AP_rise_time'][0]
                table.loc[length, 'AP1 fall time (ms)'] = feature_values['AP_fall_time'][0]
                table.loc[length, 'AHP1 abs depth'] = feature_values['AHP_depth_abs'][0]
                table.loc[length, 'AHP1 time from peak (ms)'] = feature_values['AHP_time_from_peak'][0] 
                table.loc[length, 'AHP1 depth from threshold (mV)'] = (feature_values['AHP_depth_abs'] [0] - feature_values['AP_begin_voltage'] [0]) 
                    

            #AP2
            if len(feature_values['AP_amplitude']) > 1:
                table.loc[length, 'AP2 amplitude (mV)'] = list(feature_values['AP_amplitude'])[1] # [0] returns values of first action potential, [1], for 2nd, etc. 
                table.loc[length, 'AP2 peak (mV)'] = feature_values['peak_voltage'][1]
                table.loc[length, 'AP2 width (ms)'] = feature_values['AP_width'][1]                    
                table.loc[length, 'AP2 half width (ms)'] = feature_values['spike_half_width'][1]
                table.loc[length, 'AP2 threshold (mV)'] = feature_values['AP_begin_voltage'][1]
                table.loc[length, 'AP2 peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'][1]
                table.loc[length, 'AP2 peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'][1]
                table.loc[length, 'AP2 rise rate'] = feature_values['AP_rise_rate'][1]
                table.loc[length, 'AP2 fall rate'] = feature_values['AP_fall_rate'][1]
                table.loc[length, 'AP2 rise time (ms)'] = feature_values['AP_rise_time'][1]
                table.loc[length, 'AP2 fall time (ms)'] = feature_values['AP_fall_time'][1]
                table.loc[length, 'AHP2 abs depth'] = feature_values['AHP_depth_abs'][1]
                #table.loc[length, 'AHP1_depth'] = feature_values['AHP_depth'][0] 
                table.loc[length, 'AHP2 time from peak (ms)'] = feature_values['AHP_time_from_peak'][1] 
                table.loc[length, 'AHP2 depth from threshold (mV)'] = (feature_values['AHP_depth_abs'] [1] - feature_values['AP_begin_voltage'] [1])
                
            else:
                table.loc[length, 'AP2 amplitude (mV)'] = None


           #APsL
            if len(feature_values['AP_amplitude']) > 2: 
                table.loc[length, 'APsL amplitude (mV)'] = list(feature_values['AP_amplitude'])[-2] # [0] returns values of first action potential, [1], for 2nd, etc. 
                table.loc[length, 'APsL peak (mV)'] = feature_values['peak_voltage'][-2]
                table.loc[length, 'APsL width (ms)'] = feature_values['AP_width'][-2]                    
                table.loc[length, 'APsL half width (ms)'] = feature_values['spike_half_width'][-2]
                table.loc[length, 'APsL threshold (mV)'] = feature_values['AP_begin_voltage'][-2]
                table.loc[length, 'APsL peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'][-2]
                table.loc[length, 'APsL peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'][-2]
                table.loc[length, 'APsL rise rate'] = feature_values['AP_rise_rate'][-2]
                table.loc[length, 'APsL fall rate'] = feature_values['AP_fall_rate'][-2]
                table.loc[length, 'APsL rise time (ms)'] = feature_values['AP_rise_time'][-2]
                table.loc[length, 'APsL fall time (ms)'] = feature_values['AP_fall_time'][-2]

                table.loc[length, 'AHPsL abs depth'] = feature_values['AHP_depth_abs'][-2]
                table.loc[length, 'AHPsL time from peak (ms)'] = feature_values['AHP_time_from_peak'][-2] 
                table.loc[length, 'AHPsL depth from threshold (mV)'] = (feature_values['AHP_depth_abs'] [-2] - feature_values['AP_begin_voltage'] [-2])
                
            #AP last
            if len(feature_values['AP_amplitude']) > 2:
                table.loc[length, 'APL amplitude (mV)'] = list(feature_values['AP_amplitude'])[-1] # [0] returns values of first action potential, [1], for 2nd, etc. 
                table.loc[length, 'APL peak (mV)'] = feature_values['peak_voltage'][-1]
                table.loc[length, 'APL width (ms)'] = feature_values['AP_width'][-1] 
                table.loc[length, 'APL half width (ms)'] = feature_values['spike_half_width'][-1]
                table.loc[length, 'APL threshold (mV)'] = feature_values['AP_begin_voltage'][-1]
                table.loc[length, 'APL peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'][-1]
                table.loc[length, 'APL peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'][-1]
                table.loc[length, 'APL rise rate'] = feature_values['AP_rise_rate'][-1]
                table.loc[length, 'APL fall rate'] = feature_values['AP_fall_rate'][-1]
                table.loc[length, 'APL rise time (ms)'] = feature_values['AP_rise_time'][-1]
                table.loc[length, 'APL fall time (ms)'] = feature_values['AP_fall_time'][-1]

                table.loc[length, 'AHPL abs depth'] = feature_values['AHP_depth_abs'][-1]
                table.loc[length, 'AHPL time from peak (ms)'] = feature_values['AHP_time_from_peak'][-1] 
                table.loc[length, 'AHPL depth from threshold (mV)'] = (feature_values['AHP_depth_abs'] [-1] - feature_values['AP_begin_voltage'] [-1])

            else:
                    table.loc[length, 'APL amplitude (mV)'] = None
                    
            # Comparisons
            if len(feature_values['AP_amplitude']) > 2:
                table.loc[length, 'Amplitude AP1/APL'] = (feature_values['AP_amplitude'][0] / feature_values['AP_amplitude'][-1])
                table.loc[length, 'Peak AP1/APL'] = (feature_values['peak_voltage'][0] / feature_values['peak_voltage'][-1])
                table.loc[length, 'Half width AP1/APL'] = (feature_values['spike_half_width'][0] / feature_values['spike_half_width'][-1])
                     
    return table 

def merge_ipfx_ap_tables(ipfx_table, ap_table):
    table_final = pd.merge(ipfx_table, ap_table, on='Sweep')
    return(table_final)



#! ----- Membrane Potential Table - Combination of IPFX and AP table
def generate_membrane_potential_table (abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    
    table_m=pd.DataFrame()

    # Loop function
    for sweep in abf.sweepList: #[0:num_of_traces]:  # To select a range of traces
        abf.setSweep(sweep, channel = channel)
        abf_c.setSweep(sweep, channel = channel_c)
        # Defines a trace and region of analysis
        trace = {'T': abf.sweepX*1000, #convert to ms
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
                                                'current', 'time_constant', 'voltage_base',
                                                'sag_amplitude', 'sag_time_constant', 'decay_time_constant_after_stim',
                                                'sag_ratio2', 'AP_amplitude'],
                                               raise_warnings=None)[0] # If true, returns warnings
        
        length = len(table_m)
        
        if feature_values["AP_amplitude"] is None: 
            table_m.loc[length, 'Sweep'] = sweep
            table_m.loc[length, 'Current (pA)'] = current_mean # [] to select the rows of current step
            table_m.loc[length, 'Voltage base (mV)'] = feature_values['voltage_base'][0]
            table_m.loc[length, 'Membrane voltage (mV)'] = feature_values['steady_state_voltage_stimend'][0]
            table_m.loc[length, 'Time constant (ms)'] = feature_values['time_constant']
            table_m.loc[length, 'Input resistance (Gohm)'] = (table_m.loc[length, 'Membrane voltage (mV)']/table_m.loc[length, 'Current (pA)'])
            table_m.loc[length, 'Capacitance (pF)'] = (table_m.loc[length, 'Time constant (ms)']/table_m.loc[length, 'Input resistance (Gohm)'])
            table_m.loc[length, 'Decay time constant (ms)'] = feature_values['decay_time_constant_after_stim']
            table_m.loc[length, 'Sag amplitude (mV)'] = feature_values['sag_amplitude']
            table_m.loc[length, 'Sag ratio'] = feature_values['sag_ratio2']
            table_m.loc[length, 'Sag time constant (ms)'] = feature_values['sag_time_constant']
        
        elif feature_values["AP_amplitude"] is not None: 
            
            if len(feature_values['AP_amplitude']) < 1:
                table_m.loc[length, 'Sweep'] = sweep
                table_m.loc[length, 'Current (pA)'] = current_mean # [] to select the rows of current step
                table_m.loc[length, 'Voltage base (mV)'] = feature_values['voltage_base'][0]
                table_m.loc[length, 'Membrane voltage (mV)'] = feature_values['steady_state_voltage_stimend'][0]
                table_m.loc[length, 'Time constant (ms)'] = feature_values['time_constant']
                table_m.loc[length, 'Input resistance (Gohm)'] = (table_m.loc[length, 'Membrane voltage (mV)']/table_m.loc[length, 'Current (pA)'])
                table_m.loc[length, 'Capacitance (pF)'] = (table_m.loc[length, 'Time constant (ms)']/table_m.loc[length, 'Input resistance (Gohm)'])
                table_m.loc[length, 'Decay time constant (ms)'] = feature_values['decay_time_constant_after_stim']
                table_m.loc[length, 'Sag amplitude (mV)'] = feature_values['sag_amplitude']
                table_m.loc[length, 'Sag ratio'] = feature_values['sag_ratio2']
                table_m.loc[length, 'Sag time constant (ms)'] = feature_values['sag_time_constant']

    return table_m


#! ----- Neuronal overview Table - Combination of IPFX and AP table
def generate_neuronal_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    
    def get_slope_for_input_reistance(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
        # Create results table 
        table_ir = pd.DataFrame()

        for sweep in abf.sweepList:
            # abf.setSweep(sweep)
            abf.setSweep(sweep, channel = channel)
            abf_c.setSweep(sweep, channel = channel_c)
            voltage = abf.sweepY
            current = abf_c.sweepC

            # Define the variables and region of analysis
            trace = {'T': abf.sweepX*1000, 
                    'V': abf.sweepY,
                    'stim_start': [stim_start],
                    'stim_end': [stim_end]} 
            traces = [trace]

            # Optional: Current step values
            t1 = int(t1_c*abf.dataPointsPerMs) 
            t2 = int(t2_c*abf.dataPointsPerMs)
            current_mean = np.average(abf_c.sweepC[t1:t2])
        
            feature_values = getFeatureValues(traces,
                                                    ['voltage', 'steady_state_voltage_stimend', 
                                                        'current', 'time_constant', 
                                                        'sag_amplitude', 
                                                        'sag_ratio1', 'AP_amplitude'],
                                                    raise_warnings=None)[0] # If true, returns warnings
        
            length = len(table_ir)
            
            if feature_values["AP_amplitude"] is None and current_mean < 100:
                table_ir.loc[length, 'Sweep'] = sweep
                table_ir.loc[length, 'steady_state_voltage_stimend'] = feature_values['steady_state_voltage_stimend'][0]
                table_ir.loc[length, 'current_pA'] = current_mean # [] to select the rows of current step
            elif feature_values["AP_amplitude"] is not None:
                if len(feature_values['AP_amplitude']) < 1:
                    table_ir.loc[length, 'Sweep'] = sweep
                    table_ir.loc[length, 'steady_state_voltage_stimend'] = feature_values['steady_state_voltage_stimend'][0]
                    table_ir.loc[length, 'current_pA'] = current_mean # [] to select the rows of current step

        
        current = table_ir["current_pA"].to_list()
        voltage = table_ir["steady_state_voltage_stimend"].to_list()

        # Linear regression
        m, b = np.polyfit(current, voltage, 1)

        return m
    
    def initialize_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, slope_of_input_resistance):
        # Overview table    
        table = pd.DataFrame()

        # Loop function
        # Only check the first sweep - we only need SAG, which we need from the first sweep 
        for sweep in abf.sweepList[0:1]:  # To select a range of traces
            abf.setSweep(sweep, channel = channel)
            abf_c.setSweep(sweep, channel = channel_c)
            # Defines a trace and region of analysis
            trace = {'T': abf.sweepX*1000, #convert to ms
                    'V': abf.sweepY,
                    'I': abf_c.sweepC,
                    'stim_start' : [stim_start],
                    'stim_end' : [stim_end]}
            traces = [trace]
            
            t1 = int(t1_c*abf.dataPointsPerMs) 
            t2 = int(t2_c*abf.dataPointsPerMs)
            current_mean = np.average(abf_c.sweepC[t1:t2])
            
        # Output features
            feature_values = getFeatureValues(traces,
                                                ['voltage', 'steady_state_voltage_stimend', 
                                                    'current', 'time_constant', 'voltage_base',
                                                    'sag_amplitude', 'sag_time_constant', 'decay_time_constant_after_stim',
                                                    'sag_ratio2', 'AP_amplitude'],
                                                raise_warnings=None)[0] # If true, returns warnings 
            
            length = len(table)
            table.loc[length, 'Resting membrane potential (mV)'] = feature_values['voltage_base'][0]
            table.loc[length, 'Sag amplitude (mV)'] = feature_values['sag_amplitude']
            table.loc[length, 'Sag ratio'] = feature_values['sag_ratio2']

        # Calculate time constant and add input res
        table.loc[length, 'Membrane Input Restance (GOhm)'] = slope_of_input_resistance

        return table
        
    def add_membrane_time_constant(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, overview_table, slope_of_input_resistance):
        # Created because we are looking for sweeps with -50 <= current_mean <= -40
        table_tau=pd.DataFrame()
        
        for sweep in abf.sweepList:  # To select a range of traces
            abf.setSweep(sweep, channel = channel)
            abf_c.setSweep(sweep, channel = channel_c)
            # Defines a trace and region of analysis
            trace = {'T': abf.sweepX*1000, #convert to ms
                    'V': abf.sweepY,
                    'I': abf_c.sweepC,
                    'stim_start' : [stim_start],
                    'stim_end' : [stim_end]}
            traces = [trace]

            t1 = int(t1_c*abf.dataPointsPerMs) 
            t2 = int(t2_c*abf.dataPointsPerMs)
            current_mean = np.average(abf_c.sweepC[t1:t2])

            # Output features
            feature_values = getFeatureValues(traces,
                                                ['voltage', 'steady_state_voltage_stimend', 
                                                    'current', 'time_constant', 'voltage_base',
                                                    'sag_amplitude', 'sag_time_constant', 'decay_time_constant_after_stim',
                                                    'sag_ratio2', 'AP_amplitude'],
                                                raise_warnings=None)[0] # If true, returns warnings

            length= len(table_tau)
            
            if feature_values['AP_amplitude'] is None:
                if current_mean <= -40 and current_mean >= -50:
                    table_tau.loc[length, 'Sweep'] = sweep
                    table_tau.loc[length, 'Current'] = current_mean
                    table_tau.loc[length, 'Sweep time constant (ms)'] = feature_values['time_constant']
            elif feature_values["AP_amplitude"] is not None:
                if len(feature_values['AP_amplitude']) < 1:
                    if current_mean <= -40 and current_mean >= -50:
                        table_tau.loc[length, 'Sweep'] = sweep
                        table_tau.loc[length, 'Current'] = current_mean
                        table_tau.loc[length, 'Sweep time constant (ms)'] = feature_values['time_constant']

        try:
            overview_table.loc[0,'Membrane time constant (ms)'] = table_tau['Sweep time constant (ms)'].mean()
        except Exception as e:
            overview_table.loc[0,'Membrane time constant (ms)'] = None

        overview_table.loc[0,'Membrane capacitance (pF)'] = (overview_table.loc[0, 'Membrane time constant (ms)']/slope_of_input_resistance)
    
        return overview_table
    
    def add_ap1_data(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, table):
        # ADD AP1 data for the overview   
        for sweep in abf.sweepList:  # To select a range of traces
            abf.setSweep(sweep, channel = channel)
            abf_c.setSweep(sweep, channel = channel_c)
            # Defines a trace and region of analysis
            trace = {'T': abf.sweepX*1000, #convert to ms
                    'V': abf.sweepY,
                    'I': abf_c.sweepC,
                    'stim_start' : [stim_start],
                    'stim_end' : [stim_end]}
            traces = [trace]

            t1 = int(t1_c*abf.dataPointsPerMs) 
            t2 = int(t2_c*abf.dataPointsPerMs)
            current_mean = np.average(abf_c.sweepC[t1:t2])

            feature_values = getFeatureValues(traces,
                                                ['voltage', 'steady_state_voltage_stimend', 
                                                    'current', 'time_constant', 'voltage_base',
                                                    'sag_amplitude', 'sag_time_constant', 'decay_time_constant_after_stim',
                                                    'sag_ratio2', 'AP_amplitude', 'peak_voltage', 'AP_width', 'AP_duration_half_width',
                                                    'spike_half_width', 'AP_fall_time',
                                                    'AP_begin_voltage', 'AP_peak_upstroke', 'AP_peak_downstroke',
                                                    'AP_rise_rate', 'AP_begin_indices','AHP_time_from_peak',
                                                    'AP_fall_rate','AP_rise_time','AP_phaseslope','AHP_depth_abs',
                                                    'AHP_depth','AP_duration_half_width', 
                                                    'Spikecount', 'AHP_depth_abs_slow',
                                                    'time_to_first_spike', 'AP2_AP1_diff', 'AP2_AP1_peak_diff', 'min_AHP_values', 
                                                    'min_voltage_between_spikes', 'mean_frequency', 'mean_AP_amplitude', 
                                                    'peak_indices'],
                                                raise_warnings=None)[0] # If true, returns warnings


            if feature_values['AP_amplitude'] is not None:
                if len(feature_values['AP_amplitude']) > 0 and current_mean >= 0:
                    table.loc[0, 'Rheobase (pA)'] = current_mean
                    table.loc[0, 'AP1 Latency (ms)'] = feature_values['time_to_first_spike'] [0]
                    table.loc[0, 'AP1 amplitude (mV)'] = list(feature_values['AP_amplitude'])[0] # [0] returns values of first action potential, [1], for 2nd, etc. 
                    table.loc[0, 'AP1 peak (mV)'] = feature_values['peak_voltage'][0]
                    table.loc[0, 'AP1 width (ms)'] = feature_values['AP_width'][0]    
                    table.loc[0, 'AP1 half width (ms)'] = feature_values['spike_half_width'][0]
                    table.loc[0, 'AP1 threshold (mV)'] = feature_values['AP_begin_voltage'][0]
                    table.loc[0, 'AP1 peak upstroke (V/s)'] = feature_values['AP_peak_upstroke'][0]
                    table.loc[0, 'AP1 peak downstroke (V/s)'] = feature_values['AP_peak_downstroke'][0]
                    table.loc[0,'AP1 rise rate'] = feature_values['AP_rise_rate'][0]
                    table.loc[0, 'AP1 fall rate'] = feature_values['AP_fall_rate'][0]
                    table.loc[0, 'AP1 rise time (ms)'] = feature_values['AP_rise_time'][0]
                    table.loc[0, 'AP1 fall time (ms)'] = feature_values['AP_fall_time'][0]
                    table.loc[0, 'AHP1 abs depth'] = feature_values['AHP_depth_abs'][0]
                    table.loc[0, 'AHP1 time from peak (ms)'] = feature_values['AHP_time_from_peak'][0] 
                    table.loc[0, 'AHP1 depth from threshold (mV)'] = (feature_values['AHP_depth_abs'] [0] - feature_values['AP_begin_voltage'] [0])
                    break

        return table

    # Calculate slope of input resistance
    slope_of_input_resistance  = get_slope_for_input_reistance(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
    # Create initial table using SAG data from sweep 0
    overview_table = initialize_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, slope_of_input_resistance)
    # Expnad table by adding membrane time constant
    overview_table_expanded = add_membrane_time_constant(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, overview_table, slope_of_input_resistance)
    # Add API data to complete table
    finalized_table = add_ap1_data(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end, overview_table_expanded)

    return finalized_table

#! ----- Util functions

def unlist_arrays_in_all_cells(table: pd.DataFrame):
    """
    Go through each column, and apply function to each cell.
    If the value is in an numpy array, select the first element in the array.
    Otherwise, keep the cell value as is
    """
    for col in table.columns.values:
        table[col] = table[col].apply(lambda x: x[0] if isinstance(x, np.ndarray) else x)
    
    return table

#! ----- Create Complete Table functions

def create_ap_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    # Generate tables
    ipfx_table = generate_ipfx_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
    ap_table =  generate_AP_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
    final_ap_table = merge_ipfx_ap_tables(ipfx_table, ap_table)
    # Unlist the elements in lists
    complete_ap_table = unlist_arrays_in_all_cells(final_ap_table)
    return complete_ap_table

def create_membrane_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    # Generate tables
    table_membrane_properties = generate_membrane_potential_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)
    
    # Unlist the elements in lists
    complete_membrane_properties = unlist_arrays_in_all_cells(table_membrane_properties)

    return complete_membrane_properties

def create_neuronal_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end):
    # Generate tables
    neuronal_overview_table = generate_neuronal_overview_table(abf, abf_c, channel, channel_c, t1_c, t2_c, stim_start, stim_end)  
    # Unlist the elements in lists
    complete_neuronal_overview_table = unlist_arrays_in_all_cells(neuronal_overview_table)

    return complete_neuronal_overview_table

