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
This module handles the logic connected with creation of the members of 
the workforce and determining and determining of their (more or less) 
permanent personal characteristics.
"""

import random
from collections import defaultdict
import statistics

import numpy as np
import pandas as pd

# Import other modules from this package.
import config as cfg
import wfs_behaviors as bhv
import wfs_utilities as utils


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

    # Take cfg.RANDOM_SEED_A, add 6 zeros to it, and then increment it 
    # by one. (E.g., with a random seed of 3, the first personal ID 
    # will be 3000001).
    cfg.EMP_ID_STARTING_VALUE = int(cfg.RANDOM_SEED_A * 1000000 + 1)


class Person_class:
    """
    Defines the Person class.
    """

    def __init__(self):
        """
        Initialization function for the Person class.
        """

        # --------------------------------------------------------------
        # Unique identifier for the person.
        # --------------------------------------------------------------

        # Assign an emp_id number that's one higher than the max number 
        # already used (or that equals "EMP_ID_STARTING_VALUE", if this 
        # is the first Person class person object to be created).
        if len(cfg.persons) == 0:
            self.per_id = cfg.EMP_ID_STARTING_VALUE
        else:
            self.per_id = max(cfg.persons[p].per_id for p in cfg.persons ) + 1

        # --------------------------------------------------------------
        # Sex, age, and other basic demographic traits.
        # --------------------------------------------------------------

        # Sex is randomly chosen from among "M" or "F".
        self.sex = random.choice(["M", "F"])

        # Randomly select the person's first and last name.
        if self.sex == "M":
            self.f_name = random.choice(cfg.FIRST_NAMES_M)
            self.l_name = random.choice(cfg.LAST_NAMES_M)
        else:
            self.f_name = random.choice(cfg.FIRST_NAMES_F)
            self.l_name = random.choice(cfg.LAST_NAMES_F)

        # Each person begins with a random age within the min-max range.
        self.age = cfg.MIN_PERSON_AGE + random.randint(
            0, cfg.MAX_PERSON_AGE - cfg.MIN_PERSON_AGE
            )

        # Each worker is assigned to one of several discrete
        # "Workstyle" groups that determine whether the person has
        # (1) elevated, average, or reduced daily Efficacy; (2) stable 
        # or variable daily Efficacy; (3) an elevated, average, or 
        # reduced number of Sacrifice behaviors, and (4) an elevated, 
        # average, or reduced number of Sabotage behaviors (in 
        # comparison to someone who otherwise has the same base stats).
        #
        # First, get the actual Workstyle group assignment probabilities
        # for a person of the given age and sex.
        if self.sex == "M":
            if self.age < 38:
                workstyle_prob_A = cfg.WORKSTYLE_PROB_YOUNGER_MALE_A
                workstyle_prob_B = cfg.WORKSTYLE_PROB_YOUNGER_MALE_B
                workstyle_prob_C = cfg.WORKSTYLE_PROB_YOUNGER_MALE_C
                workstyle_prob_D = cfg.WORKSTYLE_PROB_YOUNGER_MALE_D
            else:
                workstyle_prob_A = cfg.WORKSTYLE_PROB_OLDER_MALE_A
                workstyle_prob_B = cfg.WORKSTYLE_PROB_OLDER_MALE_B
                workstyle_prob_C = cfg.WORKSTYLE_PROB_OLDER_MALE_C
                workstyle_prob_D = cfg.WORKSTYLE_PROB_OLDER_MALE_D
        elif self.sex == "F":
            if self.age < 38:
                workstyle_prob_A = cfg.WORKSTYLE_PROB_YOUNGER_FEMALE_A
                workstyle_prob_B = cfg.WORKSTYLE_PROB_YOUNGER_FEMALE_B
                workstyle_prob_C = cfg.WORKSTYLE_PROB_YOUNGER_FEMALE_C
                workstyle_prob_D = cfg.WORKSTYLE_PROB_YOUNGER_FEMALE_D
            else:
                workstyle_prob_A = cfg.WORKSTYLE_PROB_OLDER_FEMALE_A
                workstyle_prob_B = cfg.WORKSTYLE_PROB_OLDER_FEMALE_B
                workstyle_prob_C = cfg.WORKSTYLE_PROB_OLDER_FEMALE_C
                workstyle_prob_D = cfg.WORKSTYLE_PROB_OLDER_FEMALE_D

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

        # --------------------------------------------------------------
        # Stats for relatively stable personal traits (core stats).
        # --------------------------------------------------------------

        # Health.
        self.stat_health = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Commitment.
        self.stat_commitment = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Perceptiveness.
        self.stat_perceptiveness = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Dexterity.
        self.stat_dexterity = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Sociality.
        self.stat_sociality = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Goodness.
        self.stat_goodness = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Strength. This is a "control stat" that has no effect on anything.
        self.stat_strength = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )
        # Openmindedness. This is a "control stat" that has no effect on anything.
        self.stat_openmindedness = generate_personal_stat(
            cfg.OTHER_STATS_STAT_MEAN, cfg.OTHER_STATS_STAT_SDEV
            )

        # --------------------------------------------------------------
        # Base probabilities for generating particular types of actual
        # behaviors or recording actions (before situational modifiers).
        # --------------------------------------------------------------
 
        # Base probability of generating a Presence behavior.
        self.prob_base_presence = \
            cfg.BASE_RATE_ATTENDANCE + \
                (self.stat_health + self.stat_commitment)/2.0 \
                    * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating an Idea behavior.
        self.prob_base_idea = \
            cfg.BASE_RATE_IDEA + self.stat_perceptiveness \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Lapse behavior.
        self.prob_base_lapse = \
            cfg.BASE_RATE_LAPSE - self.stat_perceptiveness \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Feat behavior.
        self.prob_base_feat = \
            cfg.BASE_RATE_FEAT + self.stat_dexterity \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Slip behavior.
        self.prob_base_slip = \
            cfg.BASE_RATE_SLIP - self.stat_dexterity \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Teamwork behavior.
        self.prob_base_teamwork = \
            cfg.BASE_RATE_TEAMWORK + self.stat_sociality \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Disruption behavior.
        self.prob_base_disruption = \
            cfg.BASE_RATE_DISRUPTION - self.stat_sociality \
                * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Sacrifice behavior.
        self.prob_base_sacrifice = \
            cfg.BASE_RATE_SABOTAGE + \
                (self.stat_goodness + self.stat_commitment)/2.0  \
                    * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating a Sabotage behavior.
        self.prob_base_sabotage = \
            cfg.BASE_RATE_SABOTAGE - \
                (self.stat_goodness + self.stat_commitment)/2.0  \
                    * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base Efficacy level.
        self.level_base_efficacy = \
            cfg.BASE_RATE_EFFICACY + \
                (self.stat_dexterity + self.stat_commitment)/2.0 \
                    * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # Base probability of generating an accurate Good or Poor record, as a 
        # manager (i.e., of generating a True Positive or True Negative record).
        self.prob_base_recording_accurately = \
            cfg.BASE_RATE_RECORDING_ACCURACY + \
                (self.stat_perceptiveness \
                        + self.stat_commitment \
                        + self.stat_goodness
                    )/3.0 * cfg.STAT_TO_PROB_MOD_CONV_FACTOR

        # --------------------------------------------------------------
        # Initialize modified probabilities, which will be recalculated 
        # later in functions to take situational modifiers into account.
        # --------------------------------------------------------------
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
        self.prob_modified_recording_accurately \
            = self.prob_base_recording_accurately

        # --------------------------------------------------------------
        # Derived (calculated) summary capacities.
        # --------------------------------------------------------------

        # This is general managerial capacity (calculated as an 
        # arithmetic mean).
        self.MNGR_CAP = np.average(
            a=[
                self.stat_health,
                self.stat_commitment,
                self.stat_perceptiveness,
                self.stat_goodness,
                ],
            # Attendance is so crucial that below its components are 
            # weighted more heavily than other traits.
            weights=[
                4,
                4,
                3,
                3,
                ]
            )

        # This is general worker capacity (calculated as an arithmetic 
        # mean).
        self.WRKR_CAP = np.average(
            a=[
                self.stat_health,
                self.stat_commitment,
                self.stat_dexterity,
                self.stat_goodness,
                self.stat_perceptiveness,
                self.stat_sociality,
                ],
            # Attendance is so crucial that below its components are 
            # weighted more heavily than other traits.
            weights=[
                4,
                4,
                3,
                3,
                2,
                2,
                ]
            )

        # --------------------------------------------------------------
        # Organizational traits and relationships.
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------
        # Activity data generated for the person each day the simulation
        # is run.
        # --------------------------------------------------------------

        # Full details of a person's actual behaviors and recorded 
        # behaviors are stored in one organization-wide DataFrame, not
        # directly in the Person object.

        # --------------------------------------------------------------
        # Personal metrics of actual behaviors during the simulated 
        # period.
        # --------------------------------------------------------------

        # Number of days on which a person was present during the 
        # simulated period.
        self.days_attended = 0

        # The lowest daily Efficacy generated by the person during the 
        # simulated period.
        self.eff_bhv_act_min = ""

        # The highest daily Efficacy generated by the person during the 
        # simulated period.
        self.eff_bhv_act_max = ""

        # The mean daily Efficacy generated by the person during the 
        # simulated period.
        self.eff_bhv_act_mean = ""

        # The SD of daily Efficacy generated by the person during the 
        # simulated period.
        self.eff_bhv_act_sd = ""

        # The number of Good behaviors generated by the person during 
        # the simulated period.
        self.good_act_num = ""

        # The number of Poor behaviors generated by the person during 
        # the simulated period.
        self.poor_act_num = ""

        # --------------------------------------------------------------
        # Dictionaries for certain behavior and record types, for 
        # storing the number of events of a given type occurring on each
        # day.
        # --------------------------------------------------------------

        # Such dictionaries are only created for the selected types of 
        # behaviors and records listed below, because these are the only 
        # ones that have been needed thus far.
        # 
        # Some particular types of behaviors generated and records 
        # received need to be tracked, e.g., beacuse they can alter the 
        # probability of a person's later behaviors -- and when 
        # attempting to determine what sort of behaviors a person had in
        # previous days, it's faster and easier to check these simple, 
        # internally-stored dicts for the given person than to sift
        # through the entire behavs_act_df for all persons.

        self.dict_days_with_actual_eff_values \
            = {key: None for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    +  cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_recorded_eff_values \
            = {key: None for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_idea_behaviors \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    +  cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_lapse_behaviors \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_slip_behaviors \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    +  cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_teamwork_behaviors \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    +  cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_absences_recorded \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_lapses_recorded \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_sabotages_recorded \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_slips_recorded \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_disruptions_recorded \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }
        self.dict_days_with_num_of_FN_good_records \
            = {key: 0 for key in list(range(
                cfg.day_of_sim_iter_for_first_simulated_day,
                cfg.day_of_sim_iter_for_first_simulated_day \
                    + cfg.NUM_OF_DAYS_TO_SIMULATE
                )) }

    def __str__(self):
        """
        Print/display function that overrides the default behavior of 
        simply displaying unhelpful object info when "print" is called.

        PARAMETERS
        ----------
        self
        """

        return self.f_name + " " + self.l_name + " (" + str(self.per_id) + ")"

    def attributes_to_dict(self) -> dict:
        """
        Sends selected traits to a dictionary for DataFrame creation.
        This determines which attributes will be transmitted when a 
        special dictionary is created, for conversion into an 
        easy-to-use DataFrame.

        PARAMETERS
        ----------
        self
        """

        # This converts a list of colleague Person objects into a list 
        # of the persons' ID numbers.
        colleague_ids_lambda \
            = lambda x : [y.per_id for y in x] if x is not None else None

        return {
            "Person object": self,
            cfg.PERSON_ID_HEADER_TERM: self.per_id,
            cfg.FIRST_NAME_HEADER_TERM: self.f_name,
            cfg.LAST_NAME_HEADER_TERM: self.l_name,
            cfg.SEX_HEADER_TERM: self.sex,
            cfg.AGE_HEADER_TERM: self.age,
            "Separated": self.separated,
            cfg.SPHERE_HEADER_TERM: self.sphere.title,
            cfg.SHIFT_HEADER_TERM: self.shift.title,
            cfg.TEAM_HEADER_TERM: self.team.title,
            cfg.ROLE_HEADER_TERM: self.role.title,
            cfg.MNGR_CAP_HEADER_TERM: self.MNGR_CAP,
            cfg.WRKR_CAP_HEADER_TERM: self.WRKR_CAP,
            "Sub Workstyle": self.workstyle,
            cfg.SUPERVISOR_CAP_HEADER_TERM: self.sup,
            "Sup Age": self.sup_age,
            cfg.COLLEAGUES_CAP_HEADER_TERM: self.colleagues,
            "Colleagues’ IDs": colleague_ids_lambda(self.colleagues),
            "Sub Same-Sex Colleagues Prtn": self.colleagues_of_same_sex_prtn,
            cfg.SUBORDINATES_HEADER_TERM: self.subs,
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

def generate_personal_stat(mean_u, sd_u):
    """
    The stat-generator function. This defines a personal stat that uses 
    the arguments for the mean and standard deviation for the stat.

    PARAMETERS
    ----------
    mean_u
        The mean value for the stat to be generated
    sd_u
        The standard deviation for the stat to be generated
    """

    # Here "loc" is the mean, "scale" is SD, and "size" is the quantity 
    # of numbers to generate.
    randomized_base_for_stat \
        = round(float( np.random.normal(loc=mean_u, scale=sd_u, size=1)) , 3)

    # It's possible for the number generated above to be < 0 or > 1;
    # below we ensure that the values fall between 0.0 and 1.0.
    adjusted_stat = randomized_base_for_stat

    if randomized_base_for_stat < 0:
        adjusted_stat = 0.0

    elif randomized_base_for_stat > 1:
        # Keep rerolling the stat until it generates a value ≤ 1.0. It's
        # necessary to handle it in this way, because if we simply 
        # forced all values ≥ 1.0 to be equal to 1.0, it would result in
        # a bizarre preponderance of 1.0 values. The method used here 
        # will maintain a more normal distribution.
        while randomized_base_for_stat > 1:
            randomized_base_for_stat = round(float(
                    np.random.normal(loc=mean_u, scale=sd_u, size=1)),
                3)
            adjusted_stat = randomized_base_for_stat

    return adjusted_stat


def create_initial_population_of_persons():
    """
    Creates the initial population of persons (who will not yet have 
    their final roles or tasks assigned). Creates the dictionary of 
    persons, in which each entry (person) is a separate person object of
    the Person class.
    """

    # Calculate the total number of members of the workforce community.
    # This takes the total number of "Laborers" proper (and not persons 
    # more generally) who should be part of each team; adds 1 (for the 
    # Team Leader); multiplies that by the number of teams per shift 
    # times 3 (since there are 3 shifts); and then adds 4 (for the 
    # 3 Shift Managers and 1 Production Director).
    cfg.SIZE_OF_COMM_INITIAL = \
        (cfg.NUM_OF_LABORERS_PER_TEAM + 1) \
            * (cfg.NUM_OF_TEAMS_PER_SHIFT * 3) \
        + 4

    cfg.persons = defaultdict(list)

    # Populate the community.
    for i in range(0, cfg.SIZE_OF_COMM_INITIAL):
        cfg.persons[i] = Person_class()
        # print(cfg.persons[i])


def create_df_with_selected_attributes_of_all_persons():
    """
    Returns a DataFrame with selected attributes for all persons.
    The particular personal attributes that are transmitted into this DF
    are defined in the Person class's "attributes_to_dict()" func.
    """

    persons_dict_for_df \
        = [cfg.persons[k].attributes_to_dict() for k in cfg.persons]
    cfg.persons_df = pd.DataFrame(persons_dict_for_df)
    return cfg.persons_df


class Role_class:
    """
    Defines the Role class.
    """

    def __init__(self):
        """
        Initialization function for the Role class.

        PARAMETERS
        ----------
        self
        """
        self.title = "unspecified"

    def __str__(self):
        """
        Print/display function that overrides the default behavior of 
        simply displaying unhelpful object info when "print" is called.

        PARAMETERS
        ----------
        self
        """
        return self.title


def create_all_possible_roles():
    """
    Creates the initial set of potential roles. Creates the dictionary 
    of roles, in which each entry (role) is a separate role object of 
    the Role class.
    """

    cfg.roles = defaultdict(list)

    # Populate the potential roles. Create one role object corresponding
    # to each of the items in the AVAILABLE_ROLE_TITLES list.
    for i in range(len(cfg.AVAILABLE_ROLE_TITLES)):
        cfg.roles[i] = Role_class()
        cfg.roles[i].title = cfg.AVAILABLE_ROLE_TITLES[i]


def assign_initial_role_to_each_person():
    """
    Assigns a role to each member of the community.
    """

    # ------------------------------------------------------------------
    # Assign the "Production Director" role to the 1 person
    # with the highest managerial capacity score.
    # ------------------------------------------------------------------

    # Sort the DataFrame of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(
        cfg.persons_df, cfg.MNGR_CAP_HEADER_TERM
        )

    # Identify the index of the person on the first row of the DF.
    person_index = persons_df_sorted.index[0]

    # Get the (first) role object with title "Production Director", and
    # assign it to the relevant person as his cfg.persons[x].role.
    cfg.persons[person_index].role \
        = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title \
            == cfg.PRODUCTION_DIRECTOR_TERM) ]

    # ------------------------------------------------------------------
    # Assign the "Shift Manager" role to the 3 persons
    # with the next highest managerial capacity scores.
    # ------------------------------------------------------------------

    # Identify the indices of the next three persons in the DF, then
    # get the (first) role object with title "Shift Manager", and
    # assign it to the relevant persons as their cfg.persons[x].role.
    for i in range(1, 1+3):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].role \
            = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title \
                == cfg.SHIFT_MANAGER_TERM) ]

    # ------------------------------------------------------------------
    # Assign the "Team Leader" roles to the first N persons (in the
    # original, random -- unsorted -- persons dict, not the sorted DF)
    # who don't yet have a role (i.e., who aren't a "Production 
    # Director" or "Shift Manager").
    # ------------------------------------------------------------------

    # Multiply the NUM_OF_TEAMS_PER_SHIFT * 3, since there are three 
    # shifts.
    num_of_remaining_team_leaders_to_be_designated \
        = cfg.NUM_OF_TEAMS_PER_SHIFT * 3
    for i in cfg.persons:
        if num_of_remaining_team_leaders_to_be_designated > 0:
            if cfg.persons[i].role == "":
                cfg.persons[i].role \
                    = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title \
                        == cfg.TEAM_LEADER_TERM) ]
                num_of_remaining_team_leaders_to_be_designated -= 1

    # ------------------------------------------------------------------
    # Assign the "Laborer" role to all persons who don't yet have a 
    # role.
    # ------------------------------------------------------------------

    # Get the (first) role object with title "Laborer", and
    # assign it to the relevant person as his cfg.persons[x].role.
    for i in cfg.persons:
        if cfg.persons[i].role == "":
            cfg.persons[i].role \
                = cfg.roles[ next(x for x in cfg.roles if cfg.roles[x].title \
                    == cfg.LABORER_TERM) ]


class Shift_class:
    """
    Defines the Shift class.
    """

    def __init__(self):
        """
        Initialization function for the Shift class.

        PARAMETERS
        ----------
        self
        """
        self.title = "unspecified"

    def __str__(self):
        """
        Print/display function that overrides the default behavior of 
        simply displaying unhelpful object info when "print" is called.

        PARAMETERS
        ----------
        self
        """
        return self.title


def create_shift_objects():
    """
    Creates the initial set of shifts. Creates the dictionary of shifts,
    in which each entry (shift) is a separate shift object of the Shift 
    class.
    """

    cfg.shifts = defaultdict(list)

    # Populate the shifts dict. Create one shift object corresponding to
    # each of the items in the available_shifts list.
    for i in range(len(cfg.AVAILABLE_SHIFT_TITLES)):
        cfg.shifts[i] = Shift_class()
        cfg.shifts[i].title = cfg.AVAILABLE_SHIFT_TITLES[i]


def assign_initial_shift_to_each_person():
    """
    Assigns a shift to each member of the community.
    """

    # ------------------------------------------------------------------
    # Assign the shift "unassigned" to the "Production director" and 
    # Shifts 1-3 to the three "Shift Managers".
    # ------------------------------------------------------------------

    # Sort the DataFrame of persons by descending managerial capacity.
    # The first entries will be the "Production Director" and "Shift 
    # Managers".
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted \
        = utils.sort_df_by_given_field_descending(
            cfg.persons_df, cfg.MNGR_CAP_HEADER_TERM
            )

    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].shift \
            = cfg.shifts[ next(x for x in cfg.shifts if cfg.shifts[x].title \
                == cfg.AVAILABLE_SHIFT_TITLES[i]) ]

    # ------------------------------------------------------------------
    # Step through all "Team Leaders" and, for those who don't yet have 
    # a shift assigned, assign them to Shifts 1-3. It's important to use
    # the unordered "cfg.persons" dictionary rather than the DF sorted 
    # by capacity.
    # ------------------------------------------------------------------

    # This list tracks how many Team Leaders still need to be assigned
    # for each of the three "regular" shifts. It includes an initial 0 
    # to represent the special "unassigned" shift, which doesn't need 
    # any additional members to be assigned to it.
    num_of_leaders_to_assign_per_shift = [
        0,
        cfg.NUM_OF_TEAMS_PER_SHIFT,
        cfg.NUM_OF_TEAMS_PER_SHIFT,
        cfg.NUM_OF_TEAMS_PER_SHIFT
        ]

    # Start with cfg.shifts[1], which is "Shift 1".
    for s in range( 1, (len(cfg.shifts)) ):
        for i in cfg.persons:
            if num_of_leaders_to_assign_per_shift[s] > 0:
                if cfg.persons[i].shift == "":
                    cfg.persons[i].shift = cfg.shifts[s]
                    num_of_leaders_to_assign_per_shift[s] -= 1

    # ------------------------------------------------------------------
    # Step through all "Laborers" and, for those who don't yet have a 
    # shift assigned, assign them to Shifts 1-3. It's important to use 
    # the unordered "cfg.persons" dictionary rather than the DF sorted 
    # by capacity.
    # ------------------------------------------------------------------

    # Calculate the number of Laborers proper (not persons more 
    # generally) who should be a part of each shift.
    # Subtract 4 from the size of the community, since the Production 
    # Director and Shift Managers have already been assigned to shifts.
    # Divide by 3, which is the number of shifts.
    # Subtract 8 (for the number of teams, and thus Team Leaders, in the
    # shift), since each shift has already received a Team Leader who's 
    # not an ordinary Laborer.
    cfg.NUM_OF_LABORERS_PER_SHIFT \
        = ( (cfg.SIZE_OF_COMM_INITIAL - 4) / 3 ) - cfg.NUM_OF_TEAMS_PER_SHIFT

    # This list tracks how many Laborers still need to be assigned
    # for each of the three "regular" shifts. It includes an initial 0 
    # to represent the special "unassigned" shift, which doesn't need 
    # any additional members to be assigned to it.
    num_of_laborers_to_assign_per_shift = [
        0,
        cfg.NUM_OF_LABORERS_PER_SHIFT,
        cfg.NUM_OF_LABORERS_PER_SHIFT,
        cfg.NUM_OF_LABORERS_PER_SHIFT
        ]

    # Start with cfg.shifts[1], which is "Shift 1".
    for s in range( 1, (len(cfg.shifts)) ):
        for i in cfg.persons:
            if num_of_laborers_to_assign_per_shift[s] > 0:
                if cfg.persons[i].shift == "":
                    cfg.persons[i].shift = cfg.shifts[s]
                    num_of_laborers_to_assign_per_shift[s] -= 1


class Team_class:
    """
    Defines the Team class.
    The "NUM_OF_TEAMS_PER_SHIFT" variable has already been given
    a value, as part of the workforce setup.
    """

    def __init__(self):
        """
        Initialization function for the Team class.

        PARAMETERS
        ----------
        self
        """

        self.title = "unspecified"
        self.shift = ""


    def __str__(self):
        """
        Print/display function that overrides the default behavior of 
        simply displaying unhelpful object info when "print" is called.

        PARAMETERS
        ----------
        self
        """
        return self.title


def create_team_objects():
    """
    Creates the initial set of teams. Creates the dictionary of teams, 
    in which each entry (team) is a separate team object in the Team 
    class.
    """

    cfg.teams = defaultdict(list)

    # Populate the teams dict. Create one teams object corresponding to 
    # each number in len(cfg.NUM_OF_TEAMS_PER_SHIFT).

    # The first team will be the "unassigned" team object.
    cfg.teams[0] = Team_class()
    cfg.teams[0].title = "unassigned"

    # Now we create all of the remaining, "regular" teams.
    # Here we add 1, since entry 0 is the special case just defined 
    # above. We multiply by 3, since there are three shifts.
    for i in range(1, cfg.NUM_OF_TEAMS_PER_SHIFT * 3 + 1):
        cfg.teams[i] = Team_class()
        cfg.teams[i].title = "Team " + str(i)

    # Indicate the shift that each team belongs to.
    for i in range(0, cfg.NUM_OF_TEAMS_PER_SHIFT + 1):
        cfg.teams[i].shift = cfg.SHIFT_1_TERM
    for i in range(
            cfg.NUM_OF_TEAMS_PER_SHIFT + 1, 
            cfg.NUM_OF_TEAMS_PER_SHIFT * 2 + 1):
        cfg.teams[i].shift = cfg.SHIFT_2_TERM
    for i in range(
            cfg.NUM_OF_TEAMS_PER_SHIFT * 2 + 1, 
            cfg.NUM_OF_TEAMS_PER_SHIFT * 3 + 1):
        cfg.teams[i].shift = cfg.SHIFT_3_TERM


def assign_initial_team_to_each_person():
    """
    Assigns a team to each member of the community.
    """

    # ------------------------------------------------------------------
    # Assign the team "unassigned" to the "Production Director" and 
    # "Shift Managers".
    # ------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(
        cfg.persons_df, 
        cfg.MNGR_CAP_HEADER_TERM
        )

    # The first entries will be the "Production Director" and "Shift 
    # Managers". They all have the "unassigned" team.
    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].team \
            = cfg.teams[ next(x for x in cfg.teams if cfg.teams[x].title \
                == "unassigned") ]

    # ------------------------------------------------------------------
    # Set up a means of tracking which teams still need to have a leader
    # or ordinary laborers assigned to them.
    # ------------------------------------------------------------------

    # This list tracks how many Laborers proper still need to be 
    # assigned to each team. Each team begins by needing a full 
    # complement of Laborers.
    # We begin with a list entry for the special "unassigned" team,
    # which doesn't need any laborers to be added.
    num_of_laborers_needed = [0]
    for i in range(cfg.NUM_OF_TEAMS_PER_SHIFT * 3):
        num_of_laborers_needed.append(cfg.NUM_OF_LABORERS_PER_TEAM)

    # This list tracks how many Team Leaders still need to be assigned
    # to each team. Each team begins by needing 1 Team Leader.
    # We begin with a list entry for the special "unassigned" team,
    # which doesn't need any Team leaders to be added.
    cfg.num_of_leaders_needed = [0]
    for i in range(cfg.NUM_OF_TEAMS_PER_SHIFT * 3):
        cfg.num_of_leaders_needed.append(1)

    # ------------------------------------------------------------------
    # Step through all persons (first Team Leaders, then Laborers) and, 
    # for those who don't yet have a team assigned, assign them to the 
    # first team that still needs persons of the relevant sort to be 
    # added.
    #
    # #It's important to use the unordered "cfg.persons" dictionary 
    # rather than the DataFrame sorted by capacity.
    # ------------------------------------------------------------------

    # For simplicity's sake, we can begin with cfg.teams[0], which is 
    # the special "unassigned" team. It won't actually receive any new 
    # members, though, as we've already specified above that it doesn't 
    # need any more Team Leaders added to it.
    for t in range (0, len(cfg.teams) ):

        # Handle each shift in turn, beginning with cfg.shifts[1] 
        # (not cfg.shifts[0], which is the "unassigned" shift).
        for s in range (1, len(cfg.shifts) ):

            # For each team in the given shift...
            if cfg.teams[t].shift == cfg.shifts[s].title:

                # Iterate through all persons to deal with all Team 
                # Leaders...
                for p in cfg.persons:

                    # If the team doesn't yet have an assigned Team 
                    # Leader, and the current person is a Team Leader, 
                    # assign him to the given team.
                    if cfg.num_of_leaders_needed[t] > 0:

                        if (cfg.persons[p].shift.title \
                                    == cfg.shifts[s].title) \
                                and (cfg.persons[p].role.title \
                                    == cfg.TEAM_LEADER_TERM) \
                                and (cfg.persons[p].team == ""):

                            cfg.persons[p].team = cfg.teams[t]

                            # NOTE! This line isn't used yet.
                            cfg.persons[p].sphere = str(t)

                            cfg.num_of_leaders_needed[t] -= 1

                # Iterate through all persons to deal with all 
                # Laborers...
                for p in cfg.persons:

                    # If the team doesn't yet have all its Laborers, and
                    # the current person is a Laborer, assign him to the
                    # given team.
                    if num_of_laborers_needed[t] > 0:

                        if (cfg.persons[p].shift.title \
                                    == cfg.shifts[s].title) \
                                and (cfg.persons[p].role.title \
                                    == cfg.LABORER_TERM) \
                                and (cfg.persons[p].team == ""):

                            cfg.persons[p].team = cfg.teams[t]

                            # NOTE! This line isn't used yet.
                            cfg.persons[p].sphere = str(t)

                            num_of_laborers_needed[t] -= 1


class Sphere_class:
    """
    Defines the Sphere class.
    """

    def __init__(self):
        """
        Initialization function for the Sphere class.

        PARAMETERS
        ----------
        self
        """
        self.title = "unspecified"


    def __str__(self):
        """
        Print/display function that overrides the default behavior of 
        simply displaying unhelpful object info when "print" is called.

        PARAMETERS
        ----------
        self
        """
        return self.title


def create_all_possible_spheres():
    """
    Creates the initial set of all possible spheres.
    Create the dictionary of spheres, in which each entry (sphere)
    is a separate sphere object in the Sphere class.
    """

    cfg.spheres = defaultdict(list)

    # Populate the spheres. Create one sphere object corresponding to 
    # each of the items in the AVAILABLE_SPHERE_TITLES list.
    for i in range(len(cfg.AVAILABLE_SPHERE_TITLES)):
        cfg.spheres[i] = Sphere_class()
        cfg.spheres[i].title = cfg.AVAILABLE_SPHERE_TITLES[i]


def assign_initial_sphere_to_each_person():
    """
    Assigns a sphere to each member of the community.
    """

    # ------------------------------------------------------------------
    # Assign the sphere "general management" to the "Production 
    # Director" and "Shift Managers".
    # ------------------------------------------------------------------

    # Sort the DF of persons by descending managerial capacity.
    cfg.persons_df = create_df_with_selected_attributes_of_all_persons()
    persons_df_sorted = utils.sort_df_by_given_field_descending(
        cfg.persons_df, 
        cfg.MNGR_CAP_HEADER_TERM
        )

    # The first entries will be the "Production Director" and "Shift 
    # Managers". They all have the "unassigned" team.
    for i in range(0, 4):
        person_index = persons_df_sorted.index[i]
        cfg.persons[person_index].sphere \
            = cfg.spheres[ next(x for x in cfg.spheres if cfg.spheres[x].title \
                == "general management") ]

    # ------------------------------------------------------------------
    # Assign a sphere to all remaining persons who don't yet have one.
    # ------------------------------------------------------------------

    # Rather than directly calculating which sphere a given person works
    # in, it's easier to instead calculate which sphere a particular 
    # *team* is focused on, and to then assign the given sphere to all 
    # members of that team.
    #
    # Here we first determine which sphere applies to each of the 
    # workforce's teams.

    # The first team is ascribed to sphere 0, the "unassigned" sphere.
    cfg.sphere_of_given_team = [0]

    # For each of the teams (after team 0), we calculate which sphere it
    # has by iterating through the list of spheres and adding each to 
    # the sphere_of_given_team list for however many teams are supposed 
    # to have that sphere in each shift (as specified in 
    # teams_per_sphere_per_shift above).
    #
    # That process is then repeated for shifts 2 and 3.
    for s in range(0, 3):
        for sp in range( len(cfg.spheres) ):
            cfg.sphere_of_given_team.extend(
                [sp] * cfg.teams_per_sphere_per_shift[sp]
                )

    # Here I can begin with t=1, as t=0 is a special case ("general 
    # management") that has already been handled above.
    for t in range (1, len(cfg.teams) ):

        # Handle each shift in turn, beginning with cfg.shifts[1] 
        # (not cfg.shifts[0], which is the "unassigned" shift).
        for s in range (1, len(cfg.shifts) ):

            # For each team in the given shift...
            if cfg.teams[t].shift == cfg.shifts[s].title:

                # Iterate through all persons. This catches both Team 
                # Leaders and regular Laborers.
                for p in cfg.persons:

                    if (cfg.persons[p].shift.title == cfg.shifts[s].title) \
                        and (cfg.persons[p].team.title == cfg.teams[t].title):

                            # NOTE! The line below isn't used yet.
                            cfg.persons[p].sphere \
                                = cfg.spheres[ cfg.sphere_of_given_team[t] ]


def assign_supervisor_to_each_person():
    """
    Populates the "Supervisor" attribute for all persons.
    """

    for i in cfg.persons:

        # Specify supervisor for separated persons.
        if cfg.persons[i].separated is True:
            cfg.persons[i].sup = None

        # Specify supervisor for Production Director.
        elif cfg.persons[i].role.title == cfg.PRODUCTION_DIRECTOR_TERM:
            cfg.persons[i].sup = None

        # Specify supervisor for Shift Managers.
        elif cfg.persons[i].role.title == cfg.SHIFT_MANAGER_TERM:
            # Attach the person object for the Production Director.
            cfg.persons[i].sup \
                = cfg.persons[ next(
                    x for x in cfg.persons if cfg.persons[x].role.title \
                        == cfg.PRODUCTION_DIRECTOR_TERM
                        )]

        # Specify supervisor for Team Leaders.
        elif cfg.persons[i].role.title == cfg.TEAM_LEADER_TERM:
            # Attach the person object for the Shift Manager of the 
            # laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if ( 
                (cfg.persons[x].role.title == cfg.SHIFT_MANAGER_TERM) \
                and (cfg.persons[x].shift == cfg.persons[i].shift) \
                and (cfg.persons[x].separated is False)
                ))]

        # Specify supervisor for Laborers.
        elif cfg.persons[i].role.title == cfg.LABORER_TERM:
            # Attach the person object for the Team Leader of the Laborer's team.
            cfg.persons[i].sup = cfg.persons[ next(x for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.TEAM_LEADER_TERM) \
                and (cfg.persons[x].team == cfg.persons[i].team) \
                and (cfg.persons[x].separated is False)
                ))]


def assign_subordinates_to_all_supervisors():
    """
    Populates the "Subordinates" attribute for all persons.
    """

    for i in cfg.persons:

        # Specify subordinates for separated persons.
        if cfg.persons[i].separated is True:
            cfg.persons[i].subs = None

        # Specify subordinates for Production Director.
        elif cfg.persons[i].role.title == cfg.PRODUCTION_DIRECTOR_TERM:
            subs_temp_list = []
            subs_temp_list.append(
                [cfg.persons[x] for x in cfg.persons if cfg.persons[x].role.title \
                    == cfg.SHIFT_MANAGER_TERM]
                )
            # The line below converts the nested list into a simple 
            # one-level list.
            subs_temp_list \
                = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # Specify subordinates for Shift Managers.
        elif cfg.persons[i].role.title == cfg.SHIFT_MANAGER_TERM:
            subs_temp_list = []
            subs_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.TEAM_LEADER_TERM) \
                and (cfg.persons[x].shift.title == cfg.persons[i].shift.title) \
                and (cfg.persons[x].separated is False)
                )])
            subs_temp_list \
                = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # Specify subordinates for Team Leaders.
        elif cfg.persons[i].role.title == cfg.TEAM_LEADER_TERM:
            subs_temp_list = []
            subs_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.LABORER_TERM) \
                and (cfg.persons[x].team.title == cfg.persons[i].team.title) \
                and (cfg.persons[x].separated is False)
                )])
            subs_temp_list \
                = [item for internal_list in subs_temp_list for item in internal_list]
            cfg.persons[i].subs = subs_temp_list

        # Specify subordinates for Laborers.
        elif cfg.persons[i].role.title == cfg.LABORER_TERM:
            cfg.persons[i].subs = None


def assign_colleagues_to_all_persons():
    """
    Populates the "Colleagues" attribute for all persons.
    """

    # A person's "colleagues" includes those individuals at the same 
    # level (i.e., in the same role) who are in the same relevant 
    # organizational unit as the person.
    #
    # For ordinary Laborers, collagues are the other ordinary Laborers 
    # in the same team (but *not* the Team Leader).
    #
    # For Team Leaders, collagues are the other Team Leaders in the
    # same shift (but *not* the Shift Manager).
    #
    # For Shift Managers, collagues are the other Shift Managers.
    #
    # For the Production Director, colleagues = None

    for i in cfg.persons:

        # Specify colleagues for separated persons.
        if cfg.persons[i].separated is True:
            cfg.persons[i].colleagues = None

        # Specify colleagues for Production Director.
        elif cfg.persons[i].role.title == cfg.PRODUCTION_DIRECTOR_TERM:
            cfg.persons[i].colleagues = None

        # Specify colleagues for Shift Managers.
        elif cfg.persons[i].role.title == cfg.SHIFT_MANAGER_TERM:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.SHIFT_MANAGER_TERM) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id)
                )])
            # The line below converts the nested list into a simple 
            # one-level list.
            colleagues_temp_list \
                = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list

        # Specify colleagues for Team Leaders.
        elif cfg.persons[i].role.title == cfg.TEAM_LEADER_TERM:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.TEAM_LEADER_TERM) \
                and (cfg.persons[x].shift.title == cfg.persons[i].shift.title) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id) \
                and (cfg.persons[x].separated is False)
                )])
            colleagues_temp_list \
                = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list

        # Specify colleagues for Laborers.
        elif cfg.persons[i].role.title == cfg.LABORER_TERM:
            colleagues_temp_list = []
            colleagues_temp_list.append( [cfg.persons[x] for x in cfg.persons if (
                (cfg.persons[x].role.title == cfg.LABORER_TERM) \
                and (cfg.persons[x].team.title == cfg.persons[i].team.title) \
                # Don't include a person as being his own colleague.
                and (cfg.persons[x].per_id != cfg.persons[i].per_id) \
                and (cfg.persons[x].separated is False)
                )])
            colleagues_temp_list \
                = [item for internal_list in colleagues_temp_list for item in internal_list]
            cfg.persons[i].colleagues = colleagues_temp_list


def update_persons_colleagues_of_same_sex_prtn():
    """
    For all persons, updates the calculation of the proportion of a
    person's colleagues who are of the same sex.
    """

    for p in cfg.persons:

        # This is only relevant if the person has colleagues (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].colleagues:
            sex_this_person = cfg.persons[p].sex
            colleagues_of_this_person = cfg.persons[p].colleagues
            sex_of_colleagues_list \
                = [coll.sex for coll in colleagues_of_this_person]
            colleagues_of_same_sex_num \
                = sex_of_colleagues_list.count(sex_this_person)
            colleagues_of_same_sex_prtn = \
                colleagues_of_same_sex_num \
                / len(sex_of_colleagues_list)
            cfg.persons[p].colleagues_of_same_sex_prtn \
                = colleagues_of_same_sex_prtn


def reset_modified_probs_to_base_probs_for_all_persons():
    """
    This resets all persons' modified daily probabilities for generating
    particular types of actions to the persons' base probabilities. This
    should be done at the start of each new simulated day.
    """

    for p in cfg.persons:
        cfg.persons[p].prob_modified_presence \
            = cfg.persons[p].prob_base_presence
        cfg.persons[p].prob_modified_idea = cfg.persons[p].prob_base_idea
        cfg.persons[p].prob_modified_lapse = cfg.persons[p].prob_base_lapse
        cfg.persons[p].prob_modified_feat = cfg.persons[p].prob_base_feat
        cfg.persons[p].prob_modified_slip = cfg.persons[p].prob_base_slip
        cfg.persons[p].prob_modified_teamwork \
            = cfg.persons[p].prob_base_teamwork
        cfg.persons[p].prob_modified_disruption \
            = cfg.persons[p].prob_base_disruption
        cfg.persons[p].prob_modified_sacrifice \
            = cfg.persons[p].prob_base_sacrifice
        cfg.persons[p].prob_modified_sabotage \
            = cfg.persons[p].prob_base_sabotage
        cfg.persons[p].level_modified_efficacy \
            = cfg.persons[p].level_base_efficacy
        cfg.persons[p].prob_modified_recording_accurately \
            = cfg.persons[p].prob_base_recording_accurately


def calculate_person_modifiers_to_implement_dependencies_and_covariance():
    """
    Implements dependencies and covariance among certain stats and 
    variables by adding modifiers that adjust their previously 
    random values (e.g., to provide bonuses or penalties to Efficacy
    for certain personal or environmental factors).
    """

    for p in cfg.persons:

        # If a person is already separated from employment, do not 
        # proceed with updating that person; skip ahead to the next 
        # person.
        if cfg.persons[p].separated is True:
            continue

        # --------------------------------------------------------------
        # Update the person's probability of generating certain
        # Good or Poor behaviors.
        # --------------------------------------------------------------
 
        # If the person belongs to a relevant Workstyle group that 
        # increases or decreases his likelihood of generating Ideas, 
        # elevate or reduce his probability of
        # generating an Idea today.
        cfg.persons[p].prob_modified_idea = cfg.persons[p].prob_base_idea
        if cfg.persons[p].workstyle == "Group A":
            cfg.persons[p].prob_modified_idea = \
                cfg.persons[p].prob_modified_idea \
                    * (1 + cfg.PROB_ELEVATION_FOR_IDEA_DUE_TO_WORKSTYLE)
        elif cfg.persons[p].workstyle == "Group E":
            cfg.persons[p].prob_modified_idea = \
                cfg.persons[p].prob_modified_idea \
                    * (1 - cfg.PROB_REDUCTION_FOR_IDEA_DUE_TO_WORKSTYLE)

        # If the person belongs to a relevant Workstyle group that 
        # increases or decreases his likelihood of generating 
        # Disruptions, elevate or reduce his probability of
        # generating a Disruption today.
        cfg.persons[p].prob_modified_disruption \
            = cfg.persons[p].prob_base_disruption
        if cfg.persons[p].workstyle == "Group B":
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption \
                    * (1 + cfg.PROB_ELEVATION_FOR_DISRUPTION_DUE_TO_WORKSTYLE)
        elif cfg.persons[p].workstyle == "Group D":
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption \
                    * (1 - cfg.PROB_REDUCTION_FOR_DISRUPTION_DUE_TO_WORKSTYLE)

        # --------------------------------------------------------------
        # Increased probability of Teamworks and Disruptions
        # tied to the day of the month.
        # --------------------------------------------------------------

        # Increase a person's modified probability of generating a 
        # Teamwork or Disruption behavior if it is the 23rd day of the 
        # month or later (to simulate changes in behavior arising from 
        # the pressure to meet end-of-month production deadlines).

        # If it's not yet the 23rd day of the month, there is no effect.
        # If it's the 23rd day of the month (or later), implement the 
        # effect.
        day_num = cfg.day_of_month_1_indexed
        if day_num >= 23:

            # Calculate how many days it is beyond the 22nd day of the 
            # month.
            days_past_22nd = day_num - 22

            # The effect increases in a linear fashion, being multiplied
            # by the number of days that it is past the 22nd of the 
            # month.
            cfg.persons[p].prob_modified_teamwork = \
                cfg.persons[p].prob_modified_teamwork * \
                (1 + days_past_22nd * cfg.STRENGTH_OF_EFFECT \
                    * random.uniform(
                        0.0,
                        cfg.PROB_ELEVATION_MAX_FOR_TEAMWORK_DUE_TO_DAY_IN_MONTH
                        ))
            cfg.persons[p].prob_modified_disruption = \
                cfg.persons[p].prob_modified_disruption * \
                (1 + days_past_22nd * cfg.STRENGTH_OF_EFFECT \
                    * random.uniform(
                        0.0,
                        cfg.PROB_ELEVATION_MAX_FOR_DISRUPTION_DUE_TO_DAY_IN_MONTH
                        ))

        # --------------------------------------------------------------
        # Increased probability of a Slip tied to the day of the month.
        # --------------------------------------------------------------

        # Increase a person's modified probability of generating a 
        # Slip behavior if it is the 26th day of the month or later 
        # (to simulate changes in behavior arising from the pressure to 
        # meet end-of-month production deadlines).

        # If it's not yet the 26th day of the month, there is no effect.
        # If it's the 26th day of the month (or later), implement the 
        # effect. The value of day_num has already been calculated 
        # earlier in this function.
        if day_num >= 26:

            # Calculate how many days it is beyond the 25th day of the 
            # month.
            days_past_25th = day_num - 25

            # The effect increases in a linear fashion, being multiplied
            # by the number
            # of days that it is past the 25th of the month.
            cfg.persons[p].prob_modified_slip = \
                cfg.persons[p].prob_modified_slip * \
                (1 + days_past_25th * cfg.STRENGTH_OF_EFFECT \
                    * random.uniform(
                        0.0,
                        cfg.PROB_ELEVATION_MAX_FOR_SLIP_DUE_TO_DAY_IN_MONTH
                        ))

        # --------------------------------------------------------------
        # Calculate the modifier to a person's Efficacy score.
        # --------------------------------------------------------------

        # Get the person's base Efficacy level.
        cfg.persons[p].level_modified_efficacy \
            = cfg.persons[p].level_base_efficacy

        # Implement a bonus that increases a worker's Efficacy based 
        # on Age.
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 + cfg.persons[p].age \
                * cfg.STRENGTH_OF_EFFECT * random.uniform(
                    0.0,
                    cfg.EFF_BONUS_MAX_FROM_PERSON_AGE
                    ))

        # Implement a bonus that increases a person's Efficacy as one 
        # moves deeper into the work week (with no bonus on Monday and 
        # the greatest bonus on Friday).
        # Monday has weekday_num = 0; Friday has weekday_num = 4.
        weekday_num = cfg.current_datetime_obj.weekday()
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 + weekday_num * cfg.STRENGTH_OF_EFFECT * random.uniform(
                0.0,
                cfg.EFF_BONUS_MAX_FROM_WEEKDAY
                ))

        # Implement a bonus that increases a person's average Efficacy 
        # beginning on the 20th day of the month and then resets to zero
        # bonus on the first day of the following month.
        # If it's not yet the 20th day of the month, there is no bonus.
        # If it's the 20th day of the month (or later), add the bonus.
        # The value of day_num has already been calculated earlier in 
        # this function.
        if day_num >= 20:
            # Calculate how many days it is beyond the 19th day of the 
            # month. 
            days_past_19th = day_num - 19
            # The bonus increases in a linear fashion, being multiplied 
            # by the number of days that it is past the 19th of the 
            # month.
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + days_past_19th * cfg.STRENGTH_OF_EFFECT \
                    * random.uniform(
                        0.0,
                        cfg.EFF_BONUS_MAX_FROM_DAY_IN_MONTH
                        ))

        # Implement a penalty that reduces Efficacy in the middle of the
        # calendar year.
        # This gives the current day's place within the calendar year
        # with January 1st corresponding to 1.
        day_in_year = cfg.current_datetime_obj.timetuple().tm_yday
        # This yields 1.0 for a day in the middle of the year
        # and 0.0 for January 1st or December 31st.
        penalty_multiplier_for_current_day \
            = 1.0 - ( abs(day_in_year - 182.5) / 182.5 )
        # This penalty has no random element to it.
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 - cfg.EFF_PENALTY_MAX_FROM_SEASON_OF_YEAR \
                * cfg.STRENGTH_OF_EFFECT * penalty_multiplier_for_current_day)

        # Implement a bonus that increases a person's Efficacy as one 
        # has a higher proportion of colleagues (e.g., immediate 
        # teammates) who are of the same sex as oneself.
        # This is only relevant if the person has colleagues (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].colleagues:
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.persons[p].colleagues_of_same_sex_prtn \
                    * cfg.STRENGTH_OF_EFFECT * random.uniform(
                        0.0,
                        cfg.EFF_BONUS_MAX_FROM_TEAMMATE_SEXES
                        ))

        # Implement a penalty that decreases a person's Efficacy as the
        # difference in age between the person and his supervisor 
        # increases.
        # This is only relevant if the person has a supervisor (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].sup:
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - abs(cfg.persons[p].age - cfg.persons[p].sup.age) \
                * cfg.STRENGTH_OF_EFFECT \
                    * random.uniform(
                        0.0,
                        cfg.EFF_PENALTY_MAX_FROM_SUP_AGE_DIFF
                        ))

        # (1) Bonus/Penalty to Efficacy lavel and (2) stable or variable
        # daily Efficacy, based on a person's Workstyle group.
        #
        # Implement a bonus (or penalty) that modifies a person's 
        # Efficacy, if he is in a Workstyle group whose members display 
        # elevated or reduced (and not simply moderate) Efficacy.
        # Add a degree of daily variability to a person's Efficacy that 
        # reflects the type of daily Efficacy (stable or variable) 
        # possessed by the Workstyle group to which the person belongs.

        # Group A has elevated Efficacy.
        if cfg.persons[p].workstyle == "Group A":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.WORKSTYLE_EFF_LEVEL_MODIFIER \
                * cfg.STRENGTH_OF_EFFECT * random.uniform(0.0, 1.0))
            # Group A has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group B has elevated Efficacy.
        if cfg.persons[p].workstyle == "Group B":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.WORKSTYLE_EFF_LEVEL_MODIFIER \
                * cfg.STRENGTH_OF_EFFECT * random.uniform(0.0, 1.0))
            # Group B has variable Efficacy (i.e., add up to the max 
            # variability).
            cfg.persons[p].workstyle_eff_daily_variability = \
                cfg.WORKSTYLE_EFF_MAX_DAILY_VARIABILITY \
                * cfg.STRENGTH_OF_EFFECT

        # Group C has average Efficacy (no modifier is applied).
        if cfg.persons[p].workstyle == "Group C":
            # Group C has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group D has reduced Efficacy.
        if cfg.persons[p].workstyle == "Group D":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - cfg.WORKSTYLE_EFF_LEVEL_MODIFIER \
                * cfg.STRENGTH_OF_EFFECT * random.uniform(0.0, 1.0))
            # Group D has stable Efficacy (i.e., no added variability).
            cfg.persons[p].workstyle_eff_daily_variability = 0.0

        # Group E has reduced Efficacy.
        if cfg.persons[p].workstyle == "Group E":
            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - cfg.WORKSTYLE_EFF_LEVEL_MODIFIER \
                * cfg.STRENGTH_OF_EFFECT * random.uniform(0.0, 1.0))
            # Group E has variable Efficacy (i.e., add the max 
            # variability).
            cfg.persons[p].workstyle_eff_daily_variability = \
                cfg.WORKSTYLE_EFF_MAX_DAILY_VARIABILITY \
                * cfg.STRENGTH_OF_EFFECT

        # Bonus to Efficacy lavel based on a person having had a Good 
        # behavior (Idea, Feat, Teamwork, or Sacrifice) in the previous 
        # days that was accurately recorded by his manager (i.e., a True
        # Positive record of a Good behavior).
        mod_for_TP_FN_good \
            = bhv.return_eff_modifier_for_impact_of_previous_recordings_on_bhv_of_person_today(
                cfg.persons[p], # the Person object whose behavior may be impacted
                )
        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * mod_for_TP_FN_good


def person_object_with_given_sub_ID(sub_ID_u):
    """
    Returns the person object that possesses the inputted ID number.

    PARAMETERS
    ----------
    sub_ID_u
        The subject ID for the person object being sought
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
    print(
        "Persons in community at start of simulation: ",
        cfg.SIZE_OF_COMM_INITIAL
        )
    print("Separations during retained period: ",
        cfg.behavs_act_df["Behavior Type"].value_counts()["Separation"])
    print(
        "Unique subjects of behaviors/events in retained cfg.behavs_act_df: ",
        cfg.behavs_act_df["Sub ID"].nunique()
        )
    print(
        "Total persons in persons_df at end of simulation (including priming-period separations): ",
        len(cfg.persons_df)
        )


def rebuild_selected_personal_relationships():
    """
    At some point during the day, use each Team Leader and each 
    Laborer's designated *Role*, *Shift*, and *Team* to rebuild all 
    colleague and subordinate data for Shift Managers, Team Leaders, and
    Laborers. This is done to deal with the fact that Laborers can be 
    swapped between Teams and that Team Leaders and Laborers can be 
    separated from employment and replaced in the course of the 
    simulation.
    """

    for p in cfg.persons:

        # If the person is a Laborer...
        if (cfg.persons[p].role.title == cfg.LABORER_TERM):
            # Update the person's supervisor.
            person_sup_mono_list \
                = [cfg.persons[sup] for sup in cfg.persons if (\
                    (cfg.persons[sup].role.title == "Team Leader") \
                    & (cfg.persons[sup].separated is False) \
                    & (cfg.persons[sup].team.title \
                        == cfg.persons[p].team.title) \
                    )]
            person_sup = person_sup_mono_list[0]
            cfg.persons[p].sup = person_sup

            # Update the person's colleagues.
            colleagues_temp_list \
                = [cfg.persons[coll] for coll in cfg.persons if (\
                    (cfg.persons[coll].role.title == "Laborer") \
                    & (cfg.persons[coll].separated is False) \
                    & (cfg.persons[coll].team.title \
                        == cfg.persons[p].team.title) \
                    & (cfg.persons[coll].per_id != cfg.persons[p].per_id)
                    )]
            cfg.persons[p].colleagues = colleagues_temp_list


        # If the person is a Team Leader...
        elif (cfg.persons[p].role.title == "Team Leader"):
            # Update the person's supervisor.
            person_sup_mono_list \
                = [cfg.persons[sup] for sup in cfg.persons if (\
                    (cfg.persons[sup].role.title == "Shift Manager") \
                    & (cfg.persons[sup].separated is False) \
                    & (cfg.persons[sup].shift.title \
                        == cfg.persons[p].shift.title) \
                    )]
            person_sup = person_sup_mono_list[0]
            cfg.persons[p].sup = person_sup

            # Update the person's colleagues.
            colleagues_temp_list \
                = [cfg.persons[coll] for coll in cfg.persons if (\
                    (cfg.persons[coll].role.title == "Team Leader") \
                    & (cfg.persons[coll].separated is False) \
                    & (cfg.persons[coll].shift.title \
                        == cfg.persons[p].shift.title) \
                    )]
            cfg.persons[p].colleagues = colleagues_temp_list

            # Update the person's subordinates.
            subordinates_temp_list \
                = [cfg.persons[sub] for sub in cfg.persons if (\
                    (cfg.persons[sub].role.title == "Laborer") \
                    & (cfg.persons[sub].separated is False) \
                    & (cfg.persons[sub].team.title \
                        == cfg.persons[p].team.title) \
                    )]
            cfg.persons[p].subs = subordinates_temp_list


        # If the person is a Shift Manager...
        elif (cfg.persons[p].role.title == "Shift Manager"):

            # Update the person's subordinates.
            subordinates_temp_list \
                = [cfg.persons[sub] for sub in cfg.persons if (\
                    (cfg.persons[sub].role.title == "Team Leader") \
                    & (cfg.persons[sub].separated is False) \
                    & (cfg.persons[sub].shift.title \
                        == cfg.persons[p].shift.title) \
                    )]
            cfg.persons[p].subs = subordinates_temp_list


def check_for_and_execute_worker_swaps():
    """
    Checks whether any Laborers should be swapped with Laborers 
    currently on different Teams (but on the same Shift). Typically this
    will only be run on a Monday, at the start of a new workweek.
    """

    for p in cfg.persons:

        # Only consider a swap if a person is a Laborer.
        if cfg.persons[p].role.title == cfg.LABORER_TERM:

            # Only consider a swap if a person isn't separated 
            # from employment.
            if cfg.persons[p].separated is not True:

                # If a random roll says that a swap should occur...
                if random.uniform(0.0, 1.0) \
                        < cfg.PROB_LABORER_SWAP_TO_DIFFERENT_TEAM:

                    # Create a list of all the persons who aren't 
                    # separated from employment.
                    Laborers_avail_for_swap_list = \
                        [person for person in cfg.persons \
                            if cfg.persons[person].separated is not True]

                    # Keep only the persons in the list who are 
                    # Laborers.
                    Laborers_avail_for_swap_list = \
                        [person for person in Laborers_avail_for_swap_list \
                            if cfg.persons[person].role.title \
                                == cfg.LABORER_TERM]

                    # Keep only the persons in the list who are on the 
                    # same Shift as the given worker.
                    Laborers_avail_for_swap_list = \
                        [person for person in Laborers_avail_for_swap_list \
                            if cfg.persons[person].shift \
                                == cfg.persons[p].shift]

                    # Keep only the persons in the list who are on a 
                    # different Team from the given worker.
                    Laborers_avail_for_swap_list = \
                        [person for person in Laborers_avail_for_swap_list \
                            if cfg.persons[person].team \
                                != cfg.persons[p].team]

                    # Randomly shuffle the list of Laborers and select 
                    # the first one as the person with whom the given 
                    # worker should swap Teams.
                    random.shuffle(Laborers_avail_for_swap_list)
                    Laborer_selected_for_swap \
                        = Laborers_avail_for_swap_list[0]

                    # Swap the two Laborers' Teams. (That will 
                    # automatically swap, e.g., their supervisors, as 
                    # well?)
                    first_Laborer_old_Team = cfg.persons[p].team
                    second_Laborer_old_Team \
                        = cfg.persons[Laborer_selected_for_swap].team
                    cfg.persons[p].team = second_Laborer_old_Team
                    cfg.persons[Laborer_selected_for_swap].team \
                        = first_Laborer_old_Team


def check_for_and_execute_worker_separation_and_replacement():
    """
    Checks whether any workers (Team Leaders or Laborers only) will
    be separated at the end of this day; if so, it separates them and 
    replaces them with new workers to be in place prior to the start of 
    the next day.
    """

    # If the current weekday is Saturday or Sunday, skip ahead to the 
    # next day without generating any Separation or Replacement events.
    if (cfg.current_datetime_obj.weekday() == 5) \
            or (cfg.current_datetime_obj.weekday() == 6):
        return


    # ------------------------------------------------------------------
    # Determine whether persons generate a "Resignation" behavior
    # and record or "Termination" record and 
    # create those behaviors and records.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Create a list of all the persons (if any) who are to be
    # separated and replaced on this day. The actual separation
    # and replacement will be handled in two steps;
    # they can't be handled all in a single step, because that
    # would generate an error of "dictionary changed size
    # during iteration".
    # ------------------------------------------------------------------

    list_of_persons_to_replace = []

    for p in cfg.persons:

        # If a person is the Production Director or a Shift Manager,
        # he cannot be separated; do not check whether a separation 
        # should occur.
        if cfg.persons[p].role.title == "Production Director":
            # Skip ahead to the next person.
            continue
        if cfg.persons[p].role.title == "Shift Manager":
            continue

        # If a person is already separated from employment,
        # do not check whether a separation should occur
        if cfg.persons[p].separated is True:
            continue

        # ==============================================================
        # Calculate variables that will affect whether a Separation 
        # event occurs.
        # ==============================================================

        # --------------------------------------------------------------
        # Absences recorded for the person during the period covering 
        # the current day plus the previous N days.
        # --------------------------------------------------------------

        # Find the current day's spot in the list, count backwards by N 
        # to find the spot of the list correspondingn to the first day 
        # of the period that should be searched for events, and delete 
        # any items found in the list before that point.
        #
        # Note that because workers are checked for termination events 
        # *after* the end of the workday, the day just completed is 
        # always checked for termination events. If 
        # previous_days_to_check_num = 1, then the day-just-ended is 
        # checked, *and also the 1 day previous to that*.

        list_of_absences_recorded_for_pers \
            = list(cfg.persons[p].dict_days_with_num_of_absences_recorded.values())
        previous_days_to_check_for_absences_num = 16

        # The lowest value that this can have is 0, even if there's a 
        # sizeable priming period. That's because slicing of the list 
        # [start:stop] indexes the first item in the list as 0, not 
        # (e.g.) -31.
        earliest_index_to_include = \
            (cfg.day_of_sim_iter - previous_days_to_check_for_absences_num) \
                - cfg.day_of_sim_iter_for_first_simulated_day

        cfg.day_of_sim_iter - previous_days_to_check_for_absences_num

        if earliest_index_to_include \
                <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_absences_recorded_for_pers_in_last_n_days \
                = list_of_absences_recorded_for_pers
        elif earliest_index_to_include \
                > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_absences_recorded_for_pers_in_last_n_days = \
                list_of_absences_recorded_for_pers[earliest_index_to_include:]
        pers_absences_recorded_in_last_n_days_sum = \
            sum(list_of_absences_recorded_for_pers_in_last_n_days)

        # --------------------------------------------------------------
        # Idea behaviors generated by the person to date.
        # --------------------------------------------------------------
        pers_idea_behaviors_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_idea_behaviors.values()))

        # --------------------------------------------------------------
        # Lapses recorded for the person during the period covering the 
        # current day plus the previous N days.
        # --------------------------------------------------------------

        # This calculation has the same conditions and caveats as the 
        # calculation of the number of Absences recorded during the 
        # current and previous N days.

        list_of_lapses_recorded_for_pers \
            = list(cfg.persons[p].dict_days_with_num_of_lapses_recorded.values())

        previous_days_to_check_for_lapses_num = 90
        earliest_index_to_include \
            = cfg.day_of_sim_iter - previous_days_to_check_for_lapses_num

        if earliest_index_to_include \
                <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_lapses_recorded_for_pers_in_last_n_days \
                = list_of_lapses_recorded_for_pers
        elif earliest_index_to_include \
                > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_lapses_recorded_for_pers_in_last_n_days \
                = list_of_lapses_recorded_for_pers[earliest_index_to_include:]
        pers_lapses_recorded_in_last_n_days_sum = \
            sum(list_of_lapses_recorded_for_pers_in_last_n_days)

        # --------------------------------------------------------------
        # Slips recorded for the person during the period covering the 
        # current day plus the previous N days.
        # --------------------------------------------------------------

        # This calculation has the same conditions and caveats as the 
        # calculation of the number of Absences recorded during the 
        # current and previous N days.

        list_of_slips_recorded_for_pers \
            = list(cfg.persons[p].dict_days_with_num_of_slips_recorded.values())

        previous_days_to_check_for_slips_num = 90
        earliest_index_to_include \
            = cfg.day_of_sim_iter - previous_days_to_check_for_slips_num

        if earliest_index_to_include \
                <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_slips_recorded_for_pers_in_last_n_days \
                = list_of_slips_recorded_for_pers
        elif earliest_index_to_include \
                > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_slips_recorded_for_pers_in_last_n_days = \
                list_of_slips_recorded_for_pers[earliest_index_to_include:]
        pers_slips_recorded_in_last_n_days_sum = \
            sum(list_of_slips_recorded_for_pers_in_last_n_days)

        # --------------------------------------------------------------
        # Disruptions recorded for the person during the period covering
        # the current day plus the previous N days.
        # --------------------------------------------------------------

        # This calculation has the same conditions and caveats as the 
        # calculation of the number of Absences recorded during the 
        # current and previous N days.

        list_of_disruptions_recorded_for_pers \
            = list(cfg.persons[p].dict_days_with_num_of_disruptions_recorded.values())

        previous_days_to_check_for_disruptions_num = 45
        earliest_index_to_include \
            = cfg.day_of_sim_iter - previous_days_to_check_for_disruptions_num

        if earliest_index_to_include \
                <= cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_disruptions_recorded_for_pers_in_last_n_days \
                = list_of_disruptions_recorded_for_pers
        elif earliest_index_to_include \
                > cfg.day_of_sim_iter_for_first_simulated_day:
            list_of_disruptions_recorded_for_pers_in_last_n_days \
                = list_of_disruptions_recorded_for_pers[earliest_index_to_include:]
        pers_disruptions_recorded_in_last_n_days_sum = \
            sum(list_of_disruptions_recorded_for_pers_in_last_n_days)

        # --------------------------------------------------------------
        # Sabotages recorded for the person to date.
        # --------------------------------------------------------------
        pers_sabotages_recorded_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_sabotages_recorded.values()))

        # --------------------------------------------------------------
        # Unrecorded (False Negative) Good behaviors for the person to 
        # date.
        # --------------------------------------------------------------
        pers_FN_good_records_to_date_sum = \
            sum(list(cfg.persons[p].dict_days_with_num_of_FN_good_records.values()))

        # Note that when instantiated, a given person's 
        # dict_days_with_actual_eff_values dictionary includes None 
        # values for all days, including those days that haven't been 
        # simulated yet. When calculating means, we restrict the 
        # calculation to those entries in the dict corresponding to days
        # that have already been simulated.
        #
        # Delete from the list any None values, which correspond to days
        # on which a person was absent and thus had no actual or 
        # recorded Efficacy.

        # --------------------------------------------------------------
        # Mean of actual Efficacy values.
        # --------------------------------------------------------------

        # On the first day, there won't yet be any Efficacy values.
        try:
            temp_list = \
                list(cfg.persons[p].dict_days_with_actual_eff_values.values())[
                    0:(cfg.day_of_sim_iter \
                        - cfg.day_of_sim_iter_for_first_simulated_day)
                    ]
            list_of_actual_eff_values_without_Nones \
                = [v for v in temp_list if v is not None]
            pers_actual_eff_values_mean = \
                statistics.mean(list_of_actual_eff_values_without_Nones)
        except:
            pers_actual_eff_values_mean = None

        # --------------------------------------------------------------
        # Mean of recorded Efficacy values.
        # --------------------------------------------------------------

        # On the first day, there won't yet be any Efficacy values.
        try:
            temp_list = \
                list(cfg.persons[p].dict_days_with_recorded_eff_values.values())[
                    0:(cfg.day_of_sim_iter \
                        - cfg.day_of_sim_iter_for_first_simulated_day)
                    ]
            list_of_recorded_eff_values_without_Nones \
                = [v for v in temp_list if v is not None]
            pers_recorded_eff_values_mean = \
                statistics.mean(list_of_recorded_eff_values_without_Nones)
        except:
            pers_recorded_eff_values_mean = None

        # --------------------------------------------------------------
        # Number of colleagues.
        # --------------------------------------------------------------
        try:
            pers_current_colleagues_total_num \
                = len(cfg.persons[p].colleagues)
        except:
            # This is the case of the Production Director, who has no 
            # colleagues.
            pers_current_colleagues_total_num = 0

        # --------------------------------------------------------------
        # Mean actual Efficacy behaviors for colleagues.
        # --------------------------------------------------------------
        try:
            list_of_all_colleague_actual_eff_values = []
            for c in cfg.persons[p].colleagues:
                list_of_all_colleague_actual_eff_values.extend(
                    list(c.dict_days_with_actual_eff_values.values())
                    )
            list_of_all_colleague_actual_eff_values \
                = [v for v in list_of_all_colleague_actual_eff_values \
                    if v is not None]
            pers_colleagues_actual_eff_values_mean \
                = statistics.mean(list_of_all_colleague_actual_eff_values)
        except:
            # This is the case of the Production Director, who has no 
            # colleagues.
            pers_colleagues_actual_eff_values_mean = None

        # --------------------------------------------------------------
        # Supervisor's Goodness stat.
        # --------------------------------------------------------------
        try:
            goodness_of_pers_sup = cfg.persons[p].sup.stat_goodness
        except:
            # This is the case of the Production Director, who has no 
            # supervisor.
            goodness_of_pers_sup = None

        # ==============================================================
        # Determine whether particular types of Separation events occur.
        # ==============================================================

        # --------------------------------------------------------------
        # "Low Commitment". Calculate if there's a Resignation tied to 
        # low Commitment.
        # --------------------------------------------------------------

        # If today a person's Commitment stat is less than some 
        # randomly-generated number and a random roll is less than some 
        # fixed threshold, a Resignation event will be generated. This 
        # is the most "random" sort of Resignation event, which can 
        # affect any person with a less-than-maximum Commitment level.

        pers_openness_to_resigning_through_low_commitment = \
           (1.0 - cfg.persons[p].stat_commitment)

        # If a person's Commitment is low, then on occasion...
        if pers_openness_to_resigning_through_low_commitment \
            * random.uniform(0.0, 1.0) > random.uniform(0.0, 0.03):

            # ... the person has a low but non-zero chance of resigning 
            # on a given day.
            if random.uniform(0.0, 1.0) < 0.00014:

                # Add the person's "Resignation" behavior to the 
                # behaviors DF.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p],
                    "Separation",
                    "Resignation",
                    "Low Commitment",
                    "Resignation",
                    None,
                    True,
                    )

                # Add the person to the list of persons to be replaced 
                # as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this
                # reason, there's no need to check whether he might also
                # become separated for other reasons on the same day; 
                # skip ahead to the next person.
                continue

        # --------------------------------------------------------------
        # "Ethically Inferior Supervisor". Calculate if there's a 
        # Resignation due to having a supervisor with dramatically lower
        # Goodness than oneself.
        # --------------------------------------------------------------

        # If the person's Goodness stat exceeds that of his supervisor 
        # by some specified value, a Resignation behavior will be 
        # generated if a random  roll is less than some fixed threshold 
        # on this day.

        # A Production Director has no supervisor and thus cannot resign
        # for this reason.
        if cfg.persons[p].sup is not None:

            # The smaller the number on the right, the more Resignations
            # will occur.
            if cfg.persons[p].stat_goodness - goodness_of_pers_sup >= 0.41:
                if random.uniform(0.0, 1.0) < 0.055:

                    # Add the person's "Resignation" behavior to the 
                    # behaviors DF.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p],
                        "Separation",
                        "Resignation",
                        "Ethically Inferior Supervisor",
                        "Resignation",
                        None,
                        True,
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for 
                    # this reason, there's no need to check whether he 
                    # might also become separated for other reasons on 
                    # the same day; skip ahead to the next person.
                    continue

        # --------------------------------------------------------------
        # "Unrecognized Good Behaviors". Calculate if there's a 
        # Resignation due to having multiple unrecognized (False 
        # Negative record) Good behaviors.
        # --------------------------------------------------------------

        # If a person has reached some number of unrecognized 
        # Good behaviors *during his entire career*, a Resignation 
        # behavior will be generated if a random roll is less than some
        # fixed threshold on this day.

        if pers_FN_good_records_to_date_sum >= 2:
            if random.uniform(0.0, 1.0) < 0.075:

                # Add the person's "Resignation" behavior to the 
                # behaviors DF.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p],
                    "Separation",
                    "Resignation",
                    "Unrecognized Good Behaviors",
                    "Resignation",
                    None,
                    True,
                    )

                # Add the person to the list of persons to be replaced 
                # as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this
                # reason, there's no need to check whether he might also
                # become separated for other reasons on the same day; 
                # skip ahead to the next person.
                continue

        # --------------------------------------------------------------
        # "Recruited Away". Calculate if there's a Resignation due to a 
        # person with high actual Efficacy and multiple Idea behaviors 
        # being recruited away.
        # --------------------------------------------------------------

        # If a person has generated some number of Idea behaviors 
        # *during his entire career* and has a mean actual Efficacy that
        # exceeds the organization's mean actual Efficacy by some fixed 
        # amount, a Resignation behavior will be generated if a random 
        # roll is less than some fixed threshold on this day.

        # This shouldn't be applied on the first day, because at the 
        # start of the first day, cfg.org_actual_eff_values_mean will 
        # equal 0.0. However, the fact that it requires a person to have
        # at least N Idea behaviors automatically precludes it from 
        # being applied on the first day.

        if pers_idea_behaviors_to_date_sum >= 4:
            # The smaller the number on the right, the more Resignations will occur.
            if pers_actual_eff_values_mean \
                >= cfg.org_actual_eff_values_mean + 0.395:

                if random.uniform(0.0, 1.0) < 0.04:
                    # Add the person's "Resignation" behavior to the 
                    # behaviors DF.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p],
                        "Separation",
                        "Resignation",
                        "Recruited Away",
                        "Resignation",
                        None,
                        True,
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for 
                    # this reason, there's no need to check whether he 
                    # might also become separated for other reasons on 
                    # the same day; skip ahead to the next person.
                    continue

        # --------------------------------------------------------------
        # "Underrecorded Efficacy"
        # 
        # Calculate if there's a Resignation due to a person having a 
        # Recorded Efficacy that's much lower than his Actual Efficacy.
        # --------------------------------------------------------------

        # Only allow this to happen if it's at least the Nth simulated 
        # day worked by a given person (this excludes recent replacement
        # hires).
        if cfg.persons[p].days_attended >= 15:

            # The Production Director will not have any recorded 
            # Efficacy values.
            if cfg.persons[p].role.title != "Production Director":

                # If the person's Actual Efficacy exceeds his Recorded 
                # Efficacy by a specified amount... (The smaller the 
                # number on the right, the more Resignations will 
                # occur.)
                if (pers_actual_eff_values_mean \
                    - pers_recorded_eff_values_mean) >= 0.047:

                    # ... there's a chance that the person may resign
                    # on any given day.
                    if random.uniform(0.0, 1.0) < 0.2:

                        # Add the person's "Resignation" behavior to the
                        # behaviors DF.
                        bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p],
                            "Separation",
                            "Resignation",
                            "Underrecorded Efficacy",
                            "Resignation",
                            None,
                            True,
                            )

                        # Add the person to the list of persons
                        # to be replaced as workers.
                        list_of_persons_to_replace.append(cfg.persons[p])

                        # If a person becomes separated from employment 
                        # for this reason, there's no need to check 
                        # whether he might also become separated for 
                        # other reasons on the same day; skip ahead to 
                        # the next person.
                        continue

        # --------------------------------------------------------------
        # "Poor Teammates". Calculate if there's a Resignation due to a 
        # person having much higher Actual Efficacy than his teammates 
        # and having low Goodness (i.e., willingness to generate 
        # Sacrifice behaviors).
        # --------------------------------------------------------------

        # A Production Director has no colleagues and thus cannot resign
        # for this reason.
        if cfg.persons[p].colleagues is not None:

            try:
                # Only allow this to happen if it's at least the Nth 
                # simulated day worked by a given person (this excludes 
                # recent replacement hires).
                if cfg.persons[p].days_attended >= 15:

                    # If the person's Actual Efficacy exceeds his 
                    # teammates' mean actual Efficacy by a specified 
                    # amount... (The smaller the number on the right, 
                    # the more Resignations will occur.)
                    if (pers_actual_eff_values_mean \
                        - pers_colleagues_actual_eff_values_mean) >= 0.043:

                        # ... and the person's Goodness stat is below 
                        # some threshold...
                        if cfg.persons[p].stat_goodness < 0.5:

                            # ... there's a chance that the person may 
                            # resign on any given day.
                            if random.uniform(0.0, 1.0) < 0.25:

                                # Add the person's "Resignation" 
                                # behavior to the behaviors DF.
                                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                                    cfg.persons[p],
                                    "Separation",
                                    "Resignation",
                                    "Poor Teammates",
                                    "Resignation",
                                    None,
                                    True,
                                    )

                                # Add the person to the list of persons
                                # to be replaced as workers.
                                list_of_persons_to_replace.append(cfg.persons[p])

                                # If a person becomes separated from 
                                # employment for this reason, there's no
                                # need to check whether he might also 
                                # become separated for other reasons on 
                                # the same day; skip ahead to the next 
                                # person.
                                continue

            except:
                print(
                    "per_id of person generating error for poor teammates: ",
                    cfg.persons[p].per_id
                    )
                pass

        # --------------------------------------------------------------
        # "Multiple Sabotages". Calculate if there's a Termination tied 
        # to recorded Sabotages.
        # --------------------------------------------------------------

        # A person is terminated after receiving his Nth recording of a
        # Sabotage *for his entire career*.

        if pers_sabotages_recorded_to_date_sum >= 3:

            # Add the person's "Termination" behavior to the behaviors 
            # DF. This will later be switched from an (apparent) 
            # behavior by the person to (only) a record made by his 
            # supervisor.
            bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                cfg.persons[p],
                "Separation",
                "Termination",
                "Multiple Sabotages",
                "Termination",
                None,
                True,
                )

            # Add the person to the list of persons
            # to be replaced as workers.
            list_of_persons_to_replace.append(cfg.persons[p])

            # If a person becomes separated from employment for this 
            # reason, there's no need to check whether he might also 
            # become separated for other reasons on the same day; skip 
            # ahead to the next person.
            continue

        # --------------------------------------------------------------
        # "Lapses and Below-Average Efficacy". Calculate if there's a 
        # Termination tied to multiple recorded Lapses  and 
        # significantly below-average recorded Efficacy.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if he has a 
        # specified number of Lapses *during the last N days* and 
        # below-average recorded Efficacy.

        if pers_lapses_recorded_in_last_n_days_sum >= 3:

            # The smaller the number at the end, the more persons who 
            # will be terminated.
            if pers_recorded_eff_values_mean \
                < (cfg.org_recorded_eff_values_mean - 0.23):

                # ... there's a chance that the person may be terminated
                # on any given day.
                if random.uniform(0.0, 1.0) < 0.05:

                    # Add the person's "Termination" behavior to the 
                    # behaviors DF. This will later be switched from an 
                    # (apparent) behavior by the person to (only) a 
                    # record made by his supervisor.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p],
                        "Separation",
                        "Termination",
                        "Lapses and Below-Average Efficacy",
                        "Termination",
                        None,
                        True,
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for 
                    # this reason, there's no need to check whether he
                    # might also become separated for other reasons on 
                    # the same day; skip ahead to the next person.
                    continue

        # --------------------------------------------------------------
        # "Multiple Lapses". Calculate if there's a Termination tied to 
        # multiple recorded Lapses.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if he has a 
        # specified number of Lapses *during the last N days* 
        # (regardless of his recorded Efficacy).

        if pers_lapses_recorded_in_last_n_days_sum >= 5:

            # ... there's a chance that the person may be terminated
            # on any given day. (The larger the number at the end, the 
            # more persons who will be terminated.)
            if random.uniform(0.0, 1.0) < 0.27:

                # Add the person's "Termination" behavior to the 
                # behaviors DF. This will later be switched from an 
                # (apparent) behavior by the person to (only) a record 
                # made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p],
                    "Separation",
                    "Termination",
                    "Multiple Lapses",
                    "Termination",
                    None,
                    True,
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this
                # reason, there's no need to check whether he might also
                # become separated for other reasons on the same day; 
                # skip ahead to the next person.
                continue

        # --------------------------------------------------------------
        # "Multiple Slips". Calculate if there's a Termination tied to 
        # multiple recorded Slips.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if he has a 
        # specified number of Slips *during the last N days*.

        if pers_slips_recorded_in_last_n_days_sum >= 4:

            # ... there's a chance that the person may be terminated
            # on any given day.
            if random.uniform(0.0, 1.0) <= 0.1:

                # Add the person's "Termination" behavior to the 
                # behaviors DF. This will later be switched from an 
                # (apparent) behavior by the person to (only) a record 
                # made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p],
                    "Separation",
                    "Termination",
                    "Multiple Slips",
                    "Termination",
                    None,
                    True,
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this
                # reason, there's no need to check whether he might also
                # become separated for other reasons on the same day; 
                # skip ahead to the next person.
                continue

        # --------------------------------------------------------------
        # "Multiple Disruptions". Calculate if there's a Termination 
        # tied to multiple recorded Disruptions.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if he has a 
        # specified number of Disruptions *during the last N days*.

        if pers_disruptions_recorded_in_last_n_days_sum >= 4:

            # ... there's a chance that the person may be terminated
            # on any given day.
            if random.uniform(0.0, 1.0) < 0.032:

                # Add the person's "Termination" behavior to the 
                # behaviors DF. This will later be switched from an 
                # (apparent) behavior by the person to (only) a record 
                # made by his supervisor.
                bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p],
                    "Separation",
                    "Termination",
                    "Multiple Disruptions",
                    "Termination",
                    None,
                    True,
                    )

                # Add the person to the list of persons
                # to be replaced as workers.
                list_of_persons_to_replace.append(cfg.persons[p])

                # If a person becomes separated from employment for this
                # reason, there's no need to check whether he might also
                # become separated for other reasons on the same day; 
                # skip ahead to the next person.
                continue

        # --------------------------------------------------------------
        # "Multiple Absences". Calculate if there's a Termination tied 
        # to multiple Absences.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if he has a 
        # specified number of Absences within the last N days.

        if pers_absences_recorded_in_last_n_days_sum >= 4:

            # Only allow this to happen if it's at least a certain day 
            # in the series worked by a given person (this excludes 
            # recent replacement hires); if so...
            if cfg.persons[p].days_attended >= 1:

                # ... there's a chance that the person may be terminated
                # on any given day.
                if random.uniform(0.0, 1.0) < 0.1:

                    # Add the person's "Termination" behavior to the 
                    # behaviors DF. This will later be switched from an
                    # (apparent) behavior by the person to (only) a 
                    # record made by his supervisor.
                    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p],
                        "Separation",
                        "Termination",
                        "Multiple Absences",
                        "Termination",
                        None,
                        True,
                        )

                    # Add the person to the list of persons
                    # to be replaced as workers.
                    list_of_persons_to_replace.append(cfg.persons[p])

                    # If a person becomes separated from employment for 
                    # this reason, there's no need to check whether he 
                    # might also become separated for other reasons on 
                    # the same day; skip ahead to the next person.
                    continue

        # --------------------------------------------------------------
        # "Low Efficacy". Calculate if there's a Termination tied to low
        # recorded Efficacy.
        # --------------------------------------------------------------

        # A person has a chance of being terminated if his recorded 
        # Efficacy is below some specified level.

        # During his first days, a person's 
        # pers_recorded_eff_values_mean may still be None, if he has had
        # an Absence on each day.
        if pers_recorded_eff_values_mean is not None:

            # The smaller the number at the end, the more persons who 
            # will be terminated.
            if pers_recorded_eff_values_mean \
                < (cfg.org_recorded_eff_values_mean - 0.40):

                # Only allow this to happen if it's at least a certain 
                # day in the series worked by a given person (this 
                # excludes recent replacement hires). If so...
                if cfg.persons[p].days_attended >= 15:

                    # ... there's a chance that the person may be 
                    # terminated on any given day.
                    if random.uniform(0.0, 1.0) < 0.25:

                        # Add the person's "Termination" behavior to the
                        # behaviors DF. This will later be switched from
                        # an (apparent) behavior by the person
                        # to (only) a record made by his supervisor.
                        bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p],
                            "Separation",
                            "Termination",
                            "Low Efficacy",
                            "Termination",
                            None,
                            True,
                            )

                        # Add the person to the list of persons
                        # to be replaced as workers.
                        list_of_persons_to_replace.append(cfg.persons[p])

                        # If a person becomes separated from employment 
                        # for this reason, there's no need to check 
                        # whether he might also become separated for 
                        # other reasons on the same day; skip ahead to 
                        # the next person.
                        continue

    # ==================================================================
    # Perform the actual separation events (by modifying Person 
    # objects); create new replacement workers; and swap them into the 
    # replaced persons' organizational placements.
    # ==================================================================
    for person in list_of_persons_to_replace:
        # Separate the person and replace him as a worker with a 
        # newly-generated person.
        separate_and_replace_worker_with_new_person(person)

    # Recalculate all supervisor, subordinate, and colleage relationships,
    # to account for any changes in personnel.
    assign_supervisor_to_each_person()
    assign_subordinates_to_all_supervisors()
    assign_colleagues_to_all_persons()

    # Update all persons' portion of same-sex colleagues (since a 
    # replacement worker may have a different sex than the one whom he 
    # replaced).
    update_persons_colleagues_of_same_sex_prtn()


def separate_and_replace_worker_with_new_person(person_to_separate_u):
    """
    Gets the organizational placement of a worker-to-be-separated,
    separates that person, randomly generates a new person from
    scratch, and immediately places that new person into the 
    separated person's organizational placement.

    PARAMETERS
    ----------
    person_to_separate_u
        The person to be separated
    """

    # ------------------------------------------------------------------
    # Temporarily save the details of the organizational placement
    # (Role, Shift, Team, supervisor, colleagues, subordinates)
    # of the person to be separated.
    # ------------------------------------------------------------------
    role_to_transfer = person_to_separate_u.role
    sphere_to_transfer = person_to_separate_u.sphere
    shift_to_transfer = person_to_separate_u.shift
    team_to_transfer = person_to_separate_u.team
    sup_to_transfer = person_to_separate_u.sup
    colleagues_to_transfer = person_to_separate_u.colleagues
    subs_to_transfer = person_to_separate_u.subs
    task_to_transfer = person_to_separate_u.task
    curr_actvty_to_transfer = person_to_separate_u.curr_actvty

    # ------------------------------------------------------------------
    # Randomly generate a new person.
    # ------------------------------------------------------------------

    # Get the current size of cfg.persons
    new_person_index = len(cfg.persons) + 1

    # Create the new Person object.
    cfg.persons[new_person_index] = Person_class()
    # print(cfg.persons[new_person_index])

    # ------------------------------------------------------------------
    # Separate the person who is being separated.
    # ------------------------------------------------------------------

    # Keep the person in existence and as part of the "workforce" 
    # broadly understood (so that his data can be used when generating 
    # statistics and plotting phenomena), but mark him as "separated", 
    # so that he no longer generates activities and isn't connected to a
    # supervisor, colleagues, or subordinates.
    person_to_separate_u.separated = True

    # ------------------------------------------------------------------
    # Connect and activate the new person who is being employed.
    # ------------------------------------------------------------------

    cfg.persons[new_person_index].role = role_to_transfer
    cfg.persons[new_person_index].sphere = sphere_to_transfer
    cfg.persons[new_person_index].shift = shift_to_transfer
    cfg.persons[new_person_index].team = team_to_transfer
    cfg.persons[new_person_index].sup = sup_to_transfer
    cfg.persons[new_person_index].colleagues = colleagues_to_transfer
    cfg.persons[new_person_index].subs = subs_to_transfer
    cfg.persons[new_person_index].task = task_to_transfer
    cfg.persons[new_person_index].curr_actvty = curr_actvty_to_transfer

    # Generate an "Onboarding" behavior and record for the newly hired 
    # person to the behaviors DF.
    bhv.add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
        cfg.persons[new_person_index],
        "Onboarding",
        None,
        None,
        "Onboarding",
        None,
        True,
        )


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