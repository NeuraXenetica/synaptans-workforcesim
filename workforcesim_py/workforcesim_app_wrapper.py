# ╔════════════════════════════════════════════════════════════════════╗
# ║   Synaptans WorkforceSim™: open-source software for simulating     ║
# ║   the dynamics of a factory workforce and assessing approaches     ║
# ║   to AI-based predictive analytics in the workplace.               ║
# ║                                                                    ║
# ║   Developed by Matthew E. Gladden • ©2021-22 NeuraXenetica LLC     ║
# ║                                                                    ║
# ║   This software is made available for use under                    ║
# ║   GNU General Public License Version 3                             ║
# ║   (please see https://www.gnu.org/licenses/gpl-3.0.html).          ║ 
# ╚════════════════════════════════════════════════════════════════════╝    

# ██████████████████████████████████████████████████████████████████████
# █                                                                    █
# █    █████  ██  ██ █ ███   ████   ████ █████  ███   █ ███   █████    █
# █   ██   ██ ██  ██ ██  ██ ██  ██ ██  █  ██   ██  ██ ██  ██ ██   ██   █
# █   ██      ██  ██ ██  ██ ██   █ ██  █  ██   ██   █ ██  ██ ██        █
# █    █████   ██ ██ ██  ██ ██   █ ██  █  ██   ██   █ ██  ██  █████    █
# █        ██   ███  ██  ██ ██████ ██  █  ██   ██████ ██  ██      ██   █
# █   ██   ██   ██   ██  ██ ██   █ ████   ██   ██   █ ██  ██ ██   ██   █
# █    █████    ██   ██  ██ ██   █ ██     ██   ██   █ ██  ██  █████    █
# █                                                                    █
# █                        /██\                      /███\             █
# █  █   █            █    █  █                      █   █  ██    (TM) █
# █  █   █            █    █                         █                 █
# █  █ █ █ /███\ /██\ █  █ ███ /███\ /██\ /███ /███\ \███\  █  █/█ █\  █
# █  █ █ █ █   █ █  █ ███  █   █   █ █  █ █    █  ██     █  █  ██ █ █  █
# █  █ █ █ █   █ █    █  █ █   █   █ █    █    ███   █   █  █  ██ █ █  █
# █  \█ █/ \███/ █    █  █ █   \███/ █    \███ \███  \███/  █  ██ █ █  █
# █                                                                    █
# █         @     @          @     @                                   █
# █      @    @ @  @       @    @   @@                                 █
# █     @  @   @@         @@   @ @           █\\\\\\\\\\\\\\\\\\\\\    █
# █      @@ @ @             @@@   @          ██\\\\\\\\\\\\\\\\\\\\\   █                 
# █         @  @               @   @         ███\\\\\\\\\\\\\\\\\\\\\  █                 
# █          █  █               █  █         ███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ █
# █      █\\\█\\█\          █\\\█\\█\        ███░░░░░░░░░░░░░░░░░░░░░░ █
# █      ██\\█\\█\\         ██\\█\\█\\       ███░██░██░█☺░██░██░██░██░ █
# █ \☺/  ███\\\\\\\\        ███\\\\\\\\      ███░██░██░██░██░██░██░██░ █
# █  0   ███▒▒▒▒▒▒▒▒▒  ☺    ███▒▒▒▒▒▒▒▒▒  ☺  ███░░░░░░░░░░░░░░░░░░░░░░ █
# █ / \  ███▒▒▒▒▒▒▒▒▒ /U\   ███▒▒▒▒▒▒▒▒▒ /O] ███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ █
# █      ███▒▒▒▒▒▒▒▒▒  LL   ███▒▒▒▒▒▒▒▒▒ / \ ███░░░░░░░░░░░░░░░░░░░░░░ █
# █   ☺   ██▒▒█▒███▒▒        ██▒▒███▒▒█▒      ██░████████░██░██░☺█░██░ █
# █  /8\   █▒▒█▒███▒▒     ☺   █▒▒███▒▒█▒   ☺   █░████☺███░██░██░██░██░ █
# █   /|    ▒▒▒▒███▒▒    <V>   ▒▒███▒▒▒▒  {D\   ░███[O\██░░░░░░░░░░░░░ █
# █                      / \               /|       / \                █
# █                                                                    █
# ██████████████████████████████████████████████████████████████████████

# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓▓ IMPORT MODULES
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Import other modules from the WorkforceSim Python package
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

import config as cfg
import IO_file_manager as iofm
import workforcesim_internal_logic as wfs


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Import additional Python modules (e.g., from the standard library)   
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

import os
from PIL import ImageTk, Image

import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Canvas, Button, Label, Scrollbar, Text, Entry
# from tkinter import *


# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓▓ DEFINE CLASSES AND FUNCTIONS
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions needed to run the simulation with a Tkinter GUI
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# This is a working framework for a Tkinter GUI for Synaptans. It displays 
# the splash screen until a license acceptance button is clicked, 
# and then moves to the main operational screen.

# ----------------------------------------------------------------------
# FUNCTION TO SPECIFY CONTENTS OF THE EULA TEXT TO BE DISPLAYED
# ----------------------------------------------------------------------
def return_EULA_text():

    EULA_text_m = \
    "Synaptans WorkforceSim™ version 0.1.082 is free software: you may use it, redistribute it, and/or modify it under the terms of GNU General Public License Version 3 as published by the Free Software Foundation.\n\n\
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY and without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Please see GNU General Public License Version 3 for more details.\n\n\
You should have received a copy of GNU General Public License Version 3 along with this program; if you have not, please see <https://www.gnu.org/licenses/gpl-3.0.en.html>."

    return EULA_text_m


# ----------------------------------------------------------------------
# DEFINE CLASS OF THE MAIN TKINTER APP
#
# Note: At one point, I began receiving an error about how "pyimage2" doesn't exist. I tried changing 
# the line below from "class Main_App(tk.Tk)" to "class Main_App(tk.Toplevel)", after which
# the image error stopped; however, this began producing a small second TK window that
# appeared every time the app was run. I've reverted to the earlier version of the line,
# with the hope that the image error won't reappear.
# ----------------------------------------------------------------------
class Main_App(tk.Tk):

    def __init__(self):
        super().__init__()

        cfg.main_Tkinter_window = self

        # The class creates the main Tkinter window, referenced in
        # other functions as "cfg.main_Tkinter_window" and known here as "self".

        # The main Tkinter window created above by the app
        # has the characteristics specified below, which
        # (unless overridden) will apply to all of the
        # screens and subscreens later shown by the app.

        # Allow the Escape key to exit the app.
        self.bind("<Escape>", lambda x: self.destroy())

        # Start the app in (broken) fullscreen mode, if desired.
        # self.attributes("-fullscreen", True)

        # ---------------------------------------------------------------------
        # Specify colors to be used in key components.
        # ---------------------------------------------------------------------
        cfg.main_window_bg_color = "#56566a" #darkish plum
        cfg.splash_screen_main_frame_bg_color = "#41414b" # also the bg color for logos; darker plum
        cfg.splash_screen_main_frame_text_color = "white" #white
        cfg.EULA_box_bg_color = "#e5e5ea" #light gray
        cfg.ops_input_section_outer_margin_color = "black" #black
        cfg.ops_input_section_main_text_area_bg_color = "#41414b" #darker plum
        cfg.ops_input_section_main_text_area_label_hint_text_color = "white" #white
        cfg.ops_input_section_main_text_area_arg_entry_text_color = "#00096f" #dark blue
        cfg.ops_results_section_bg_before_figures_appear_color = "#41414b" #darker plum
        cfg.ops_results_section_fig_bg_color = "#34343C" #darkest plum
        cfg.ops_results_section_fig_axis_bg_color = "black" #black

        # ---------------------------------------------------------------------
        # Other elements.
        # ---------------------------------------------------------------------

        # Set the main window background color.
        self['bg'] = cfg.main_window_bg_color

        # Set the initial size for the window.
        #
        # The lines below initiate the window with a fixed pixel size.
        cfg.width_of_main_tkinter_window = 1200 #This size determines how wide the main Tkinter window is, in pixels.
        # self.geometry('1200x700')
        geometry_string = str(cfg.width_of_main_tkinter_window) + 'x700' #Tkinter needs the window dimensions formatted as a string, not a tuple.
        self.geometry(geometry_string)
        #
        # The line below starts the window as maximized.
        # self.state('zoomed')

        # Set the minimum size to which the window can be shrunk.
        self.minsize(cfg.width_of_main_tkinter_window - 140, 700)

        # Set the title that will appear in the top window bar,
        # to the right of the icon.
        self.title("Synaptans WorkforceSim™ (version 0.1.081)")

        # Set the width of the content (splash screen, ops screen, etc.)
        # that will appear within the main Tkinter window.        
        cfg.width_of_content_in_main_tkinter_window = 1000
        
        # Set the height of the ops screen canvas. This needs to be set
        # to a number large enough to allow space for however many
        # plots are being displayed in the current version of the program.        
        cfg.height_of_ops_screen_canvas = 6200

        # Set the vertical spacing (in pixels) between the upper left
        # corner of each additional plot added to the ops results screen.
        cfg.image_spacing_vertical_px = 620
        
        # ---------------------------------------------------------------------
        # Create the splash screen frame, which will then in turn
        # create the later frames to be viewed.
        # ---------------------------------------------------------------------

        # The splash screen frame is created as a subframe of
        # cfg.main_Tkinter_window (here known as "self").
        create_splash_screen_frame(self)

# ----------------------------------------------------------------------
# DEFINE FUNC TO CREATE AND RUN SPLASH (LICENSING) SCREEN
# ----------------------------------------------------------------------

# The splash screen frame is created as a subframe of the main Tkinter window.
#
# This frame will automatically call functions to create the program's other
# windows, once the license acceptance button is clicked by the user.

def create_splash_screen_frame(main_Tkinter_window):

        cfg.splash_screen_m = Frame(
            cfg.main_Tkinter_window,
            width=cfg.width_of_content_in_main_tkinter_window,
            )
        cfg.splash_screen_m['bg'] = cfg.splash_screen_main_frame_bg_color
        # cfg.splash_screen_m.pack(fill='both', expand=1)
        cfg.splash_screen_m.pack(fill='none', expand=False)

        # This label appears in the splash screen, near the top;
        # it contains the name of the software.
        splash_screen_m_title_label = Label(
            cfg.splash_screen_m, 
            text="Synaptans WorkforceSim™",
            bg=cfg.splash_screen_m['bg'],
            fg=cfg.splash_screen_main_frame_text_color,
            font=("Verdana", 28)
            )
        splash_screen_m_title_label.pack(pady=10)

        # This label appears in the splash screen, near the top;
        # it contains a tagline about the software.
        splash_screen_m_subtitle_label = Label(
            cfg.splash_screen_m, 
            text="Open-source software for simulating the dynamics of a factory workforce\nand assessing AI-based approaches to predictive workplace analytics",
            bg=cfg.splash_screen_m['bg'],
            fg=cfg.splash_screen_main_frame_text_color,
            font=("Verdana", 12)
            )
        splash_screen_m_subtitle_label.pack(pady=8)

        # Display a custom logo on the splash screen, beneath the Label text.
        # from PIL import ImageTk, Image
        logo_canvas = Canvas(
            cfg.splash_screen_m, 
            width=310, 
            height=180,
            highlightthickness=0, #This is needed to keep an annoying whitish-gray border from appearing
            )
        
        # The line below works in the Tkinter app, but PyInstaller doesn't bundle the image.
        # cfg.logo_image = ImageTk.PhotoImage(Image.open("Combined logos 02.png"), master=cfg.splash_screen_m)

        # The line below is designed to make it possible for PyInstaller to bundle the image.
        logo_image_path_and_filename = os.path.join(
            cfg.input_files_dir,
            "Cognitive_Firewall_and_NeuraXenetica_logos_01_180_ht.png"
            )
        cfg.logo_image = ImageTk.PhotoImage(Image.open(resource_path(logo_image_path_and_filename)), master=cfg.splash_screen_m)

        logo_canvas.create_image(0, 0, anchor="nw", image=cfg.logo_image)
        logo_canvas.pack(pady=30)
        cfg.splash_screen_m.update()


        #This label appears in the splash screen, near the top;
        #it contains info about the software's publisher.
        splash_screen_m_publisher_label = Label(
            cfg.splash_screen_m, 
            text="Developed with support from Cognitive Firewall LLC and NeuraXenetica LLC by Matthew E. Gladden\n©2021-2022 NeuraXenetica LLC",
            bg=cfg.splash_screen_m['bg'],
            fg=cfg.splash_screen_main_frame_text_color,
            font=("Verdana", 8)
            )
        splash_screen_m_publisher_label.pack(pady=5)

        #Within the splash screen frame, create a subframe that will include
        #the licensing apparatus (text, a scrollbar, and, beneath them, a button).
        license_box = Frame(cfg.splash_screen_m)
        license_box.pack(fill='both', expand=1, padx=20, pady=20)

        #Add a license-acceptance button, placed at the bottom of the
        #licensing box.
        cfg.license_accept_button = Button(license_box, text="Click to accept the license and load the simulation operations screen", command=license_accept_button_clicked)
        cfg.license_accept_button.pack(side="bottom", padx=0, pady=0)
        
        #Add a frame containing the EULA and an accompanying scrollbar. To avoid
        #weird sizing problems, they must both be children of a parent frame, rather than
        #making the scrollbar a child of the textbox.
        textbox_and_scrollbar_frame = Frame(license_box)
        textbox_and_scrollbar_frame.pack(fill='both', expand=1, padx=20, pady=20)

        #Add the actual textbox as a child of textbox_and_scrollbar_frame.
        EULA_textbox_m = tk.Text(
            textbox_and_scrollbar_frame,
            wrap="word",
            )
        EULA_scrollbar_m = Scrollbar(textbox_and_scrollbar_frame)
        EULA_textbox_m.config(yscrollcommand=EULA_scrollbar_m.set)
        EULA_text_m = return_EULA_text()
        EULA_textbox_m.insert(tk.END, EULA_text_m)
        EULA_textbox_m.config(state="disabled") #This makes the text non-editable.
        EULA_scrollbar_m.config(command=EULA_textbox_m.yview)
        EULA_scrollbar_m.pack(side="right", fill="y")
        EULA_textbox_m['bg'] = cfg.EULA_box_bg_color
        EULA_textbox_m.pack(fill="both", padx=0, pady=0)
        

        textbox_and_scrollbar_frame.update()
        cfg.splash_screen_m.update()
        cfg.main_Tkinter_window.update()


# ----------------------------------------------------------------------
# DEFINE FUNC TO RUN WHEN LICENSE AGREEMENT BUTTON IS CLICKED
# ----------------------------------------------------------------------

#This function runs when the license acceptance button is clicked;
#it creates the main functional window of the program.

def license_accept_button_clicked():

        #This destroys the splash screen.
        cfg.splash_screen_m.destroy()
        cfg.main_Tkinter_window.update()
        
        #This calls the function to create the main operational program screen,
        #replacing the destroyed splash screen.
        create_main_operational_screen_frame(cfg.workforce_sim_app)


# ----------------------------------------------------------------------
# DEFINE FUNC CREATE AND RUN MAIN OPERATIONAL SCREEN, AS A SUBFRAME
# OF THE MAIN TKINTER WINDOW
# ----------------------------------------------------------------------

def create_main_operational_screen_frame(main_Tkinter_window):

        # ---------------------------------------------------------------------
        # SET UP BASIC LOOK AND LAYOUT OF THE MAIN OPERATIONAL SCREEN
        # ---------------------------------------------------------------------

        #Create a vertical scrollbar for the main operational screen.
        cfg.ops_screen_scrollbar_m = ttk.Scrollbar(
            cfg.main_Tkinter_window,
            orient="vertical",
            )

        #Create a canvas, which is needed for scrolling to work.
        #(Canvas objects can scroll; frame objects can't.)
        cfg.ops_screen_m_canvas = Canvas(
            cfg.main_Tkinter_window, 
            background=cfg.ops_results_section_bg_before_figures_appear_color,
            #Note that the height should be manually set to stretch far enough
            #to include all graphs that will be produced.
            height=cfg.height_of_ops_screen_canvas,
            width=cfg.width_of_content_in_main_tkinter_window,
            #
            #It's critical to set the final value in "scrollregion" 
            #-- the y-value -- to be at least equal to the height above.
            #
            #The fourth value in the parentheses below is what determines how far down the
            #ops screen can scroll, regardless of how much vertical
            #content it actually contains.
            scrollregion=(0, 0, cfg.width_of_content_in_main_tkinter_window, cfg.height_of_ops_screen_canvas),
            )

        cfg.ops_screen_scrollbar_m.config(command=cfg.ops_screen_m_canvas.yview)

        #Create the operational screen frame in which content will be displayed.
        cfg.ops_screen_m = Frame(
            cfg.ops_screen_m_canvas, 
            height=10,
            width=cfg.width_of_content_in_main_tkinter_window,
            )
        
        #Mutually link the scrollbar and cfg.ops_screen_m_canvas,
        #for scrolling purposes.
        #
        cfg.ops_screen_m_canvas.config(yscrollcommand=cfg.ops_screen_scrollbar_m.set)
        
        #Position the scrollbar, canvas, and frame in the main_Tkinter_window.
        #
        cfg.ops_screen_scrollbar_m.pack(side="right", fill="y")
        cfg.ops_screen_m_canvas.pack(side="left", fill="y", expand=True)
        #
        #In order for scrolling to work, it's critical that the ops_screen_m frame
        #be positioned by using "create_window", and not via grid, pack, or place.
        cfg.ops_screen_m_canvas.create_window( 
            (0,0), 
            window=cfg.ops_screen_m, 
            #The width below has a great impact.
            width=cfg.width_of_content_in_main_tkinter_window,
            anchor="nw",
            )

        cfg.ops_screen_m['bg'] = cfg.ops_input_section_outer_margin_color
        ops_screen_m_label = Label(
            cfg.ops_screen_m,
            text="Operations Screen\n(Please see the program’s documentation for instructions)",
            bg=cfg.ops_input_section_outer_margin_color,
            fg=cfg.splash_screen_main_frame_text_color,
            font=("Verdana", 11),
            )
        ops_screen_m_label.pack(pady=20)

        cfg.ops_screen_m_canvas.update()
        cfg.ops_screen_m.update()
        cfg.main_Tkinter_window.update()
        
        
        # ---------------------------------------------------------------------
        # SET UP THE OPS INPUT SUBFRAME (ON THE MAIN OPERATIONAL SCREEN);
        # CREATE ENTRY BOXES FOR INPUT, WITH LABELS AND HINTS
        # ---------------------------------------------------------------------

        #Create an ops_input_frame (for receiving user input) 
        #as a subframe of the main ops_screen_m.
        
        ops_input_frame = Frame(
            cfg.ops_screen_m,
            )
        ops_input_frame['bg'] = cfg.ops_input_section_main_text_area_bg_color
        ops_input_frame.pack(fill=None, expand=False)


        #Create the "Labels" that will explain each field
        #of input to be entered by the user and the "Entry" boxes
        #in which the user will actually enter arguments.
        row_for_first_entry_box = 0
        input_label_width = 35,
        input_label_bg_color = ops_input_frame['bg']
        input_label_fg_color = cfg.ops_input_section_main_text_area_label_hint_text_color
        input_label_font = ("Verdana", 11)
        input_entry_box_width = 7,
        input_entry_box_fg_color = cfg.ops_input_section_main_text_area_arg_entry_text_color
        input_entry_box_font = ("Verdana", 11)
        input_hint_width = 50
        input_hint_bg_color = ops_input_frame['bg']
        input_hint_fg_color = cfg.ops_input_section_main_text_area_label_hint_text_color
        input_hint_font = ("Verdana", 9)
        
        min_person_age_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Minimum age for an individual: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        min_person_age_label.grid(column=0, row=row_for_first_entry_box, sticky="e")
        cfg.min_person_age_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.min_person_age_entry_box.grid(column=1, row=row_for_first_entry_box, sticky="e")
        cfg.min_person_age_entry_box.insert(0, 20)
        min_person_age_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The minimum age (integer; range = 16-99) that an \nemployee may have at the start of the simulation",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        min_person_age_hint.grid(column=2, row=row_for_first_entry_box, sticky="w")
        
        max_person_age_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Maximum age for an individual: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        max_person_age_label.grid(column=0, row=row_for_first_entry_box+1, sticky="e")
        cfg.max_person_age_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.max_person_age_entry_box.grid(column=1, row=row_for_first_entry_box+1, sticky="e")
        cfg.max_person_age_entry_box.insert(0, 65)
        max_person_age_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The maximum age (integer; range = 40-100) that an \nemployee may have at the start of the simulation",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        max_person_age_hint.grid(column=2, row=row_for_first_entry_box+1, sticky="w")
        
        num_persons_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Desired number of personnel: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        num_persons_label.grid(column=0, row=row_for_first_entry_box+2, sticky="e")
        cfg.num_persons_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.num_persons_entry_box.grid(column=1, row=row_for_first_entry_box+2, sticky="e")
        cfg.num_persons_entry_box.insert(0, 724)
        #
        #The cursor will start out focused in this entry box.
        cfg.num_persons_entry_box.focus()
        num_persons_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="Desired size of workforce (integer; range = 52-4996); \nwill be rounded down to even out teams",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        num_persons_hint.grid(column=2, row=row_for_first_entry_box+2, sticky="w")

        ATD_stat_mean_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Mean value for ATD stat: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        ATD_stat_mean_label.grid(column=0, row=row_for_first_entry_box+3, sticky="e")
        cfg.ATD_stat_mean_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.ATD_stat_mean_entry_box.grid(column=1, row=row_for_first_entry_box+3, sticky="e")
        cfg.ATD_stat_mean_entry_box.insert(0, 0.91)
        ATD_stat_mean_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The mean value (float; range = 0.0-1.0) \nfor the randomized attendance stat",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        ATD_stat_mean_hint.grid(column=2, row=row_for_first_entry_box+3, sticky="w")

        ATD_stat_sdev_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Standard deviation for ATD stat: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        ATD_stat_sdev_label.grid(column=0, row=row_for_first_entry_box+4, sticky="e")
        cfg.ATD_stat_sdev_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.ATD_stat_sdev_entry_box.grid(column=1, row=row_for_first_entry_box+4, sticky="e")
        cfg.ATD_stat_sdev_entry_box.insert(0, 0.09)
        ATD_stat_sdev_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The standard deviation (float; range = 0.0-1.0) \nfor the randomized attendance stat",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        ATD_stat_sdev_hint.grid(column=2, row=row_for_first_entry_box+4, sticky="w")

        other_stats_stat_mean_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Mean value for other stats: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        other_stats_stat_mean_label.grid(column=0, row=row_for_first_entry_box+5, sticky="e")
        cfg.other_stats_stat_mean_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.other_stats_stat_mean_entry_box.grid(column=1, row=row_for_first_entry_box+5, sticky="e")
        cfg.other_stats_stat_mean_entry_box.insert(0, 0.73)
        other_stats_stat_mean_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The mean value (float; range = 0.0-1.0) for \nother randomized stats",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        other_stats_stat_mean_hint.grid(column=2, row=row_for_first_entry_box+5, sticky="w")

        other_stats_stat_sdev_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Standard deviation for other stats: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        other_stats_stat_sdev_label.grid(column=0, row=row_for_first_entry_box+6, sticky="e")
        cfg.other_stats_stat_sdev_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.other_stats_stat_sdev_entry_box.grid(column=1, row=row_for_first_entry_box+6, sticky="e")
        cfg.other_stats_stat_sdev_entry_box.insert(0, 0.17)
        other_stats_stat_sdev_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The standard deviation (float; range = 0.0-1.0) \nfor other randomized stats",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        other_stats_stat_sdev_hint.grid(column=2, row=row_for_first_entry_box+6, sticky="w")

        random_seed_A_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Random seed A: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        random_seed_A_label.grid(column=0, row=row_for_first_entry_box+7, sticky="e")
        cfg.random_seed_A_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.random_seed_A_entry_box.grid(column=1, row=row_for_first_entry_box+7, sticky="e")
        cfg.random_seed_A_entry_box.insert(0, 11)
        random_seed_A_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="A random seed (integer; range = 1-99999), \nto allow randomization with reproducibility of results",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        random_seed_A_hint.grid(column=2, row=row_for_first_entry_box+7, sticky="w")

        random_seed_B_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Random seed B: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
#        random_seed_B_label.grid(column=0, row=row_for_first_entry_box+8, sticky="e")
        cfg.random_seed_B_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
#        cfg.random_seed_B_entry_box.grid(column=1, row=row_for_first_entry_box+8, sticky="e")
        cfg.random_seed_B_entry_box.insert(0, 22)
        random_seed_B_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="A random seed (integer; range = 1-99999), \nto allow randomization with reproducibility of results",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
#        random_seed_B_hint.grid(column=2, row=row_for_first_entry_box+8, sticky="w")

        random_seed_C_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Random seed C: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
#        random_seed_C_label.grid(column=0, row=row_for_first_entry_box+9, sticky="e")
        cfg.random_seed_C_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
#        cfg.random_seed_C_entry_box.grid(column=1, row=row_for_first_entry_box+9, sticky="e")
        cfg.random_seed_C_entry_box.insert(0, 33)
        random_seed_C_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="A random seed (integer; range = 1-99999), \nto allow randomization with reproducibility of results",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
#        random_seed_C_hint.grid(column=2, row=row_for_first_entry_box+9, sticky="w")

        random_seed_D_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Random seed D: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
#        random_seed_D_label.grid(column=0, row=row_for_first_entry_box+10, sticky="e")
        cfg.random_seed_D_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
#        cfg.random_seed_D_entry_box.grid(column=1, row=row_for_first_entry_box+10, sticky="e")
        cfg.random_seed_D_entry_box.insert(0, 44)
        random_seed_D_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="A random seed (integer; range = 1-99999), \nto allow randomization with reproducibility of results",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
#        random_seed_D_hint.grid(column=2, row=row_for_first_entry_box+10, sticky="w")

        num_days_to_simulate_label = Label(
            ops_input_frame, 
            width=input_label_width,
            anchor="e",
            text="Number of days to simulate: ", 
            bg=input_label_bg_color,
            fg=input_label_fg_color,
            font=input_label_font,
            )
        num_days_to_simulate_label.grid(column=0, row=row_for_first_entry_box+11, sticky="e")
        cfg.num_days_to_simulate_entry_box = ttk.Entry(
            ops_input_frame, 
            width=input_entry_box_width,
            foreground=input_entry_box_fg_color,
            font=input_entry_box_font,
            )
        cfg.num_days_to_simulate_entry_box.grid(column=1, row=row_for_first_entry_box+11, sticky="e")
        cfg.num_days_to_simulate_entry_box.insert(0, 30)
        num_days_to_simulate_hint = Label(
            ops_input_frame, 
            width=input_hint_width,
            anchor="w",
            justify="left",
            text="The total number (integer; range = 1-200) \nof days of work that should be simulated",
            bg=input_hint_bg_color,
            fg=input_hint_fg_color,
            font=input_hint_font,
            )
        num_days_to_simulate_hint.grid(column=2, row=row_for_first_entry_box+11, sticky="w")


        confirm_sim_settings_button = Button(ops_input_frame, text="Click to run the simulation!", command=confirm_sim_settings_button_clicked)
        confirm_sim_settings_button.grid(columnspan=3, row=13, sticky="ew", padx=100, pady=20)


        # ---------------------------------------------------------------------
        # SET UP THE OPS RESULTS SUBFRAME (ON THE MAIN OPERATIONAL SCREEN)
        # ---------------------------------------------------------------------

        #Create an (initially blank) ops_results_frame (for displaying simulation results) 
        #as a subframe of the main ops_screen_m.

        cfg.ops_results_frame = Frame(
            cfg.ops_screen_m,
            )
        cfg.main_Tkinter_window.update()


# ----------------------------------------------------------------------
# DEFINE FUNC TO RUN WHEN THE "RUN SIMULATION" BUTTON IS CLICKED
# ----------------------------------------------------------------------

def confirm_sim_settings_button_clicked():

    # >>>>> GATHER AND VALIDATE USER INPUT FROM THE ENTRY BOXES <<<<<

    #The "try... except" statements below perform simple input validation;
    #only if the content of each entry box can be successfully converted
    #into the desired number type does the function move forward
    #with destroying the old ops_results_frame and generating a new one.
    
    try: 
        cfg.min_person_age_input = int( cfg.min_person_age_entry_box.get() )
        if cfg.min_person_age_input < 16:
            cfg.min_person_age_input = 16
            cfg.min_person_age_entry_box.delete(0, 'end')
            cfg.min_person_age_entry_box.insert(0, 16)
        if cfg.min_person_age_input > 99:
            cfg.min_person_age_input = 99
            cfg.min_person_age_entry_box.delete(0, 'end')
            cfg.min_person_age_entry_box.insert(0, 99)
    except ValueError: return
        
    try: 
        cfg.max_person_age_input = int( cfg.max_person_age_entry_box.get() )
        if cfg.max_person_age_input < 40:
            cfg.max_person_age_input = 40
            cfg.max_person_age_entry_box.delete(0, 'end')
            cfg.max_person_age_entry_box.insert(0, 40)
        if cfg.max_person_age_input > 100:
            cfg.max_person_age_input = 100
            cfg.max_person_age_entry_box.delete(0, 'end')
            cfg.max_person_age_entry_box.insert(0, 100)
        if cfg.max_person_age_input <= cfg.min_person_age_input:
            cfg.max_person_age_input = cfg.min_person_age_input + 1
            cfg.max_person_age_entry_box.delete(0, 'end')
            cfg.max_person_age_entry_box.insert(0, cfg.max_person_age_input)
    except ValueError: return
        
    #NOTE: I'm not sure why I have this line here.
    cfg.num_persons_input = 0
    try:
        cfg.num_persons_input = int( cfg.num_persons_entry_box.get() )
        if cfg.num_persons_input < 52:
            cfg.num_persons_input = 52
            cfg.num_persons_entry_box.delete(0, 'end')
            cfg.num_persons_entry_box.insert(0, 52)
        if cfg.num_persons_input > 4996:
            cfg.num_persons_input = 4996
            cfg.num_persons_entry_box.delete(0, 'end')
            cfg.num_persons_entry_box.insert(0, 4996)
    except ValueError: return
    
    try: 
        cfg.ATD_stat_mean_input = float( cfg.ATD_stat_mean_entry_box.get() )
        if cfg.ATD_stat_mean_input < 0.0:
            cfg.ATD_stat_mean_input = 0.0
            cfg.ATD_stat_mean_entry_box.delete(0, 'end')
            cfg.ATD_stat_mean_entry_box.insert(0, 0.0)
        if cfg.ATD_stat_mean_input > 1.0:
            cfg.ATD_stat_mean_input = 1.0
            cfg.ATD_stat_mean_entry_box.delete(0, 'end')
            cfg.ATD_stat_mean_entry_box.insert(0, 1.0)
    except ValueError: return
    
    try: 
        cfg.ATD_stat_sdev_input = float( cfg.ATD_stat_sdev_entry_box.get() )
        if cfg.ATD_stat_sdev_input < 0.0:
            cfg.ATD_stat_sdev_input = 0.0
            cfg.ATD_stat_sdev_entry_box.delete(0, 'end')
            cfg.ATD_stat_sdev_entry_box.insert(0, 0.0)
        if cfg.ATD_stat_sdev_input > 1.0:
            cfg.ATD_stat_sdev_input = 1.0
            cfg.ATD_stat_sdev_entry_box.delete(0, 'end')
            cfg.ATD_stat_sdev_entry_box.insert(0, 1.0)
    except ValueError: return
    
    try: 
        cfg.other_stats_stat_mean_input = float( cfg.other_stats_stat_mean_entry_box.get() )
        if cfg.other_stats_stat_mean_input < 0.0:
            cfg.other_stats_stat_mean_input = 0.0
            cfg.other_stats_stat_mean_entry_box.delete(0, 'end')
            cfg.other_stats_stat_mean_entry_box.insert(0, 0.0)
        if cfg.other_stats_stat_mean_input > 1.0:
            cfg.other_stats_stat_mean_input = 1.0
            cfg.other_stats_stat_mean_entry_box.delete(0, 'end')
            cfg.other_stats_stat_mean_entry_box.insert(0, 1.0)
    except ValueError: return
    
    try: 
        cfg.other_stats_stat_sdev_input = float( cfg.other_stats_stat_sdev_entry_box.get() )
        if cfg.other_stats_stat_sdev_input < 0.0:
            cfg.other_stats_stat_sdev_input = 0.0
            cfg.other_stats_stat_sdev_entry_box.delete(0, 'end')
            cfg.other_stats_stat_sdev_entry_box.insert(0, 0.0)
        if cfg.other_stats_stat_sdev_input > 1.0:
            cfg.other_stats_stat_sdev_input = 1.0
            cfg.other_stats_stat_sdev_entry_box.delete(0, 'end')
            cfg.other_stats_stat_sdev_entry_box.insert(0, 1.0)
    except ValueError: return
    
    try: 
        cfg.random_seed_A_input = int( cfg.random_seed_A_entry_box.get() )
        if cfg.random_seed_A_input <1:
            cfg.random_seed_A_input = 1
            cfg.num_persons_entry_box.delete(0, 'end')
            cfg.num_persons_entry_box.insert(0, 1)
        if cfg.random_seed_A_input > 99999:
            cfg.random_seed_A_input = 99999
            cfg.num_persons_entry_box.delete(0, 'end')
            cfg.num_persons_entry_box.insert(0, 99999)
    except ValueError: return
    
    try: cfg.random_seed_B_input = int( cfg.random_seed_B_entry_box.get() )
    except ValueError: return
    
    try: cfg.random_seed_C_input = int( cfg.random_seed_C_entry_box.get() )
    except ValueError: return
    
    try: cfg.random_seed_D_input = int( cfg.random_seed_D_entry_box.get() )
    except ValueError: return
    
    try: 
        cfg.num_days_to_simulate_input = int( cfg.num_days_to_simulate_entry_box.get() )
        if cfg.num_days_to_simulate_input < 1:
            cfg.num_days_to_simulate_input = 1
            cfg.num_days_to_simulate_entry_box.delete(0, 'end')
            cfg.num_days_to_simulate_entry_box.insert(0, 1)
        if cfg.num_days_to_simulate_input > 200:
            cfg.num_days_to_simulate_input = 200
            cfg.num_days_to_simulate_entry_box.delete(0, 'end')
            cfg.num_days_to_simulate_entry_box.insert(0, 200)
    except ValueError: return
    

    # >>>>> DESTROY EXISTING OPS RESULTS FRAME AND CREATE A NEW ONE <<<<<

    cfg.ops_results_frame.destroy()
    cfg.ops_results_frame = Frame(
        cfg.ops_screen_m, 
#        height=100,
        )
    cfg.ops_results_frame['bg'] = cfg.ops_results_section_bg_before_figures_appear_color
#    cfg.ops_results_frame.pack(fill='both', expand=1)
    cfg.ops_results_frame.pack(fill="y", expand=True)


    # ---------------------------------------------------------------------
    # RUN THE SIMULATION
    #
    # Iterate the simulation through the desired time period
    # and calculate resulting metrics.
    # ---------------------------------------------------------------------

    #Define a function that will pass input to the simulation and run it
    #with the given arguments.

    
    wfs.run_core_simulation()

    
    #Note that the simulation can easily generate many Matplotlib
    #plots, which are *all* saved to variables -- but in my current
    #version of Tkinter framework, I can *choose* which of those to
    #actually display to the user in the Output Results frame.
    
    #In the main SWS engine, I can have a console that can run two
    #different functions/versions: one that runs in Tkinter,
    #and one that runs internally, in JN.
    
    
    # ---------------------------------------------------------------------
    # VISUALIZE AND DISPLAY THE RESULTS
    #
    # Plot and display the results of the simulation for the user.
    # ---------------------------------------------------------------------

    plot_image_canvas = Canvas(
        cfg.ops_results_frame, 
#        width=1200, 
        width=cfg.width_of_content_in_main_tkinter_window, 
        #Increasing this height allows more of the picture to appear.
        #But only to a limited extent; further resizing eventually gets blocked.
        height=cfg.height_of_ops_screen_canvas,
        background=cfg.ops_results_section_bg_before_figures_appear_color,
        highlightthickness=0, #This is needed to keep an annoying whitish-gray border from appearing
        )

    #Display an image generated by the core simulator.

#    cfg.plot_image_01 = ImageTk.PhotoImage(png_plt_num_goods_vs_num_poors_hist2d_02)
#    plot_image_canvas.create_image(0, 0, anchor="nw", image=cfg.plot_image_01)
#    plot_image_canvas.pack(fill="y", expand=True)

    cfg.plot_image_01 = ImageTk.PhotoImage(cfg.png_plt_distribution_of_WRKR_CAP_scores_hist)
    plot_image_canvas.create_image(0, 0, anchor="nw", image=cfg.plot_image_01)

    cfg.plot_image_02 = ImageTk.PhotoImage(cfg.png_plt_distribution_of_MNGR_CAP_scores_hist)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*1, anchor="nw", image=cfg.plot_image_02)

    cfg.plot_image_03 = ImageTk.PhotoImage(cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*2, anchor="nw", image=cfg.plot_image_03)

    cfg.plot_image_04 = ImageTk.PhotoImage(cfg.png_plt_MNGR_CAP_by_age_scatter)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*3, anchor="nw", image=cfg.plot_image_04)

    cfg.plot_image_05 = ImageTk.PhotoImage(cfg.png_plt_WRKR_CAP_by_shift_bar)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*4, anchor="nw", image=cfg.plot_image_05)

    cfg.plot_image_06 = ImageTk.PhotoImage(cfg.png_plt_MNGR_CAP_by_role_bar)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*5, anchor="nw", image=cfg.plot_image_06)

    cfg.plot_image_07 = ImageTk.PhotoImage(cfg.png_plt_WRKR_CAP_by_team_bar)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*6, anchor="nw", image=cfg.plot_image_07)

    cfg.plot_image_08 = ImageTk.PhotoImage(cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*7, anchor="nw", image=cfg.plot_image_08)

    cfg.plot_image_09 = ImageTk.PhotoImage(cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d)
    plot_image_canvas.create_image(0, cfg.image_spacing_vertical_px*8, anchor="nw", image=cfg.plot_image_09)

    plot_image_canvas.grid(column=0, row=0)



    cfg.ops_results_frame.update()
    cfg.main_Tkinter_window.update()


# ----------------------------------------------------------------------
# INSTANTIATE THE WORKFORCE SIM APP AND RUN IT
# ----------------------------------------------------------------------

def run_tkinter_workforce_sim_app():

#    perform_tkinter_imports()

#    global Main_App
    cfg.workforce_sim_app = Main_App()
    cfg.workforce_sim_app.mainloop()


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions to run the simulation via particular GUIs
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

def run_swfs_selected_elements_as_tkinter_app():

    print("Welcome to Synaptans WorkforceSim™!\nThis software is ©2021-22 NeuraXenetica LLC and made available for use under GNU General Public License Version 3.\nPlease use the main interface window (which should open separately) to configure and run the simulation.")

    # Perform basic setup tasks.
    iofm.specify_directory_structure()
       
    # Run the Tkinter GUI Main_App function.    #
    run_tkinter_workforce_sim_app()
    # That func, in turn, will need to be updated
    # so that after setting up the GUI and gathering
    # user input, it calls the "run_core_simulation()" function.
    #
    # The run_tkinter_workforce_sim_app()
    # will need to be updated to then gather selected
    # plots generated by the code
    # and to display them to the user.


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions needed for PyInstaller
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE FUNC NEEDED FOR PYINSTALLER TO BUNDLE IMAGES
#
# This function is needed to help make it possible for PyInstaller to
# bundle images from my hard drive (e.g., CF logo files) as part
# of the Windows exe file.
# ----------------------------------------------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)
