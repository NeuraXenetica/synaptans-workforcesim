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
This module handles the simulation’s “Level 1” logic, which simulates
the *actual* behaviors performed by workers during each day of the
simulated time period. These behaviors reflect the “reality” of the
daily productivity and interpersonal interactions of production workers
in the factory.
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

from datetime import timedelta
import random


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
# █ Functions for iterating the simulation through one day
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def configure_behavs_act_df():
    """
    Configures behavs_act_df -- the master DF that contains an entry for
    every actual behavior performed by workers (including a worker's
    absence, which is itself a sort of behavior) -- by creating initial
    columns needed for adding behavioral entries.
    """

    # Create as an empty DF.
    cfg.behavs_act_df = pd.DataFrame()

    # Create the DF's initial columns.
    cfg.behavs_act_df["Person ID"] = 0
    cfg.behavs_act_df["First Name"] = "" 
    cfg.behavs_act_df["Last Name"] = ""
    cfg.behavs_act_df["Sex"] = ""
    cfg.behavs_act_df["Age"] = 0
    cfg.behavs_act_df["Workstyle"] = ""
    cfg.behavs_act_df["Sphere"] = ""
    cfg.behavs_act_df["Shift"] = ""
    cfg.behavs_act_df["Team"] = ""
    cfg.behavs_act_df["Role"] = ""
    cfg.behavs_act_df["Supervisor ID"] = 0
    cfg.behavs_act_df["Supervisor Age"] = None
    cfg.behavs_act_df["Sub-Sup Age Difference"] = None
    cfg.behavs_act_df["Colleague IDs"] = []
    cfg.behavs_act_df["Same-Sex Colleagues Prtn"] = None
    #cfg.behavs_act_df["Subordinate IDs"] = []
    cfg.behavs_act_df["Behavior Datetime"] = None
    cfg.behavs_act_df["Behavior Date"] = None
    cfg.behavs_act_df["Weekday Num"] = None
    cfg.behavs_act_df["Weekday Name"] = ""
    cfg.behavs_act_df["Week in Series"] = None
    cfg.behavs_act_df["Behavior Type"] = "" # the "main type" of the behavior (e.g., "Attendance")
    #cfg.behavs_act_df["Behavior Subtype"] = ""
    cfg.behavs_act_df["Behavior Comptype"] = "" # the "comparison type" of the behavior (e.g., for plotting)
    cfg.behavs_act_df["Actual Efficacy"] = None
    cfg.behavs_act_df["Actual Efficacy (SD)"] = None
    cfg.behavs_act_df["Record Type"] = ""
    cfg.behavs_act_df["Record Comptype"] = ""
    cfg.behavs_act_df["Recorded Efficacy"] = None
    cfg.behavs_act_df["Note"] = None
    cfg.behavs_act_df["Record Conf Mat"] = None


    # ---------------------------------------------------------------------
    # Add empty columns for one-hot encoding of the Behavior Types and
    # Comptypes for noting workers' actual behaviors.
    # ---------------------------------------------------------------------
    # Create blank new one-hot-encoding columns for Behavior Types.
    for behav_type in [
        "Attendance",
        "Good",
        "Poor",
        "Efficacy",
        ]:

        col_name = behav_type + " (Behavior Type)"
        cfg.behavs_act_df[col_name] = None

    # Create blank new one-hot-encoding columns for Behavior Comptypes.
    for behav_comptype in [
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
        ]:

        col_name = behav_comptype + " (Behavior Comptype)"
        cfg.behavs_act_df[col_name] = None

    # ---------------------------------------------------------------------
    # Add empty columns for one-hot encoding of the Record Types and
    # Comptypes for noting managers' records that purport to register
    # workers' behaviors.
    # ---------------------------------------------------------------------
    # Create blank new one-hot-encoding columns for Record Types.
    for behav_type in [
        "Attendance",
        "Good",
        "Poor",
        "Efficacy",
        ]:

        col_name = behav_type + " (Record Type)"
        cfg.behavs_act_df[col_name] = None

    # Create blank new one-hot-encoding columns for Record Comptypes.
    for behav_comptype in [
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
        ]:

        col_name = behav_comptype + " (Record Comptype)"
        cfg.behavs_act_df[col_name] = None


def print_modified_probabilities_of_a_person(
    person_u, # Person object for the person whose stats should be printed
    ):

    print("person_u.prob_modified_presence: ", person_u.prob_modified_presence)
    print("person_u.prob_modified_idea: ", person_u.prob_modified_idea)
    print("person_u.prob_modified_lapse: ", person_u.prob_modified_lapse)
    print("person_u.prob_modified_feat: ", person_u.prob_modified_feat)
    print("person_u.prob_modified_slip: ", person_u.prob_modified_slip)
    print("person_u.prob_modified_teamwork: ", person_u.prob_modified_teamwork)
    print("person_u.prob_modified_disruption: ", person_u.prob_modified_disruption)
    print("person_u.prob_modified_sacrifice: ", person_u.prob_modified_sacrifice)
    print("person_u.prob_modified_sabotage: ", person_u.prob_modified_sabotage)
    print("person_u.prob_modified_recording_accurately: ", person_u.prob_modified_recording_accurately)


def add_one_behav_to_behavs_act_df(
    person_object_u, # Person object for the person who performed the behavior
    behavior_type_u, # behavior type (string)
    behavior_comptype_u, # behavior comptype (string)
    eff_score_u, # the actual Efficacy (if relevant) demonstrated in the behavior
    ):
    """
    Adds a particular behavior by a particular person (e.g., as
    just generated by a daily behavior-generator) to behavs_act_df,
    the master DF of all actual behaviors performed by persons
    (including absences). It copies into the behavs_act_df relevant
    facts (e.g., the ID of a person's supervisor) as they exist
    *in the moment of the behavior*, thereby creating a lasting
    record of the circumstances in which the behavior occurred.
    """

    # ---------------------------------------------------------------------
    # Calculates the contents of columns containing data
    # regarding the behavior performed and person who performed it.
    # ---------------------------------------------------------------------

    # Calculate the value for the person's "Supervisor ID" field.
    # Determines whether the person has a supervisor or not (e.g., if he
    # is the factory's Production Director, who has no supervisor).
    try:
        sup_ID_to_use = person_object_u.sup.per_id
    except AttributeError:
        sup_ID_to_use = None

    # Calculate the value for the person's "Colleague IDs" field.
    # Determines whether the person has a supervisor or not (e.g., if he
    # is the factory's Production Director, who has no supervisor).
    try:
        colleague_IDs_to_use = [p.per_id for p in person_object_u.colleagues]
    except TypeError:
        colleague_IDs_to_use = None

    # Calculate the value for the "Supervisor Age" field and the
    # "Sub-Sup Age Difference" field, which is
    # the absolute value of the difference in ages between the subject
    # and his supervisor.
    # This is only relevant if a person has a supervisor (e.g.,
    # isn't the factory's Production Director).
    try:
        sup_age_to_use = person_object_u.sup.age
        sub_sup_age_diff = abs(person_object_u.sup.age - person_object_u.age)
    except:
        sup_age_to_use = None
        sub_sup_age_diff = None

    # Calculate the value for the "Week in Series" column.
    week_in_series = utils.return_week_in_series_for_given_date(
        cfg.current_datetime_obj.date(), # the date whose week should be returned
        )

    behav_to_add_df = pd.DataFrame({
        "Person ID": [person_object_u.per_id],
        "First Name": [person_object_u.f_name],
        "Last Name": [person_object_u.l_name],
        "Sex": [person_object_u.sex],
        "Age": [person_object_u.age],
        "Workstyle": [person_object_u.workstyle],
        "Health": [person_object_u.stat_health],
        "Commitment": [person_object_u.stat_commitment],
        "Perceptiveness": [person_object_u.stat_perceptiveness],
        "Dexterity": [person_object_u.stat_dexterity],
        "Sociality": [person_object_u.stat_sociality],
        "Goodness": [person_object_u.stat_goodness],
        "Strength": [person_object_u.stat_strength],
        "Openmindedness": [person_object_u.stat_openmindedness],
        #"Sphere": [person_object_u.sphere.title],
        "Shift": [person_object_u.shift.title],
        "Team": [person_object_u.team.title],
        "Role": [person_object_u.role.title],
        "Supervisor ID": [sup_ID_to_use],
        "Supervisor Age": [sup_age_to_use],
        "Sub-Sup Age Difference": [sub_sup_age_diff],
        "Colleague IDs": [colleague_IDs_to_use],
        "Same-Sex Colleagues Prtn": [person_object_u.colleagues_of_same_sex_prtn],
        "Behavior Datetime": [cfg.current_datetime_obj],
        "Behavior Date": [cfg.current_datetime_obj.date()],
        "Weekday Num": [cfg.current_datetime_obj.weekday()],
        "Weekday Name": [cfg.current_datetime_obj.strftime("%A")],
        "Week in Series": week_in_series,
        "Behavior Type": [behavior_type_u],
        "Behavior Comptype": [behavior_comptype_u],
        "Actual Efficacy": [eff_score_u],
        "Actual Efficacy (SD)": [eff_score_u], # The SD value will be calculated later.
        })

    # ---------------------------------------------------------------------
    # Add empty columns for one-hot encoding of the Behavior Types and
    # Comptypes for noting workers' actual behaviors.
    # ---------------------------------------------------------------------
    # Create blank new one-hot-encoding columns for Behavior Types.
    for behav_type in [
        "Attendance",
        "Good",
        "Poor",
        "Efficacy",
        ]:

        col_name = behav_type + " (Behavior Type)"
        behav_to_add_df[col_name] = None

    # Create blank new one-hot-encoding columns for Behavior Comptypes.
    for behav_comptype in [
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
        ]:

        col_name = behav_comptype + " (Behavior Comptype)"
        behav_to_add_df[col_name] = None

    # ---------------------------------------------------------------------
    # Add empty columns for one-hot encoding of the Record Types and
    # Comptypes for noting managers' records that purport to register
    # workers' behaviors.
    # ---------------------------------------------------------------------
    # Create blank new one-hot-encoding columns for Record Types.
    for behav_type in [
        "Attendance",
        "Good",
        "Poor",
        "Efficacy",
        ]:

        col_name = behav_type + " (Record Type)"
        behav_to_add_df[col_name] = None

    # Create blank new one-hot-encoding columns for Record Comptypes.
    for behav_comptype in [
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
        ]:

        col_name = behav_comptype + " (Record Comptype)"
        behav_to_add_df[col_name] = None


    # This newly created behav_to_add_df will only have a single row.
    # It's necessary to manually one-hot encode the Behavior Type
    # and Behavior Comptype.

    # One-hot encode the Behavior Type.
    behavior_type_OHE_col_name = \
        str(behavior_type_u) + " (Behavior Type)"
    behav_to_add_df[behavior_type_OHE_col_name].values[0] = 1

    # One-hot encode the Behavior Comptype.
    behavior_comptype_OHE_col_name = \
        str(behavior_comptype_u) + " (Behavior Comptype)"
    behav_to_add_df[behavior_comptype_OHE_col_name].values[0] = 1


    # Adds a new row to cfg.behavs_act_df with relevant data
    # for the given behavior and person who performed it.
    cfg.behavs_act_df = pd.concat(
        [
            cfg.behavs_act_df,
            behav_to_add_df,
            ],
        ignore_index=True,
        axis=0,
        )


def simulate_one_day_of_behaviors():
    """
    Simulates one day's worth of workers' actual behaviors.
    """

    for p in cfg.persons:

        # ---------------------------------------------------------------------
        # Calculate the person's attendance status and generate a "Presence" or
        # "Absence" behavior.
        # ---------------------------------------------------------------------

        # Every person has some probability of randomly generating an Absence.
        # First, check to see if that occurs.

        # If the person's modified probability of a Presence is less than
        # a random number from 0.00-1.00, the person is absent (i.e.,
        # performs an Absence behavior).
        if cfg.persons[p].prob_modified_presence < random.uniform(0.0, 1.0):
            attendance_today = "absent"

            # Add the person's "Absence" behavior to the behaviors DF.
            add_one_behav_to_behavs_act_df(
                cfg.persons[p], # Person object for the person who performed the behavior
                "Attendance", # behavior type (string)
                "Absence", # behavior comptype (string)
                None, # the actual Efficacy (if relevant) demonstrated in the behavior
                )

        # If the person *doesn't* generate a random Absence behavior, check to see if he
        # generates one as a result of having had at least 1 Lapse and 1 Slip in the
        # previous 4 days.
        else:
            lapses_num_previous_4_days = 0
            for n in [-4, -3, -2, -1]:
                lapses_num = return_num_of_events_of_type_for_person_on_DpmN(
                    cfg.persons[p], # the Person object whose events are to be searched
                    n, # relative number of the earlier/later day to seek (-1, 1, etc.)
                    "Lapse (Behavior Comptype)" # name of the column in which sought events are tallied
                    )
                # lapses_num will be None if the date tested falls outside the sim's range.
                if isinstance(lapses_num, int):
                    lapses_num_previous_4_days += lapses_num

            slips_num_previous_4_days = 0
            for n in [-4, -3, -2, -1]:
                slips_num = return_num_of_events_of_type_for_person_on_DpmN(
                    cfg.persons[p], # the Person object whose events are to be searched
                    n, # relative number of the earlier/later day to seek (-1, 1, etc.)
                    "Slip (Behavior Comptype)" # name of the column in which sought events are tallied
                    )
                # slips_num will be None if the date tested falls outside the sim's range.
                if isinstance(slips_num, int):
                    slips_num_previous_4_days += slips_num

            # If the person has at least 1 Lapse and 1 Slip in the previous 4 days...
            if (lapses_num_previous_4_days >= 1) & (slips_num_previous_4_days >= 1):

                # ... he has a 90% chance of having an Absence today.
                if (random.uniform(0.0, 1.0) <= 0.9):
                    attendance_today = "absent"

                    # Add the person's "Absence" behavior to the behaviors DF.
                    add_one_behav_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Attendance", # behavior type (string)
                        "Absence", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        )

                # If he succeeds at the 10% roll, then he is present today.
                else:
                    attendance_today = "present"

                    # Add the person's "Presence" behavior to the behaviors DF.
                    add_one_behav_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Attendance", # behavior type (string)
                        "Presence", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        )

            # If he doesn't have at least 1 Lapse and 1 Slip in the previous 4 days,
            # then he is present today.
            else:
                attendance_today = "present"

                # Add the person's "Presence" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Attendance", # behavior type (string)
                    "Presence", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )


        # ---------------------------------------------------------------------
        # If the person is present, calculate whether (or how) he performs
        # particular types of behaviors.
        # ---------------------------------------------------------------------
        if attendance_today == "present":

            # ---------------------------------------------------------------------
            # Calculate his Efficacy level for the day
            # and generate an "Efficacy" behavior.
            # ---------------------------------------------------------------------

            eff_sco_today = round( float( (
                 cfg.persons[p].level_modified_efficacy ) \
                * 1 + ( np.random.normal(loc=0, scale=cfg.base_max_efficacy_variability, size=1) \
                    * cfg.persons[p].workstyle_eff_daily_variability
                ) ), 3 )

            if eff_sco_today < 0:
                eff_sco_today = 0


            # Add the person's "Efficacy" behavior to the behaviors DF.
            add_one_behav_to_behavs_act_df(
                cfg.persons[p], # Person object for the person who performed the behavior
                "Efficacy", # behavior type (string)
                "Efficacy", # behavior comptype (string)
                eff_sco_today, # the actual Efficacy (if relevant) demonstrated in the behavior
                )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs an Idea
            # behavior; if so, generate an actual Idea behavior.
            # ---------------------------------------------------------------------

            # If the person belongs to a relevant Workstyle group that increases or decreases
            # his likelihood of generating Ideas, elevate or reduce his probability of
            # generating an Idea today.
            if cfg.persons[p].workstyle == "Group A":
                cfg.persons[p].prob_modified_idea = \
                    cfg.persons[p].prob_modified_idea * (1 + cfg.prob_elevation_for_idea_due_to_workstyle)
            elif cfg.persons[p].workstyle == "Group E":
                cfg.persons[p].prob_modified_idea = \
                    cfg.persons[p].prob_modified_idea * (1 - cfg.prob_reduction_for_idea_due_to_workstyle)

            # If the person meets the threshold to generate an Idea behavior...
            if cfg.persons[p].prob_modified_idea >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # Add the person's "Idea" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Idea", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Lapse
            # behavior; if so, generate an actual Lapse behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Lapse behavior...
            if cfg.persons[p].prob_modified_lapse >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Lapse" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Lapse", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Feat
            # behavior; if so, generate an actual Feat behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Feat behavior...
            if cfg.persons[p].prob_modified_feat >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # Add the person's "Feat" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Feat", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Slip
            # behavior; if so, generate an actual Slip behavior.
            # ---------------------------------------------------------------------

            # Every person has some probability of randomly generating a Slip.
            # First, check to see if that occurs.
            #
            # If the person meets the threshold to generate a random Slip behavior...
            if cfg.persons[p].prob_modified_slip >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Slip" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Slip", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # If the person *doesn't* generate a random Slip behavior, check to see if he
            # generates one as a result of having had 2 or more Lapses in the
            # previous 4 days.
            else:
                lapses_num_previous_4_days = 0
                for n in [-4, -3, -2, -1]:
                    lapses_num = return_num_of_events_of_type_for_person_on_DpmN(
                        cfg.persons[p], # the Person object whose events are to be searched
                        n, # relative number of the earlier/later day to seek (-1, 1, etc.)
                        "Lapse (Behavior Comptype)" # name of the column in which sought events are tallied
                        )
                    # lapses_num will be None if the date tested falls outside the sim's range.
                    if isinstance(lapses_num, int):
                        lapses_num_previous_4_days += lapses_num

                # If the person has 2 or more Lapses in the previous 4 days...
                if lapses_num_previous_4_days >= 2:

                    # ... he has a 90% chance of having a Slip today.
                    if (random.uniform(0.0, 1.0) <= 0.9):

                        # Add the person's "Slip" behavior to the behaviors DF.
                        add_one_behav_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Poor", # behavior type (string)
                            "Slip", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            )


            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Teamwork
            # behavior; if so, generate an actual Teamwork behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Teamwork behavior...
            if cfg.persons[p].prob_modified_teamwork >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # Add the person's "Teamwork" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Teamwork", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )


            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Disruption
            # behavior; if so, generate an actual Disruption behavior.
            # ---------------------------------------------------------------------

            # If the person belongs to a relevant Workstyle group that increases or decreases
            # his likelihood of generating Disruptions, elevate or reduce his probability of
            # generating a Disruption today.
            if cfg.persons[p].workstyle == "Group B":
                cfg.persons[p].prob_modified_disruption = \
                    cfg.persons[p].prob_modified_disruption * (1 + cfg.prob_elevation_for_disruption_due_to_workstyle)
            elif cfg.persons[p].workstyle == "Group D":
                cfg.persons[p].prob_modified_disruption = \
                    cfg.persons[p].prob_modified_disruption * (1 - cfg.prob_reduction_for_disruption_due_to_workstyle)

            # If the person meets the threshold to generate a Disruption behavior...
            if cfg.persons[p].prob_modified_disruption >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Disruption" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Disruption", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Sacrifice
            # behavior; if so, generate an actual Sacrifice behavior.
            # ---------------------------------------------------------------------

            # Every person has some probability of randomly generating a Sacrifice.
            # First, check to see if that occurs.

            # If the person meets the threshold to generate a Sacrifice behavior...
            if cfg.persons[p].prob_modified_sacrifice >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # Add the person's "Sacrifice" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Sacrifice", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )

            # If the person *doesn't* generate a random Sacrifice behavior, check to see if he
            # generates one as a result of having had 2 or more Teamworks in the
            # previous 5 days.
            else:
                teamworks_num_previous_5_days = 0
                for n in [-5, -4, -3, -2, -1]:
                    teamworks_num = return_num_of_events_of_type_for_person_on_DpmN(
                        cfg.persons[p], # the Person object whose events are to be searched
                        n, # relative number of the earlier/later day to seek (-1, 1, etc.)
                        "Teamwork (Behavior Comptype)" # name of the column in which sought events are tallied
                        )
                    # teamworks_num will be None if the date tested falls outside the sim's range.
                    if isinstance(teamworks_num, int):
                        teamworks_num_previous_5_days += teamworks_num

                # If the person has 2 or more Teamworks in the previous 5 days...
                if teamworks_num_previous_5_days >= 2:

                    # ... he has a 90% chance of having a Sacrifice today.
                    if (random.uniform(0.0, 1.0) <= 0.8):

                        # Add the person's "Sacrifice" behavior to the behaviors DF.
                        add_one_behav_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Good", # behavior type (string)
                            "Sacrifice", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            )


            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Sabotage
            # behavior; if so, generate an actual Sabotage behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Sabotage behavior...
            if cfg.persons[p].prob_modified_sabotage >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Sabotage" behavior to the behaviors DF.
                add_one_behav_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Sabotage", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    )


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for calculating metrics after the simulation's conclusion
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def calculate_metrics_for_persons_in_simulated_period():
    """
    Calculate minimum, maximum, and mean Efficacy scores for each
    person during the simulated period.
    """

    for p in cfg.persons:

        # Prepare a DF containing only the behaviors for the given person.
        behavs_act_df_this_pers = utils.return_df_with_rows_filtered_to_one_val_in_col(
            cfg.behavs_act_df, # the input DF
            "Person ID", # the column by which to filter rows
            cfg.persons[p].per_id, # the value to seek in the col (i.e., the restrictor)
            )

        days_present = behavs_act_df_this_pers["Presence (Behavior Comptype)"].count()

        # NOTE! These really shouldn't be "scores". They're actual behaviors.
        eff_bhv_act_min = behavs_act_df_this_pers["Actual Efficacy"].min()
        eff_bhv_act_max = behavs_act_df_this_pers["Actual Efficacy"].max()
        eff_bhv_act_mean = behavs_act_df_this_pers["Actual Efficacy"].mean()
        eff_bhv_act_sd = behavs_act_df_this_pers["Actual Efficacy"].std()

        # NOTE! This will generate an error if there *aren't* any Good or Poor
        # behaviors in the dataset -- which is possible, if the number of persons
        # or number of days simulated is very small.
        good_count = behavs_act_df_this_pers["Good (Behavior Type)"].count()
        poor_count = behavs_act_df_this_pers["Poor (Behavior Type)"].count()

        # print("person", str(p), min_eff_sco, mean_eff_sco, max_eff_sco)

        cfg.persons[p].days_attended = days_present
        cfg.persons[p].eff_bhv_act_min = eff_bhv_act_min
        cfg.persons[p].eff_bhv_act_max = eff_bhv_act_max
        cfg.persons[p].eff_bhv_act_mean = eff_bhv_act_mean
        cfg.persons[p].eff_bhv_act_sd = eff_bhv_act_sd
        cfg.persons[p].good_act_num = good_count
        cfg.persons[p].poor_act_num = poor_count


def return_behavs_act_df_for_person_for_DpmN(
    version_of_behavs_act_df_to_use_u, # version of behavs_act_df to use
    person_u, # the Person object whose data should be sought
    DpmN_N_value_u, # relative number of the earlier/later day to seek (-1, 1, etc.)
    ):
    """
    Returns a version of behavs_act_df that has been trimmed to
    only include behaviors of a given Person on a given day, as
    defined relative to the current day (-3, -2, -1, etc.).
    """

    # Restrict the DF to only entries for the given subject.
    temp_df = version_of_behavs_act_df_to_use_u.copy()
    temp_df = temp_df[ temp_df["Person ID"] == person_u.per_id ]

    # Restrict the DF to only entries for the targeted date.
    target_date = cfg.current_datetime_obj + timedelta(days = DpmN_N_value_u)
    temp_df = temp_df[ temp_df["Person ID"] == person_u.per_id ] 

    temp_df = utils.return_df_with_rows_filtered_to_one_val_in_col(
        temp_df, # the input DF
        "Behavior Datetime", # the column by which to filter rows
        target_date, # the value to seek in the col (i.e., the restrictor)
        )

    return temp_df


def return_num_of_events_of_type_for_person_on_DpmN(
    person_u, # the Person object whose events are to be searched
    DpmN_N_value_u, # relative number of the earlier/later day to seek (-1, 1, etc.)
    column_to_search_for_events_u # name of the column in which sought events are tallied
    ):
    """
    Return the number of events of a certain Type (or Comptype)
    for a given person on a given day defined relative to the
    current day. It will return None if that day doesn't exist (e.g.,
    because it would fall outside of the time range of the simualation).
    """

    # If the sought day falls before the start of the sim's time range, return None.
    if cfg.day_of_sim_iter + DpmN_N_value_u < 0:
        return None
    # If the sought day falls after the end of the sim's time range, return None.
    elif cfg.day_of_sim_iter + DpmN_N_value_u >= cfg.num_of_days_to_simulate:
        return None

    # Get behavs_act_df for the given person for the relevant day.
    temp_df = return_behavs_act_df_for_person_for_DpmN(
        cfg.behavs_act_df, # version of behavs_act_df to use
        person_u, # the Person object whose data should be sought
        DpmN_N_value_u, # relative number of the earlier/later day to seek (-1, 1, etc.)
        )

    events_num = temp_df[column_to_search_for_events_u].sum()
    return events_num


def return_eff_modifier_for_impact_of_previous_recordings_on_bhv_of_person_today(
    person_u, # the Person object whose behavior may be impacted
    ):
    """
    Returns a modifier for use in a person's daily Efficacy behavior
    calculation that reflects the impact of the fact that his supervisor
    accurately (True Positive) or inaccurately (False Negative) recorded
    Good behaviors performed by the person in the previous days.
    """

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Get any Eff modifier component resulting from accurately recorded
    # █ (True Positive) Idea, Feat, Teamwork, or Sacrifice behavior
    # █ in recent days.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    # Initialize these values.
    num_TP_recs_Dm3_good = 0.0
    num_TP_recs_Dm2_good = 0.0
    num_TP_recs_Dm1_good = 0.0

    # Create a DF with just True Positive behaviors for the person in question.
    temp_df = utils.return_df_with_rows_filtered_to_one_val_in_col(
        cfg.behavs_act_df, # the input DF
        "Person ID", # the column by which to filter rows
        person_u, # the value to seek in the col (i.e., the restrictor)
        )
    temp_df_TP_good = temp_df[ 
        (temp_df["Behavior Type"] == "Good") \
        & (temp_df["Record Conf Mat"] == "True Positive")
        ]

    # Check for an accurately recorded behavior of the given type
    # on D-3. Only run this check if the current day of the simulation
    # is day 4 or later.
    if cfg.day_of_sim_iter >= 4:
        target_date = cfg.current_datetime_obj + timedelta(days = -3)
        temp_df_TP_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm3_good = len(temp_df_TP_good)

    # Check for an accurately recorded behavior of the given type
    # on D-2. Only run this check if the current day of the simulation
    # is day 3 or later.
    if cfg.day_of_sim_iter >= 3:
        target_date = cfg.current_datetime_obj + timedelta(days = -2)
        temp_df_TP_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm3_good = len(temp_df_TP_good)

    # Check for an accurately recorded behavior of the given type
    # on D-1. Only run this check if the current day of the simulation
    # is day 2 or later.
    if cfg.day_of_sim_iter >= 2:
        target_date = cfg.current_datetime_obj + timedelta(days = -1)
        temp_df_TP_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm3_good = len(temp_df_TP_good)

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Get any Eff modifier component resulting from inaccurately recorded
    # █ (False Negative) Idea, Feat, Teamwork, or Sacrifice behavior
    # █ in recent days.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    # Initialize these values.
    num_FN_recs_Dm3_good = 0.0
    num_FN_recs_Dm2_good = 0.0
    num_FN_recs_Dm1_good = 0.0

    # Create a DF with just False Negative behaviors for the person in question.
    temp_df = utils.return_df_with_rows_filtered_to_one_val_in_col(
        cfg.behavs_act_df, # the input DF
        "Person ID", # the column by which to filter rows
        person_u, # the value to seek in the col (i.e., the restrictor)
        )
    temp_df_FN_good = temp_df[ 
        (temp_df["Behavior Type"] == "Good") \
        & (temp_df["Record Conf Mat"] == "False Negative")
        ]

    # Check for an inaccurately recorded behavior of the given type
    # on D-3. Only run this check if the current day of the simulation
    # is day 4 or later.
    if cfg.day_of_sim_iter >= 4:
        target_date = cfg.current_datetime_obj + timedelta(days = -3)
        temp_df_FN_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm3_good = len(temp_df_FN_good)

    # Check for an inaccurately recorded behavior of the given type
    # on D-2. Only run this check if the current day of the simulation
    # is day 3 or later.
    if cfg.day_of_sim_iter >= 3:
        target_date = cfg.current_datetime_obj + timedelta(days = -2)
        temp_df_FN_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm3_good = len(temp_df_FN_good)

    # Check for an inaccurately recorded behavior of the given type
    # on D-1. Only run this check if the current day of the simulation
    # is day 2 or later.
    if cfg.day_of_sim_iter >= 2:
        target_date = cfg.current_datetime_obj + timedelta(days = -1)
        temp_df_FN_good = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Behavior Datetime", # the column by which to filter rows
            target_date, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm3_good = len(temp_df_FN_good)

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Calculate the overall modifier.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    mod_to_eff_for_previous_TP_FN_records_good = \
        1 + \
        (
            # Add any positive modifiers for TP records.
            1.0 * num_TP_recs_Dm3_good * cfg.strength_of_good_TP_record_impact_on_eff \
            + 2.0 * num_TP_recs_Dm2_good * cfg.strength_of_good_TP_record_impact_on_eff \
            + 3.0 * num_TP_recs_Dm1_good * cfg.strength_of_good_TP_record_impact_on_eff \
            # Add any negative modifiers for FN records.
            - 1.0 * num_FN_recs_Dm3_good * cfg.strength_of_good_FN_record_impact_on_eff \
            - 2.0 * num_FN_recs_Dm2_good * cfg.strength_of_good_FN_record_impact_on_eff \
            - 3.0 * num_FN_recs_Dm1_good * cfg.strength_of_good_FN_record_impact_on_eff
            ) \
        * cfg.strength_of_effect

    return mod_to_eff_for_previous_TP_FN_records_good


def display_simple_behavior_statistics():

    # Get the number of Good and Poor behaviors.
    behavs_good_num = \
        cfg.behavs_act_df["Behavior Type"].value_counts()["Good"]
    behavs_poor_num = \
        cfg.behavs_act_df["Behavior Type"].value_counts()["Poor"]

    behavs_good_num_per_pers_per_day = \
        behavs_good_num / cfg.size_of_comm_initial / cfg.num_of_days_to_simulate
    behavs_poor_num_per_pers_per_day = \
        behavs_poor_num / cfg.size_of_comm_initial / cfg.num_of_days_to_simulate

    print("Number of Good behaviors: ", behavs_good_num)
    print("Good behaviors per person per day: ", behavs_good_num_per_pers_per_day)
    print("Number of Poor behaviors: ", behavs_poor_num)
    print("Poor behaviors per person per day: ", behavs_poor_num_per_pers_per_day)



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