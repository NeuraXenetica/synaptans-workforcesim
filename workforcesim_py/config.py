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

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Basic configuration variables
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ---------------------------------------------------------------------
# Variables relating to I/O and files.
# ---------------------------------------------------------------------
current_working_dir = "" # This value will be calculated.
input_files_dir = "" # This value will be calculated.
output_files_dir = "" # This value will be calculated.
export_path_and_filename = "" # This value will be calculated.


# ---------------------------------------------------------------------
# Core simulation configuration variables.
# ---------------------------------------------------------------------

# A unique code for the given run of the simulation, which can be used
# as a prefix for the files to be saved that are associated with the run.
unique_file_prefix_code_for_simulation_run = None

random_seed_A = 4 # ◀■=■=■=■=■
#random_seed_B = 0
#random_seed_C = 0
#random_seed_D = 0

# The overall "strength of effect" modifier that influences
# the strength of a number of effects (e.g., interdependencies).
strength_of_effect = 0.25

# If an OEE system is in use, each manager records workers' Efficacy
# with 100% accuracy. If no OEE system is in use, the manager makes a 
# subjective estimate of workers' Efficacy.
oee_system_in_use = False

emp_id_starting_value = 0 # This value will be calculated.


# ---------------------------------------------------------------------
# Variables relating to simulation iteration date and time.
# ---------------------------------------------------------------------
sim_starting_date = "2021-12-13"

# The number of days must be >1, in order to avoid problem when
# generating the SD of certain entry values (e.g., Efficacy behaviors).
# This is the number of *workdays* that should actually be simulated,
# which (because of the existence of weekends) is less than the number
# of calendar days spanned by the period.
num_of_days_to_simulate = 10 # ◀■■■■■■■

current_datetime_obj = None # This value will be calculated.
day_of_sim_iter = 0 # This value will be updated; 0 is the first simulated day.


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Personnel-related variables
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

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
# Workforce configuration variables.
# ---------------------------------------------------------------------
min_person_age = 18
max_person_age = 65
#ATD_stat_mean = 0.8
#ATD_stat_sdev = 0.2
other_stats_stat_mean = 0.8 # ◀■=■=■=■=■
other_stats_stat_sdev = 0.2 # ◀■=■=■=■=■

# Set the initial size of the community.
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
num_of_laborers_per_team = 1 # ◀■■■■■■■

# This value will be calculated, based on num_of_laborers_per_team.
size_of_comm_initial = 0

num_of_teams_per_shift = 8 # This value will be calculated?


# ---------------------------------------------------------------------
# Workstyle group membership probabilities.
# ---------------------------------------------------------------------
# The probability that a newly created worker is assigned to
# a given Workstyle group. For each demographic type, the sum of these 
# numbers should be 1.0.

workstyle_prob_older_female_A = 0.43
workstyle_prob_older_female_B = 0.04
workstyle_prob_older_female_C = 0.28
workstyle_prob_older_female_D = 0.21
workstyle_prob_older_female_E = 0.04

workstyle_prob_younger_female_A = 0.28
workstyle_prob_younger_female_B = 0.04
workstyle_prob_younger_female_C = 0.37
workstyle_prob_younger_female_D = 0.28
workstyle_prob_younger_female_E = 0.03

workstyle_prob_older_male_A = 0.39
workstyle_prob_older_male_B = 0.28
workstyle_prob_older_male_C = 0.21
workstyle_prob_older_male_D = 0.10
workstyle_prob_older_male_E = 0.02

workstyle_prob_younger_male_A = 0.18
workstyle_prob_younger_male_B = 0.37
workstyle_prob_younger_male_C = 0.04
workstyle_prob_younger_male_D = 0.21
workstyle_prob_younger_male_E = 0.20


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Variables relating to behaviors, records, and other actions
# █ (including action probabilities, impacts, and contests)
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ---------------------------------------------------------------------
# Variables relating to workers' daily behaviors.
# ---------------------------------------------------------------------

# The master DF containing an entry for every actual behavior performed
# by workers (including a worker's absence, which is itself a sort of
# behavior).
behavs_act_df = None


# ---------------------------------------------------------------------
# Base rates for particular actions by personnel.
# ---------------------------------------------------------------------
base_rate_attendance = 0.93
base_rate_idea = 0.008
base_rate_lapse = 0.08
base_rate_feat = 0.008
base_rate_slip = 0.08
base_rate_teamwork = 0.008
base_rate_disruption = 0.08
base_rate_sacrifice = 0.008
base_rate_sabotage = 0.08
base_rate_efficacy = 0.32
base_rate_false_positive = 0.01

# If a person has, e.g., a Sociality stat of 0.85, this number is the multiplier
# that determines how large an impact that stat will have on, e.g., the person's
# probability of generating a Teamwork behavior. If the number below is 0.05,
# then the person's personal base probability of generating a Teamwork behavior
# will be increased by 0.85 * 0.05. In the case of Poor behaviors, the
# multiplied stat is subtracted from (rather than added to) the base rate.
stat_to_prob_mod_conv_factor = 0.05

# Regardless of whether he belongs to a Workstyle group that adds additional
# variability to his daily Efficacy, every worker's daily Efficacy behaviors
# display a certain base level of variability, determined by this number.
# This number is the "scale" for the np.random.normal function (centered on 0)
# added to the modifier of a person's daily Efficacy score.
base_max_efficacy_variability = 1.5

# The base accuracy with which managers make records.
base_rate_recording_accuracy = 0.65

# Random ± variance added to actual Efficacy when a manager is
# estimating that actual Efficacy in order to record it. The 
# larger the number, the more inaccurate the Efficacy records
# will be.
#
# NOTE! This is currently a plain random number; changing it to
# a randomized number using a mean and SD would be more realistic. 
variance_to_eff_as_recorded_by_manager = 0.25

# This is the maximum amount of the modifier by which a person's
# Efficacy level can be increased or decreased by
# virtue of being in a Workstyle group with elevated or reduced (and not
# simply average) Efficacy.
# 
# This value is multiplied by strength_of_effect
# and by a random number (0.0-1.0), so for most persons, the actual Efficacy
# multiplier resulting from membership in a workstyle group will be
# significantly less than this number.
workstyle_eff_level_modifier = 1.4 # ◀■=■=■=■=■

# This is the maximum daily variability that can be added to the actual
# Efficacy of a member of a Workstyle group that has "variable" Efficacy.
# Members of groups with "stable" Efficacy add no such added variability.
#
# This value is multiplied by strength_of_effect
# and by a random number (0.0-1.0), so for most persons, the actual Efficacy
# variability resulting from membership in a workstyle group will be
# significantly less than this number.
workstyle_eff_max_daily_variability = 1.9 # ◀■=■=■=■=■

# These are the maximum daily bonuses or penalties that give a particular
# person an elevated or reduced probability of performing certain
# types of actions (an Idea, a Slip, etc.) under certain circumstances.
prob_elevation_for_disruption_due_to_workstyle = 0.04
prob_reduction_for_disruption_due_to_workstyle = 0.5
prob_elevation_for_idea_due_to_workstyle = 0.04
prob_reduction_for_idea_due_to_workstyle = 0.57

# These are the maximum daily bonuses or penalties that can be added to
# a person's Efficacy modifier, based on a given factor such as:
#     - the person's age
#     - the current day of the week
#     - the proportion of the person's teammates who are of the same sex
#     - the difference in age between the person and his supervisor
# This value is the maximum value "max" for the modifier random.uniform(0.0, max),
# which is multiplied by the overall strength_of_effect.
eff_bonus_max_from_person_age = 0.083
eff_bonus_max_from_weekday = 0.65
eff_bonus_max_from_teammate_sexes = 1.8
eff_penalty_max_from_sup_age_diff = 0.04


# ---------------------------------------------------------------------
# The power of the system's "defense rolls".
# ---------------------------------------------------------------------
# The higher these numbers are, the more difficult it will be for
# persons to generated certain types of actions (e.g., actual behaviors
# or recording actions).

# The maximum number (a randomly generated number between 0.0 and this number)
# that a person may need to beat with their adjusted stats and levels, in order
# to generate a Good or Poor behavior on a particular day.
#
# Adjusting these numbers is the simplest way of "coarsely" increasing
# or decreasing the overall number of Good or Poor behaviors as a whole.
defense_roll_max_behavior_good = 1.0 # ◀■=■=■=■=■
defense_roll_max_behavior_poor = 0.9 # ◀■=■=■=■=■

# The maximum number (a randomly generated number between 0.0 and this number)
# that a person may need to beat with their adjusted stats and levels, in order
# to generate a True Positive recording action on a particular day.
defense_roll_max_recording_TP = 0.8 # ◀■=■=■=■=■


# ---------------------------------------------------------------------
# The strength of influence of certain events on other events.
# ---------------------------------------------------------------------

# Overall strength of the positive impact that a person's receiving a True Positive
# record of a Good behavior that he had performed has over the following three days
# on his actual Efficacy behaviors.
strength_of_good_TP_record_impact_on_eff = 0.35 # ◀■=■=■=■=■

# Overall strength of the negative impact that a person's receiving a False Negative
# record of a Good behavior that he had performed has over the following three days
# on his actual Efficacy behaviors.
strength_of_good_FN_record_impact_on_eff = 0.38 # ◀■=■=■=■=■


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Variables relating to visualizations
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ---------------------------------------------------------------------
# Variables relating to plotting of results.
# ---------------------------------------------------------------------
plot_figure_dpi = 500
plot_savefig_dpi = 500
plot_figsize = (6.5, 3)
plot_xy_label_fontsize = 7
plot_xy_label_color = "#9ea3ff" #lavender
plot_xy_label_pad = 4
plot_hist_data_color = "#ff00ff" #magenta
plot_scatter_data_color = "#ff00ff" #magenta
plot_line_data_color = "#00FA95" #bright green
plot_line_data_width = 1.85
plot_bar_data_color = "#ffa74d" #orange-yellow
plot_background_facecolor = '#404040' # dark gray
figure_background_facecolor = '#34343C' #darkest plum
plot_bar_transition_grad_color = "#2A2A2A" # darker gray
plot_bar_bottom_grad_color = "#191919" # almost black
plot_xy_ticks_fontsize = 7
plot_xy_ticks_color = "#fc8293" #salmon
plot_title_fontsize = 8
plot_title_color = "#5cffe5" #cyan

ops_results_section_fig_bg_color = "#34343C" #darkest plum
ops_results_section_fig_axis_bg_color = "black" #black


# ---------------------------------------------------------------------
# Variables storing in-memory PNG charts, graphs, and other images 
# created through the plotting of results.
# ---------------------------------------------------------------------


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ The user's version of organizational terms to be used
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
# █ when randomly generating persons
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# ---------------------------------------------------------------------
# First names.
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

# ---------------------------------------------------------------------
# Last names.
# ---------------------------------------------------------------------

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