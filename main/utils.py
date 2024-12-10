
import os
import sys


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development and PyInstaller builds.
    Used to access CSV and image files
    """
    if hasattr(sys, '_MEIPASS'):
        # If running as a PyInstaller bundle, adjust the path
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
