# ╔════════════════════════════════════════════════════════════════════╗
# ║   Synaptans WorkforceSim™ is open-source software for simulating   ║
# ║   the complex dynamics of a factory workforce.                     ║
# ║                                                                    ║
# ║   Developed by Matthew E. Gladden • ©2021-23 NeuraXenetica LLC     ║
# ║   This software is made available for use under                    ║
# ║   GNU General Public License Version 3                             ║
# ║   (please see https://www.gnu.org/licenses/gpl-3.0.html).          ║
# ╚════════════════════════════════════════════════════════════════════╝

"""
This module stores configuration settings and constants and variables 
that are used by multiple modules within the package.
"""

# ======================================================================
# Constants/variables relating to I/O and files.
# ======================================================================

# These values will be calculated with the app is launched.
CURRENT_WORKING_DIR = ""
STATIC_DIR = ""
PLOTS_DIR = ""
DATASETS_DIR = ""
GRAPHICS_DIR = ""
EXPORT_PATH_AND_FILENAME = ""

# ======================================================================
# Variables relating to the web app.
# ======================================================================

plots_to_display_list = []
visualization_data_source = "stored_dataset"
dataset_csv_for_download_url = None

# ======================================================================
# Core simulation configuration constants/variables.
# ======================================================================

# A unique code for the given run of the simulation, which can be used
# as a prefix for the files to be saved that are associated with the 
# run. (The variant is formatted to be used as a suffix rather than a 
# prefix.)
unique_file_prefix_code_for_simulation_run = None
unique_file_suffix_code_for_simulation_run = None

# The main random seed used in modules.
RANDOM_SEED_A = 99

# The overall "strength of effect" modifier that influences the strength
#  of a number of effects (e.g., interdependencies).
STRENGTH_OF_EFFECT = 1.0

# If an OEE system is in use, each manager records workers' Efficacy
# with 100% accuracy. If no OEE system is in use, the manager makes a 
# subjective estimate of workers' Efficacy.
OEE_SYSTEM_IN_USE = False

EMP_ID_STARTING_VALUE = 0

# ======================================================================
# Variables relating to simulation iteration date and time.
# ======================================================================

# This is the time at which processing of the simulation begins on the
# user's computer; it's used for tracking elapsed processing time.
sim_processing_start_datetime = None

# This is the first date of the period to be simulated (not the 
# date on which the simulation is actually run). If an initial priming 
# period is being included, this is the start of the priming period, not
# the first date of the "focal period" whose results will be retained 
# for analysis.
SIM_STARTING_DATE = "2021-12-20" # ◀ E.g., "2021-10-01"

# This is the first date of the "focal period" that should be retained
# in the dataset and used for analysis and visualization. If this is
# later than SIM_STARTING_DATE, the difference represents a sort of
# "priming period" for initializing the simulation's dynamics. This 
# helps "smooth out" the simulation results and account for the fact 
# that (e.g.) some types of separations that require a certain number of
# events to occur or days to pass *can't* happen at the beginning of the
# simulation.
#
# Setting this value to the same as SIM_STARTING_DATE allows one to 
# simulate the opening of a brand new factory that *had* no previous 
# workers or history.
SIM_STARTING_DATE_FOR_ANALYSIS = "2022-01-01"

# The number of days must be > 1, in order to avoid problems when
# generating the SD of certain entry values (e.g., Efficacy behaviors).
#
# This number doesn't include any "priming period" for the simulation; 
# it is the number of simulated days in the "focal period" that should 
# be retained in the dataset for analysis and visualization.
NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS = 20 # ◀ E.g., 546 days = 18 months

# The total number of days to be simulated (including both the days in 
# the priming period and the number of days to be simulated for analysis
# and visualization). This number will be calculated automatically.
NUM_OF_DAYS_TO_SIMULATE = None

# Number of days in the priming period (if any). This will be
# automatically calculated.
NUM_OF_DAYS_IN_PRIMING_PERIOD = None

current_datetime_obj = None
day_of_sim_iter = 0

# This value will be updated based on the simulated calendar.
day_of_month_1_indexed = None

# This number will be stored permanently as a reference; it will not
# be updated with each new simulated day. If the simulation has, e.g.,
# a 3-day priming period, then this value will be -3.
day_of_sim_iter_for_first_simulated_day = None

# ======================================================================
# Personnel-related constants/variables.
# ======================================================================

# ----------------------------------------------------------------------
# Variables relating to personnel and the community as a whole.
# ----------------------------------------------------------------------

# The dictionary of persons, in which each entry (person)
# is a separate person object of the Person class.
persons = {}

# A DataFrame containing selected attributes of all persons.
persons_df = None

# The dictionary of roles, in which each entry (role)
# is a separate role object of the Role class.
roles = {}

# The dictionary of shifts, in which each entry (shift)
# is a separate shift object of the Shift class.
shifts = {}

# The total number of persons with the role of "Laborer" (and not 
# persons more generally) who should be part of each shift. This value 
# will be calculated.
NUM_OF_LABORERS_PER_SHIFT = 0

# The dictionary of teams, in which each entry (team)
# is a separate team object of the Team class.
teams = {}

# During initialization, this list tracks how many Team Leaders still 
# need to be assigned to each team. Each team begins by needing 1 Team 
# Leader (apart from the special "unassigned" team, which doesn't need 
# any Team leaders to be added).
num_of_leaders_needed = []

# The dictionary of spheres, in which each entry (sphere)
# is a separate sphere object of the Sphere class.
spheres = {}

# This list tracks which sphere each team belongs to.
# (The first team has sphere 0, the special "unassigned" sphere.)
sphere_of_given_team = []

# ----------------------------------------------------------------------
# Workforce configuration constants/variables.
# ----------------------------------------------------------------------

# Minimum and maximum age of persons at the start of the simulation.
MIN_PERSON_AGE = 18
MAX_PERSON_AGE = 65

# Mean and standard deviation used in generating certain personal stats.
OTHER_STATS_STAT_MEAN = 0.8
OTHER_STATS_STAT_SDEV = 0.2

# Here the initial size of the community is set by specifying
# the total number of "Laborers" proper (and not persons more generally)
# who should be part of each team.
#
# The value of this variable determines how many total persons will
# constitute the organization's workforce.
#
# The total size of the workforce community will be:
#       cfg.SIZE_OF_COMM_INITIAL = \
#           (cfg.NUM_OF_LABORERS_PER_TEAM) * 24 + 24 + 4
#
# This yields, e.g., the following workforce sizes:
#
#       NUM_OF_LABORERS_PER_TEAM        Total size of workforce
#       1                               52
#       2                               76
#       3                               100
#       4                               124
#       5                               148
#       10                              268
#       15                              388
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
NUM_OF_LABORERS_PER_TEAM = 3
NUM_OF_TEAMS_PER_SHIFT = 8

# This value will be calculated, based on NUM_OF_LABORERS_PER_TEAM.
SIZE_OF_COMM_INITIAL = 0

# ----------------------------------------------------------------------
# Workstyle group membership probabilities.
# ----------------------------------------------------------------------
# This is the probability that a newly created worker is assigned to
# a given Workstyle group. For each demographic type, the sum of these 
# numbers should be 1.0.
WORKSTYLE_PROB_OLDER_FEMALE_A = 0.43
WORKSTYLE_PROB_OLDER_FEMALE_B = 0.04
WORKSTYLE_PROB_OLDER_FEMALE_C = 0.28
WORKSTYLE_PROB_OLDER_FEMALE_D = 0.21
WORKSTYLE_PROB_OLDER_FEMALE_E = 0.04
WORKSTYLE_PROB_YOUNGER_FEMALE_A = 0.28
WORKSTYLE_PROB_YOUNGER_FEMALE_B = 0.04
WORKSTYLE_PROB_YOUNGER_FEMALE_C = 0.37
WORKSTYLE_PROB_YOUNGER_FEMALE_D = 0.28
WORKSTYLE_PROB_YOUNGER_FEMALE_E = 0.03
WORKSTYLE_PROB_OLDER_MALE_A = 0.39
WORKSTYLE_PROB_OLDER_MALE_B = 0.28
WORKSTYLE_PROB_OLDER_MALE_C = 0.21
WORKSTYLE_PROB_OLDER_MALE_D = 0.10
WORKSTYLE_PROB_OLDER_MALE_E = 0.02
WORKSTYLE_PROB_YOUNGER_MALE_A = 0.18
WORKSTYLE_PROB_YOUNGER_MALE_B = 0.37
WORKSTYLE_PROB_YOUNGER_MALE_C = 0.04
WORKSTYLE_PROB_YOUNGER_MALE_D = 0.21
WORKSTYLE_PROB_YOUNGER_MALE_E = 0.20

# ======================================================================
# Variables relating to behaviors, records, and other elements of 
# events (including action probabilities, impacts, and contests).
# ======================================================================

# ----------------------------------------------------------------------
# Kinds of behaviors and records.
# ----------------------------------------------------------------------

BEHAV_TYPES = [
    "Separation",
    "Onboarding",
    "Attendance",
    "Good",
    "Poor",
    "Efficacy",
    ]

BEHAV_SUBTYPES = [
    "Resignation",
    "Termination",
    "Presence",
    "Absence",
    "Idea",
    "Lapse",
    "Feat",
    "Slip",
    "Teamwork",
    "Disruption",
    "Sacrifice",
    "Sabotage",
    ]

BEHAV_NATURES = [
    "Low Commitment",
    "Ethically Inferior Supervisor",
    "Unrecognized Good Behaviors",
    "Recruited Away",
    "Underrecorded Efficacy",
    "Poor Teammates",
    "Multiple Sabotages",
    "Lapses and Below-Average Efficacy",
    "Multiple Lapses",
    "Multiple Slips",
    "Multiple Disruptions",
    "Multiple Absences",
    "Low Efficacy",
    ]

# "Comptypes" are "comparative types" or "comparison types"; they 
# reflect that aspect of a behavior that's most relevant when plotting 
# it against other types of events. For some types of behaviors, the 
# Comptype is the same as a behavior's Type; for others, it's the same 
# as a behavior's Subtype.
BEHAV_COMPTYPES = [
    "Resignation",
    "Termination",
    "Onboarding",
    "Presence",
    "Absence",
    "Idea",
    "Lapse",
    "Feat",
    "Slip",
    "Teamwork",
    "Disruption",
    "Sacrifice",
    "Sabotage",
    "Efficacy",
    ]

RECORD_TYPES = [
    "Separation",
    "Onboarding",
    "Attendance",
    "Good",
    "Poor",
    "Efficacy",
    ]

RECORD_SUBTYPES = []
RECORD_NATURES = []

RECORD_COMPTYPES = [
    "Resignation",
    "Termination",
    "Onboarding",
    "Presence",
    "Absence",
    "Idea",
    "Lapse",
    "Feat",
    "Slip",
    "Teamwork",
    "Disruption",
    "Sacrifice",
    "Sabotage",
    "Efficacy",
    ]

# ----------------------------------------------------------------------
# Constants/variables relating to workers' daily behaviors.
# ----------------------------------------------------------------------

# This is the master DF containing an entry for every actual behavior 
# performed by workers (including a worker's Absence, which is itself 
# a sort of behavior).
behavs_act_df = None
#
# This transformed version of the DF has had features and targets 
# engineered, for use in machine-learning-based analyses. Each row 
# represents a single day of activity for a single person.
pers_day_df = None

# An archival copy of behavs_act_df that includes entries made during
# any "priming period" (whose contents will be excluded from analysis
# and visualizations).
behavs_act_df_w_priming_period = None

# This is the temporary *list* of behaviors (each as an individual DF) 
# for a given day to be added to behavs_act_df in one step, after all 
# of the behaviors for the day have been calculated.
list_of_behavs_to_add_to_behavs_act_df = []

# The average of all *actual* Efficacy values recorded in the 
# organization to date.
org_actual_eff_values_mean = 0.0

# The average of all *recorded* Efficacy values recorded in the 
# organization to date.
org_recorded_eff_values_mean = 0.0

# ----------------------------------------------------------------------
# Base rates for particular actions by personnel.
# ----------------------------------------------------------------------
BASE_RATE_ATTENDANCE = 0.93
BASE_RATE_ATTENDANCE_sat = 0.0015

# This is low, to compensate for the fact that some Workstyles generate 
# a high number.
BASE_RATE_IDEA = 0.0085 

BASE_RATE_LAPSE = 0.062
BASE_RATE_FEAT = 0.025
BASE_RATE_SLIP = 0.05
BASE_RATE_TEAMWORK = 0.022
BASE_RATE_DISRUPTION = 0.048

# This is low, to compensate for its being additionally triggered by certain event combinations.
BASE_RATE_SACRIFICE = 0.0055

BASE_RATE_SABOTAGE = 0.04
BASE_RATE_EFFICACY = 0.36
BASE_RATE_FALSE_POSITIVE = 0.01

# If a person has, e.g., a Sociality stat of 0.85, this number is the 
# multiplier that determines how large an impact that stat will have on,
# e.g., the person's probability of generating a Teamwork behavior. If 
# the number below is 0.05, then the person's personal base probability 
# of generating a Teamwork behavior will be increased by 0.85 * 0.05. 
# In the case of Poor behaviors, the multiplied stat is subtracted from 
# (rather than added to) the base rate.
STAT_TO_PROB_MOD_CONV_FACTOR = 0.05

# Regardless of whether he belongs to a Workstyle group that adds 
# additional variability to his daily Efficacy, every worker's daily 
# Efficacy behaviors display a certain base level of variability, 
# determined by this number. This number is the "scale" for the 
# np.random.normal function (centered on 0) added to the modifier of a 
# person's daily Efficacy score.
BASE_MAX_EFFICACY_VARIABILITY = 0.15

# The base accuracy with which managers make records.
BASE_RATE_RECORDING_ACCURACY = 0.65

# Random ± variance added to actual Efficacy when a manager is
# estimating that actual Efficacy in order to record it. The larger the 
# number, the more inaccurate the Efficacy records will be.
# NOTE! This is currently an ordinary random number; changing it to
# a randomized number using a mean and SD would be more realistic. 
VARIANCE_TO_EFF_AS_RECORDED_BY_MANAGER = 0.25

# This is the maximum amount of the modifier by which a person's
# Efficacy level can be increased or decreased by virtue of being in a 
# Workstyle group with elevated or reduced (and not simply average) 
# Efficacy.
# 
# This value is multiplied by STRENGTH_OF_EFFECT and by a random number 
# (0.0-1.0), so for most persons, the actual Efficacy multiplier 
# resulting from membership in a workstyle group will be significantly 
# less than this number.
WORKSTYLE_EFF_LEVEL_MODIFIER = 0.4525

# This is the maximum daily variability that can be added to the actual
# Efficacy of a member of a Workstyle group that has "variable" Efficacy.
# Members of groups with "stable" Efficacy add no such added variability.
#
# This value is multiplied by STRENGTH_OF_EFFECT and by a random number 
# (0.0-1.0), so for most persons, the actual Efficacy variability 
# resulting from membership in a workstyle group will be significantly 
# less than this number.
WORKSTYLE_EFF_MAX_DAILY_VARIABILITY = 3.8

# These are the maximum daily bonuses or penalties that give a 
# particular person an elevated or reduced probability of generating 
# certain types of behaviors (an Idea, a Slip, etc.) under certain 
# circumstances.
PROB_ELEVATION_FOR_IDEA_DUE_TO_WORKSTYLE = 1.35
PROB_REDUCTION_FOR_IDEA_DUE_TO_WORKSTYLE = 0.8
PROB_ELEVATION_FOR_DISRUPTION_DUE_TO_WORKSTYLE = 1.4
PROB_REDUCTION_FOR_DISRUPTION_DUE_TO_WORKSTYLE = 0.95

PROB_ELEVATION_MAX_FOR_TEAMWORK_DUE_TO_DAY_IN_MONTH = 0.45
PROB_ELEVATION_MAX_FOR_DISRUPTION_DUE_TO_DAY_IN_MONTH = 0.4375
PROB_ELEVATION_MAX_FOR_SLIP_DUE_TO_DAY_IN_MONTH = 0.625

# These are the maximum daily bonuses or penalties that can be added to
# a person's Efficacy modifier, based on a given factor such as:
#     - the person's age
#     - the current day of the week
#     - the proportion of the person's teammates who are of the same sex
#     - the difference in age between the person and his supervisor
# This value is the maximum value "max" for the modifier 
# random.uniform(0.0, max), which is multiplied by the overall 
# STRENGTH_OF_EFFECT.
EFF_BONUS_MAX_FROM_PERSON_AGE = 0.0275
EFF_BONUS_MAX_FROM_WEEKDAY = 0.1625
EFF_BONUS_MAX_FROM_TEAMMATE_SEXES = 0.75
EFF_PENALTY_MAX_FROM_SUP_AGE_DIFF = 0.0275
EFF_BONUS_MAX_FROM_DAY_IN_MONTH = 0.05
EFF_PENALTY_MAX_FROM_SEASON_OF_YEAR = 0.225

# The probability that, on the given day, a given Laborer will have 
# his position (i.e., Team) swapped with that of a Laborer working 
# on a different Team in the same shift.
PROB_LABORER_SWAP_TO_DIFFERENT_TEAM = 0.05

# ----------------------------------------------------------------------
# The power of the system's "defense rolls".
# ----------------------------------------------------------------------
# The higher these numbers are, the more difficult it will be for
# persons to generated certain types of actions (e.g., actual behaviors
# or recording actions).

# The maximum number (a randomly generated number between 0.0 and this 
# number) that a person may need to beat with their adjusted stats and 
# levels, in order to generate a Good or Poor behavior on a particular 
# day.
#
# Adjusting these numbers is the simplest way of "coarsely" increasing
# or decreasing the overall number of Good or Poor behaviors as a whole.
DEFENSE_ROLL_MAX_BEHAVIOR_GOOD = 3.0
DEFENSE_ROLL_MAX_BEHAVIOR_POOR = 3.0

# The maximum number (a randomly generated number between 0.0 and this 
# number) that a person may need to beat with their adjusted stats and 
# levels, in order to generate a True Positive recording action on a 
# particular day.
DEFENSE_ROLL_MAX_RECORDING_TP = 0.8

# ----------------------------------------------------------------------
# The strength of influence of certain events on other events.
# ----------------------------------------------------------------------

# Overall strength of the positive impact that a person's receiving a 
# True Positive record of a Good behavior that he had performed has over
# the following three days on his actual Efficacy behaviors.
STRENGTH_OF_GOOD_TP_RECORD_IMPACT_ON_EFF = 0.07

# Overall strength of the negative impact that a person's receiving a 
# False Negative record of a Good behavior that he had performed has 
# over the following three days on his actual Efficacy behaviors.
STRENGTH_OF_GOOD_FN_RECORD_IMPACT_ON_EFF = 0.1875

# ======================================================================
# Constants/variables relating to visualizations.
# ======================================================================
PLOT_FIGURE_DPI = 500
PLOT_SAVEFIG_DPI = 500
PLOT_FIGSIZE = (6.5, 3)
PLOT_XY_LABEL_FONTSIZE = 7
PLOT_XY_LABEL_PAD = 4
PLOT_LINE_DATA_WIDTH = 1.85
PLOT_XY_TICKS_FONTSIZE = 7
PLOT_TITLE_FONTSIZE = 8

PLOT_COLOR_LAVENDER = "#9ea3ff"
PLOT_COLOR_MAGENTA = "#ff00ff"
PLOT_COLOR_GREEN = "#00FA95"
PLOT_COLOR_GOLD = "#ffa74d"
PLOT_COLOR_DARK_PLUM = '#34343C' # darkest plum
PLOT_COLOR_SALMON = "#fc8293" # salmon
PLOT_COLOR_CYAN = "#5cffe5" # cyan
PLOT_COLOR_MEDIUM_GRAY = '#404040' # dark gray
PLOT_COLOR_DARKER_GRAY = "#2A2A2A" # darker gray
PLOT_COLOR_DARKEST_GRAY = "#191919" # almost black
PLOT_COLOR_BLACK = "black" # black

# ======================================================================
# Organizational terms to be used.
# ======================================================================

# ---------------------------------------------------------------------
# Terms used as column headers in DF tables and reports.
# ----------------------------------------------------------------------
PERSON_ID_HEADER_TERM = "Sub ID"
FIRST_NAME_HEADER_TERM = "Sub First Name"
LAST_NAME_HEADER_TERM = "Sub Last Name"
SEX_HEADER_TERM = "Sub Sex"
AGE_HEADER_TERM = "Sub Age"
SPHERE_HEADER_TERM = "Sphere"
SHIFT_HEADER_TERM = "Sub Shift"
TEAM_HEADER_TERM = "Sub Team"
ROLE_HEADER_TERM = "Sub Role"
MNGR_CAP_HEADER_TERM = "MNGR_CAP"
WRKR_CAP_HEADER_TERM = "WRKR_CAP"
SUPERVISOR_CAP_HEADER_TERM = "Supervisor"
COLLEAGUES_CAP_HEADER_TERM = "Colleagues"
SUBORDINATES_HEADER_TERM = "Subordinates"

# ----------------------------------------------------------------------
# Terms associated with "AVAILABLE_ROLE_TITLES".
# ----------------------------------------------------------------------
# Specify the names of the four available roles, in hierarchical order 
# from the "highest." The entries in the list must be maintained in 
# order, as items in the list of role titles are sometimes referenced
# by functions using their index number.
PRODUCTION_DIRECTOR_TERM = "Production Director"
SHIFT_MANAGER_TERM = "Shift Manager"
TEAM_LEADER_TERM = "Team Leader"
LABORER_TERM = "Laborer"

AVAILABLE_ROLE_TITLES = [
    PRODUCTION_DIRECTOR_TERM,
    SHIFT_MANAGER_TERM,
    TEAM_LEADER_TERM,
    LABORER_TERM,
    ]

# ----------------------------------------------------------------------
# Terms associated with "AVAILABLE_SHIFT_TITLES".
# ----------------------------------------------------------------------
# Specify the names of the one "unassigned" shift object and the three 
# regular shifts. The entries in the list must be maintained in order,
# as items in the list of shift titles are sometimes referenced by 
# functions using their index number.
UNASSIGNED_SHIFT_TERM = "unassigned"
SHIFT_1_TERM = "Shift 1"
SHIFT_2_TERM = "Shift 2"
SHIFT_3_TERM = "Shift 3"

AVAILABLE_SHIFT_TITLES = [
    UNASSIGNED_SHIFT_TERM,
    SHIFT_1_TERM,
    SHIFT_2_TERM,
    SHIFT_3_TERM,
    ]

# ----------------------------------------------------------------------
# Terms associated with "AVAILABLE_SPHERE_TITLES".
# ----------------------------------------------------------------------
# The first sphere in the list, corresponding to "general management", 
# is reserved for the Production Director and Shift Managers. There are 
# not any entire teams associated with that sphere. The remaining 
# spheres in this list may have any nature, and there can be any number 
# of different terms in the list.
AVAILABLE_SPHERE_TITLES = [
    "general management",
    "manufacturing",
    "packaging",
    "logistics",
    "engineering",
    ]

# Specify the number of teams per shift handling each of the spheres 
# listed above. The first sphere, "general management", doesn't have an 
# entire team; it's represented by the Production Director and Shift 
# Managers. Its number will always be 0.
teams_per_sphere_per_shift = [
    0,
    4,
    2,
    1,
    1,
    ]

# ======================================================================
# Male and female first and last names available for use when randomly 
# generating persons
# ======================================================================

FIRST_NAMES_M = [
    "Adam",
    "Andrew",
    "Anthony",
    "Benjamin",
    "Brian",
    "Carlos",
    "Charles",
    "Christopher",
    "Daniel",
    "David",
    "Dennis",
    "Douglas",
    "Edward",
    "Eric",
    "Francis",
    "George",
    "Gregory",
    "Harold",
    "Henry",
    "James",
    "Jason",
    "Jeffrey",
    "John",
    "Jose",
    "Joseph",
    "Joshua",
    "Juan",
    "Kenneth",
    "Kevin",
    "Luis",
    "Mark",
    "Martin",
    "Marvin",
    "Michael",
    "Nathan",
    "Patrick",
    "Paul",
    "Peter",
    "Phillip",
    "Richard",
    "Robert",
    "Ryan",
    "Samuel",
    "Scott",
    "Sean",
    "Stephen",
    "Thomas",
    "Timothy",
    "Victor",
    "William",
    ]

FIRST_NAMES_F = [
    "Alice",
    "Alma",
    "Amanda",
    "Angela",
    "Anna",
    "Barbara",
    "Carol",
    "Christine",
    "Claudia",
    "Cynthia",
    "Diane",
    "Dorothy",
    "Elizabeth",
    "Emily",
    "Eva",
    "Helen",
    "Jennifer",
    "Jessica",
    "Joan",
    "Joyce",
    "Juanita",
    "Karen",
    "Katherine",
    "Kathleen",
    "Kimberly",
    "Laura",
    "Linda",
    "Margaret",
    "Maria",
    "Martha",
    "Mary",
    "Melissa",
    "Michelle",
    "Nancy",
    "Nicole",
    "Patricia",
    "Rebecca",
    "Rita",
    "Ruth",
    "Samantha",
    "Sandra",
    "Sarah",
    "Sharon",
    "Shirley",
    "Stephanie",
    "Susan",
    "Tamara",
    "Theresa",
    "Tonya",
    "Virginia",
    ]

LAST_NAMES_M = [
    "Anderson",
    "Andreassen",
    "Bailey",
    "Baker",
    "Barnes",
    "Bauer",
    "Beaumont",
    "Brown",
    "Butler",
    "Byrne",
    "Carter",
    "Castellano",
    "Chao",
    "Chen",
    "Collins",
    "Cooper",
    "Dahl",
    "Davis",
    "Dietrich",
    "Evans",
    "Fiore",
    "Fischer",
    "Flores",
    "Fournier",
    "Frazier",
    "Garcia",
    "Gonzalez",
    "Graziano",
    "Grigoryan",
    "Hansen",
    "Hall",
    "Hernandez",
    "Hoffman",
    "Howard",
    "Huang",
    "Hunt",
    "Ishii",
    "Johansen",
    "Johnson",
    "Jones",
    "Kim",
    "Kowalczyk",
    "Lambert",
    "Lee",
    "Lewis",
    "Lombardo",
    "Lopez",
    "Lorenz",
    "Marino",
    "Marshall",
    "Martinez",
    "Milano",
    "Miller",
    "Mitchell",
    "Moore",
    "Murphy",
    "Nguyen",
    "Novak",
    "Olson",
    "Ortiz",
    "Owens",
    "Park",
    "Parker",
    "Patel",
    "Phillips",
    "Pierce",
    "Reed",
    "Reynolds",
    "Rivera",
    "Robinson",
    "Rodriguez",
    "Romano",
    "Rossi",
    "Ruiz",
    "Sandoval",
    "Schmidt",
    "Smith",
    "Stepanyan",
    "Suzuki",
    "Taylor",
    "Thompson",
    "Tran",
    "Virtanen",
    "Vogel",
    "Walker",
    "Warren",
    "Washington",
    "Watson",
    "Webb",
    "Weber",
    "Wieczorek",
    "Williams",
    "Wilson",
    "Winter",
    "Wright",
    "Yang",
    "Yoshida",
    "Yoon",
    "Young",
    "Zimmerman",
    ]

LAST_NAMES_F = [
    "Anderson",
    "Andreassen",
    "Bailey",
    "Baker",
    "Barnes",
    "Bauer",
    "Beaumont",
    "Brown",
    "Butler",
    "Byrne",
    "Carter",
    "Castellano",
    "Chao",
    "Chen",
    "Collins",
    "Cooper",
    "Dahl",
    "Davis",
    "Dietrich",
    "Evans",
    "Fiore",
    "Fischer",
    "Flores",
    "Fournier",
    "Frazier",
    "Garcia",
    "Gonzalez",
    "Graziano",
    "Grigoryan",
    "Hansen",
    "Hall",
    "Hernandez",
    "Hoffman",
    "Howard",
    "Huang",
    "Hunt",
    "Ishii",
    "Johansen",
    "Johnson",
    "Jones",
    "Kim",
    "Kowalczyk",
    "Lambert",
    "Lee",
    "Lewis",
    "Lombardo",
    "Lopez",
    "Lorenz",
    "Marino",
    "Marshall",
    "Martinez",
    "Milano",
    "Miller",
    "Mitchell",
    "Moore",
    "Murphy",
    "Nguyen",
    "Novak",
    "Olson",
    "Ortiz",
    "Owens",
    "Park",
    "Parker",
    "Patel",
    "Phillips",
    "Pierce",
    "Reed",
    "Reynolds",
    "Rivera",
    "Robinson",
    "Rodriguez",
    "Romano",
    "Rossi",
    "Ruiz",
    "Sandoval",
    "Schmidt",
    "Smith",
    "Stepanyan",
    "Suzuki",
    "Taylor",
    "Thompson",
    "Tran",
    "Virtanen",
    "Vogel",
    "Walker",
    "Warren",
    "Washington",
    "Watson",
    "Webb",
    "Weber",
    "Wieczorek",
    "Williams",
    "Wilson",
    "Winter",
    "Wright",
    "Yang",
    "Yoshida",
    "Yoon",
    "Young",
    "Zimmerman",
    ]


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