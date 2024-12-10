#? Final Task
# Set colorof checkbutton as white. Make them ttk


#!  SIMON TO DO IN GIUSY
#! CURRENT PROBLEMS
#! Roll back scaling fuckups - last clean commit was "commit 825c82b", not hard to change

#! ALSO if this fails, maybe create frames using COLUMNWIDTH to make tbe frame span multiple cols
#!  https://www.tutorialspoint.com/implementing-a-scrollbar-using-grid-manager-on-a-tkinter-window
#! AND 
#! columnspan  https://www.youtube.com/watch?v=woUeOOPEvDc&t=149s&ab_channel=plus2net

#!  First run Learnings
# Use TTK on Labels as well, PC fucks them up (fix the sizes too) - almost done, only TPs, status, errors left
#? Instead of showing errors on the bottom, show them on the right side. The right can either have status AND errors,
#? So thats the status page. Halfassed imp now, continue playing with it, increase size etc. Maybe have it replace title
# Fix the window size  - dont use pixels, doestn work on small window - testing no gemetry speec
# Remove y padding i suppose
# IF the user selects an excel file, they get to define the name themselves
#   For both excel files
#   If user provides name, use name, Else, use default name
#   Shift name logic to class, as a semi validation step
#! ----------


# 3.12 worked on all except ipfx

# IPFX and EFEL (pretty sure ipfx is the main) were the culprits
# But, worked with an older python env (3.7.3)  

#! Validation
# ! https://www.pythonguis.com/tutorials/input-validation-tkinter/ use a similar function as this one,
#! Read and think about this tomorrow, which is bes. leaning the one that blocks trigger magic
# ! and use it as a command for all entry that are with numbers
# ! When click run, run the validation on the class (it goes BEFORE popul)
#  ! If any  fail - then put up error value saying " Make sure field X is float"
#! there are 2 kinds, i think "trigger button" is best, then turn the text red if it failed (the title)
#? Do both. Validate real time and change to red. And the SUbmit button - error just needs to say
#? "Highlighted fields need to be float or integers"
# 1. Create valudate function
# 2. On trigger analysis ,run validation first
# 3. if any of the values fail - put up an error message demaing better data and dont run calc
# - one
#! ------- Code structure also means the calc cant be run unless all are filled in


# Instructions to Install
# - Install Python (3.7.3 works, but thats for VENV, Find Guide)
# - Create Virtual Environment (find Guide)
# - Spin up a VENV with Python 3.7.3 or so
# - Activate VENV
# - Install all packages from requirements file (hopefully works, giusy to try)
# - Navigate to Folder (use CD, find guide)
# - Activate program with "python3 run_analysis.py"

# Instructions to Run
# - Activate VENV
# - Navigate to Folder (use CD, find guide)
# - Activate program with "python3 run_analysis.py"

# https://www.geeksforgeeks.org/what-are-widgets-in-tkinter/

# V3 has column buttons
# V4 - first working version 


#TODO
#! TOP
#? TODO - Giusy changed firing rate calc, needs to give me
#! The rest
#TODO - Only allow run ifall values  have been filled in - halfassed with validation  - done?

# TODO
# TODO 1. Add menu that links to sources / my github where you get info
#    ------ Move Folder validation to the other validations?
# TODO 2. Split into multiple files, use a folder hierarchy + rename files
# TODO 4. Is it possible to spin up a VENV in a script?..
# TODO 5. Giusy code changes + new table
# TODO 6 - Do we need a "stop analysis" button?..  - NO
#! FIX THE [] in tables. create a utility function that loops all columns and all rows
#? Can be done

# TODO but need Giusy Input - Auto detect time start and end


#! Sceptical  of the requirements  file...
#       - 2 Scripts - 1 for install, 1 for runnnig
# https://stackoverflow.com/questions/57921255/how-to-create-python-virtual-environment-within-a-python-script
# CHange the settings for the window - should not be pixelbased OR make it update somehow 

#! Running Settings for trial data
    # #Total lenght of the recording (s)
    # start= 0.0
    # end= 3
    # #Set channels
    # channel=0 #for recording
    # channel_c=0 #for current
    # #Current steps
    # t1_c=500
    # t2_c=600
    # #Start and end of stimulation (ms)
    # stim_start=303
    # stim_end=1103

# Nah too much effort. Instead
# Describe setup (30 min with luck)
# Describe howtto run(activate VENV + Run File...  thats ok)


#Style Stuff
# style.configure(
#     'Custom.TButton',
#     background='#FFFFFF', # White
#     bordercolor='#00FF00', # Green
#     lightcolor='#FF0000', # Red
#     darkcolor='#0000FF', # Blue
#     borderwidth=4,
#     foreground='#00FFFF', # Cyan
    # )

# Set the theme with the theme_use method
# style.theme_use("forest-dark")
# ('aqua', 'step', 'clam', 'alt', 'default', 'classic')



#  To reset whole class
# Also reset the whole class to nothing,  just in case
# data_for_analysis = data_to_use(folder_name = '', output_folder_name = '',
#                                 start_duration = '', end_duration = '', 
#                                 start_current = '', end_current = '', 
#                                 start_stimulation= '', end_stimulation = '', 
#                                 channel_1 ='', channel_2 = '',
#                                 graph_1_state = '', graph_2_state = '', graph_3_state = '', graph_4_state = '',
#                                 ap_table = '', membrane_table = '')


#! This doesnt work because itt treats all  widgets like the same, combos and entries
#  Loops through all widgets, and checks # if its an entry, do this.. maybe this is better
# Then my current solution above?
#! No - the problem here is that it treats combos as if they were entry
# for widget in root.winfo_children():
#     if isinstance(widget, Entry):
#         widget.delete(0, END)
#         widget.configure(style = 'Default.TEntry') 



# how to run thread with arguments
# https://docs.python.org/3/library/threading.html#threading.Thread
# just specify in the  threadings.Trehad(target = , args = []), wit harguments as list

# Lets trt 3.9.1 - problemssss maybe 3.8.. but not 3.9 because ipfx and efel suck
# 3.7.3 works... lets try a higher one
# Need
# ipfx 
# efel
# pyabf
# Pandas
# openpyxl

#! Gen 2
# Effort: High
# - Stop analysis button - i think its best to just switch the runnin one - think itsfixed?
# - Giusy - Add sample images for the graphs (?) - solved, tty chatgpt, need images 
#! - Add new window button with config for what columns to include in the end - Next... 
#? 1. Add "read output columns" from an excel or CSV - thats actually the easy part... Lets just add 1 col
#? ---- This should be done within GUI, and passed as a variable. Should convert the T/F into a df of cols
#? ---- Need to convert the Excel into a bunch of checkboxes... can this be done in a loop? Maybe i should do this seperately
#? ---- So basically, ingest Excel, create checkboxes in loop, read true or false based on it.
#? ---- Step 1 is reading and creating, step 2 is writting to it (next steps) 
#? 2. Add ability to update (so update the config file)
#? 3. Crack button to open config window - done
# --- Maybe add a button next to the (?)?
# --- Could just store a simple CSV or something that it reads from and its  saved every time its changed
# --- acctually save 2. Just true or false ,  this  prevents DB ned


# Effort: Medium
# Giusy -  Update code with Giusy changes -  Done
# - Add averages table - NOPE
# - Add link to Github and Done
# - Cfeate my own new env and try to install to figure out the requirements issue

# Effort: Low
# - Remove SAG firing rate table - done 
# - Giusy - Switch some names on variables - done
# - Remove start/end - done
# - add "hover_delay=50" to every tooltip - done
# - Ddd suppress warningsin general - dangerous though

# Daemon threads - they end when the main thread ends.
# downside - it stops the thread from being able to cleanup. Its just breaks
# It might be better to use python events, to exit threads.
# Rather than Daemon...
# Need to use Eveents - and need to coordinate them for SIGINT (if someone stops the pogram) AND stop button
# OK So step 1
# - Set up Event
# - Replace Daemon with Event cancel using SIG

# OK so now it kinda works.
# We dont run daemon threads but the button works, and cancelling works (but you need to finish running the lap)
# So... tthe dream is switching the run and stop button once clicked
# Except stopped needs to be come "stopping..." then "Run" once complete

# Step 1:
# - Hide Stop button. Only show when start has been clicked - done
# - Start button exists. Hidden when run, but comes back after run
# - Put them in the same place - done

#? Remaining
# - Check above
# - Add link to Github and Paper - done ish
# - Giusy - Add sample images for the graphs (?) - solved, ty chatgpt, need images 
# - Write colmn on which packages are used - first draft done

# - More testing
# - Create new virtual envs and install reqiuirements. figure out the correct install order
# - Fix screen size - alternatively... scroll... hate scroll but might be more correct
# - Maybe add columnspan = 2 in the printed results tree, since its cutting off "success"
# BONUS - in settings, button for selecting / unselecting ALL columns
#! - MOST IMPORTANT - FIX PRINTOUT BOX WIDTH, borken. Run with 0 - 1120 to break - made improvements but not perf
#! - on PC - background behind text is white, the rest is gray. Standardize background colors - maybe fixde?
#! - In file menu list thing, add button that opens new window (like settings) that contains the 3 
#! references needed to use it, ready to to be copy pasted (name and DOI) - Done

#! TOP TO DO
#? - Store 'last opened folder' as new target folder (pretty ezpz) - done
#? - Fix requirements so Luis can test the whole thing
#! --- This is top priority - make it work with requirements install + find some guides 
#! --- on  virtual environments and such for noobs.
#! --- Pretty sure i can just use the freeze command to create ea new req file
#? - Giusy will bring new things to add (new table)
#? --- When Giusy is done, split up the code into more files. 
#? --- Copy the whole folder and start from re-structure all of it. Clean and delete stuff, V6



numpy==1.18.5
scikit-build==0.18.0
scikit-image==0.16.2
scipy==1.7.3
pandas==0.25.3

removed pandas on giusys

# TODO
#! - Add new excel function that either creates Excel file, or adds a new row to the shet - done
#! - Add buttons to select the table - Done
#? - Make sure validation and such works properly (like reset button etc.) - semi-done
#! - Add config table for neuronal overview table - Done
#? - Update config for AP table
#! - Test test test. Giusy to test
#! - Clean up code. Remove redundancies and fix naming. Do with Giusy 
#! - Try to put Graphs and Plots next to each other...  Would make it lower - done, to testt on PC

