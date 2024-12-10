from tkinter import ttk, Frame, Toplevel, Canvas,Scrollbar, VERTICAL
from gui_style_definitions import init_gui_style

#! ------------------------------ Menu for subsetting cols ------------------------------
# here
def to_reference():
    top = Toplevel()
    init_gui_style(top)
    top.title("References & Licenses")
    # --------------------------------------------------------------------
    # Create a canvas inside the Toplevel
    canvas = Canvas(top)
    canvas.grid(row = 0, column = 0, sticky = 'nsew')
    # Add a vertical scrollbar to the canvas
    scrollbar = Scrollbar(top, orient=VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    # Create a frame inside the canvas to hold the content
    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    
    canvas.configure(background='white')
    frame.configure(background='white')

    # Populate frame
    title = ttk.Label(frame, text="References", style = "TopHeader.TLabel")
    title.grid(row=1, column=1, sticky = 'w', pady = (5,3), padx=(10, 0), columnspan = 1)
    
    general_description_text = f"""If you publish data obtained with this software, please cite the following papers."""
    description = ttk.Label(frame, text=general_description_text, style = "SubHeader.TLabel")
    description.grid(row = 2, column = 1, padx=(10, 0), sticky = 'w', columnspan = 1)

    reference_1_text = f"""\
    This is a placeholder for the paper introducing Auto ANT.\n"""
    description = ttk.Label(frame, text=reference_1_text, style = "pText.TLabel")
    description.grid(row = 3, column = 1, sticky = 'w', columnspan = 1)

    reference_2_text = f"""\
    Efel package:
    Ranjan, R., Van Geit, W., Moor, R., Rössert, C., Riquelme, J. L., Damart, T., Jaquier, A., Tuncel, A., Mandge, D., & Kilic, I. (2024). 
    eFEL (5.7.13). Zenodo. https://doi.org/10.5281/zenodo.14222078\n"""
    description = ttk.Label(frame, text=reference_2_text, style = "pText.TLabel")
    description.grid(row = 4, column = 1, sticky = 'w', columnspan = 1)

    # Mid Title
    title = ttk.Label(frame, text="Licenses", style = "TopHeader.TLabel")
    title.grid(row=6, column=1, sticky = 'w', pady = (5,3), padx=(10, 0), columnspan = 1)
    
    license_intro_text = f"""This software relies upon the ipfx python package, which has the following license:"""
    license_intro = ttk.Label(frame, text=license_intro_text, style = "SubHeader.TLabel")
    license_intro.grid(row = 7, column = 1, padx=(10, 0), sticky = 'w', columnspan = 1)

    license_overview_text = f"""\
    Allen Institute Software License - This software license is the 2-clause BSD license 
    plus a third clause that prohibits redistribution for commercial purposes without further permission.\

    Copyright (c) 2018. Allen Institute. All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the 
    following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the 
    following disclaimer in the documentation and/or other materials provided with the distribution.

    3. Redistributions for commercial purposes are not permitted without the Allen Institute's written permission.
    For purposes of this license, commercial purposes is the incorporation of the Allen Institute's software into
    anything for which you will charge fees or other compensation. Contact terms@alleninstitute.org for commercial
    licensing opportunities.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

    description = ttk.Label(frame, text=license_overview_text, style = "pText.TLabel")
    description.grid(row = 8, column = 1, sticky = 'w', columnspan = 1)

    # Update the scroll region to include the new content
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Configure row and column weights in the Toplevel window
    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)

    # Bind mouse scroll to canvas scrolling
    def _on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    #? ---------------- Close button ----------------
    def close_window():
        top.destroy()

    close_button = ttk.Button(top,
                             text="Close", 
                             command=close_window,
                             style = 'Cite.TButton')

    close_button.grid(row = 1, column=0, padx = (30,30), pady = (20,20), sticky = 'we')