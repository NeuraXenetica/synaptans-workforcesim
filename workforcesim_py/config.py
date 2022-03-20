# -*- coding: utf-8 -*-

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

"""
This module stores configuration settings and variables that are used by
multiple modules.
"""

# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ PRELIMINARY STEPS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Configure code analysis
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# This disables pylint convention-violation alerts that see
# variables as "constants" and thus require them to use
# the UPPER_CASE naming style, when in fact they are used
# by modules as variables.
# pylint: disable=C0103


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE VARIABLES
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ---------------------------------------------------------------------
# Variables relating to personnel and the community as a whole.
# ---------------------------------------------------------------------

# The dictionary of persons, in which each entry (person)
# is a separate person object of the Person class.
persons = {} # This value will be calculated.

# A Pandas DataFrame containing selected attributes of all persons.
persons_df = None # This value will be calculated.

# The dictionary of roles, in which each entry (role)
# is a separate role object of the Role class.
roles = {} # This value will be calculated.

# The dictionary of shifts, in which each entry (shift)
# is a separate shift object of the Shift class.
shifts = {} # This value will be calculated.

# The total number of "Laborers" proper (and not persons more generally)
# who should be part of each shift.
num_of_laborers_per_shift = 0 # This value will be calculated.

# The dictionary of teams, in which each entry (team)
# is a separate team object of the Team class.
teams = {} # This value will be calculated.

# This list tracks how many Team Leaders still need to be assigned
# to each team. Each team begins by needing 1 Team Leader
# (apart from the special "unassigned" team, which doesn't
# need any Team leaders to be added).
num_of_leaders_needed = [] # This value will be calculated.

# The dictionary of spheres, in which each entry (sphere)
# is a separate sphere object of the Sphere class.
spheres = {} # This value will be calculated.

# This list tracks which sphere each team belongs to.
# (The first team has sphere 0, the special "unassigned" sphere.)
sphere_of_given_team = [] # This value will be calculated.


# ---------------------------------------------------------------------
# Variables relating to workers' daily behaviors.
# ---------------------------------------------------------------------

# The master DF containing an entry for every actual behavior performed
# by workers (including a worker's absence, which is itself a sort of
# behavior).
behavs_act_df = None


# ---------------------------------------------------------------------
# Variables relating to simulation iteration date and time.
# ---------------------------------------------------------------------
current_datetime_obj = None # This value will be calculated.
day_of_sim_iter = 0 # This value will be calculated.


# ---------------------------------------------------------------------
# Variables supplied (or confirmed) by a user in the program's GUI.
# ---------------------------------------------------------------------
min_person_age = 18
max_person_age = 65
#ATD_stat_mean = 0.8
#ATD_stat_sdev = 0.2
other_stats_stat_mean = 0.8
other_stats_stat_sdev = 0.2
random_seed_A = 1
#random_seed_B = 0
#random_seed_C = 0
#random_seed_D = 0
sim_starting_date = "2021-12-13"
num_of_days_to_simulate = 5 # ◀■■■■■■■


# ---------------------------------------------------------------------
# Base rates for particular actions by personnel.
# ---------------------------------------------------------------------
base_rate_attendance = 0.93
base_rate_idea = 0.08
base_rate_lapse = 0.05
base_rate_feat = 0.08
base_rate_slip = 0.05
base_rate_teamwork = 0.08
base_rate_disruption = 0.05
base_rate_sacrifice = 0.08
base_rate_sabotage = 0.05
base_rate_efficacy = 0.42
base_rate_recording_accuracy = 0.85
base_rate_false_positive = 0.01

strength_of_effect = 0.25


# ---------------------------------------------------------------------
# Workforce configuration variables.
# ---------------------------------------------------------------------

#Set the initial size of the community.

# The total number of "Laborers" proper (and not persons more generally)
# who should be part of each team.
#
# The value of this variable determines how many total persons will
# constitute the organization's workforce.
#
# The total size of the workforce community will be:
#       cfg.size_of_comm_initial = \
#       (cfg.num_of_laborers_per_team) * 24 + 4
#
# This would yield, e.g., the following workforce sizes:
#
#       num_of_laborers_per_team        Total size of workforce
#       1                               52
#       2                               76
#       3                               100
#       4                               124
#       5                               148
#       10                              268
#       20                              508
#       30                              748
#       40                              988
#       41                              1012
#       50                              1228
#       60                              1468
#       62                              1516
#       70                              1708
#       82                              1996
#       83                              2020
#       123                             2980
#       124                             3004
#       207                             4996
#       208                             5020
#
num_of_laborers_per_team = 5 # ◀■■■■■■■

# This value will be calculated, based on num_of_laborers_per_team.
size_of_comm_initial = 0

num_of_teams_per_shift = 8 # This value will be calculated?

emp_id_starting_value = 10001

# If an OEE system is in use, each manager records workers' Efficacy
# with 100% accuracy. If no OEE system is in use, the manager makes a 
# subjective estimate of workers' Efficacy.
oee_system_in_use = False


# ---------------------------------------------------------------------
# Variables relating to plotting of results.
# ---------------------------------------------------------------------
plot_figure_dpi = 500
plot_savefig_dpi = 500
plot_figsize = (6.5, 3)
plot_xy_label_fontsize = 7
plot_xy_label_color = "#9ea3ff" #lavendar
plot_xy_label_pad = 4
plot_hist_data_color = "#ff00ff" #magenta
plot_scatter_data_color = "#ff00ff" #magenta
plot_line_data_color = "#00FA95" #bright green
plot_line_data_width = 1.85
plot_bar_data_color = "#ffa74d" #orange-yellow
plot_background_facecolor = '#404040'
figure_background_facecolor = '#34343C' #darkest plum
plot_xy_ticks_fontsize = 7
plot_xy_ticks_color = "#fc8293" #salmon
plot_title_fontsize = 8
plot_title_color = "#5cffe5" #cyan


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
png_plt_Eff_by_weekday_bar = None
png_plt_Eff_by_age_bar = None
png_plt_Eff_by_same_gender_colleagues_prtn_scatter = None
png_plt_Eff_by_same_gender_colleagues_prtn_bar = None
png_plt_Eff_by_same_gender_colleagues_prtn_line = None
png_plt_sub_sup_age_diff_vs_recorded_eff_line = None


ops_results_section_fig_bg_color = "#34343C" #darkest plum
ops_results_section_fig_axis_bg_color = "black" #black


# ---------------------------------------------------------------------
# Variables relating to I/O and files.
# ---------------------------------------------------------------------
current_working_dir = "" # This value will be calculated.
input_files_dir = "" # This value will be calculated.
output_files_dir = "" # This value will be calculated.
export_path_and_filename = "" # This value will be calculated.


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ The user's version of organizational terms to be used.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ---------------------------------------------------------------------
# Terms used as column headers in DF tables and reports.
# ---------------------------------------------------------------------
person_id_header_term = "Person ID" # the user's term for the "Person ID" column header
first_name_header_term = "First Name" # the user's term for the "First name" column header
last_name_header_term = "Last Name" # the user's term for the "Last name" column header
sex_header_term = "Sex" # the user's term for the "Sex" column header
age_header_term = "Age" # the user's term for the "Age" column header
sphere_header_term = "Sphere" # the user's term for the "Sphere" column header
shift_header_term = "Shift" # the user's term for the "Shift" column header
team_header_term = "Team" # the user's term for the "Team" column header
role_header_term = "Role" # the user's term for the "Role" column header
MNGR_CAP_header_term = "MNGR_CAP" # the user's term for the "MNGR_CAP" column header
WRKR_CAP_header_term = "WRKR_CAP" # the user's term for the "WRKR_CAP" column header
supervisor_header_term = "Supervisor" # the user's term for the "Supervisor" column header
colleagues_header_term = "Colleagues" # the user's term for the "Colleagues" column header
subordinates_header_term = "Subordinates" # the user's term for the "Subordinates" column header

# ---------------------------------------------------------------------
# Terms associated with "available_role_titles".
# ---------------------------------------------------------------------

# Specify the names of the four available roles,
# in hierarchical order from the "highest."
# The entries in the list must be maintained in order,
# as items in the list of role titles are sometimes referenced
# by functions using their index number.
production_director_term = "Production Director" # the user term for "Production Director"
shift_manager_term = "Shift Manager" # the user term for "Shift Manager"
team_leader_term = "Team Leader" # the user term for "Team Leader"
laborer_term = "Laborer" # the user term for (ordinary) "Laborer"

available_role_titles = [
    production_director_term,
    shift_manager_term,
    team_leader_term,
    laborer_term,
    ]

# ---------------------------------------------------------------------
# Terms associated with "available_shift_titles".
# ---------------------------------------------------------------------

# Specify the names of the one "unassigned" shift object
# and the three regular shifts.
# The entries in the list must be maintained in order,
# as items in the list of role titles are sometimes referenced
# by functions using their index number.
unassigned_shift_term = "unassigned" # the user term for the "unassigned" shift object
shift_1_term = "Shift 1"  # the user term for the "Shift 1" shift object
shift_2_term = "Shift 2"  # the user term for the "Shift 2" shift object
shift_3_term = "Shift 3"  # the user term for the "Shift 3" shift object

available_shift_titles = [
    unassigned_shift_term,
    shift_1_term,
    shift_2_term,
    shift_3_term,
    ]

# ---------------------------------------------------------------------
# Terms associated with "available_sphere_titles".
# ---------------------------------------------------------------------

# This is a list of terms, not a single term.
# The first sphere in the list, corresponding to "general management", 
# is reserved for the Production Director and Shift Managers.
# There are not any entire teams associated with that sphere.
# The remaining spheres in this list may have any nature, and there
# can be any number of different terms in the list.
available_sphere_titles = [
    "general management", #this is the user term for "general management", specific to the Production Director and Shift Managers
    "manufacturing",
    "packaging",
    "logistics",
    "engineering",
    ]

# Specify the number of teams per shift handling each of the
# spheres listed above.
# The first sphere, "general management", doesn't have an entire
# team; it's represented by the Production director and Shift managers.
# Its number will always be 0.
teams_per_sphere_per_shift = [
    0, #this number (always 0) is for "general management", specific to the Production Director and Shift Managers
    4,
    2,
    1,
    1,
    ]


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Male and female first and last names available for use
# █ when randomly generating persons.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

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



# ••••-••••-••••-••••-••••-••••-••••--••••-••••-••••-••••-••••-••••-••••

# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ 
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ 
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
# ● 
# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

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