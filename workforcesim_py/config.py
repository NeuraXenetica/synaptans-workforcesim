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
# ▓▓ DEFINE GLOBAL VARIABLES
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

# The dictionary of persons, in which each entry (person)
# is a separate person object of the Person class.
persons = {}

# A Pandas DataFrame containing selected attributes of all persons.
persons_df = None

# The dictionary of roles, in which each entry (role)
# is a separate role object of the Role class.
roles = {}

# The dictionary of shifts, in which each entry (shift)
# is a separate shift object of the Shift class.
shifts = {}

# The total number of "Laborers" proper (and not persons more generally)
# who should be part of each shift.
num_of_laborers_per_shift = 0

# The dictionary of teams, in which each entry (team)
# is a separate team object of the Team class.
teams = {}

# The total number of "Laborers" proper (and not persons more generally)
# who should be part of each team.
num_of_laborers_per_team = 0

# This list tracks how many Team Leaders still need to be assigned
# to each team. Each team begins by needing 1 Team Leader
# (apart from the special "unassigned" team, which doesn't 
# need any Team leaders to be added).
num_of_leaders_needed = []

# The dictionary of spheres, in which each entry (sphere)
# is a separate sphere object of the Sphere class.
teams = {}

# This list tracks which sphere each team belongs to.
# (The first team has sphere 0, the special "unassigned" sphere.)
sphere_of_given_team = []

# ---------------------------------------------------------------------
# Terms used as column headers in DataFrame tables and reports.
# ---------------------------------------------------------------------
person_id_header_term = ""
first_name_header_term = ""
last_name_header_term = ""
sex_header_term = ""
age_header_term = ""
sphere_header_term = ""
shift_header_term = ""
role_header_term = ""
MNGR_CAP_header_term = ""
WRKR_CAP_header_term = ""
supervisor_header_term = ""
colleagues_header_term = ""
subordinates_header_term = ""

# ---------------------------------------------------------------------
# Terms associated with "available_role_titles".
# ---------------------------------------------------------------------
production_director_term = ""
shift_manager_term = ""
team_leader_term = ""
laborer_term = ""
available_role_titles = []

# ---------------------------------------------------------------------
# Terms associated with "available_shift_titles".
# ---------------------------------------------------------------------
unassigned_shift_term = ""
shift_1_term = ""
shift_2_term = ""
shift_3_term = ""
available_shift_titles = []

# ---------------------------------------------------------------------
# Terms associated with "available_sphere_titles".
# ---------------------------------------------------------------------
available_sphere_titles = []
teams_per_sphere_per_shift = []

# ---------------------------------------------------------------------
# Variables relating to simulation iteration date and time.
# ---------------------------------------------------------------------
current_datetime_obj = None
day_of_sim_iter = 0

# ---------------------------------------------------------------------
# Variables supplied (or confirmed) by a user in the program's GUI. 
# ---------------------------------------------------------------------
min_person_age = 0
max_person_age = 0
size_of_comm_initial = 0
ATD_stat_mean = 0.0
ATD_stat_sdev = 0.0
other_stats_stat_mean = 0.0
other_stats_stat_sdev = 0.0
random_seed_A = 0
random_seed_B = 0
random_seed_C = 0
random_seed_D = 0
num_of_days_to_simulate = 0

# ---------------------------------------------------------------------
# Workforce configuration variables. 
# ---------------------------------------------------------------------
emp_id_starting_value = 0
num_of_teams_per_shift = 0

# ---------------------------------------------------------------------
# Variables relating to plotting of results.
# ---------------------------------------------------------------------
plot_figure_dpi = 0
plot_savefig_dpi = 0
plot_figsize = 0.0
plot_xy_label_fontsize = 0
plot_xy_label_color = ""
plot_xy_label_pad = 0
plot_hist_data_color = ""
plot_scatter_data_color = ""
plot_bar_data_color = ""
plot_background_facecolor = ""
figure_background_facecolor = ""
plot_xy_ticks_fontsize = 0
plot_xy_ticks_color = ""
plot_title_fontsize = 0
plot_title_color = ""

# ---------------------------------------------------------------------
# In-memory PNG charts, graphs, and other images created
# through the plotting of results.
# ---------------------------------------------------------------------
png_plt_distribution_of_WRKR_CAP_scores_hist = None
png_plt_distribution_of_MNGR_CAP_scores_hist = None
png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter = None
png_plt_MNGR_CAP_by_age_scatter = None
png_plt_WRKR_CAP_by_shift_bar = None
png_plt_MNGR_CAP_by_role_bar = None
png_plt_WRKR_CAP_by_team_bar = None
png_plt_WRKR_CAP_vs_mean_Eff_scatter = None
png_plt_num_Good_vs_Poor_actions_by_person_hist2d = None

# ---------------------------------------------------------------------
# Variables relating to the Tkinter app, windows, and other TK elements.
# ---------------------------------------------------------------------
main_Tkinter_window = None
width_of_main_tkinter_window = 0
width_of_content_in_main_tkinter_window = 0
height_of_ops_screen_canvas = 0
image_spacing_vertical_px = 0
splash_screen_m = None
logo_image = None
license_accept_button = None

ops_screen_scrollbar_m = None
ops_screen_m_canvas = None
ops_screen_m = None

# Boxes for entering user input.
min_person_age_entry_box = None
max_person_age_entry_box = None
num_persons_entry_box = None
ATD_stat_mean_entry_box = None
ATD_stat_sdev_entry_box = None
other_stats_stat_mean_entry_box = None
other_stats_stat_sdev_entry_box = None
random_seed_A_entry_box = None
random_seed_B_entry_box = None
random_seed_C_entry_box = None
random_seed_D_entry_box = None
num_days_to_simulate_entry_box = None

# The actual contents of the user input.
min_person_age_input = 0
max_person_age_input = 0
num_persons_input = 0
ATD_stat_mean_input = 0.0
ATD_stat_sdev_input = 0.0
other_stats_stat_mean_input = 0.0
other_stats_stat_sdev_input = 0.0
random_seed_A_input = 0
random_seed_B_input = 0
random_seed_C_input = 0
random_seed_D_input = 0
num_days_to_simulate_input = 0

# Generated PNG plot images as they are to be displayed onscreen by Tkinter.
plot_image_01 = None
plot_image_02 = None
plot_image_03 = None
plot_image_04 = None
plot_image_05 = None
plot_image_06 = None
plot_image_07 = None
plot_image_08 = None
plot_image_09 = None

ops_results_frame = None
Main_App = None
workforce_sim_app = None

# Colors to be used in key components.
main_window_bg_color = ""
splash_screen_main_frame_bg_color = "" # also the bg color for logos 
splash_screen_main_frame_text_color = ""
EULA_box_bg_color = ""
ops_input_section_outer_margin_color = ""
ops_input_section_main_text_area_bg_color = ""
ops_input_section_main_text_area_label_hint_text_color = ""
ops_input_section_main_text_area_arg_entry_text_color = ""
ops_results_section_bg_before_figures_appear_color = ""
ops_results_section_fig_bg_color = ""
ops_results_section_fig_axis_bg_color = ""

# ---------------------------------------------------------------------
# Variables relating to I/O and files.
# ---------------------------------------------------------------------
current_working_dir = ""
input_files_dir = ""
output_files_dir = ""
export_path_and_filename = ""

# ---------------------------------------------------------------------
# Male and female first and last names available for use 
# when randomly generating persons.
# ---------------------------------------------------------------------
first_names_M = [
    "Brian",
    "Carlos",
    "Charles",
    "Christopher",
    "Daniel",
    "David",
    "George",
    "James",
    "Jason",
    "Jeffrey",
    "John",
    "Jose",
    "Joseph",
    "Kenneth",
    "Luis",
    "Mark",
    "Marvin",
    "Michael",
    "Paul",
    "Richard",
    "Robert",
    "Sean",
    "Steven",
    "Thomas",
    "William",
    ]

first_names_F = [
    "Alma",
    "Amanda",
    "Barbara",
    "Christine",
    "Claudia",
    "Elizabeth",
    "Emily",
    "Eva",
    "Jennifer",
    "Joan",
    "Juanita",
    "Kathleen",
    "Kimberly",
    "Laura",
    "Linda",
    "Maria",
    "Mary",
    "Nancy",
    "Patricia",
    "Rita",
    "Samantha",
    "Sarah",
    "Susan",
    "Tamara",
    "Tonya",
    ]

last_names_M = [
    "Anderson",
    "Bailey",
    "Baker",
    "Brown",
    "Carter",
    "Cooper",
    "Davis",
    "Evans",
    "Garcia",
    "Hall",
    "Hernandez",
    "Hoffman",
    "Howard",
    "Johnson",
    "Jones",
    "Martinez",
    "Miller",
    "Mitchell",
    "Moore",
    "Murray",
    "Olson",
    "Ortiz",
    "Owens",
    "Phillips",
    "Pierce",
    "Reed",
    "Rodriguez",
    "Smith",
    "Taylor",
    "Thompson",
    "Tran",
    "Warren",
    "Washington",
    "Williams",
    "Wilson",
    ]

last_names_F = [
    "Anderson",
    "Bailey",
    "Baker",
    "Brown",
    "Carter",
    "Cooper",
    "Davis",
    "Evans",
    "Garcia",
    "Hall",
    "Hernandez",
    "Hoffman",
    "Howard",
    "Johnson",
    "Jones",
    "Martinez",
    "Miller",
    "Mitchell",
    "Moore",
    "Murray",
    "Olson",
    "Ortiz",
    "Owens",
    "Phillips",
    "Pierce",
    "Reed",
    "Rodriguez",
    "Smith",
    "Taylor",
    "Thompson",
    "Tran",
    "Warren",
    "Washington",
    "Williams",
    "Wilson",
    ]

# ██████████████████████████████████████████████████████████████████████
# ██ 
# ██████████████████████████████████████████████████████████████████████

# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓▓ 
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ 
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░ 
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
