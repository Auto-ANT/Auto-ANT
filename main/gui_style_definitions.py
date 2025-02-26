"""
gui_style_definitions.py 
This file contains styles for the GUI

"""
from tkinter import ttk


def init_gui_style(root):
    # Create a style
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(background='white')

    # ----------------------------------------------------------------------------------
    # Create Standard Style

    #? Buttons
    style.configure('Trigger.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'dark green', 
                    bordercolor = 'dark green',
                    padx=(10, 10),pady=(20, 20),
                    height = 20)

    style.configure('Reset.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'OrangeRed2', 
                    bordercolor = 'OrangeRed2',
                    padx=(10, 10),pady=(20, 20),
                    height = 20)

    style.configure('Stop.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'red', 
                    bordercolor = 'red',
                    padx=(10, 10),pady=(20, 20),
                    height = 20)

    style.configure('Cite.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'darkblue', 
                    bordercolor = 'darkblue',
                    padx=(10, 10),pady=(20, 20),
                    height = 15)
    
    style.configure('Logs.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'dimgrey', 
                    bordercolor = 'dimgrey',
                    padx=(10, 10),pady=(20, 20),
                    height = 15)
    

    style.configure('CloseWindow.TButton', 
                    font = ('calibri', 12, 'bold'),
                    foreground = 'black', 
                    bordercolor = 'black',
                    padx=(10, 10),pady=(20, 20),
                    height = 15)
    

    style.configure('Gear.TButton', 
                    foreground = 'white', 
                    background = 'white',
                    bordercolor = 'white',
                    borderwidth = 0,
                    padx = 0, pady = 0)
    
    style.configure('Save_settings.TButton', 
                font = ('calibri', 12, 'bold'),
                foreground = 'darkgreen', 
                bordercolor = 'darkgreen',
                padx=(10, 10),pady=(20, 20),
                height = 20)
    
    #-------------------------------------------------
    style.configure('FolderNeutral.TButton', 
                    foreground = 'black', 
                    bordercolor = 'black',
                    width = 20,
                    font = ('calibri', 10, 'bold'))

    style.configure('FolderValid.TButton', 
                    foreground = 'green', 
                    bordercolor = 'green',
                    width = 20,
                    font = ('calibri', 10, 'bold'))

    style.configure('FolderFail.TButton', 
                    foreground = 'red', 
                    bordercolor = 'red',
                    width = 20,
                    font = ('calibri', 10, 'bold'))

    #? Entry Styles
    style.configure('Default.TEntry',
                    borderwidth = 2,
                    bordercolor = 'grey'
                    )

    style.configure('Approved.TEntry',
                    borderwidth = 2,
                    bordercolor = 'green'
                    )
    style.configure('Failed.TEntry',
                    borderwidth = 2,
                    bordercolor = 'red'
                    )
    
    style.configure('FileName.TEntry',
                    borderwidth = 2,
                    bordercolor = 'grey',
                    foreground  = 'darkgrey',
                    font = ('calibri', 3)
                    )


    #? Combobutton Styles
    style.configure('Default.TCombobox',
                    borderwidth = 2,
                    bordercolor = 'grey'
                    )

    style.configure('Approved.TCombobox',
                    borderwidth = 2,
                    bordercolor = 'green'
                    )
    style.configure('Failed.TCombobox',
                    borderwidth = 2,
                    bordercolor = 'red'
                    )
    
    #? Label Styles
    style.configure('TopHeader.TLabel',
                    font = ('arial', 18, 'bold'),
                    background = 'white')

    style.configure('MidHeader.TLabel',
                    font = ('calibri', 14, 'bold'),
                    background = 'white'
                    )
    
    style.configure('SubHeader.TLabel',
                    font = ('calibri', 12, 'bold'),
                    background = 'white'
                    )
    
    style.configure('Variable.TLabel',
                    font = ('calibri', 12),
                    background = 'white')
    
    # Column 4
    style.configure('StatusTitle.TLabel',
                    underline=1, 
                    font=("Arial", 14, "bold"),
                    background = 'white')

    style.configure('Status.TLabel',
                    font=("Arial", 12),
                    background = 'white')
    
    style.configure('Error.TLabel',
                    font=("Arial", 14, "bold"), 
                    foreground='red',
                    background = 'white')


    style.configure('Hover.TLabel',
                    font = ('calibri', 14, 'bold'),
                    foreground = 'gray', 
                    background = 'white',
                    padx = (5,0))

    # Logo
    style.configure('Logo.TLabel',
                    foreground = 'gray', 
                    background = 'white',
                    padx = (5,0))
    
    # Info text in configuration windows
    style.configure('pText.TLabel',
                font = ('calibri', 12),
                background = 'white',
                )
                
