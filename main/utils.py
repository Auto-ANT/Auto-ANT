"""
utils.py 
This file contains functions that are used within multiple files, including 
utility function for reesourc paths, and functions for errorhandling

"""
import os
import sys
import numpy as np 

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development and PyInstaller builds.
    Used to access CSV and image files
    """
    if hasattr(sys, '_MEIPASS'):
        # If running as a PyInstaller bundle, adjust the path
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



# ---------------------------- Error Handling ----------------------------
class NoSweepsError(Exception):
    """Raised when the resulting table is empty due to invalid inputs."""
    pass

class WrongRecordingChannelError(Exception):
    """Raised when the resulting table is empty due to invalid inputs."""
    pass

class WrongProtocolChannelError(Exception):
    """Raised when the resulting table is empty due to invalid inputs."""
    pass
class NoNegativeSweepsError(Exception):
    """Raised when there are no negative sweeps."""
    pass


def verify_no_firing_sweeps(data):
    """ If there is no data in the table (ipfx or ap) it indicats no sweeps were found
        Used By:
            - Firing Properties table (ipfx or ap)"""
    
    if len(data) ==  0:
        raise NoSweepsError('There were no sweeps fulfilling the requirement for firing properties.')

def verify_negative_sweeps(data):
    """If all values are above 0 it indicates there are no sweeps fulfilling the requirement
        Used by:
            - Membrane table
            - Neuronal Overview Table
            - Current-Voltage linear regression plot"""
    
    if np.all(np.array(data) >= 0):
        raise NoNegativeSweepsError('It may be no sweeps fulfilling the requirement for membrane.')
    
def verify_recording_channel(data):
    """If the standard deviation for each sweep is less than 1 for all sweeps
        it indicates the incorrect recording channel
        Used by:
            - All tables
            - All plots"""
    # Calculate standard deviation
    all_stds = [np.std(sweep) for sweep in data]

    if all(x < 1 for x in all_stds):
        raise WrongRecordingChannelError('It may be the wrong Recording Channel.')
    
def verify_protocol_channel(data):
    """If all values are 0 it indicates the wrong protocol channel
        Used by:
            - All tables
            - All plots"""
    if np.all(np.array(data) == 0):
        raise WrongProtocolChannelError('It may be the wrong Protocol Channel.')
    
    
def simplify_error_message(e, target_file):
    """ 
    Takes error messages and provides a simplified message which is shown
    in the GUI status window
    """
    # print(e.args[0])

    # General Errors
    if "outside of time range" in e.args[0]: 
        return "Protocol start/end is outside the range. Please modfify start or end"
    
    # If end is smaller than start 
    elif "stim_end needs to be larger than stim_start" in e.args[0]:
        return "Protocol end needs to be larger than start"
    
    # If wrong recording channel
    elif e.args[0] == "It may be the wrong Recording Channel.":
        return "Evaluate Recording Channel"
    
    # If wrong protocol channel
    elif e.args[0] == "It may be the wrong Protocol Channel.":
        return "Evaluate Protocol Channel"
    
    # Specific Errors
    elif e.args[0] == 'There were no sweeps fulfilling the requirement for firing properties.':
        return "Error with Firing properties sweeps."

    elif e.args[0] == 'It may be no sweeps fulfilling the requirement for membrane.':
        return "Error with Membrane sweeps."

    elif target_file == "Passive membrane properties":
        if "object is not subscriptable" in e.args[0]:
            return "Verfiy Protocol start and end time"
        
    elif target_file == "Neuronal overview table":
        if "object is not subscriptable" in e.args[0]:
            return "Verfiy Protocol start and end time"
        
    return "There was an error. Please check the logs for details"