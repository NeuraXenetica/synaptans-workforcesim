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
This module handles the simulation’s “Level 0” logic, which involves the
creation of the members of the workforce and determining and determining
of their (more or less) permanent personal characteristics.
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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import standard modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import random
from collections import defaultdict
import statistics


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import numpy as np
import pandas as pd


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# Imports of the form "from . import X as x" have been added for use
# in the distributed package; imports of the form "import X as x" are
# retained for use when debugging the modules in VS Code.

if __name__ == "__main__":
    import config as cfg
    import wfs_behaviors as bhv # WorkforceSim logic, level 01 (workers' actual behaviors)
    import wfs_utilities as utils
else:
    try:
        from . import config as cfg
    except:
        import config as cfg
    try:
        from . import wfs_behaviors as bhv # WorkforceSim logic, level 01 (workers' actual behaviors)
    except:
        import wfs_behaviors as bhv # WorkforceSim logic, level 01 (workers' actual behaviors)
    try:
        from . import wfs_utilities as utils
    except:
        import wfs_utilities as utils


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the "Person" class and related functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def calculate_id_starting_value():
    """
    Calculates the value of the personal ID number to be assigned to the
    first Person object created. The ID number will have a value
    incremented by 1 for each subsequent person. The ID number's first
    digits correspond to the random seed used for the simulation, which
    allows multiple simulations employing different random seeds to be
    combined, for purposes of smoothing out any irregularities resulting
    from the imperfectly random nature of the seed and random-number
    generator -- *without* having to deal with the problems that arise
    if multiple persons have the same ID number.    
    """

    # Take cfg.cfg.random_seed_A, add 6 zeros to it, and then
    # increment it by one. (E.g., with a random seed of 3, the first
    # personal ID will be 3000001).

    cfg.emp_id_starting_value = int(cfg.random_seed_A * 1000000 + 1)


class Person_class:
    """
    Defines the Person class.
    """

    def __init__(self):
        """
        Initialization function for the Person class.
        """

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

        # Workstyle. Each worker is assigned to one of several discrete
        # "Workstyle" groups that determine whether the person has
        # (1) elevated, average, or reduced daily Efficacy; (2) stable or
        # variable daily Efficacy; (3) an elevated, average, or reduced
        # number of Sacrifice behaviors, and (4) an elevated, average, or
        # reduced number of Sabotage behaviors (in comparison to someone
        # who otherwise has the same base stats).
        #
        # First, get the actual Workstyle group assignment probabilities
        # for a person of the given age and sex.
        if self.sex == "M":
            if self.age < 38:
                workstyle_prob_A = cfg.workstyle_prob_younger_male_A
                workstyle_prob_B = cfg.workstyle_prob_younger_male_B
                workstyle_prob_C = cfg.workstyle_prob_younger_male_C
                workstyle_prob_D = cfg.workstyle_prob_younger_male_D
            else:
                workstyle_prob_A = cfg.workstyle_prob_older_male_A
                workstyle_prob_B = cfg.workstyle_prob_older_male_B
                workstyle_prob_C = cfg.workstyle_prob_older_male_C
                workstyle_prob_D = cfg.workstyle_prob_older_male_D
        elif self.sex == "F":
            if self.age < 38:
                workstyle_prob_A = cfg.workstyle_prob_younger_female_A
                workstyle_prob_B = cfg.workstyle_prob_younger_female_B
                workstyle_prob_C = cfg.workstyle_prob_younger_female_C
                workstyle_prob_D = cfg.workstyle_prob_younger_female_D
            else:
                workstyle_prob_A = cfg.workstyle_prob_older_female_A
                workstyle_prob_B = cfg.workstyle_prob_older_female_B
                workstyle_prob_C = cfg.workstyle_prob_older_female_C
                workstyle_prob_D = cfg.workstyle_prob_older_female_D

        # Now assign the person to a particular Workstyle group.
        rand_num = random.uniform(0.0, 1.0)

        if rand_num <= (
                workstyle_prob_A):
            self.workstyle = "Group A"

        elif rand_num <= (
                workstyle_prob_A \
                + workstyle_prob_B):
            self.workstyle = "Group B"

        elif rand_num <= (
                workstyle_prob_A \
                + workstyle_prob_B \
                + workstyle_prob_C):
            self.workstyle = "Group C"

        elif rand_num <= (
                workstyle_prob_A \
                + workstyle_prob_B \
                + workstyle_prob_C \
                + workstyle_prob_D):
            self.workstyle = "Group D"

        else:
            self.workstyle = "Group E"


        # ---------------------------------------------------------------------
        # Stats for relatively stable personal traits (core stats).
        # ---------------------------------------------------------------------

        # Health.
        self.stat_health = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Commitment.
        self.stat_commitment = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Perceptiveness.
        self.stat_perceptiveness = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Dexterity.
        self.stat_dexterity = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Sociality.
        self.stat_sociality = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Goodness.
        self.stat_goodness = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Strength. This is a "control stat" that has no effect on anything.
        self.stat_strength = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)

        # Openmindedness. This is a "control stat" that has no effect on anything.
        self.stat_openmindedness = generate_personal_stat(cfg.other_stats_stat_mean, cfg.other_stats_stat_sdev)


        # ---------------------------------------------------------------------
        # Base probabilities for generating particular types of actual
        # behaviors or recording actions (before situational modifiers).
        # ---------------------------------------------------------------------
 
        # Base probability of generating a Presence behavior (before multipliers).
        self.prob_base_presence = \
            cfg.base_rate_attendance + \
                (self.stat_health + self.stat_commitment)/2.0 * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating an Idea behavior (before multipliers).
        self.prob_base_idea = \
            cfg.base_rate_idea + self.stat_perceptiveness * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Lapse behavior (before multipliers).
        self.prob_base_lapse = \
            cfg.base_rate_lapse - self.stat_perceptiveness * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Feat behavior (before multipliers).
        self.prob_base_feat = \
            cfg.base_rate_feat + self.stat_dexterity * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Slip behavior (before multipliers).
        self.prob_base_slip = \
            cfg.base_rate_slip - self.stat_dexterity * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Teamwork behavior (before multipliers).
        self.prob_base_teamwork = \
            cfg.base_rate_teamwork + self.stat_sociality * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Disruption behavior (before multipliers).
        self.prob_base_disruption = \
            cfg.base_rate_disruption - self.stat_sociality * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Sacrifice behavior (before multipliers).
        self.prob_base_sacrifice = \
            cfg.base_rate_sabotage + \
                (self.stat_goodness + self.stat_commitment)/2.0  * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating a Sabotage behavior (before multipliers).
        self.prob_base_sabotage = \
            cfg.base_rate_sabotage - \
                (self.stat_goodness + self.stat_commitment)/2.0  * cfg.stat_to_prob_mod_conv_factor

        # Base Efficacy level (before multipliers).
        self.level_base_efficacy = \
            cfg.base_rate_efficacy + \
                (self.stat_dexterity + self.stat_commitment)/2.0 * cfg.stat_to_prob_mod_conv_factor

        # Base probability of generating an accurate Good or Poor record, as a 
        # manager (i.e., of generating a True Positive or True Negative record)
        # (before multipliers).
        self.prob_base_recording_accurately = \
            cfg.base_rate_recording_accuracy + \
                (self.stat_perceptiveness + self.stat_commitment + self.stat_goodness)/3.0 * cfg.stat_to_prob_mod_conv_factor


        # ---------------------------------------------------------------------
        # Initialize modified probabilities, which will be recalculated later
        # in functions to take situational modifiers into account.
        # ---------------------------------------------------------------------
        self.prob_modified_presence = self.prob_base_presence
        self.prob_modified_idea = self.prob_base_idea
        self.prob_modified_lapse = self.prob_base_lapse
        self.prob_modified_feat = self.prob_base_feat
        self.prob_modified_slip = self.prob_base_slip
        self.prob_modified_teamwork = self.prob_base_teamwork
        self.prob_modified_disruption = self.prob_base_disruption
        self.prob_modified_sacrifice = self.prob_base_sacrifice
        self.prob_modified_sabotage = self.prob_base_sabotage

        self.level_modified_efficacy = self.level_base_efficacy
        self.prob_modified_recording_accurately = self.prob_base_recording_accurately


        # ---------------------------------------------------------------------
        # Derived (calculated) summary capacities.
        # ---------------------------------------------------------------------

        # This is general managerial capacity (calculated as an arithmetic mean).
        self.MNGR_CAP = np.average(
            a=[
                self.stat_health,
                self.stat_commitment,
                self.stat_perceptiveness,
                self.stat_goodness,
                ],
            # Attendance is so crucial that below its components are weighted
            # more heavily than other traits.
            weights=[
                4,
                4,
                3,
                3,
                ]
            )

        # This is general worker capacity (calculated as an arithmetic mean).
        self.WRKR_CAP = np.average(
            a=[
                self.stat_health,
                self.stat_commitment,
                self.stat_dexterity,
                self.stat_goodness,
                self.stat_perceptiveness,
                self.stat_sociality,
                ],
            # Attendance is so crucial that below its components are weighted
            # more heavily than other traits.
            weights=[
                4,
                4,
                3,
                3,
                2,
                2,
                ]
            )

        # ---------------------------------------------------------------------
        # Organizational traits and relationships.
        # ---------------------------------------------------------------------

        # If self.separated == True, a person has been separated from
        # employment (e.g., has resigned or been terminated). If False,
        # the person remains employed.
        self.separated = False

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

        # Proportion of the person's colleagues who are of the same sex
        # as the person.
        self.colleagues_of_same_sex_prtn = None

        # The age of a person's supervisor.
        self.sup_age = None


        # ---------------------------------------------------------------------
        # Activity data generated for the person each day the simulation is run.
        # ---------------------------------------------------------------------

        # Full details of a person's actual behaviors and recorded behaviors are 
        # stored in one organization-wide DF, not directly in the Person object.

        # ---------------------------------------------------------------------
        # Personal metrics of actual behaviors during the simulated period.
        # ---------------------------------------------------------------------

        # Number of days on which a person was present during the simulated period.
        self.days_attended = 0

        # The lowest daily Efficacy generated by the person during the simulated period.
        self.eff_bhv_act_min = ""

        # The highest daily Efficacy generated by the person during the simulated period.
        self.eff_bhv_act_max = ""

        # The mean daily Efficacy generated by the person during the simulated period.
        self.eff_bhv_act_mean = ""

        # The SD of daily Efficacy generated by the person during the simulated period.
        self.eff_bhv_act_sd = ""

        # The number of Good behaviors generated by the person during the simulated period.
        self.good_act_num = ""

        # The number of Poor behaviors generated by the person during the simulated period.
        self.poor_act_num = ""

        # ---------------------------------------------------------------------
        # Dictionaries for certain behavior and record types, for storing the
        # number of events of a given type occurring on each day.
        # ---------------------------------------------------------------------

        # Such dictionaries are only created for the selected types of behaviors and
        # records listed below, because these are the only ones that have been
        # needed thus far.
        # 
        # Some particular types of behaviors generated and records received need to be
        # tracked, e.g., beacuse they can alter the probability of a
        # person's later behaviors -- and when attempting to determine what sort of
        # behaviors a person had in previous days, it's faster and easier to check
        # these simple, internally-stored dicts for the given person than to sift
        # through the entire behavs_act_df for all persons.

        self.dict_days_with_actual_eff_values = {key: None for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_recorded_eff_values = {key: None for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }

        self.dict_days_with_num_of_idea_behaviors = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_lapse_behaviors = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_slip_behaviors = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_teamwork_behaviors = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }

        self.dict_days_with_num_of_absences_recorded = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_lapses_recorded = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_sabotages_recorded = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_slips_recorded = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_disruptions_recorded = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }
        self.dict_days_with_num_of_FN_good_records = {key: 0 for key in list(range(
            cfg.day_of_sim_iter_for_first_simulated_day,
            cfg.day_of_sim_iter_for_first_simulated_day +  cfg.num_of_days_to_simulate
            )) }


        # ---------------------------------------------------------------------
        # Other attributes.
        # ---------------------------------------------------------------------


    # ---------------------------------------------------------------------
    # Related functions.
    # ---------------------------------------------------------------------

    def __str__(self):
        """
        Print/display function that overrides the default behavior of simply
        displaying unhelpful object info when "print" is called.
        """
        return self.f_name + " " + self.l_name + " (" + str(self.per_id) + ")"


    def attributes_to_dict(self) -> dict:
        """
        Sends selected traits to dictionary for DF creation.
        This determines which attributes will be transmitted when a special
        dictionary is created, for conversion into an easy-to-use DF.
        """

        # This converts a list of colleague Person objects into a list of
        # the persons' ID numbers.
        colleague_ids_lambda = lambda x : [y.per_id for y in x] if x is not None else None

        return {
            "Person object": self,
            cfg.person_id_header_term: self.per_id,
            cfg.first_name_header_term: self.f_name,
            cfg.last_name_header_term: self.l_name,
            cfg.sex_header_term: self.sex,
            cfg.age_header_term: self.age,
            "Separated": self.separated,
            cfg.sphere_header_term: self.sphere.title,
            cfg.shift_header_term: self.shift.title,
            cfg.team_header_term: self.team.title,
            cfg.role_header_term: self.role.title,
            cfg.MNGR_CAP_header_term: self.MNGR_CAP,
            cfg.WRKR_CAP_header_term: self.WRKR_CAP,
            "Sub Workstyle": self.workstyle,
            cfg.supervisor_header_term: self.sup,
            "Sup Age": self.sup_age,
            cfg.colleagues_header_term: self.colleagues,
            "Colleagues’ IDs": colleague_ids_lambda(self.colleagues),
            "Sub Same-Sex Colleagues Prtn": self.colleagues_of_same_sex_prtn,
            cfg.subordinates_header_term: self.subs,
            "Days Attended": self.days_attended,
            "Min Eff": self.eff_bhv_act_min,
            "Max Eff": self.eff_bhv_act_max,
            "Mean Eff": self.eff_bhv_act_mean,
            "SD of Eff": self.eff_bhv_act_sd,
            "Num Goods": self.good_act_num,
            "Num Poors": self.poor_act_num,
            "Sub Health": self.stat_health,
            "Sub Commitment": self.stat_commitment,
            "Modified Efficacy": self.level_modified_efficacy,
            }


def generate_personal_stat(
    mean_u, # The mean value for the stat to be generated
    sd_u, # The standard deviation for the stat to be generated
    ):
    """
    The stat-generator function.
    This defines a personal stat that uses the arguments
    for the mean and standard deviation for the stat.
    """

    # Here "loc" is the mean, "scale" is SD,
    # and "size" is the number of numbers to generate.
    randomized_base_for_stat = round( float( np.random.normal(loc=mean_u, scale=sd_u, size=1) ) , 3)

    # It's possible for the number generated above to be < 0 or > 1;
    # below we ensure that the values fall between 0.0 and 1.0.
    adjusted_stat = randomized_base_for_stat

    if randomized_base_for_stat < 0:
        adjusted_stat = 0.0

    elif randomized_base_for_stat > 1:
        # Keep rerolling the stat until it generates a value ≤ 1.0. It's necessary
        # to handle it in this way, because if we simply forced all values ≥ 1.0
        # to be equal to 1.0, it would result in a bizarre preponderance of 1.0
        # values. The method used here will maintain a more normal distribution.
        while randomized_base_for_stat > 1:
            randomized_base_for_stat = round( float( np.random.normal(loc=mean_u, scale=sd_u, size=1) ) , 3)
            adjusted_stat = randomized_base_for_stat

    return adjusted_stat


def create_initial_population_of_persons():
    """
    Creates the initial population of persons
    (who will not yet have their final roles or tasks assigned).
    Creates the dictionary of persons, in which each entry (person)
    is a separate person object of the Person class.
    """

    # Calculate the total number of members of the workforce community.
    # This takes the total number of "Laborers" proper (and not persons more 
    # generally) who should be part of each team; adds 1 (for the Team Leader);
    # multiplies that by the number of teams per shift times 3 (since there are 3 shifts);
    # and then adds 4 (for the 3 Shift Managers and 1 Production Director).
    cfg.size_of_comm_initial = \
        (cfg.num_of_laborers_per_team + 1) * (cfg.num_of_teams_per_shift * 3) + 4

    cfg.persons = defaultdict(list)

    # Populate the community.
    for i in range(0, cfg.size_of_comm_initial):
        cfg.persons[i] = Person_class()
        # print(cfg.persons[i])


def create_df_with_selected_attributes_of_all_persons():
    """
    Returns a DF with selected attributes for all persons.
    The particular personal attributes that are transmitted into this DF
    are defined in the Person class's "attributes_to_dict()" func.
    """

    persons_dict_for_df = [cfg.persons[k].attributes_to_dict() for k in cfg.persons]
    cfg.persons_df = pd.DataFrame(persons_dict_for_df)
    return cfg.persons_df


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the "Role" class and related functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class Role_class:
    """
    Defines the Role class.    
    """

    def __init__(self):
        """
        Initialization function for the Role class.
        """
        self.title = "unspecified"


    def __str__(self):
        """
        Print/display function that overrides the default behavior of simply
        displaying unhelpful object info when "print" is called.
        """
        return self.title


def create_all_possible_roles():
    """
    Creates initial set of potential roles.
    Creates the dictionary of roles, in which each entry (role)
    is a separate role object of the Role class.
    """

    cfg.roles = defaultdict(list)

    # Populate the potential roles.
    # Create one role object corresponding to each
    # of the items in the available_role_titles list.
    for i in range(len(cfg.available_role_titles)):
        cfg.roles[i] = Role_class()
        cfg.roles[i].title = cfg.available_role_titles[i]


def assign_initial_role_to_each_person():
    """
    Assigns a role to each member of the community.
    """

    # ---------------------------------------------------------------------
    # Assign the "Production Director" role to the 1 person
    # with the highest managerial capacity score.
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the "Shift" class and related functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class Shift_class:
    """
    Defines the Shift class.    
    """

    def __init__(self):
        """
        Initialization function for the Shift class.
        """
        self.title = "unspecified"


    def __str__(self):
        """
        Print/display function that overrides the default behavior of simply
        displaying unhelpful object info when "print" is called.
        """
        return self.title


def create_shift_objects():
    """
    Creates the initial set of shifts.
    Creates the dictionary of shifts, in which each entry (shift)
    is a separate shift object of the Shift class.
    """

    cfg.shifts = defaultdict(list)

    # Populate the shifts dict.
    # Create one shift object corresponding to each
    # of the items in the available_shifts list.
    for i in range(len(cfg.available_shift_titles)):
        cfg.shifts[i] = Shift_class()
        cfg.shifts[i].title = cfg.available_shift_titles[i]


def assign_initial_shift_to_each_person():
    """
    Assigns a shift to each member of the community.
    """

    # ---------------------------------------------------------------------
    # Assign the shift "unassigned" to the "Production director" and 
    # Shifts 1-3 to the three "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    # The first entries will be the "Production Director" and "Shift Managers".
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the "Team" class and related functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class Team_class:
    """
    Defines the Team class.
    The "num_of_teams_per_shift" variable has already been given
    a value, as part of the workforce setup.
    """

    def __init__(self):
        """
        Initialization function for the Team class.
        """

        self.title = "unspecified"
        self.shift = ""


    def __str__(self):
        """
        Print/display function that overrides the default behavior of simply
        displaying unhelpful object info when "print" is called.
        """
        return self.title


def create_team_objects():
    """
    Creates the initial set of teams.
    Creates the dictionary of teams, in which each entry (team)
    is a separate team object in the Team class.
    """

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


def assign_initial_team_to_each_person():
    """
    Assigns a team to each member of the community.
    """

    # ---------------------------------------------------------------------
    # Assign the team "unassigned" to the "Production Director" and 
    # "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

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
    # Step through all persons (first Team Leaders, then Laborers) and, 
    # for those who don't yet have a team assigned, assign them to the 
    # first team that still needs persons of the relevant sort to be added. 
    #
    # #It's important to use the unordered "cfg.persons" dictionary 
    # rather than the DF sorted by capacity.
    # ---------------------------------------------------------------------

    # For simplicity's sake, we can begin with cfg.teams[0], which is the special 
    # "unassigned" team. It won't actually receive any new members, though, as we've 
    # already specified above that it doesn't need any more Team Leaders added to it.
    for t in range (0, len(cfg.teams) ):

        # Handle each shift in turn, beginning with cfg.shifts[1] (not cfg.shifts[0],
        # which is the "unassigned" shift).
        for s in range (1, len(cfg.shifts) ):

            # For each team in the given shift...
            if cfg.teams[t].shift == cfg.shifts[s].title:

                # Iterate through all persons to deal with all Team Leaders...
                for p in cfg.persons:

                    # If the team doesn't yet have an assigned Team Leader, and the current person
                    # is a Team Leader, assign him to the given team.
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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the "Sphere" class and related functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class Sphere_class:
    """
    Defines the Sphere class.
    """

    def __init__(self):
        """
        Initialization function for the Sphere class.
        """
        self.title = "unspecified"


    def __str__(self):
        """
        Print/display function that overrides the default behavior of simply
        displaying unhelpful object info when "print" is called.
        """
        return self.title


def create_all_possible_spheres():
    """
    Creates the initial set of all possible spheres.
    Create the dictionary of spheres, in which each entry (sphere)
    is a separate sphere object in the Sphere class.
    """

    cfg.spheres = defaultdict(list)

    # Populate the spheres.
    # Create one sphere object corresponding to each
    # of the items in the available_sphere_titles list.
    for i in range(len(cfg.available_sphere_titles)):
        cfg.spheres[i] = Sphere_class()
        cfg.spheres[i].title = cfg.available_sphere_titles[i]


def assign_initial_sphere_to_each_person():
    """
    Assigns a sphere to each member of the community.
    """

    # ---------------------------------------------------------------------
    # Assign the sphere "general management" to the "Production Director" and 
    # "Shift Managers".
    # ---------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(cfg.persons_df, cfg.MNGR_CAP_header_term)

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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for populating persons' "supervisor", "subordinate",
# █ and "colleague" attributes
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def assign_supervisor_to_each_person():
    """
    Populates the "Supervisor" attribute for all persons.
    """

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify supervisor for separated persons.
        # ---------------------------------------------------------------------
        if cfg.persons[i].separated is True:
            cfg.persons[i].sup = None

        # ---------------------------------------------------------------------
        # Specify supervisor for Production Director.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.production_director_term:
            cfg.persons[i].sup = None

        # ---------------------------------------------------------------------
        # Specify supervisor for Shift Managers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.shift_manager_term:

            # Attach the person object for the Production Director.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if cfg.persons[x].role.title == cfg.production_director_term) ]

        # ---------------------------------------------------------------------
        # Specify supervisor for Team Leaders.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.team_leader_term:

            # Attach the person object for the Shift Manager of the laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if ( 
                (cfg.persons[x].role.title == cfg.shift_manager_term) \
                and (cfg.persons[x].shift == cfg.persons[i].shift) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
                ) ) ]

        # ---------------------------------------------------------------------
        # Specify supervisor for Laborers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.laborer_term:

            # Attach the person object for the Team Leader of the Laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.team_leader_term) \
                and (cfg.persons[x].team == cfg.persons[i].team) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
                ) ) ]


def assign_subordinates_to_all_supervisors():
    """
    Populates the "Subordinates" attribute for all persons.
    """

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify subordinates for separated persons.
        # ---------------------------------------------------------------------
        if cfg.persons[i].separated is True:
            cfg.persons[i].subs = None

        # ---------------------------------------------------------------------
        # Specify subordinates for Production Director.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.production_director_term:
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
                and (cfg.persons[x].shift.title == cfg.persons[i].shift.title) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
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
                and (cfg.persons[x].team.title == cfg.persons[i].team.title) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
                )])

            #The line below converts the nested list into a simple one-level list.
            subs_temp_list = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # ---------------------------------------------------------------------
        # Specify subordinates for Laborers.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.laborer_term:
            cfg.persons[i].subs = None


def assign_colleagues_to_all_persons():
    """
    Populates the "Colleagues" attribute for all persons.
    """

    # A person's "colleagues" includes those individuals at the same level (i.e.,
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
    # For the Production Director, colleagues = None

    for i in cfg.persons:

        # ---------------------------------------------------------------------
        # Specify colleagues for separated persons.
        # ---------------------------------------------------------------------
        if cfg.persons[i].separated is True:
            cfg.persons[i].colleagues = None

        # ---------------------------------------------------------------------
        # Specify colleagues for Production Director.
        # ---------------------------------------------------------------------
        elif cfg.persons[i].role.title == cfg.production_director_term:
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
                and (cfg.persons[x].per_id != cfg.persons[i].per_id) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
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
                and (cfg.persons[x].per_id != cfg.persons[i].per_id) \
                and (cfg.persons[x].separated is False) # It's necessary to exclude separated workers.
                )])

            # The line below converts the nested list into a simple one-level list.
            colleagues_temp_list = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Other functions
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def update_persons_colleagues_of_same_sex_prtn():
    """
    For all persons, updates the calculation of the proportion of a
    a person's colleagues who are of the same sex.
    """

    for p in cfg.persons:

        # This is only relevant if the person has colleagues (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].colleagues:

            sex_this_person = cfg.persons[p].sex

            colleagues_of_this_person = cfg.persons[p].colleagues
            sex_of_colleagues_list = [coll.sex for coll in colleagues_of_this_person]

            colleagues_of_same_sex_num = sex_of_colleagues_list.count(sex_this_person)
            colleagues_of_same_sex_prtn = \
                colleagues_of_same_sex_num \
                / len(sex_of_colleagues_list)
            cfg.persons[p].colleagues_of_same_sex_prtn = colleagues_of_same_sex_prtn


def reset_modified_probs_to_base_probs_for_all_persons():
    """
    This resets all persons' modified daily probabilities for generating
    particular types of actions to the persons' base probabilities. This
    should be done at the start of each new simulated day.
    """

    for p in cfg.persons:

        cfg.persons[p].prob_modified_presence = cfg.persons[p].prob_base_presence
        cfg.persons[p].prob_modified_idea = cfg.persons[p].prob_base_idea
        cfg.persons[p].prob_modified_lapse = cfg.persons[p].prob_base_lapse
        cfg.persons[p].prob_modified_feat = cfg.persons[p].prob_base_feat
        cfg.persons[p].prob_modified_slip = cfg.persons[p].prob_base_slip
        cfg.persons[p].prob_modified_teamwork = cfg.persons[p].prob_base_teamwork
        cfg.persons[p].prob_modified_disruption = cfg.persons[p].prob_base_disruption
        cfg.persons[p].prob_modified_sacrifice = cfg.persons[p].prob_base_sacrifice
        cfg.persons[p].prob_modified_sabotage = cfg.persons[p].prob_base_sabotage

        cfg.persons[p].level_modified_efficacy = cfg.persons[p].level_base_efficacy
        cfg.persons[p].prob_modified_recording_accurately = cfg.persons[p].prob_base_recording_accurately


def calculate_person_modifiers_to_implement_dependencies_and_covariance():
    """
    Implements dependencies and covariance among certain stats and 
    variables by adding modifiers that adjust their previously 
    random values (e.g., to provide bonuses or penalties to Efficacy
    for certain personal or environmental factors).
    """

    for p in cfg.persons:

        # If a person is already separated from employment,
        # do not proceed with updating that person;
        # skip ahead to the next person.
        if cfg.persons[p].separated is True:
            continue


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● Update the person's probability of generating certain
        # ● Good or Poor behaviors.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

        # If the person belongs to a relevant Workstyle group that increases or decreases
        # his likelihood of generating Ideas, elevate or reduce his probability of
        # generating an Idea today.
        cfg.persons[p].prob_modified_idea = cfg.persons[p].prob_base_idea
        if cfg.persons[p].workstyle == "Group A":
            cfg.persons[p].prob_modified_idea = \
                cfg.persons[p].prob_modified_idea * (1 + cfg.prob_elevation_for_idea_due_to_workstyle)
        elif cfg.persons[p].workstyle == "Group E":
            cfg.persons[p].prob_modified_idea = \
                cfg.persons[p].prob_modified_idea * (1 - cfg.prob_reduction_for_idea_due_to_workstyle)

        # If the person belongs to a relevant Workstyle group that increases or decreases
        # his likelihood of generating Disruptions, elevate or reduce his probability of
        # generating a Disruption today.
        cfg.persons[p].prob_modified_disruption = cfg.persons[p].prob_base_disruption
        if cfg.persons[p].workstyle == "Group B":
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption * (1 + cfg.prob_elevation_for_disruption_due_to_workstyle)
        elif cfg.persons[p].workstyle == "Group D":
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption * (1 - cfg.prob_reduction_for_disruption_due_to_workstyle)


        # ---------------------------------------------------------------------
        # Increased probability of Teamworks and Disruptions
        # tied to the day of the month.
        # ---------------------------------------------------------------------

        # Increase a person's modified probability of generating a Teamwork
        # or Disruption behavior if it is the 23rd day of the month or later 
        # (to simulate changes in behavior arising from the pressure to meet 
        # end-of-month production deadlines).

        # If it's not yet the 23rd day of the month, there is no effect.
        # If it's the 23rd day of the month (or later), implement the effect.
        day_num = cfg.day_of_month_1_indexed
        if day_num >= 23:

            # Calculate how many days it is beyond the 22nd day of the month.
            days_past_22nd = day_num - 22

            # The effect increases in a linear fashion, being multiplied by the number
            # of days that it is past the 22nd of the month.
            cfg.persons[p].prob_modified_teamwork = \
                cfg.persons[p].prob_modified_teamwork * \
                (1 + days_past_22nd * cfg.strength_of_effect * random.uniform(0.0, cfg.prob_elevation_max_for_teamwork_due_to_day_in_month))
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption * \
                (1 + days_past_22nd * cfg.strength_of_effect * random.uniform(0.0, cfg.prob_elevation_max_for_disruption_due_to_day_in_month))


        # ---------------------------------------------------------------------
        # Increased probability of a Slip tied to the day of the month.
        # ---------------------------------------------------------------------

        # Increase a person's modified probability of generating a 
        # Slip behavior if it is the 26th day of the month or later 
        # (to simulate changes in behavior arising from the pressure to meet 
        # end-of-month production deadlines).

        # If it's not yet the 26th day of the month, there is no effect.
        # If it's the 26th day of the month (or later), implement the effect.
        # The value of day_num has already been calculated earlier in this function.
        if day_num >= 26:

            # Calculate how many days it is beyond the 25th day of the month.
            days_past_25th = day_num - 25

            # The effect increases in a linear fashion, being multiplied by the number
            # of days that it is past the 25th of the month.
            cfg.persons[p].prob_modified_slip = \
                cfg.persons[p].prob_modified_slip * \
                (1 + days_past_25th * cfg.strength_of_effect * random.uniform(0.0, cfg.prob_elevation_max_for_slip_due_to_day_in_month))


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● Calculate the modifier to a person's Efficacy score.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

        # Get the person's base Efficacy level.
        cfg.persons[p].level_modified_efficacy = cfg.persons[p].level_base_efficacy


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on a person's Age.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a worker's Efficacy based on Age.
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 + cfg.persons[p].age * cfg.strength_of_effect * random.uniform(0.0, cfg.eff_bonus_max_from_person_age))


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on the day of the week.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a person's Efficacy as one moves
        # deeper into the work week (with no bonus on Monday and the greatest
        # bonus on Friday).

        # Monday has weekday_num = 0; Friday has weekday_num = 4.
        weekday_num = cfg.current_datetime_obj.weekday()
        #print("weekday_num: ", weekday_num)

        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 + weekday_num * cfg.strength_of_effect * random.uniform(0.0, cfg.eff_bonus_max_from_weekday))

        #weekday_name = cfg.current_datetime_obj.strftime("%A")
        #print("weekday_name: ", weekday_name)


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on day of the month.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a person's average Efficacy beginning 
        # on the 20th day of the month and then resets to zero bonus on the first day
        # of the following month.

        # If it's not yet the 20th day of the month, there is no bonus.
        # If it's the 20th day of the month (or later), add the bonus.
        # The value of day_num has already been calculated earlier in this function.
        if day_num >= 20:

            # Calculate how many days it is beyond the 19th day of the month. 
            days_past_19th = day_num - 19

            # The bonus increases in a linear fashion, being multiplied by the number
            # of days that it is past the 19th of the month.
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + days_past_19th * cfg.strength_of_effect * random.uniform(0.0, cfg.eff_bonus_max_from_day_in_month))


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on season of the year.
        # ---------------------------------------------------------------------

        # Implement a penalty that reduces Efficacy in the middle of the calendar
        # year.

        # This gives the current day's place within the calendar year
        # with January 1st corresponding to 1.
        day_in_year = cfg.current_datetime_obj.timetuple().tm_yday

        # This yields 1.0 for a day in the middle of the year
        # and 0.0 for January 1st or December 31st.
        penalty_multiplier_for_current_day = 1.0 - ( abs(day_in_year - 182.5) / 182.5 )

        # This penalty has no random element to it.
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 - cfg.eff_penalty_max_from_season_of_year * cfg.strength_of_effect * penalty_multiplier_for_current_day)


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on sex of teammates.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a person's Efficacy as one has a
        # higher proportion of colleagues (e.g., immediate teammates) who are
        # of the same sex as oneself.

        # This is only relevant if the person has colleagues (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].colleagues:

            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.persons[p].colleagues_of_same_sex_prtn * cfg.strength_of_effect * random.uniform(0.0, cfg.eff_bonus_max_from_teammate_sexes))


        # ---------------------------------------------------------------------
        # Penalty to Efficacy based on difference in age with supervisor.
        # ---------------------------------------------------------------------

        # Implement a penalty that decreases a person's Efficacy as the
        # difference in age between the person and his supervisor increases.

        # This is only relevant if the person has a supervisor (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].sup:

            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - abs(cfg.persons[p].age - cfg.persons[p].sup.age) \
                * cfg.strength_of_effect * random.uniform(0.0, cfg.eff_penalty_max_from_sup_age_diff))


        # ---------------------------------------------------------------------
        # (1) Bonus/Penalty to Efficacy lavel and (2) stable or variable
        # daily Efficacy, based on a person's Workstyle group.
        # ---------------------------------------------------------------------

        # Implement a bonus (or penalty) that modifies a person's Efficacy, if
        # he is in a Workstyle group whose members display elevated or reduced
        # (and not simply moderate) Efficacy.
        # Add a degree of daily variability to a person's Efficacy that reflects
        # the type of daily Efficacy (stable or variable) possessed by
        # the Workstyle group to which the person belongs.

        # Group A has elevated Efficacy.
        if cfg.persons[p].workstyle == "Group A":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.workstyle_eff_level_modifier \
                * cfg.strength_of_effect * random.uniform(0.0, 1.0))

            # Group A has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group B has elevated Efficacy.
        if cfg.persons[p].workstyle == "Group B":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.workstyle_eff_level_modifier \
                * cfg.strength_of_effect * random.uniform(0.0, 1.0))

            # Group B has variable Efficacy (i.e., add up to the max variability).
            cfg.persons[p].workstyle_eff_daily_variability = \
                cfg.workstyle_eff_max_daily_variability \
                * cfg.strength_of_effect

        # Group C has average Efficacy (no modifier is applied).
        if cfg.persons[p].workstyle == "Group C":

            # Group C has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group D has reduced Efficacy.
        if cfg.persons[p].workstyle == "Group D":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - cfg.workstyle_eff_level_modifier \
                * cfg.strength_of_effect * random.uniform(0.0, 1.0))

            # Group D has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group E has reduced Efficacy.
        if cfg.persons[p].workstyle == "Group E":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - cfg.workstyle_eff_level_modifier \
                * cfg.strength_of_effect * random.uniform(0.0, 1.0))

            # Group E has variable Efficacy (i.e., add the max variability).
            cfg.persons[p].workstyle_eff_daily_variability = \
                cfg.workstyle_eff_max_daily_variability \
                * cfg.strength_of_effect


        # ---------------------------------------------------------------------
        # Bonus to Efficacy lavel based on a person having had a Good behavior
        # (Idea, Feat, Teamwork, or Sacrifice) in the previous days that was
        # accurately recorded by his manager (i.e., a True Positive record of
        # a Good behavior).
        # ---------------------------------------------------------------------

        mod_for_TP_FN_good = bhv.return_eff_modifier_for_impact_of_previous_recordings_on_bhv_of_person_today(
            cfg.persons[p], # the Person object whose behavior may be impacted
            )
        #print("Daily mod_for_TP_FN_good for person: ", mod_for_TP_FN_good)

        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * mod_for_TP_FN_good

        #print("person's final cfg.persons[p].level_modified_efficacy: ", cfg.persons[p].level_modified_efficacy)


def person_object_with_given_sub_ID(
    sub_ID_u, # the subject ID for the person object being sought
    ):
    """
    Returns the person object that possesses the inputted ID number.
    """

    for p in cfg.persons:
        if cfg.persons[p].per_id == sub_ID_u:
            return cfg.persons[p]

    return None


def display_simple_personnel_statistics():
    """
    Calculates and displays some simple statistics regarding
    persons' demographics and stats.
    """

    # Calculate the total number of persons.
    print("Persons in community at start of simulation: ", cfg.size_of_comm_initial)
    print("Separations during retained period: ",
        cfg.behavs_act_df["Behavior Type"].value_counts()["Separation"])
    print("Unique subjects of behaviors/events in retained cfg.behavs_act_df: ", cfg.behavs_act_df["Sub ID"].nunique())
    print("Total persons in persons_df at end of simulation (including priming-period separations): ", len(cfg.persons_df))

    # Calculate the portion of persons in Workstyle Group A.
    workstyle_A_num = list(cfg.persons_df["Sub Workstyle"]).count("Group A")
    workstyle_A_prtn = workstyle_A_num / len(cfg.persons_df)

    # Calculate the portion of persons in Workstyle Group B.
    workstyle_B_num = list(cfg.persons_df["Sub Workstyle"]).count("Group B")
    workstyle_B_prtn = workstyle_B_num / len(cfg.persons_df)

    # Calculate the portion of persons in Workstyle Group C.
    workstyle_C_num = list(cfg.persons_df["Sub Workstyle"]).count("Group C")
    workstyle_C_prtn = workstyle_C_num / len(cfg.persons_df)

    # Calculate the portion of persons in Workstyle Group D.
    workstyle_D_num = list(cfg.persons_df["Sub Workstyle"]).count("Group D")
    workstyle_D_prtn = workstyle_D_num / len(cfg.persons_df)

    # Calculate the portion of persons in Workstyle Group E.
    workstyle_E_num = list(cfg.persons_df["Sub Workstyle"]).count("Group E")
    workstyle_E_prtn = workstyle_E_num / len(cfg.persons_df)

    """
    print("Portion of persons with each Workstyle: ",
        "A:", round(workstyle_A_prtn, 3),
        "B:", round(workstyle_B_prtn, 3),
        "C:", round(workstyle_C_prtn, 3),
        "D:", round(workstyle_D_prtn, 3),
        "E:", round(workstyle_E_prtn, 3),
        )
    """


def check_for_and_execute_worker_separation_and_replacement():
    """
    Checks whether any workers (Team Leaders or Laborers only) will
    be separated at the end of this day; if so, it separates
    them and replaces them with new workers to be in place
    prior to the start of the next day.
    """

    # If the current weekday is Saturday or Sunday, skip ahead to the next day
    # without generating any Separation or Replacement events.
    if (cfg.current_datetime_obj.weekday() == 5) | (cfg.current_datetime_obj.weekday() == 6):
        return


    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
    # ● Determine whether persons generate a "Resignation" behavior
    # ● and record or "Termination" record and 
    # ● create those behaviors and records.
    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

    # ---------------------------------------------------------------------
    # Create a list of all the persons (if any) who are to be
    # separated and replaced on this day. The actual separation
    # and replacement will be handled in two steps;
    # they can't be handled all in a single step, because that
    # would generate an error of "dictionary changed size
    # during iteration".
    # ---------------------------------------------------------------------

    list_of_persons_to_replace = []

    for p in cfg.persons:

        # If a person is the Production Director or a Shift Manager,
        # he cannot be separated; do not check whether a separation should occur.
        if cfg.persons[p].role.title == "Production Director":
            # Skip ahead to the next person.
            continue
        if cfg.persons[p].role.title == "Shift Manager":
            # Skip ahead to the next person.
            continue

        # If a person is already separated from employment,
        # do not check whether a separation should occur
        if cfg.persons[p].separated is True:
            # Skip ahead to the next person.
            continue


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● Calculate variables that will affect whether a Separation event occurs.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

        # ---------------------------------------------------------------------
        # Absences recorded for the person during the period covering the current day 
        # plus the previous N days.
        # ---------------------------------------------------------------------

        # Find the current day's spot in the list, count backwards by N to find the
        # spot of the list correspondingn to the first day of the period that should be 
        # searched for events, and delete any items found in the list before that point.
        #
        # Note that because workers are checked for termination events *after* the end of
        # the workday, the day just completed is always checked for termination events.
        # If previous_days_to_check_num = 1, then the day-just-ended is checked, *and also
        # the 1 day previous to that*.

        list_of_absences_recorded_for_pers = list(cfg.persons[p].dict_days_with_num_of_absences_recorded.values())

        previous_days_to_check_for_absences_num = 16


        # This needs to be rewritten (?); the slicing of the list [] uses 0 as its initial value, not -31 (?).

        # The lowest value that this can have is 0, even if there's a sizeable priming period.
        # That's because slicing of the list [start:stop] indexes the first item in the list
        # as 0, not (e.g.) -31.
        earliest_index_to_include = \
            (cfg.day_of_sim_iter - previous_days_to_check_for_absences_num) \
                - cfg.day_of_sim_iter_for_first_simulated_day

        cfg.day_of_sim_iter - previous_days_to_check_for_absences_num

        if earliest_index_to_include <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_absences_recorded_for_pers_in_last_n_days = list_of_absences_recorded_for_pers
        elif earliest_index_to_include > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_absences_recorded_for_pers_in_last_n_days = \
                list_of_absences_recorded_for_pers[earliest_index_to_include:]
        pers_absences_recorded_in_last_n_days_sum = \
            sum(list_of_absences_recorded_for_pers_in_last_n_days)

        # ---------------------------------------------------------------------
        # Idea behaviors generated by the person to date.
        # ---------------------------------------------------------------------
        pers_idea_behaviors_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_idea_behaviors.values()))

        # ---------------------------------------------------------------------
        # Lapses recorded for the person during the period covering the current day 
        # plus the previous N days.
        # ---------------------------------------------------------------------

        # This calculation has the same conditions and caveats as the calculation
        # of the number of Absences recorded during the current and previous N days.

        list_of_lapses_recorded_for_pers = list(cfg.persons[p].dict_days_with_num_of_lapses_recorded.values())

        previous_days_to_check_for_lapses_num = 90
        earliest_index_to_include = cfg.day_of_sim_iter - previous_days_to_check_for_lapses_num

        if earliest_index_to_include <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_lapses_recorded_for_pers_in_last_n_days = list_of_lapses_recorded_for_pers
        elif earliest_index_to_include > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_lapses_recorded_for_pers_in_last_n_days = \
                list_of_lapses_recorded_for_pers[earliest_index_to_include:]
        pers_lapses_recorded_in_last_n_days_sum = \
            sum(list_of_lapses_recorded_for_pers_in_last_n_days)

        # ---------------------------------------------------------------------
        # Slips recorded for the person during the period covering the current day 
        # plus the previous N days.
        # ---------------------------------------------------------------------

        # This calculation has the same conditions and caveats as the calculation
        # of the number of Absences recorded during the current and previous N days.

        list_of_slips_recorded_for_pers = list(cfg.persons[p].dict_days_with_num_of_slips_recorded.values())

        previous_days_to_check_for_slips_num = 90
        earliest_index_to_include = cfg.day_of_sim_iter - previous_days_to_check_for_slips_num

        if earliest_index_to_include <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_slips_recorded_for_pers_in_last_n_days = list_of_slips_recorded_for_pers
        elif earliest_index_to_include > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_slips_recorded_for_pers_in_last_n_days = \
                list_of_slips_recorded_for_pers[earliest_index_to_include:]
        pers_slips_recorded_in_last_n_days_sum = \
            sum(list_of_slips_recorded_for_pers_in_last_n_days)

        # ---------------------------------------------------------------------
        # Disruptions recorded for the person during the period covering the current day 
        # plus the previous N days.
        # ---------------------------------------------------------------------

        # This calculation has the same conditions and caveats as the calculation
        # of the number of Absences recorded during the current and previous N days.

        list_of_disruptions_recorded_for_pers = list(cfg.persons[p].dict_days_with_num_of_disruptions_recorded.values())

        previous_days_to_check_for_disruptions_num = 45
        earliest_index_to_include = cfg.day_of_sim_iter - previous_days_to_check_for_disruptions_num

        if earliest_index_to_include <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_disruptions_recorded_for_pers_in_last_n_days = list_of_disruptions_recorded_for_pers
        elif earliest_index_to_include > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_disruptions_recorded_for_pers_in_last_n_days = \
                list_of_disruptions_recorded_for_pers[earliest_index_to_include:]
        pers_disruptions_recorded_in_last_n_days_sum = \
            sum(list_of_disruptions_recorded_for_pers_in_last_n_days)

        # ---------------------------------------------------------------------
        # Sabotages recorded for the person to date.
        # ---------------------------------------------------------------------
        pers_sabotages_recorded_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_sabotages_recorded.values()))

        # ---------------------------------------------------------------------
        # Unrecorded (False Negative) Good behaviors for the person to date.
        # ---------------------------------------------------------------------
        pers_FN_good_records_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_FN_good_records.values()))

        # Note that when instantiated, a given person's dict_days_with_actual_eff_values
        # dictionary includes None values for all days, including those days that 
        # haven't been simulated yet. When calculating means, we restrict the calculation
        # to those entries in the dict corresponding to days that have already been
        # simulated.
        #
        # Delete from the list any None values, which correspond to days
        # on which a person was absent and thus had no actual or recorded Efficacy.

        # ---------------------------------------------------------------------
        # Mean of actual Efficacy values.
        # ---------------------------------------------------------------------

        # On the first day, there won't yet be any Efficacy values.
        try:
            temp_list = \
                list(cfg.persons[p].dict_days_with_actual_eff_values.values())[0:(cfg.day_of_sim_iter - cfg.day_of_sim_iter_for_first_simulated_day)]
            list_of_actual_eff_values_without_Nones = [v for v in temp_list if v is not None]
            pers_actual_eff_values_mean = \
                statistics.mean(list_of_actual_eff_values_without_Nones)
        except:
            pers_actual_eff_values_mean = None

        # ---------------------------------------------------------------------
        # Mean of recorded Efficacy values.
        # ---------------------------------------------------------------------

        # On the first day, there won't yet be any Efficacy values.
        try:
            temp_list = \
                list(cfg.persons[p].dict_days_with_recorded_eff_values.values())[0:(cfg.day_of_sim_iter - cfg.day_of_sim_iter_for_first_simulated_day)]
            list_of_recorded_eff_values_without_Nones = [v for v in temp_list if v is not None]
            pers_recorded_eff_values_mean = \
                statistics.mean(list_of_recorded_eff_values_without_Nones)
        except:
            pers_recorded_eff_values_mean = None

        # ---------------------------------------------------------------------
        # Number of colleagues.
        # ---------------------------------------------------------------------
        try:
            pers_current_colleagues_total_num = len(cfg.persons[p].colleagues)
        except:
            # This is the case of the Production Director, who has no colleagues.
            pers_current_colleagues_total_num = 0

        # ---------------------------------------------------------------------
        # Mean actual Efficacy behaviors for colleagues.
        # ---------------------------------------------------------------------
        try:
            list_of_all_colleague_actual_eff_values = []
            for c in cfg.persons[p].colleagues:
                list_of_all_colleague_actual_eff_values.extend(list(c.dict_days_with_actual_eff_values.values()))
            list_of_all_colleague_actual_eff_values = [v for v in list_of_all_colleague_actual_eff_values if v is not None]
            pers_colleagues_actual_eff_values_mean = \
                statistics.mean(list_of_all_colleague_actual_eff_values)
        except:
            # This is the case of the Production Director, who has no colleagues.
            pers_colleagues_actual_eff_values_mean = None

        # ---------------------------------------------------------------------
        # Supervisor's Goodness stat.
        # ---------------------------------------------------------------------
        try:
            goodness_of_pers_sup = cfg.persons[p].sup.stat_goodness
        except:
            # This is the case of the Production Director, who has no supervisor.
            goodness_of_pers_sup = None


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● Determine whether particular types of Separation events occur.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

        # ---------------------------------------------------------------------
        # "Low Commitment"
        # 
        # Calculate if there's a Resignation tied to low Commitment.
        # ---------------------------------------------------------------------

        # If today a person's Commitment stat is less than some randomly-generated 
        # number and a random roll is less than some fixed threshold, a Resignation
        # event will be generated. This is the most "random" sort of Resignation event,
        # which can affect any person with a less-than-maximum Commitment level.

        pers_openness_to_resigning_through_low_commitment = \
           (1.0 - cfg.persons[p].stat_commitment)

        # If a person's Commitment is low, then on occasion...
        if pers_openness_to_resigning_through_low_commitment * random.uniform(0.0, 1.0) > \
            random.uniform(0.0, 0.03):
            # (The smaller the number on the right above, the fewer Resignations will occur.)

            # ... the person has a low but non-zero chance of resigning 
            # on a given day.
            # (The smaller the number on the right above, the fewer Resignations will occur.)
            if random.uniform(0.0, 1.0) < 0.00014:

                # Add the person's "Resignation" behavior to the behaviors DF.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Separation", # behavior type (string)
                    "Resignation", # behavior subtype (string)
                    "Low Commitment", # behavior nature (string)
                    "Resignation", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this reason,
                # there's no need to check whether he might also become separated
                # for other reasons on the same day; skip ahead to the next person.
                continue


        # ---------------------------------------------------------------------
        # "Ethically Inferior Supervisor"
        # 
        # Calculate if there's a Resignation due to having a supervisor
        # with dramatically lower Goodness than oneself.
        # ---------------------------------------------------------------------

        # If the person's Goodness stat exceeds that of his supervisor by some
        # specified value, a Resignation behavior will be generated if a random 
        # roll is less than some fixed threshold on this day.

        # A Production Director has no supervisor and thus cannot resign
        # for this reason.
        if cfg.persons[p].sup is not None:

            # The smaller the number on the right, the more Resignations will occur.
            if cfg.persons[p].stat_goodness - goodness_of_pers_sup >= 0.41: # was 0.43 0.45 0.6 0.67 0.71 0.8
                if random.uniform(0.0, 1.0) < 0.055: # was 0.035 0.013 0.015 

                    # Add the person's "Resignation" behavior to the behaviors DF.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Separation", # behavior type (string)
                        "Resignation", # behavior subtype (string)
                        "Ethically Inferior Supervisor", # behavior nature (string)
                        "Resignation", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        True, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for this reason,
                    # there's no need to check whether he might also become separated
                    # for other reasons on the same day; skip ahead to the next person.
                    continue


        # ---------------------------------------------------------------------
        # "Unrecognized Good Behaviors"
        # 
        # Calculate if there's a Resignation due to having multiple
        # unrecognized (False Negative record) Good behaviors.
        # ---------------------------------------------------------------------

        # If a person has reached some number of unrecognized Good behaviors *during
        # his entire career*, a Resignation behavior will be generated if a random 
        # roll is less than some fixed threshold on this day.

        if pers_FN_good_records_to_date_sum >= 2:

            if random.uniform(0.0, 1.0) < 0.075: # was 0.03

                # Add the person's "Resignation" behavior to the behaviors DF.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Separation", # behavior type (string)
                    "Resignation", # behavior subtype (string)
                    "Unrecognized Good Behaviors", # behavior nature (string)
                    "Resignation", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this reason,
                # there's no need to check whether he might also become separated
                # for other reasons on the same day; skip ahead to the next person.
                continue


        # ---------------------------------------------------------------------
        # "Recruited Away"
        # 
        # Calculate if there's a Resignation due to a person with high actual
        # Efficacy and multiple Idea behaviors being recruited away.
        # ---------------------------------------------------------------------

        # If a person has generated some number of Idea behaviors *during his entire
        # career* and has a mean actual Efficacy that exceeds the organization's 
        # mean actual Efficacy by some fixed amount, a Resignation behavior will be 
        # generated if a random roll is less than some fixed threshold on this day.

        # This shouldn't be applied on the first day, because at the start of the
        # first day, cfg.org_actual_eff_values_mean will equal 0.0.
        # However, the fact that it requires a person to have at least N Idea
        # behaviors automatically precludes it from being applied on the first day.

        if pers_idea_behaviors_to_date_sum >= 4: # was 3
            # The smaller the number on the right, the more Resignations will occur.
            if pers_actual_eff_values_mean >= cfg.org_actual_eff_values_mean + 0.395: # was 0.41 0.43 0.45 0.47 0.5 0.55

                if random.uniform(0.0, 1.0) < 0.04: # was 0.055

                    # Add the person's "Resignation" behavior to the behaviors DF.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Separation", # behavior type (string)
                        "Resignation", # behavior subtype (string)
                        "Recruited Away", # behavior nature (string)
                        "Resignation", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        True, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for this reason,
                    # there's no need to check whether he might also become separated
                    # for other reasons on the same day; skip ahead to the next person.
                    continue


        # ---------------------------------------------------------------------
        # "Underrecorded Efficacy"
        # 
        # Calculate if there's a Resignation due to a person having a Recorded
        # Efficacy that's much lower than his Actual Efficacy.
        # ---------------------------------------------------------------------

        # Only allow this to happen if it's at least the Nth simulated day
        # worked by a given person (this excludes recent replacement hires).
        if cfg.persons[p].days_attended >= 15:

            # The Production Director will not have any recorded Efficacy values.
            if cfg.persons[p].role.title != "Production Director":

                # If the person's Actual Efficacy exceeds his Recorded Efficacy
                # by a specified amount...
                # (The smaller the number on the right, the more Resignations will occur.)
                if (pers_actual_eff_values_mean - pers_recorded_eff_values_mean) >= 0.047: # was 0.0485 0.047 0.05 0.052

                    # ... there's a chance that the person may resign
                    # on any given day.
                    if random.uniform(0.0, 1.0) < 0.2: # was 0.07

                        # Add the person's "Resignation" behavior to the behaviors DF.
                        bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Separation", # behavior type (string)
                            "Resignation", # behavior subtype (string)
                            "Underrecorded Efficacy", # behavior nature (string)
                            "Resignation", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            True, # whether to include a record (e.g., for a Separation or Onboarding event)
                            )

                        # Add the person to the list of persons
                        # to be replaced as workers.
                        list_of_persons_to_replace.append(cfg.persons[p])

                        # If a person becomes separated from employment for this reason,
                        # there's no need to check whether he might also become separated
                        # for other reasons on the same day; skip ahead to the next person.
                        continue


        # ---------------------------------------------------------------------
        # "Poor Teammates"
        # 
        # Calculate if there's a Resignation due to a person having much higher
        # Actual Efficacy than his teammates and having low Goodness (i.e.,
        # willingness to generate Sacrifice behaviors).
        # ---------------------------------------------------------------------

        # A Production Director has no colleagues and thus cannot resign
        # for this reason.
        if cfg.persons[p].colleagues is not None:

            try:
                # Only allow this to happen if it's at least the Nth simulated day
                # worked by a given person (this excludes recent replacement hires).
                if cfg.persons[p].days_attended >= 15:

                    # If the person's Actual Efficacy exceeds his teammates' mean actual Efficacy
                    # by a specified amount...
                    # (The smaller the number on the right, the more Resignations will occur.)
                    if (pers_actual_eff_values_mean - pers_colleagues_actual_eff_values_mean) >= 0.043: # was 0.05 0.07 0.09

                        # ... and the person's Goodness stat is below some threshold...
                        if cfg.persons[p].stat_goodness < 0.5: # was 0.65

                            # ... there's a chance that the person may resign
                            # on any given day.
                            if random.uniform(0.0, 1.0) < 0.25: # was 0.2

                                # Add the person's "Resignation" behavior to the behaviors DF.
                                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                                    cfg.persons[p], # Person object for the person who performed the behavior
                                    "Separation", # behavior type (string)
                                    "Resignation", # behavior subtype (string)
                                    "Poor Teammates", # behavior nature (string)
                                    "Resignation", # behavior comptype (string)
                                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                                    )

                                # Add the person to the list of persons
                                # to be replaced as workers.
                                list_of_persons_to_replace.append(cfg.persons[p])

                                # If a person becomes separated from employment for this reason,
                                # there's no need to check whether he might also become separated
                                # for other reasons on the same day; skip ahead to the next person.
                                continue

            except:
                print("per_id of person generating error for poor teammates: ", cfg.persons[p].per_id)
                pass


        # ---------------------------------------------------------------------
        # "Multiple Sabotages"
        # 
        # Calculate if there's a Termination tied to recorded Sabotages.
        # ---------------------------------------------------------------------

        # A person is terminated after receiving his Nth recording of a
        # Sabotage *for his entire career*.

        if pers_sabotages_recorded_to_date_sum >= 3: # was 4

            # Add the person's "Termination" behavior to the behaviors DF.
            # This will later be switched from an (apparent) behavior by the person
            # to (only) a record made by his supervisor.
            bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                cfg.persons[p], # Person object for the person who performed the behavior
                "Separation", # behavior type (string)
                "Termination", # behavior subtype (string)
                "Multiple Sabotages", # behavior nature (string)
                "Termination", # behavior comptype (string)
                None, # the actual Efficacy (if relevant) demonstrated in the behavior
                True, # whether to include a record (e.g., for a Separation or Onboarding event)
                )

            # Add the person to the list of persons
            # to be replaced as workers.
            list_of_persons_to_replace.append(cfg.persons[p])

            # If a person becomes separated from employment for this reason,
            # there's no need to check whether he might also become separated
            # for other reasons on the same day; skip ahead to the next person.
            continue


        # ---------------------------------------------------------------------
        # "Lapses and Below-Average Efficacy"
        # 
        # Calculate if there's a Termination tied to multiple recorded Lapses 
        # and significantly below-average recorded Efficacy.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if he has a specified
        # number of Lapses *during the last N days* and below-average recorded Efficacy.

        if pers_lapses_recorded_in_last_n_days_sum >= 3: # was 2

            # The smaller the number at the end, the more persons who will be terminated.
            if pers_recorded_eff_values_mean < (cfg.org_recorded_eff_values_mean - 0.23): # was 0.25

                # ... there's a chance that the person may be terminated
                # on any given day.
                if random.uniform(0.0, 1.0) < 0.05: # was 0.08

                    # Add the person's "Termination" behavior to the behaviors DF.
                    # This will later be switched from an (apparent) behavior by the person
                    # to (only) a record made by his supervisor.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Separation", # behavior type (string)
                        "Termination", # behavior subtype (string)
                        "Lapses and Below-Average Efficacy", # behavior nature (string)
                        "Termination", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        True, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for this reason,
                    # there's no need to check whether he might also become separated
                    # for other reasons on the same day; skip ahead to the next person.
                    continue


        # ---------------------------------------------------------------------
        # "Multiple Lapses"
        # 
        # Calculate if there's a Termination tied to multiple recorded Lapses.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if he has a specified
        # number of Lapses *during the last N days* (regardless of his recorded Efficacy).

        if pers_lapses_recorded_in_last_n_days_sum >= 5: # was 4

            # ... there's a chance that the person may be terminated
            # on any given day.
            # (The larger the number at the end, the more persons who will be terminated.)
            if random.uniform(0.0, 1.0) < 0.27: # was 0.25

                # Add the person's "Termination" behavior to the behaviors DF.
                # This will later be switched from an (apparent) behavior by the person
                # to (only) a record made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Separation", # behavior type (string)
                    "Termination", # behavior subtype (string)
                    "Multiple Lapses", # behavior nature (string)
                    "Termination", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this reason,
                # there's no need to check whether he might also become separated
                # for other reasons on the same day; skip ahead to the next person.
                continue


        # ---------------------------------------------------------------------
        # "Multiple Slips"
        # 
        # Calculate if there's a Termination tied to multiple recorded Slips.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if he has a specified
        # number of Slips *during the last N days*.

        if pers_slips_recorded_in_last_n_days_sum >= 4: # was 5

            # ... there's a chance that the person may be terminated
            # on any given day.
            if random.uniform(0.0, 1.0) <= 0.1: # was 0.12

                # Add the person's "Termination" behavior to the behaviors DF.
                # This will later be switched from an (apparent) behavior by the person
                # to (only) a record made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Separation", # behavior type (string)
                    "Termination", # behavior subtype (string)
                    "Multiple Slips", # behavior nature (string)
                    "Termination", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this reason,
                # there's no need to check whether he might also become separated
                # for other reasons on the same day; skip ahead to the next person.
                continue


        # ---------------------------------------------------------------------
        # "Multiple Disruptions"
        # 
        # Calculate if there's a Termination tied to multiple recorded 
        # Disruptions.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if he has a specified
        # number of Disruptions *during the last N days*.

        if pers_disruptions_recorded_in_last_n_days_sum >= 4: # was 3

            # ... there's a chance that the person may be terminated
            # on any given day.
            if random.uniform(0.0, 1.0) < 0.032: # was 0.035 0.03

                # Add the person's "Termination" behavior to the behaviors DF.
                # This will later be switched from an (apparent) behavior by the person
                # to (only) a record made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Separation", # behavior type (string)
                    "Termination", # behavior subtype (string)
                    "Multiple Disruptions", # behavior nature (string)
                    "Termination", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    True, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this reason,
                # there's no need to check whether he might also become separated
                # for other reasons on the same day; skip ahead to the next person.
                continue


        # ---------------------------------------------------------------------
        # "Multiple Absences"
        # 
        # Calculate if there's a Termination tied to multiple Absences.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if he has a specified
        # number of Absences within the last N days.

        if pers_absences_recorded_in_last_n_days_sum >= 4: # was 4

            # Only allow this to happen if it's at least a certain day in the series
            # worked by a given person (this excludes recent replacement hires); if so...
            if cfg.persons[p].days_attended >= 1:

                # ... there's a chance that the person may be terminated
                # on any given day.
                if random.uniform(0.0, 1.0) < 0.1: # was 0.3

                    # Add the person's "Termination" behavior to the behaviors DF.
                    # This will later be switched from an (apparent) behavior by the person
                    # to (only) a record made by his supervisor.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Separation", # behavior type (string)
                        "Termination", # behavior subtype (string)
                        "Multiple Absences", # behavior nature (string)
                        "Termination", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        True, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for this reason,
                    # there's no need to check whether he might also become separated
                    # for other reasons on the same day; skip ahead to the next person.
                    continue


        # ---------------------------------------------------------------------
        # "Low Efficacy"
        # 
        # Calculate if there's a Termination tied to low recorded Efficacy.
        # ---------------------------------------------------------------------

        # A person has a chance of being terminated if his recorded Efficacy
        # is below some specified level.

        # During his first days, a person's pers_recorded_eff_values_mean may still be None,
        # if he has had an Absence on each day.
        if pers_recorded_eff_values_mean is not None:

            # The smaller the number at the end, the more persons who will be terminated.
            if pers_recorded_eff_values_mean < (cfg.org_recorded_eff_values_mean - 0.40): # was 0.405

                # Only allow this to happen if it's at least a certain day in the series.
                # worked by a given person (this excludes recent replacement hires). If so...
                if cfg.persons[p].days_attended >= 15:

                    # ... there's a chance that the person may be terminated
                    # on any given day.
                    if random.uniform(0.0, 1.0) < 0.25: # was 0.15

                        # Add the person's "Termination" behavior to the behaviors DF.
                        # This will later be switched from an (apparent) behavior by the person
                        # to (only) a record made by his supervisor.
                        bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Separation", # behavior type (string)
                            "Termination", # behavior subtype (string)
                            "Low Efficacy", # behavior nature (string)
                            "Termination", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            True, # whether to include a record (e.g., for a Separation or Onboarding event)
                            )

                        # Add the person to the list of persons
                        # to be replaced as workers.
                        list_of_persons_to_replace.append(cfg.persons[p])

                        # If a person becomes separated from employment for this reason,
                        # there's no need to check whether he might also become separated
                        # for other reasons on the same day; skip ahead to the next person.
                        continue


    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
    # ● Perform the actual separation events (by modifying Person objects);
    # ● create new replacement workers; and swap them into the replaced
    # ● persons' organizational placements.
    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

    for person in list_of_persons_to_replace:

        # Separate the person and replace him 
        # as a worker with a newly-generated person.
        separate_and_replace_worker_with_new_person(
            person, # the person to be separated
            )

    # Recalculate all supervisor, subordinate, and colleage relationships,
    # to account for any changes in personnel.
    assign_supervisor_to_each_person()
    assign_subordinates_to_all_supervisors()
    assign_colleagues_to_all_persons()

    # Update all persons' portion of same-sex colleagues
    # (since a replacement worker may have a different sex
    # than the one whom he replaced).
    update_persons_colleagues_of_same_sex_prtn()


def separate_and_replace_worker_with_new_person(
    person_to_separate_u, # the person to be separated
    ):
    """
    Gets the organizational placement of a worker-to-be-separated,
    separates that person, randomly generates a new person from
    scratch, and immediately places that new person into the 
    separated person's organizational placement.
    """

    # ---------------------------------------------------------------------
    # Temporarily save the details of the organizational placement
    # (Role, Shift, Team, supervisor, colleagues, subordinates)
    # of the person to be separated.
    # ---------------------------------------------------------------------

    role_to_transfer = person_to_separate_u.role
    sphere_to_transfer = person_to_separate_u.sphere
    shift_to_transfer = person_to_separate_u.shift
    team_to_transfer = person_to_separate_u.team
    sup_to_transfer = person_to_separate_u.sup
    colleagues_to_transfer = person_to_separate_u.colleagues
    subs_to_transfer = person_to_separate_u.subs
    task_to_transfer = person_to_separate_u.task
    curr_actvty_to_transfer = person_to_separate_u.curr_actvty

    # ---------------------------------------------------------------------
    # Randomly generate a new person.
    # ---------------------------------------------------------------------

    # Get the current size of cfg.persons
    new_person_index = len(cfg.persons) + 1

    # Create the new Person object.
    cfg.persons[new_person_index] = Person_class()
    # print(cfg.persons[new_person_index])

    # ---------------------------------------------------------------------
    # Separate the person who is being separated.
    # ---------------------------------------------------------------------

    # Keep the person in existence and as part of the "workforce" broadly
    # understood (so that his data can be used when generating statistics
    # and plotting phenomena), but mark him as "separated", so that he
    # no longer generates activities and isn't connected to a supervisor,
    # colleagues, or subordinates.

    person_to_separate_u.separated = True

    # ---------------------------------------------------------------------
    # Connect and activate the new person who is being employed.
    # ---------------------------------------------------------------------

    cfg.persons[new_person_index].role = role_to_transfer
    cfg.persons[new_person_index].sphere = sphere_to_transfer
    cfg.persons[new_person_index].shift = shift_to_transfer
    cfg.persons[new_person_index].team = team_to_transfer
    cfg.persons[new_person_index].sup = sup_to_transfer
    cfg.persons[new_person_index].colleagues = colleagues_to_transfer
    cfg.persons[new_person_index].subs = subs_to_transfer
    cfg.persons[new_person_index].task = task_to_transfer
    cfg.persons[new_person_index].curr_actvty = curr_actvty_to_transfer

    # Generate an "Onboarding" behavior and record for the
    # newly hired person to the behaviors DF.
    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
        cfg.persons[new_person_index], # Person object for the person who performed the behavior
        "Onboarding", # behavior type (string)
        None, # behavior subtype (string)
        None, # behavior nature (string)
        "Onboarding", # behavior comptype (string)
        None, # the actual Efficacy (if relevant) demonstrated in the behavior
        True, # whether to include a record (e.g., for a Separation or Onboarding event)
        )



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