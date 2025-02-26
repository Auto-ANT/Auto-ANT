
"""
view_logs.py 
This file contains all logic for the logs page.
It displays the logs since the last opening of the Auto ANT.
"""
from tkinter import ttk, Frame, Toplevel, Canvas,Scrollbar, Text, END
from gui_style_definitions import init_gui_style
from utils import get_resource_path


def to_logs():

    def on_frame_configure(canvas):
        """Reset the scroll region to encompass the inner frame."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Create the main window
    top = Toplevel()
    init_gui_style(top)
    top.title("Logs")

    # Configure grid layout for the root window
    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)

    # Create a canvas
    canvas = Canvas(top, bg="white")
    canvas.grid(row=0, column=0, sticky="nsew")  # Fill the entire window

    # Add a vertical scrollbar
    scrollbar = Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")  # Attach to the right side

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    frame = Frame(canvas, bg="white")

    # Create window inside canvas and store window_id to configure later
    window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    # Adjust scroll region when the frame size changes
    def on_frame_resize(event):
        canvas.itemconfig(window_id, width=event.width, height=event.height)

    frame.bind("<Configure>", lambda event: on_frame_configure(canvas))
    canvas.bind("<Configure>", on_frame_resize)

    # Add a Text widget inside the frame
    text = Text(frame, wrap='word')
    text.pack(expand=True, fill='both')

    # Load log content
    with open(get_resource_path('main/autoANT.log'), 'r') as file:
        log_content = file.read()

    # Insert log content into Text widget
    text.insert(END, log_content)

    # Ensure Text widget gets focus when clicked
    def on_text_click(event):
        text.focus_set()

    text.bind("<Button-1>", on_text_click)

    # Enable canvas scrolling with mouse wheel
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Windows and MacOS mouse wheel support
    canvas.bind_all("<MouseWheel>", on_mousewheel)        # Windows
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

    # #? ---------------- Close button ----------------
    def close_window():
        top.destroy()

    close_button = ttk.Button(top,
                             text="Close", 
                             command=close_window,
                             style = 'CloseWindow.TButton')
    
    close_button.grid(row = 1, column=0, padx = (30,30), pady = (20,50), sticky = 'we')