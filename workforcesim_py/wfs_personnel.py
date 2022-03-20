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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import numpy as np
import pandas as pd


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import config as cfg
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

        # ---------------------------------------------------------------------
        # Stats for relatively stable personal traits.
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


        # ---------------------------------------------------------------------
        # Base probabilities for generating particular types of actual
        # behaviors or recording actions (before situational modifiers).
        # ---------------------------------------------------------------------
 
        # Base probability of generating a Presence behavior (before multipliers).
        self.prob_base_presence = (
            cfg.base_rate_attendance \
            + self.stat_health * 0.1 * 1/2 \
            + self.stat_commitment * 0.1 * 1/2
            )

        # Base probability of generating an Idea behavior (before multipliers).
        self.prob_base_idea = (
            cfg.base_rate_idea + self.stat_perceptiveness * 0.05
            )

        # Base probability of generating a Lapse behavior (before multipliers).
        self.prob_base_lapse = (
            cfg.base_rate_lapse - self.stat_perceptiveness * 0.05
            )

        # Base probability of generating a Feat behavior (before multipliers).
        self.prob_base_feat = (
            cfg.base_rate_feat + self.stat_dexterity * 0.05
            )

        # Base probability of generating a Slip behavior (before multipliers).
        self.prob_base_slip = (
            cfg.base_rate_slip - self.stat_dexterity * 0.05
            )

        # Base probability of generating a Teamwork behavior (before multipliers).
        self.prob_base_teamwork = (
            cfg.base_rate_teamwork + self.stat_sociality * 0.05
            )

        # Base probability of generating a Disruption behavior (before multipliers).
        self.prob_base_disruption = (
            cfg.base_rate_disruption - self.stat_sociality * 0.05
            )

        # Base probability of generating a Sacrifice behavior (before multipliers).
        self.prob_base_sacrifice = (
            cfg.base_rate_sacrifice + self.stat_goodness * 0.05
            )

        # Base probability of generating a Sabotage behavior (before multipliers).
        self.prob_base_sabotage = (
            cfg.base_rate_sabotage - self.stat_goodness * 0.05
            )

        # Base Efficacy level (before multipliers).
        self.level_base_efficacy = (
            cfg.base_rate_efficacy \
            + self.stat_dexterity * 0.1 * 1/2 \
            + self.stat_commitment * 0.1 * 1/2
            )


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

        # Proportion of the person's colleagues who are of the same gender.
        self.colleagues_of_same_sex_prtn = None

        # The age of a person's supervisor.
        self.sup_age = None


        # ---------------------------------------------------------------------
        # Activity data generated for the person each day the simulation is run.
        # ---------------------------------------------------------------------

        # Actual behaviors are stored in one organization-wide DF, and recorded
        # behaviors are stored in a different organization-wide DF. Such
        # activities aren't directly stored in a Person object.

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
            "Supervisor Age": self.sup_age,
            cfg.colleagues_header_term: self.colleagues,
            "Same-Sex Colleagues Prtn": self.colleagues_of_same_sex_prtn,
            cfg.subordinates_header_term: self.subs,
            "Days Attended": self.days_attended,
            "Min Eff": self.eff_sco_act_min,
            "Max Eff": self.eff_sco_act_max,
            "Mean Eff": self.eff_sco_act_mean,
            "Num Goods": self.good_act_num,
            "Num Poors": self.poor_act_num,
            "Health": self.stat_health,
            "Commitment": self.stat_commitment,
            "Modified Efficacy": self.level_modified_efficacy,
            }


def generate_personal_stat(
    mean_u,
    sd_u
    ):
    """
    The stat-generator function.
    This defines a personal stat that by default uses the arguments
    for the mean and standard deviation for the stat that are
    specified below; these can be overridden by manually adding
    arguments when the function is called.
    """
    
    # Here "loc" is the mean, "scale" is SD,
    # and "size" is the number of numbers to generate.
    randomized_base_for_stat = round( float( np.random.normal(loc=mean_u, scale=sd_u, size=1) ) , 3)
    
    # It's possible for the number generated above to be < -1 or > 1;
    # below we manually set -1 and +1 as the min and max.   
    adjusted_stat = randomized_base_for_stat
    
    if randomized_base_for_stat < -1:
        adjusted_stat = -1.0
    elif randomized_base_for_stat > 1:
        adjusted_stat = 1.0
    
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

def assign_initial_supervisor_to_each_person():
    """
    Populates the initial "Supervisor" attribute for all persons.
    """

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


def assign_initial_subordinates_to_all_supervisors():
    """
    Populates the initial "Subordinates" attribute for all persons.
    """

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


def assign_initial_colleagues_to_all_persons():
    """
    Populates the initial "Colleagues" attribute for all persons.
    """

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


def update_persons_colleagues_of_same_sex_prtn():
    """
    For all persons, updates the calculation of the proportion of a
    a person's colleagues who are of the same gender.
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


def calculate_person_modifiers_to_implement_dependencies_and_covariance():
    """
    Implements dependencies and covariance among certain stats and 
    variables by adding modifiers that adjust their previously 
    random values (e.g., to provide bonuses or penalties to Efficacy
    for certain personal or environmental factors).
    """

    for p in cfg.persons:

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
            (1 + cfg.persons[p].age * cfg.strength_of_effect * random.uniform(0.0, 0.083))


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on the day of the week.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a person's Efficacy as one moves
        # deeper into the work week (with no bonus on Monday and the greatest
        # bonus on Friday).

        # Monday has weekday_num = 0; Friday has weekday_num = 4.
        weekday_num = cfg.current_datetime_obj.weekday()
#        print("weekday_num: ", weekday_num)

        cfg.persons[p].level_modified_efficacy = \
            cfg.persons[p].level_modified_efficacy * \
            (1 + weekday_num * cfg.strength_of_effect * random.uniform(0.0, 0.65))

        #weekday_name = cfg.current_datetime_obj.strftime("%A")
        #print("weekday_name: ", weekday_name)

#        print(
#            "person's level_modified_efficacy after weekday bonus: ",
#            cfg.persons[p].level_modified_efficacy
#            )


        # ---------------------------------------------------------------------
        # Bonus to Efficacy based on gender of teammates.
        # ---------------------------------------------------------------------

        # Implement a bonus that increases a person's Efficacy as one has a
        # higher proportion of colleagues (e.g., immediate teammates) who are
        # of the same gender as oneself.

        # This is only relevant if the person has colleagues (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].colleagues:

            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 + cfg.persons[p].colleagues_of_same_sex_prtn * cfg.strength_of_effect * random.uniform(0.0, 1.8))


        # ---------------------------------------------------------------------
        # Penalty to Efficacy based on age of supervisor.
        # ---------------------------------------------------------------------

        # Implement a penalty that decreases a person's Efficacy as the
        # difference in age between the person and his supervisor increases.

        # This is only relevant if the person has a supervisor (i.e.,
        # isn't the factory's Production Director).
        if cfg.persons[p].sup:

            cfg.persons[p].level_modified_efficacy = \
                cfg.persons[p].level_modified_efficacy * \
                (1 - abs(cfg.persons[p].age - cfg.persons[p].sup.age) \
                * cfg.strength_of_effect * random.uniform(0.0, 0.04))



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