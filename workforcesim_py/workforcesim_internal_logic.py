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


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Import additional Python modules (e.g., from the standard library)   
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

import random
import statistics
import warnings
from collections import defaultdict
import io
import os
import numpy as np
from datetime import datetime
from PIL import ImageTk, Image

#pip install wheel
#pip install pandas

try: import pandas
except ImportError:
    from pip._internal import main as pip
    pip(['install', '--user', 'pandas'])
    import pandas
import pandas as pd

try: import matplotlib
except ImportError:
    from pip._internal import main as pip
    pip(['install', '--user', 'matplotlib'])
    import matplotlib
import matplotlib.pyplot as plt

#import matplotlib
#from matplotlib.backends.backend_tkagg import(
#    FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.figure import Figure


# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓▓ DEFINE CLASSES AND FUNCTIONS
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define utility functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# FUNC TO SORT DATAFRAME BY A GIVEN COLUMN (DESCENDING)
# ----------------------------------------------------------------------
def sort_df_by_given_field_descending(df_u, col_name_u):
    df_sorted = df_u.copy()
    df_sorted = df_sorted.sort_values(by=col_name_u, ascending=False)
    return df_sorted


# ----------------------------------------------------------------------
# FUNCTION TO SPECIFY USER-INPUTTED TERMS USED IN THE ORGANIZATION
# ----------------------------------------------------------------------
def define_user_terms(
    # Specify terms used as column headers in DF tables.
    person_id_header_term_u, #person_id_header_term_u, the user's term for the "Person ID" column header
    first_name_header_term_u, #first_name_header_term_u, the user's term for the "First name" column header
    last_name_header_term_u, #last_name_header_term_u, the user's term for the "Last name" column header
    sex_header_term_u, #sex_header_term_u, the user's term for the "Sex" column header
    age_header_term_u, #age_header_term_u, the user's term for the "Age" column header
    sphere_header_term_u, #sphere_header_term_u, the user's term for the "Sphere" column header
    shift_header_term_u, #shift_header_term_u, the user's term for the "Shift" column header
    team_header_term_u, #team_header_term_u, the user's term for the "Team" column header
    role_header_term_u, #role_header_term_u, the user's term for the "Role" column header
    MNGR_CAP_header_term_u, #MNGR_CAP_header_term_u, the user's term for the "MNGR_CAP" column header
    WRKR_CAP_header_term_u, #WRKR_CAP_header_term_u, the user's term for the "WRKR_CAP" column header
    supervisor_header_term_u, #supervisor_header_term_u, the user's term for the "Supervisor" column header
    colleagues_header_term_u, #colleagues_header_term_u, the user's term for the "Colleagues" column header
    subordinates_header_term_u, #subordinates_header_term_u, the user's term for the "Subordinates" column header

    # Terms associated with "available_role_titles"
    production_director_term_u, #production_director_term_u, the user term for "Production Director"
    shift_manager_term_u, #shift_manager_term_u, the user term for "Shift Manager"
    team_leader_term_u, #team_leader_term_u, the user term for "Team Leader"
    laborer_term_u, #laborer_term_u, the user term for (ordinary) "Laborer"
    
    # Terms associated with "available_shift_titles"
    unassigned_shift_term_u, #unassigned_shift_term_u, the user term for the "unassigned" shift object
    shift_1_term_u,  #shift_1_term_u, the user term for the "Shift 1" shift object
    shift_2_term_u,  #shift_2_term_u, the user term for the "Shift 2" shift object
    shift_3_term_u,  #shift_3_term_u, the user term for the "Shift 3" shift object

    # Terms associated with "available_sphere_titles".
    
    # This is a list of terms, not a single term.
    # The first term in the list always corresponds to "general management".
    available_sphere_title_terms_u,
    
    # This is a list of numbers, not a single term.
    # The first number in the list is always 0; it's the number of teams assigned to "general management".
    teams_per_sphere_per_shift_u
    ):

    # ---------------------------------------------------------------------
    # Define terms used as column headers in DF tables and reports.
    # ---------------------------------------------------------------------
    cfg.person_id_header_term = person_id_header_term_u
    cfg.first_name_header_term = first_name_header_term_u
    cfg.last_name_header_term = last_name_header_term_u
    cfg.sex_header_term = sex_header_term_u
    cfg.age_header_term = age_header_term_u
    cfg.sphere_header_term = sphere_header_term_u
    cfg.shift_header_term = shift_header_term_u
    cfg.team_header_term = team_header_term_u
    cfg.role_header_term = role_header_term_u
    cfg.MNGR_CAP_header_term = MNGR_CAP_header_term_u
    cfg.WRKR_CAP_header_term = WRKR_CAP_header_term_u
    cfg.supervisor_header_term = supervisor_header_term_u
    cfg.colleagues_header_term = colleagues_header_term_u
    cfg.subordinates_header_term = subordinates_header_term_u

    # ---------------------------------------------------------------------
    # Define terms associated with "available_role_titles".
    # ---------------------------------------------------------------------

    # Specify the names of the four available roles,
    # in hierarchical order from the "highest."
    # The entries in the list must be maintained in order,
    # as items in the list of role titles are sometimes referenced
    # by functions using their index number.
    cfg.production_director_term = production_director_term_u
    cfg.shift_manager_term = shift_manager_term_u
    cfg.team_leader_term = team_leader_term_u
    cfg.laborer_term = laborer_term_u

    cfg.available_role_titles = [
        cfg.production_director_term,
        cfg.shift_manager_term,
        cfg.team_leader_term,
        cfg.laborer_term,
        ]

    # ---------------------------------------------------------------------
    # Define terms associated with "available_shift_titles".
    # ---------------------------------------------------------------------

    # Specify the names of the one "unassigned" shift object
    # and the three regular shifts.
    # The entries in the list must be maintained in order,
    # as items in the list of role titles are sometimes referenced
    # by functions using their index number.
    cfg.unassigned_shift_term = unassigned_shift_term_u
    cfg.shift_1_term = shift_1_term_u
    cfg.shift_2_term = shift_2_term_u
    cfg.shift_3_term = shift_3_term_u
    
    cfg.available_shift_titles = [
        cfg.unassigned_shift_term,
        cfg.shift_1_term,
        cfg.shift_2_term,
        cfg.shift_3_term,
        ]

    # ---------------------------------------------------------------------
    # Define terms associated with "available_sphere_titles".
    # ---------------------------------------------------------------------

    # This is a list of terms, not a single term.
    # The first sphere in the list, corresponding to "general management", 
    # is reserved for the Production Director and Shift Managers.
    # There are not any entire teams associated with that sphere.
    # The remaining spheres in this list may have any nature, and there
    # can be any number of different terms in the list.
    cfg.available_sphere_titles = available_sphere_title_terms_u

    # Specify the number of teams per shift handling each of the
    # spheres listed above.
    # The first sphere, "general management", doesn't have an entire
    # team; it's represented by the Production director and Shift managers.
    # Its number will always be 0.
    cfg.teams_per_sphere_per_shift = teams_per_sphere_per_shift_u


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define the "Person" class and related functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE THE "PERSON" CLASS
# ----------------------------------------------------------------------
class Person_class:

    # ---------------------------------------------------------------------
    # Define initialization function.
    # ---------------------------------------------------------------------
    def __init__(self):

        # ---------------------------------------------------------------------
        # Unique identifier for the person.
        # ---------------------------------------------------------------------

        # Assign an emp_id number that's one higher than the max number already
        # used (or that equals "emp_id_starting_value", if this is the first
        # Person class person object to be created).
        if len(cfg.persons) == 0:
            self.per_id = cfg.emp_id_starting_value
        else:
            self.per_id = max(cfg.persons[p].per_id for p in cfg.persons ) + 1

        # ---------------------------------------------------------------------
        # Gender, age, and other basic demographic traits.
        # ---------------------------------------------------------------------

        # Sex is randomly chosen from among "M" or "F"
        self.sex = random.choice(["M", "F"])

        # Randomly select the person's first and last name.
        if self.sex == "M":
            self.f_name = random.choice(cfg.first_names_M)
            self.l_name = random.choice(cfg.last_names_M)
        else:
            self.f_name = random.choice(cfg.first_names_F)
            self.l_name = random.choice(cfg.last_names_F)

        # Each person begins with a random age within the min-max range.
        self.age = cfg.min_person_age + random.randint(0, cfg.max_person_age - cfg.min_person_age)

        # ---------------------------------------------------------------------
        # Stable personal capacities.
        # ---------------------------------------------------------------------
 
        # Ambition.
        self.AMB = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Attendance.
        # Note that this uses a custom mean and SD.
        self.ATD = generate_personal_stat(cfg.ATD_stat_mean, cfg.ATD_stat_sdev)

        # Physical dexterity.
        self.DEX = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Dedication and loyalty.
        self.DCN = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Extroversion.
        self.EXT = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Fairness.
        self.FRN = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Reconciliability and forgiveness; the ability not to bear grudges or sabotage work.
        self.RCN = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Honesty.
        self.HON = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Industriousness.
        self.IND = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Ability to inspire and lead.
        self.INS = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Intelligence.
        self.INT = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Eagerness and ability to learn.
        self.LRN = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Orderliness and self-organization.
        self.ORD = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Perceptiveness.
        self.PER = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Political and diplomatic sensitivity.
        self.POL = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Positivity.
        self.POS = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Degree of risk-taking (either "boldness" or "carelessness").
        self.RSK = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Responsibility and conscientiousness.
        self.RSP = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Selflessness.
        self.SFL = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Sociality.
        self.SOC = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Speed and efficiency.
        self.SPD = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Supportiveness of others.
        self.SPT = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Physical strength.
        self.STR = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Technological aptitude.
        self.TEC = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Teaching ability.
        self.TCH = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Wisdom.
        self.WIS = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # ---------------------------------------------------------------------
        # Derived (calculated) summary capacities.
        # ---------------------------------------------------------------------

        # This is general managerial capacity (calculated as an arithmetic mean).
        self.MNGR_CAP = np.average(
            a=[
                self.ATD,
                self.IND,
                self.INS,
                self.INT,
                self.ORD,
                self.POL,
                self.POS,
                self.RSP,
                self.TCH,
                ],
            # Attendance is so crucial that below it is weighted
            # more heavily than other traits.
            weights=[
                3,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                ]
            )
        
        # This is general worker capacity (calculated as an arithmetic mean).
        self.WRKR_CAP = np.average(
            a=[
                self.ATD,
                self.DEX,
                self.IND,
                self.LRN,
                self.RSP,
                ],
            # Attendance is so crucial that below it is weighted
            # more heavily than other traits.
            weights=[
                3,
                1,
                1,
                1,
                1,
                ]
            )

        # ---------------------------------------------------------------------
        # Organizational traits and relationships.
        # ---------------------------------------------------------------------

        # Each person begins with no assigned role.
        self.role = ""

        # Each person begins with no assigned sphere.
        self.sphere = ""

        # Each person begins with no assigned shift.
        self.shift = ""

        # Each person begins with no assigned team.
        self.team = ""

        # Each person begins with no assigned supervisor.
        self.sup = ""

        # Each person begins with no assigned colleagues.
        self.colleagues = ""

        # Each person begins with no assigned subordinates.
        self.subs = ""

        # Each person begins with no assigned task.
        self.task = "none"

        # Each person begins with no current activity.
        self.curr_actvty = "none"

        # ---------------------------------------------------------------------
        # Activity data generated for the person each day the simulation is run.
        # ---------------------------------------------------------------------

        # Each person begins with default dictionary in which his actual
        # daily behaviors will be recorded.
        self.behavs_act = defaultdict(list) # <<<<<<<<<<<<<<<<<

        # The "date" list will store the date of each new day iterated in the sim.
        self.behavs_act["date"] = []

        # The "attnd_act" list will record whether a person was actually in attendance
        # on each new day iterated in the sim. It may be "present", "absent",
        # or "non-scheduled" - but not None.
        self.behavs_act["attnd_act"] = []

        # The "task" list will store the task (if any) that a person worked on
        # during each new day iterated in the sim. It may be None (e.g., if
        # a person was absent on that day).
        self.behavs_act["task"] = []

        # The "teammates" list will store the teammates (if any) that a person 
        # worked with on his task during each new day iterated in the sim. It may 
        # be None (e.g., if a person was absent on that day).
        self.behavs_act["teammates"] = []

        # The "eff_sco_act" list will record the degree of Efficacy (from 0.0-1.0)
        # with which a person actually worked on days when he was present.
        # If a person was not in attendance, the value will be None (rather than 0.0).
        self.behavs_act["eff_sco_act"] = []

        # The "good_act" list will record the number of Good actions that the
        # person performed during each day iterated in the sim. The value will be
        # None if the person was not in attendance; otherwise, it will be
        # an int ≥0.
        self.behavs_act["good_act"] = []

        # The "poor_act" list will record the number of Poor actions that the
        # person performed during each day iterated in the sim. The value will be
        # None if the person was not in attendance; otherwise, it will be
        # an int ≥0.
        self.behavs_act["poor_act"] = []

        # ---------------------------------------------------------------------
        # Personal metrics of actual behaviors during the simulated period.
        # ---------------------------------------------------------------------

        # Number of days on which a person was present during the simulated period.
        self.days_attended = ""

        # The lowest daily Efficacy generated by the person during the simulated period.
        self.eff_sco_act_min = ""

        # The highest daily Efficacy generated by the person during the simulated period.
        self.eff_sco_act_max = ""

        # The mean daily Efficacy generated by the person during the simulated period.
        self.eff_sco_act_mean = ""

        # The number of Good behaviors generated by the person during the simulated period.
        self.good_act_num = ""

        # The number of Poor behaviors generated by the person during the simulated period.
        self.poor_act_num = ""

        # ---------------------------------------------------------------------
        # Other attributes.
        # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Define print/display function.
    # This overrides the default behavior of simply
    # displaying vague object info when "print" is called.
    # ---------------------------------------------------------------------
    def __str__(self):
        return self.f_name + " " + self.l_name + " (" + str(self.per_id) + ")"


    # ---------------------------------------------------------------------
    # Define function for sending selected traits to dict for DF creation.
    # ---------------------------------------------------------------------

    # This determines which attributes will be transmitted when a special
    # dictionary is created, for conversion into an easy-to-use DF.
    def attributes_to_dict(self) -> dict:
        return {
            cfg.person_id_header_term: self.per_id,
            cfg.first_name_header_term: self.f_name,
            cfg.last_name_header_term: self.l_name,
            cfg.sex_header_term: self.sex,
            cfg.age_header_term: self.age,
            cfg.sphere_header_term: self.sphere.title,
            cfg.shift_header_term: self.shift.title,
            cfg.team_header_term: self.team.title,
            cfg.role_header_term: self.role.title,
            cfg.MNGR_CAP_header_term: self.MNGR_CAP,
            cfg.WRKR_CAP_header_term: self.WRKR_CAP,
            cfg.supervisor_header_term: self.sup,
            cfg.colleagues_header_term: self.colleagues,
            cfg.subordinates_header_term: self.subs,
            "Days attended": self.days_attended,
            "Min Eff": self.eff_sco_act_min,
            "Max Eff": self.eff_sco_act_max,
            "Mean Eff": self.eff_sco_act_mean,
            "Num Goods": self.good_act_num,
            "Num Poors": self.poor_act_num,
            #"AMB": self.AMB,
            "ATD": self.ATD,
            #"DEX": self.DEX,
            #"DCN": self.DCN,
            #"EXT": self.EXT,
            #"FRN": self.FRN,
            #"RCN": self.RCN,
            #"HON": self.HON,
            #"IND": self.IND,
            #"INS": self.INS,
            #"INT": self.INT,
            #"LRN": self.LRN,
            #"ORD": self.ORD,
            #"PER": self.PER,
            #"POL": self.POL,
            #"POS": self.POS,
            #"RSK": self.RSK,
            #"RSP": self.RSP,
            #"SFL": self.SFL,
            #"SOC": self.SOC,
            #"SPD": self.SPD,
            #"SPT": self.SPT,
            #"STR": self.STR,
            "TEC": self.TEC,
            #"TCH": self.TCH,
            #"WIS": self.WIS,
            }
    
# ----------------------------------------------------------------------
# DEFINE THE STAT-GENERATOR FUNCTION
#
# This defines a personal stat that by default uses the arguments
# for the mean and standard deviation for the stat that are
# specified below; these can be overridden by manually adding
# arguments when the function is called.
# ----------------------------------------------------------------------
def generate_personal_stat(mean_u, sd_u):
    
    # Here "loc" is the mean, "scale" is SD,
    # and "size" is the number of numbers to generate.
    randomized_base_for_stat = round( float( np.random.normal(loc=mean_u, scale=sd_u, size=1) ) , 3)
    
    # It's possible for the number generated above to be <0 or >1;
    # below we manually set 0 and 1 as the min and max.   
    adjusted_stat = randomized_base_for_stat
    
    if randomized_base_for_stat < 0:
        adjusted_stat = 0.0
    elif randomized_base_for_stat > 1:
        adjusted_stat = 1.0
    
    return adjusted_stat

# ----------------------------------------------------------------------
# FUNCTION TO CREATE INITIAL POPULATION OF PERSONS
# (who will not yet have their final roles or tasks assigned)
#
# Create the dictionary of persons, in which each entry (person)
# is a separate person object of the Person class.
# ----------------------------------------------------------------------
def create_initial_population_of_persons():
    cfg.persons = defaultdict(list)

    # Populate the community.
    for i in range(0, cfg.size_of_comm_initial):
        cfg.persons[i] = Person_class()
        # print(cfg.persons[i])


# ----------------------------------------------------------------------
# FUNC TO RETURN A DF WITH SELECTED ATTRIBUTES FOR ALL PERSONS
#
# The particular personal attributes that are transmitted into this DF
# are defined in the Person class's "attributes_to_dict()" func.
# ----------------------------------------------------------------------
def create_df_with_selected_attributes_of_all_persons():
    persons_dict_for_df = [cfg.persons[k].attributes_to_dict() for k in cfg.persons]
    cfg.persons_df = pd.DataFrame(persons_dict_for_df)
    return cfg.persons_df


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define the "Role" class and related functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE THE "ROLE" CLASS
# ----------------------------------------------------------------------
class Role_class:

    # ---------------------------------------------------------------------
    # Define initialization function.
    # ---------------------------------------------------------------------
    def __init__(self):
        self.title = "unspecified"

    # ---------------------------------------------------------------------
    # Define print/display function.
    # This overrides the default behavior of simply
    # displaying vague object info when "print" is called.
    # ---------------------------------------------------------------------
    def __str__(self):
        return self.title

    
# ----------------------------------------------------------------------
# FUNCTION TO CREATE INITIAL SET OF POTENTIAL ROLES
#
# Create the dictionary of roles, in which each entry (role)
# is a separate role object of the Role class.
# ----------------------------------------------------------------------
def create_all_possible_roles():

    cfg.roles = defaultdict(list)

    # Populate the potential roles.
    # Create one role object corresponding to each
    # of the items in the available_role_titles list.
    for i in range(len(cfg.available_role_titles)):
        cfg.roles[i] = Role_class()
        cfg.roles[i].title = cfg.available_role_titles[i]


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO ASSIGN A ROLE TO EACH MEMBER OF THE COMMUNITY
# ----------------------------------------------------------------------
def assign_initial_role_to_each_person():
    
    # ---------------------------------------------------------------------
    # Assign the "Production Director" role to the 1 person
    # with the highest managerial capacity score.
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

    # Identify the index of the person on the first row of the DF.
    person_index = persons_df_sorted.index[0]
    
    # Get the (first) role object with title "Production Director", and
    # assign it to the relevant person as his cfg.persons[x].role.
    cfg.persons[person_index].role = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title == cfg.production_director_term) ]
    
    # ---------------------------------------------------------------------
    # Assign the "Shift Manager" role to the 3 persons
    # with the next highest managerial capacity scores.
    # ---------------------------------------------------------------------

    # Identify the indices of the next three persons in the DF, then
    # get the (first) role object with title "Shift Manager", and
    # assign it to the relevant persons as their cfg.persons[x].role.
    for i in range(1, 1+3):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].role = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title == cfg.shift_manager_term) ]

    # ---------------------------------------------------------------------
    # Assign the "Team Leader" roles to the first N persons (in the
    # original, random -- unsorted -- persons dict, not the sorted DF)
    # who don't yet have a role (i.e., who aren't a "Production Director"
    # or "Shift Manager").
    # ---------------------------------------------------------------------
    
    # Multiply the num_of_teams_per_shift * 3, since there are three shifts.
    num_of_remaining_team_leaders_to_be_designated = cfg.num_of_teams_per_shift * 3
    for i in cfg.persons:
        if num_of_remaining_team_leaders_to_be_designated > 0:
            if cfg.persons[i].role == "":
                cfg.persons[i].role = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title == cfg.team_leader_term) ]
                num_of_remaining_team_leaders_to_be_designated -= 1

    # ---------------------------------------------------------------------
    # Assign the "Laborer" role to all persons
    # who don't yet have a role.
    # ---------------------------------------------------------------------

    # Get the (first) role object with title "Laborer", and
    # assign it to the relevant person as his cfg.persons[x].role.
    for i in cfg.persons:
        if cfg.persons[i].role == "":
            cfg.persons[i].role = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title == cfg.laborer_term) ]

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define the "Shift" class and related functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE THE "SHIFT" CLASS
# ----------------------------------------------------------------------
class Shift_class:

    # ---------------------------------------------------------------------
    # Define initialization function.
    # ---------------------------------------------------------------------
    def __init__(self):

        self.title = "unspecified"

    # ---------------------------------------------------------------------
    # Define print/display function.
    # This overrides the default behavior of simply
    # displaying vague object info when "print" is called.
    # ---------------------------------------------------------------------
    def __str__(self):
        return self.title


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO CREATE INITIAL SET OF SHIFTS
#
# Create the dictionary of shifts, in which each entry (shift)
# is a separate shift object of the Shift class.
# ----------------------------------------------------------------------
def create_shift_objects():

    cfg.shifts = defaultdict(list)

    # Populate the shifts dict.
    # Create one shift object corresponding to each
    # of the items in the available_shifts list.
    for i in range(len(cfg.available_shift_titles)):
        cfg.shifts[i] = Shift_class()
        cfg.shifts[i].title = cfg.available_shift_titles[i]


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO ASSIGN A SHIFT TO EACH MEMBER OF THE COMMUNITY
# ----------------------------------------------------------------------

def assign_initial_shift_to_each_person():

    # ---------------------------------------------------------------------
    # Assign the shift "unassigned" to the "Production director" and 
    # Shifts 1-3 to the three "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    # The first entries will be the "Production Director" and "Shift Managers".
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].shift = cfg.shifts[ next(x for x in cfg.shifts if cfg.shifts[x].title == cfg.available_shift_titles[i]) ]

    # ---------------------------------------------------------------------
    # Step through all "Team Leaders" and, for those who don't yet have a shift
    # assigned, assign them to Shifts 1-3. It's important to use the
    # unordered "cfg.persons" dictionary rather than the DF sorted by capacity.
    # ---------------------------------------------------------------------
    
    # This list tracks how many Team Leaders still need to be assigned
    # for each of the three "regular" shifts.
    # It includes an initial 0 to represent the special "unassigned" shift, 
    # which doesn't need any additional members to be assigned to it.
    num_of_leaders_to_assign_per_shift = [0, cfg.num_of_teams_per_shift, cfg.num_of_teams_per_shift, cfg.num_of_teams_per_shift]

    # Start with cfg.shifts[1], which is "Shift 1".
    for s in range( 1, (len(cfg.shifts)) ):
        for i in cfg.persons:
            if num_of_leaders_to_assign_per_shift[s] > 0:
                if cfg.persons[i].shift == "":
                    
                    cfg.persons[i].shift = cfg.shifts[s]
                    num_of_leaders_to_assign_per_shift[s] -= 1


    # ---------------------------------------------------------------------
    # Step through all "Laborers" and, for those who don't yet have a shift
    # assigned, assign them to Shifts 1-3. It's important to use the
    # unordered "cfg.persons" dictionary rather than the DF sorted by capacity.
    # ---------------------------------------------------------------------
    
    # Calculate the number of Laborers proper (not persons more generally)
    # who should be a part of each shift.
    # Subtract 4 from the size of the community, since the Production Director
    # and Shift Managers have already been assigned to shifts.
    # Divide by 3, which is the number of shifts.
    # Subtract 8 (for the number of teams, and thus Team Leaders, in the shift),
    # since each shift has already received a Team Leader who's not an ordinary Laborer.
    cfg.num_of_laborers_per_shift = ( (cfg.size_of_comm_initial - 4) / 3 ) - cfg.num_of_teams_per_shift

    # This list tracks how many Laborers still need to be assigned
    # for each of the three "regular" shifts.
    # It includes an initial 0 to represent the special "unassigned" shift, which
    # doesn't need any additional members to be assigned to it.
    num_of_laborers_to_assign_per_shift = [0, cfg.num_of_laborers_per_shift, cfg.num_of_laborers_per_shift, cfg.num_of_laborers_per_shift]

    # Start with cfg.shifts[1], which is "Shift 1".
    for s in range( 1, (len(cfg.shifts)) ):
        for i in cfg.persons:
            if num_of_laborers_to_assign_per_shift[s] > 0:
                if cfg.persons[i].shift == "":
                    cfg.persons[i].shift = cfg.shifts[s]
                    num_of_laborers_to_assign_per_shift[s] -= 1


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define the "Team" class and related functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE THE "TEAM" CLASS
# The "num_of_teams_per_shift" variable has already been given
# a value, as part of the workforce setup.
# ----------------------------------------------------------------------
class Team_class:

    # ---------------------------------------------------------------------
    # Define initialization function.
    # ---------------------------------------------------------------------
    def __init__(self):

        self.title = "unspecified"
        self.shift = ""

    # ---------------------------------------------------------------------
    # Define print/display function.
    # This overrides the default behavior of simply
    # displaying vague object info when "print" is called.
    # ---------------------------------------------------------------------
    def __str__(self):
        return self.title


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO CREATE INITIAL SET OF TEAMS
# Create the dictionary of teams, in which each entry (team)
# is a separate team object in the Team class.
# ----------------------------------------------------------------------
def create_team_objects():

    cfg.teams = defaultdict(list)

    # Populate the teams dict.
    # Create one teams object corresponding to each
    # number in len(cfg.num_of_teams_per_shift).

    # The first team will be the "unassigned" team object.
    cfg.teams[0] = Team_class()
    cfg.teams[0].title = "unassigned"
    
    # Now we create all of the remaining, "regular" teams.
    # Here we add 1, since entry 0 is the special case just defined above.
    # We multiply by 3, since there are three shifts.
    for i in range(1, cfg.num_of_teams_per_shift * 3 + 1):
        cfg.teams[i] = Team_class()
        cfg.teams[i].title = "Team " + str(i)
        
    # Indicate the shift that each team belongs to.
    for i in range(0, cfg.num_of_teams_per_shift + 1):
        cfg.teams[i].shift = cfg.shift_1_term
    for i in range(cfg.num_of_teams_per_shift + 1, cfg.num_of_teams_per_shift * 2 + 1):
        cfg.teams[i].shift = cfg.shift_2_term
    for i in range(cfg.num_of_teams_per_shift * 2 + 1, cfg.num_of_teams_per_shift * 3 + 1):
        cfg.teams[i].shift = cfg.shift_3_term


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO ASSIGN A TEAM TO EACH MEMBER OF THE COMMUNITY
# ----------------------------------------------------------------------
def assign_initial_team_to_each_person():
    
    # ---------------------------------------------------------------------
    # Assign the team "unassigned" to the "Production Director" and 
    # "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

    # The first entries will be the "Production Director" and "Shift Managers".
    # They all have the "unassigned" team.
    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].team = cfg.teams[ next(x for x in cfg.teams if cfg.teams[x].title == "unassigned") ]

    # ---------------------------------------------------------------------
    # Set up a means of tracking which teams still need to have a leader
    # or ordinary laborers assigned to them.
    # ---------------------------------------------------------------------

    # >>>>> This list tracks how many Laborers proper still need to be assigned
    # >>>>> to each team. Each team begins by needing a full complement of Laborers.

    # Calculate the total number of "Laborers" proper (and not persons more generally)
    # who should be part of each team.
    # Subtract 4 from the size of the community, since the Production Director
    # and Shift Managers have already been assigned to teams.
    # Subtract the number of teams per shift *3, since each team will also include
    # one leader who isn't an ordinary laborer, and there are three shifts.
    # Divide by 3, because there are three shifts.
    cfg.num_of_laborers_per_team = (cfg.size_of_comm_initial - 4 - (cfg.num_of_teams_per_shift)*3 ) \
        / (cfg.num_of_teams_per_shift) / 3

    # We begin with a list entry for the special "unassigned" team,
    # which doesn't need any laborers to be added.
    num_of_laborers_needed = [0]
    for i in range(cfg.num_of_teams_per_shift * 3):
        num_of_laborers_needed.append(cfg.num_of_laborers_per_team)
    
    # >>>>> This list tracks how many Team Leaders still need to be assigned
    # >>>>> to each team. Each team begins by needing 1 Team Leader.

    # We begin with a list entry for the special "unassigned" team,
    # which doesn't need any Team leaders to be added.
    cfg.num_of_leaders_needed = [0]
    for i in range(cfg.num_of_teams_per_shift * 3):
        cfg.num_of_leaders_needed.append(1)

    # ---------------------------------------------------------------------
    #Step through all persons (first Team Leaders, then Laborers) and, 
    #for those who don't yet have a team assigned, assign them to the 
    #first team that still needs persons of the relevant sort to be added. 
    #    
    #It's important to use the unordered "cfg.persons" dictionary 
    #rather than the DF sorted by capacity.
    # ---------------------------------------------------------------------

    # For simplicity's sake, I can begin with cfg.teams[0], which is the special 
    # "unassigned" team. It won't actually receive any new members, though, as I've 
    # already specified above that it doesn't need any more Team leaders added to it.
    for t in range (0, len(cfg.teams) ):

        # Handle each shift in turn, beginning with cfg.shifts[1] (not cfg.shifts[0],
        # which is the "unassigned" shift).
        for s in range (1, len(cfg.shifts) ):

            # For each team in the given shift...
            if cfg.teams[t].shift == cfg.shifts[s].title:

                # Iterate through all persons to deal with all Team Leaders...
                for p in cfg.persons:

                    # If the team doesn't yet have a Leader, and the current person
                    # is a Leader, assign him to the given team.
                    if cfg.num_of_leaders_needed[t] > 0:

                        if (cfg.persons[p].shift.title == cfg.shifts[s].title) \
                        and (cfg.persons[p].role.title == cfg.team_leader_term) \
                        and (cfg.persons[p].team == ""):

                            cfg.persons[p].team = cfg.teams[t]

                            # NOTE! The code below isn't working yet.
                            cfg.persons[p].sphere = str(t)
                            
                            cfg.num_of_leaders_needed[t] -= 1

                # Iterate through all persons to deal with all Laborers...
                for p in cfg.persons:

                    # If the team doesn't yet have all its Laborers, and the
                    # current person is a Laborer, assign him to the given team.
                    if num_of_laborers_needed[t] > 0:

                        if (cfg.persons[p].shift.title == cfg.shifts[s].title) \
                        and (cfg.persons[p].role.title == cfg.laborer_term) \
                        and (cfg.persons[p].team == ""):

                            cfg.persons[p].team = cfg.teams[t]
                            
                            # NOTE! The code below isn't working yet.
                            cfg.persons[p].sphere = str(t)
                            
                            num_of_laborers_needed[t] -= 1

                            
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Define the "Sphere" class and related functions
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# DEFINE THE "SPHERE" CLASS
# ----------------------------------------------------------------------
class Sphere_class:

    # ---------------------------------------------------------------------
    # Define initialization function.
    # ---------------------------------------------------------------------
    def __init__(self):

        self.title = "unspecified"

    # ---------------------------------------------------------------------
    # Define print/display function.
    # ---------------------------------------------------------------------
    # This overrides the default behavior of simply
    # displaying vague object info when "print" is called.
    def __str__(self):
        return self.title

    
# ----------------------------------------------------------------------
# DEFINE FUNCTION TO CREATE INITIAL SET OF ALL POSSIBLE SPHERES
# Create the dictionary of spheres, in which each entry (sphere)
# is a separate sphere object in the Sphere class.
# ----------------------------------------------------------------------
def create_all_possible_spheres():

    cfg.spheres = defaultdict(list)

    # Populate the spheres.
    # Create one sphere object corresponding to each
    # of the items in the available_sphere_titles list.
    for i in range(len(cfg.available_sphere_titles)):
        cfg.spheres[i] = Sphere_class()
        cfg.spheres[i].title = cfg.available_sphere_titles[i]


# ----------------------------------------------------------------------
# DEFINE FUNCTION TO ASSIGN A SPHERE TO EACH PERSON
# ----------------------------------------------------------------------

def assign_initial_sphere_to_each_person():

    # ---------------------------------------------------------------------
    # Assign the sphere "general management" to the "Production Director" and 
    # "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

    # The first entries will be the "Production Director" and "Shift Managers".
    # They all have the "unassigned" team.
    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].sphere = cfg.spheres[ next(x for x in cfg.spheres if cfg.spheres[x].title == "general management") ]

    # ---------------------------------------------------------------------
    # Assign a sphere to all remaining persons who don't yet have one.
    # ---------------------------------------------------------------------

    # Rather than directly calculating which sphere a given person works in,
    # it's easier to instead calculate which sphere a particular *team* is
    # focused on, and to then assign the given sphere to all members of that team.
    #
    # Here we first determine which sphere applies to each of the workforce's teams.

    # The first team is ascribed to sphere 0, the "unassigned" sphere.
    cfg.sphere_of_given_team = [0]
    
    # For each of the teams (after team 0), we calculate which sphere it has by
    # iterating through the list of spheres and adding each to the sphere_of_given_team
    # list for however many teams are supposed to have that sphere in each shift
    # (as specified in teams_per_sphere_per_shift above).
    #
    # That process is then repeated for shifts 2 and 3.
    for s in range(0, 3):
        for sp in range( len(cfg.spheres) ):
            cfg.sphere_of_given_team.extend( [sp] * cfg.teams_per_sphere_per_shift[sp] )

    # Here I can begin with t=1, as t=0 is a special case ("general management")
    # that has already been handled above.
    for t in range (1, len(cfg.teams) ):
        
        # Handle each shift in turn, beginning with cfg.shifts[1] (not cfg.shifts[0],
        # which is the "unassigned" shift).
        for s in range (1, len(cfg.shifts) ):

            # For each team in the given shift...
            if cfg.teams[t].shift == cfg.shifts[s].title:

                # Iterate through all persons. This catches both Team Leaders
                # and regular Laborers.
                for p in cfg.persons:

                    if (cfg.persons[p].shift.title == cfg.shifts[s].title) \
                        and (cfg.persons[p].team.title == cfg.teams[t].title):

                            # NOTE! The code below isn't working yet.
                            cfg.persons[p].sphere = cfg.spheres[ cfg.sphere_of_given_team[t] ]


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions for populating persons' "supervisor", "subordinate",
# ▒▒ and "colleague" attributes
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# FUNCTION TO POPULATE INITIAL "SUPERVISOR" ATTRIBUTE FOR ALL PERSONS
# ----------------------------------------------------------------------
def assign_initial_supervisor_to_each_person():

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify supervisor for Production Director.
        # ---------------------------------------------------------------------
        if cfg.persons[i].role.title == cfg.production_director_term:
            cfg.persons[i].sup = None

        # ---------------------------------------------------------------------
        # Specify supervisor for Shift Managers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.shift_manager_term:

            # Attach the person object for the Production Manager.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if cfg.persons[x].role.title == cfg.production_director_term) ]

        # ---------------------------------------------------------------------
        # Specify supervisor for Team Leaders.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.team_leader_term:

            # Attach the person object for the Shift Manager of the laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if ( 
                (cfg.persons[x].role.title == cfg.shift_manager_term) \
                and (cfg.persons[x].shift == cfg.persons[i].shift)
                ) ) ]

        # ---------------------------------------------------------------------
        # Specify supervisor for laborers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.laborer_term:

            # Attach the person object for the Team Leader of the Laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.team_leader_term) \
                and (cfg.persons[x].team == cfg.persons[i].team)
                ) ) ]

# ----------------------------------------------------------------------
# FUNCTION TO POPULATE INITIAL "SUBORDINATES" ATTRIBUTE FOR ALL PERSONS
# ----------------------------------------------------------------------
def assign_initial_subordinates_to_all_supervisors():

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify subordinates for Production Director.
        # ---------------------------------------------------------------------
        if cfg.persons[i].role.title == cfg.production_director_term:
            subs_temp_list = []
            subs_temp_list.append( [cfg.persons[x] for x in cfg.persons if cfg.persons[x].role.title == cfg.shift_manager_term] )

            # The line below converts the nested list into a simple one-level list.
            subs_temp_list = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # ---------------------------------------------------------------------
        # Specify subordinates for Shift Managers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.shift_manager_term:
            subs_temp_list = []
            subs_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.team_leader_term) \
                and (cfg.persons[x].shift.title == cfg.persons[i].shift.title)
                )])

            # The line below converts the nested list into a simple one-level list.
            subs_temp_list = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # ---------------------------------------------------------------------
        # Specify subordinates for Team Leaders.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.team_leader_term:
            subs_temp_list = []
            subs_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.laborer_term) \
                and (cfg.persons[x].team.title == cfg.persons[i].team.title)
                )])

            #The line below converts the nested list into a simple one-level list.
            subs_temp_list = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # ---------------------------------------------------------------------
        # Specify subordinates for Laborers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.laborer_term:
            cfg.persons[i].subs = None


# ----------------------------------------------------------------------
# FUNCTION TO POPULATE INITIAL "COLLEAGUES" ATTRIBUTE FOR ALL PERSONS
# ----------------------------------------------------------------------

# A person's "colleagues" includes those Laborers at the same level (i.e.,
# in the same role) who are in the same relevant organizational unit as
# the person.
#
# For ordinary Laborers, collagues are the other ordinary Laborers in the
# same team (but *not* the Team Leader).
#
# For Team Leaders, collagues are the other Team Leaders in the
# same shift (but *not* the Shift Manager).
#
# For Shift Managers, collagues are the other Shift Managers.
#
# For the Production Manager, colleagues = None

def assign_initial_colleagues_to_all_persons():

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify colleagues for Production Director.
        # ---------------------------------------------------------------------
        if cfg.persons[i].role.title == cfg.production_director_term:
            cfg.persons[i].colleagues = None

        # ---------------------------------------------------------------------
        # Specify colleagues for Shift Managers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.shift_manager_term:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.shift_manager_term) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id)
                )])

            # The line below converts the nested list into a simple one-level list.
            colleagues_temp_list = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list

        # ---------------------------------------------------------------------
        # Specify colleagues for Team Leaders.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.team_leader_term:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.team_leader_term) \
                and (cfg.persons[x].shift.title == cfg.persons[i].shift.title) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id)
                )])

            # The line below converts the nested list into a simple one-level list.
            colleagues_temp_list = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list

        # ---------------------------------------------------------------------
        # Specify colleagues for Laborers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.laborer_term:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.laborer_term) \
                and (cfg.persons[x].team.title == cfg.persons[i].team.title) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id)
                )])

            # The line below converts the nested list into a simple one-level list.
            colleagues_temp_list = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions for iterating the simulation through one day
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# FUNCTION TO ADVANCE DATE BY ONE DAY
# ----------------------------------------------------------------------
def advance_date_by_one_day():

    from datetime import timedelta
    
    cfg.current_datetime_obj += timedelta(days = 1)
    cfg.day_of_sim_iter += 1

    # print(cfg.current_datetime_obj.date() )


# ----------------------------------------------------------------------
# FUNCTION TO SIMULATE ONE DAY'S WORTH 
# OF PERSONS' BEHAVIORS AND OBSERVATIONS
# ----------------------------------------------------------------------
def simulate_one_day_of_activities():

    for p in cfg.persons:

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" the date of this new day.
        # ---------------------------------------------------------------------
        cfg.persons[p].behavs_act["date"].append( cfg.current_datetime_obj.date() )

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his calculated attendance status.
        # ---------------------------------------------------------------------

        # If a weighted average of a person's ATD, DCN, and RSP scores is GREATER
        # THAN or equal to a random number from to 0.0-1.00, the person is present.
        if ( ( cfg.persons[p].ATD*0.8 + cfg.persons[p].DCN*0.1 + cfg.persons[p].RSP*0.1 ) >= random.uniform(0.0, 1.0) ):
            attendance_today = "present"
        else:
            attendance_today = "absent"

        cfg.persons[p].behavs_act["attnd_act"].append(attendance_today)

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his calculated task.
        # ---------------------------------------------------------------------
        cfg.persons[p].behavs_act["task"].append(None)

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his calculated teammates.
        # ---------------------------------------------------------------------
        cfg.persons[p].behavs_act["teammates"].append(None)

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his Efficacy score for the day.
        # ---------------------------------------------------------------------

        # A person's Efficacy score for the day is equal to a weighted average
        # of his IND, SPD, and TEC scores, adjusted by a pos or neg random number
        # generated with a specified mean ("loc") and SD ("scale").
        
        if attendance_today == "absent":
            eff_sco_today = None
        else:
            eff_sco_today = round( float( ( cfg.persons[4].IND*0.8 + cfg.persons[4].SPD*0.1 + cfg.persons[4].RSP*0.1 ) \
                + np.random.normal(loc=0, scale=0.15, size=1) ), 3 )
            if eff_sco_today < 0:
                eff_sco_today = 0

        cfg.persons[p].behavs_act["eff_sco_act"].append(eff_sco_today)

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his calculated number
        # of actual Good behaviors.
        # ---------------------------------------------------------------------

        if attendance_today == "absent":
            good_today = None
        else:
            # If the average of a person's DCN, SFL, and SPT stats is greater
            # than or equal to some threshold value plus a random number, the person 
            # generates 1 Good action.
            if ( ( cfg.persons[p].INS/6.0 + cfg.persons[p].POS/6.0 + cfg.persons[p].RCN/6.0 + cfg.persons[p].RSP/6.0 + cfg.persons[p].SPT/6.0 + cfg.persons[p].TCH/6.0 ) \
                    >= (0.2 + random.uniform(0.0, 0.8)) ):
                good_today = 1
            else:
                good_today = 0
                
        cfg.persons[p].behavs_act["good_act"].append(good_today)

        # ---------------------------------------------------------------------
        # Append to the person's "behavs_act" his calculated number
        # of actual Poor behaviors.
        # ---------------------------------------------------------------------

        if attendance_today == "absent":
            poor_today = None
        else:
            # If the average of a person's HON, ORD, and SPT stats is less than
            # than or equal to some threshold value plus a random number, the person 
            # generates 1 Poor action.
            if ( ( cfg.persons[p].DEX/6.0 + cfg.persons[p].IND/6.0 + cfg.persons[p].ORD/6.0 + cfg.persons[p].POS/6.0 + cfg.persons[p].RSP/6.0 + cfg.persons[p].SPT/6.0 ) \
                    <= (0.2 + random.uniform(0.0, 0.8)) ):
                poor_today = 1
            else:
                poor_today = 0
                
        cfg.persons[p].behavs_act["poor_act"].append(poor_today)


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions for calculating metrics after the simulation's conclusion
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

# ----------------------------------------------------------------------
# FUNCTION TO CALCULATE MIN, MAX, AND MEAN EFFICACY SCORES 
# FOR EACH PERSON DURING THE SIMULATED PERIOD
# ----------------------------------------------------------------------
def calculate_metrics_for_persons_in_simulated_period():

    for p in cfg.persons:

        days_present = ( cfg.persons[p].behavs_act["attnd_act"] ).count("present")
        
        # I need to manually exclude "None" entries from the list, in order for "min" to work.
        # "default = None" is to avoid errors in the case of an empty list.
        min_eff_sco = min( (e for e in (cfg.persons[p].behavs_act["eff_sco_act"]) if e is not None), default=None )

        # I need to manually exclude "None" entries from the list, in order for "max" to work.
        max_eff_sco = max( (e for e in (cfg.persons[p].behavs_act["eff_sco_act"]) if e is not None), default=None )

        # I need to manually exclude "None" entries from the list, in order for "mean" to work.
        # Unlike "min" and "max" internal list brackets need to be added here, to get np.mean to work without error.
        # It still generates a warning ("Mean of empty slice"), which I simply suppress,
        # and, in the case of an empty list, generates NaN as the result.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mean_eff_sco = round( np.mean([ e for e in (cfg.persons[p].behavs_act["eff_sco_act"]) if e is not None ]), 3)

        good_count = sum( g for g in cfg.persons[p].behavs_act["good_act"] if g is not None )
        poor_count = sum( poor for poor in cfg.persons[p].behavs_act["poor_act"] if poor is not None )

        # print("person", str(p), min_eff_sco, mean_eff_sco, max_eff_sco)

        cfg.persons[p].days_attended = days_present
        cfg.persons[p].eff_sco_act_min = min_eff_sco
        cfg.persons[p].eff_sco_act_max = max_eff_sco
        cfg.persons[p].eff_sco_act_mean = mean_eff_sco
        cfg.persons[p].good_act_num = good_count
        cfg.persons[p].poor_act_num = poor_count
    

# ----------------------------------------------------------------------
# DEFINE FUNC TO IMPLEMENT DEPENDENCIES AND COVARIANCE AMONG CERTAIN
# PERSONAL STATS BY ADJUSTING THEIR PREVIOUSLY RANDOM VALUES
# ----------------------------------------------------------------------
def adjust_personal_stats_to_implement_dependencies_and_covariance(
    # technological aptitude += (age * this factor)
    infl_year_of_age_on_TEC, #infl_year_of_AGE_on_TEC
    ):

    for p in cfg.persons:

        #Each person's random technical aptitude (self.TEC) is adjusted
        #by some amount for each year of age (self.age).
        cfg.persons[p].TEC = cfg.persons[p].TEC - (cfg.persons[p].age * infl_year_of_age_on_TEC)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░ Functions for generating PNG plots as variables stored in memory 
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_distribution_of_WRKR_CAP_scores_hist():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)
    # fig.patch.set_visible(False) #This "turns off" the frame, leaving only the axis visible.

    plt.hist(cfg.persons_df["WRKR_CAP"], bins=100, color=cfg.plot_hist_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of persons\n in given WRKR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Distribution of values of persons'\n worker capacity (WRKR_CAP) score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_distribution_of_WRKR_CAP_scores_hist = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_distribution_of_WRKR_CAP_scores_hist.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_distribution_of_WRKR_CAP_scores_hist


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_distribution_of_MNGR_CAP_scores_hist():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.hist(cfg.persons_df["MNGR_CAP"], bins=100, color=cfg.plot_hist_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('MNGR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of persons\n in given MNGR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Distribution of values of persons'\n managerial capacity (MNGR_CAP) score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_distribution_of_MNGR_CAP_scores_hist = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_distribution_of_MNGR_CAP_scores_hist.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_distribution_of_MNGR_CAP_scores_hist
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def MNGR_CAP_vs_WRKR_CAP_scores_scatter():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('1.0')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.scatter(cfg.persons_df["WRKR_CAP"], cfg.persons_df["MNGR_CAP"], alpha=0.4, color=cfg.plot_scatter_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('MNGR_Cap score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of each person’s\n WRKR_CAP and MNGR_CAP scores", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_MNGR_CAP_by_age_scatter():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.scatter(cfg.persons_df["Age"], cfg.persons_df["MNGR_CAP"], alpha=0.4, color=cfg.plot_scatter_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Age', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('MNGR_Cap score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of each person’s age\n and MNGR_CAP score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_by_age_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_by_age_scatter.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_MNGR_CAP_by_age_scatter
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_WRKR_CAP_by_shift_bar():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.bar(cfg.persons_df["Shift"], cfg.persons_df["WRKR_CAP"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Shift', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n WRKR_CAP scores by shift", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_by_shift_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_by_shift_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_WRKR_CAP_by_shift_bar
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_MNGR_CAP_by_role_bar():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.bar(cfg.persons_df["Role"], cfg.persons_df["MNGR_CAP"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Organizational role', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average MNGR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(rotation=90, fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n MNGR_CAP scores by role filled", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_by_role_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_by_role_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_MNGR_CAP_by_role_bar
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_WRKR_CAP_by_team_bar():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('auto')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.bar(cfg.persons_df["Team"], cfg.persons_df["WRKR_CAP"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Team', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(rotation=90, fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n WRKR_CAP scores by team", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_by_team_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_by_team_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_WRKR_CAP_by_team_bar
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_WRKR_CAP_vs_mean_Eff_scatter():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('1.0')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.scatter(cfg.persons_df["WRKR_CAP"], cfg.persons_df["Mean Eff"], alpha=0.4, color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Mean Efficacy during simulated period', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of persons’\n WRKR_CAP scores and mean daily Efficacy", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_vs_mean_Eff_scatter.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def plot_num_Good_vs_Poor_actions_by_person_hist2d():

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi
    plt.gca().set_aspect('1.0')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    plt.hist2d(cfg.persons_df["Num Goods"], cfg.persons_df["Num Poors"], bins=20)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Number of Good workplace actions per person', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of Poor workplace actions per person', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Number of persons’ Good and Poor\n workplace actions performed", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    plt.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_num_Good_vs_Poor_actions_by_person_hist2d.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d


# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▒▒ Functions for running the simulation
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

def run_core_simulation():
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # CHECK WHETHER USER HAS SUPPLIED VALUES FOR CERTAIN VARIABLES
    # VIA A WRAPPER GUI (E.G., TKINTER OR KIVY)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    try: 
        cfg.min_person_age_input
        cfg.min_person_age = cfg.min_person_age_input
    except:
        cfg.min_person_age = 20
        
    try: 
        cfg.max_person_age_input
        cfg.max_person_age = cfg.max_person_age_input
    except:
        cfg.max_person_age = 65

    try: 
        cfg.num_persons_input
        num_persons_rounded_int = int( cfg.num_persons_input / 24) * 24 + 4
        cfg.size_of_comm_initial = num_persons_rounded_int
    except:
        cfg.size_of_comm_initial = 724

    try: 
        cfg.ATD_stat_mean_input
        cfg.ATD_stat_mean = cfg.ATD_stat_mean_input
    except:
        cfg.ATD_stat_mean = 0.91

    try: 
        cfg.ATD_stat_sdev_input
        cfg.ATD_stat_sdev = cfg.ATD_stat_sdev_input
    except:
        cfg.ATD_stat_sdev = 0.09

    try: 
        cfg.other_stats_stat_mean_input
        cfg.other_stats_stat_mean = cfg.other_stats_stat_mean_input
    except:
        cfg.other_stats_stat_mean = 0.73

    try: 
        cfg.other_stats_stat_sdev_input
        cfg.other_stats_stat_sdev = cfg.other_stats_stat_sdev_input
    except:
        cfg.other_stats_stat_sdev = 0.17

    try: 
        cfg.random_seed_A_input
        cfg.random_seed_A = cfg.random_seed_A_input
    except:
        cfg.random_seed_A = 11

    try: 
        cfg.random_seed_B_input
        cfg.random_seed_B = cfg.random_seed_B_input
    except:
        cfg.random_seed_B = 22

    try: 
        cfg.random_seed_C_input
        cfg.random_seed_C = cfg.random_seed_C_input
    except:
        cfg.random_seed_C = 33

    try: 
        cfg.random_seed_D_input
        cfg.random_seed_D = cfg.random_seed_D_input
    except:
        cfg.random_seed_D = 44

    try: 
        cfg.num_days_to_simulate_input
        cfg.num_of_days_to_simulate = cfg.num_days_to_simulate_input
    except:
        cfg.num_of_days_to_simulate = 30

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # SET VALUES OF WORKFORCE CONFIGURATION VARIABLES
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    sim_starting_date = "2021-12-13"

    cfg.current_datetime_obj = datetime.strptime(sim_starting_date, '%Y-%m-%d')
    cfg.day_of_sim_iter = 0

    cfg.emp_id_starting_value = 10001

    # ---------------------------------------------------------------------
    #Set the initial size of the community.
    # ---------------------------------------------------------------------

    # Viable numbers are:
    # cfg.size_of_comm_initial = n*24 + 4
    # cfg.num_of_teams_per_shift = 8

    cfg.num_of_teams_per_shift = 8

    # cfg.size_of_comm_initial = 100
    # cfg.num_of_teams_per_shift = 8

    # cfg.size_of_comm_initial = 724
    # cfg.num_of_teams_per_shift = 8

    # cfg.size_of_comm_initial = 964
    # cfg.num_of_teams_per_shift = 8

    # cfg.size_of_comm_initial = 4996
    # cfg.num_of_teams_per_shift = 8

    # ---------------------------------------------------------------------
    # Specify values of variables relating to plotting of results.
    # ---------------------------------------------------------------------

    plt.rcParams['figure.dpi'] = 200
    cfg.plot_figure_dpi = 200

    plt.rcParams['savefig.dpi'] = 200
    cfg.plot_savefig_dpi = 200

    # By setting the x-val for plot_figsize = 
    # width_of_content_in_main_tkinter_window / plot_figure_dpi (or plot_savefig_dpi),
    # it makes each plot exactly fill the available horizontal space, and thus
    # eliminates the need to try to center plots horizontally (which is difficult).
    #
    # cfg.plot_figsize = (4, 3)
    cfg.plot_figsize = (cfg.width_of_content_in_main_tkinter_window / cfg.plot_figure_dpi, 3)
    cfg.plot_xy_label_fontsize = 7
    cfg.plot_xy_label_color = "#9ea3ff" #lavendar
    cfg.plot_xy_label_pad = 4
    cfg.plot_hist_data_color = "#ff00ff" #magenta
    cfg.plot_scatter_data_color = "#ff00ff" #magenta
    cfg.plot_bar_data_color = "#ffa74d" #orange-yellow
    cfg.plot_background_facecolor = '#404040'
    cfg.figure_background_facecolor = '#34343C' #darkest plum
    cfg.plot_xy_ticks_fontsize = 7
    cfg.plot_xy_ticks_color = "#fc8293" #salmon
    cfg.plot_title_fontsize = 8
    cfg.plot_title_color = "#5cffe5" #cyan
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # DEFINE THE USER'S VERSION OF ORGANIZATIONAL TERMS TO BE USED
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    define_user_terms(
        # Specify terms used as column headers in DF tables.
        "Person ID", #person_id_header_term_u, the user's term for the "Person ID" column header
        "First Name", #first_name_header_term_u, the user's term for the "First name" column header
        "Last Name", #last_name_header_term_u, the user's term for the "Last name" column header
        "Sex", #sex_header_term_u, the user's term for the "Sex" column header
        "Age", #age_header_term_u, the user's term for the "Age" column header
        "Sphere", #sphere_header_term_u, the user's term for the "Sphere" column header
        "Shift", #shift_header_term_u, the user's term for the "Shift" column header
        "Team", #team_header_term_u, the user's term for the "Team" column header
        "Role", #role_header_term_u, the user's term for the "Role" column header
        "MNGR_CAP", #MNGR_CAP_header_term_u, the user's term for the "MNGR_CAP" column header
        "WRKR_CAP", #WRKR_CAP_header_term_u, the user's term for the "WRKR_CAP" column header
        "Supervisor", #supervisor_header_term_u, the user's term for the "Supervisor" column header
        "Colleagues", #colleagues_header_term_u, the user's term for the "Colleagues" column header
        "Subordinates", #subordinates_header_term_u, the user's term for the "Subordinates" column header

        # Specify the names of the four available roles,
        # in hierarchical order from the "highest."
        # The entries in the list must be maintained in order,
        # as items in the list of role titles are sometimes referenced
        # by functions using their index number.
        "Production Director", #production_director_term_u, the user term for "Production Director"
        "Shift Manager", #shift_manager_term_u, the user term for "Shift Manager"
        "Team Leader", #team_leader_term_u, the user term for "Team Leader"
        "Laborer", #laborer_term_u, the user term for (ordinary) "Laborer"

        # Specify the names of the one "unassigned" shift object
        # and the three regular shifts.
        # The entries in the list must be maintained in order,
        # as items in the list of role titles are sometimes referenced
        # by functions using their index number.
        "unassigned", #unassigned_shift_term_u, the user term for the "unassigned" shift object
        "Shift 1",  #shift_1_term_u, the user term for the "Shift 1" shift object
        "Shift 2",  #shift_2_term_u, the user term for the "Shift 2" shift object
        "Shift 3",  #shift_3_term_u, the user term for the "Shift 3" shift object

        # Specify the names of the different spheres or discplines that teams handle
        # (e.g., "general management", "manufacturing", "packaging", "logistics",
        # and "engineering"); each team be linked with exactly one sphere.
        #
        # The first sphere, "general management", is reserved for the Production Director and Shift Managers.
        # There are not any entire teams associated with that sphere.
        # The remaining spheres in this list may have any nature, and there
        # can be any number of different terms in the list.
        [
            "general management", #this is the user term for "general management", specific to the Production Director and Shift Managers
            "manufacturing",
            "packaging",
            "logistics",
            "engineering",
            ],
        #
        # Specify the number of teams per shift handling each of the
        # spheres listed above.
        # The first sphere, "general management", doesn't have an entire
        # team; it's represented by the Production director and Shift managers.
        # Its number will always be 0.
        [
            0, #this number (always 0) is for "general management", specific to the Production Director and Shift Managers
            4,
            2,
            1,
            1,
            ],
        )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # RUN FUNCTIONS TO SET UP WORKFORCE BASED ON INPUTTED VARIABLES
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    random.seed(cfg.random_seed_A)
    np.random.seed(cfg.random_seed_A)

    create_all_possible_roles()
    create_shift_objects()
    create_team_objects()
    create_all_possible_spheres()
    # create_initial_set_of_tasks()
    # create_initial_set_of_activities()

    create_initial_population_of_persons()
    adjust_personal_stats_to_implement_dependencies_and_covariance(
        # technological aptitude += (age in years * this factor)
        -0.005, #infl_year_of_age_on_TEC
        )

    assign_initial_role_to_each_person()
    assign_initial_shift_to_each_person()
    assign_initial_team_to_each_person()
    assign_initial_sphere_to_each_person()
    assign_initial_supervisor_to_each_person()
    assign_initial_colleagues_to_all_persons()
    assign_initial_subordinates_to_all_supervisors()

    # update_current_tasks()
    # calculate_and_display_new_screen()

    pd.set_option('display.max_rows', 100)
    # pd.set_option('display.max_colwidth', 0)
    # pd.set_option('display.min_rows', 100)

    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    # display(cfg.persons_df)

    for d in range(cfg.num_of_days_to_simulate):
        simulate_one_day_of_activities()
        advance_date_by_one_day()

    calculate_metrics_for_persons_in_simulated_period()

    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    
    # Before creating any new plots, it's necessary to manually delete
    # any existing matplotlib plots from memory -- otherwise, warning
    # messages will be generated after there are 20 plots in memory.
    plt.close("all")
    #
    # Here we generate the *full spectrum* of results graphics that
    # the simulator is capable of generating, regardless of whether
    # they will all be displayed for the user in a particular GUI.
    #
    cfg.png_plt_distribution_of_WRKR_CAP_scores_hist = plot_distribution_of_WRKR_CAP_scores_hist()
    cfg.png_plt_distribution_of_MNGR_CAP_scores_hist = plot_distribution_of_MNGR_CAP_scores_hist()
    cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter = MNGR_CAP_vs_WRKR_CAP_scores_scatter()
    cfg.png_plt_MNGR_CAP_by_age_scatter = plot_MNGR_CAP_by_age_scatter()
    cfg.png_plt_WRKR_CAP_by_shift_bar = plot_WRKR_CAP_by_shift_bar()
    cfg.png_plt_MNGR_CAP_by_role_bar = plot_MNGR_CAP_by_role_bar()
    cfg.png_plt_WRKR_CAP_by_team_bar = plot_WRKR_CAP_by_team_bar()
    cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter = plot_WRKR_CAP_vs_mean_Eff_scatter()
    cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d = plot_num_Good_vs_Poor_actions_by_person_hist2d()

    print("Simulation results have been calculated.")


# cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
# display(cfg.persons_df)
