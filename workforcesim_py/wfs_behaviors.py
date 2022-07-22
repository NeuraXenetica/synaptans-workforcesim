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
daily productivity and interpersonal interactions of workers
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
    import wfs_utilities as utils
    import wfs_personnel as pers
else:
    try:
        from . import config as cfg
    except:
        import config as cfg
    try:
        from . import wfs_utilities as utils
    except:
        import wfs_utilities as utils
    try:
        from . import wfs_personnel as pers
    except:
        import wfs_personnel as pers


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
    Absence, which is itself a sort of behavior) -- by creating initial
    columns needed for adding behavior entries.
    """

    # Create as an empty DF.
    cfg.behavs_act_df = pd.DataFrame()

    # Create the DF's initial columns.
    cfg.behavs_act_df["Sub ID"] = 0
    cfg.behavs_act_df["Sub First Name"] = "" 
    cfg.behavs_act_df["Sub Last Name"] = ""
    cfg.behavs_act_df["Sub Age"] = 0
    cfg.behavs_act_df["Sub Sex"] = ""
    cfg.behavs_act_df["Sub Shift"] = ""
    cfg.behavs_act_df["Sub Team"] = ""
    cfg.behavs_act_df["Sub Role"] = ""
    cfg.behavs_act_df["Sub Colleague IDs"] = []
    cfg.behavs_act_df["Sub Same-Sex Colleagues Prtn"] = None
    cfg.behavs_act_df["Sub Health"] = None
    cfg.behavs_act_df["Sub Commitment"] = None
    cfg.behavs_act_df["Sub Perceptiveness"] = None
    cfg.behavs_act_df["Sub Dexterity"] = None
    cfg.behavs_act_df["Sub Sociality"] = None
    cfg.behavs_act_df["Sub Goodness"] = None
    cfg.behavs_act_df["Sub Strength"] = None
    cfg.behavs_act_df["Sub Openmindedness"] = None
    cfg.behavs_act_df["Sub Workstyle"] = ""
    cfg.behavs_act_df["Sup ID"] = 0
    cfg.behavs_act_df["Sup First Name"] = "" 
    cfg.behavs_act_df["Sup Last Name"] = ""
    cfg.behavs_act_df["Sup Age"] = None
    cfg.behavs_act_df["Sup-Sub Age Difference"] = None
    cfg.behavs_act_df["Sup Sex"] = ""
    cfg.behavs_act_df["Sup Role"] = ""
    cfg.behavs_act_df["Sup Commitment"] = None
    cfg.behavs_act_df["Sup Perceptiveness"] = None
    cfg.behavs_act_df["Sup Goodness"] = None
    cfg.behavs_act_df["Event Datetime"] = None
    cfg.behavs_act_df["Event Date"] = None
    cfg.behavs_act_df["Week in Series"] = None
    cfg.behavs_act_df["Day in Series (1-based)"] = None
    cfg.behavs_act_df["Weekday Num"] = None
    cfg.behavs_act_df["Weekday Name"] = ""
    cfg.behavs_act_df["Behavior Type"] = "" # the "main type" of the behavior (e.g., "Attendance")
    cfg.behavs_act_df["Behavior Comptype"] = "" # the "comparison type" of the behavior for plotting (e.g., "Absence")
    cfg.behavs_act_df["Behavior Nature"] = "" # the "nature" of the behavior (e.g., "Excused Absence")
    cfg.behavs_act_df["Actual Efficacy"] = None
    cfg.behavs_act_df["Actual Efficacy (SD)"] = None
    cfg.behavs_act_df["Record Type"] = ""
    cfg.behavs_act_df["Record Comptype"] = ""
    cfg.behavs_act_df["Record Nature"] = ""
    cfg.behavs_act_df["Recorded Efficacy"] = None
    cfg.behavs_act_df["Note"] = None
    cfg.behavs_act_df["Record Conf Mat"] = None
    #cfg.behavs_act_df["Subordinate IDs"] = []
    #cfg.behavs_act_df["Behavior Subtype"] = "" # the "subtype" of the behavior (e.g., "Absence")
    #cfg.behavs_act_df["Record Subtype"] = ""


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


def add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
    person_object_u, # Person object for the person who performed the behavior
    behavior_type_u, # behavior type (string)
    behavior_subtype_u, # behavior subtype (string)
    behavior_nature_u, # behavior nature (string)
    behavior_comptype_u, # behavior comptype (string)
    eff_score_u, # the actual Efficacy (if relevant) demonstrated in the behavior
    include_record_u, # whether to include a record (e.g., for a Separation or Onboarding event)
    ):
    """
    Adds a particular behavior by a particular person (e.g., as
    just generated by a daily behavior-generator) to behavs_act_df,
    the master DF of all actual behaviors performed by persons
    (including Absences). It copies into the behavs_act_df relevant
    facts (e.g., the ID of a person's supervisor) as they exist
    *in the moment of the behavior*, thereby creating a lasting
    record of the circumstances in which the behavior occurred.
    """

    # NOTE: This function originally immediately added each new behavior
    # to behavs_act_df as a concatenated row, but that approach generates
    # exponential copying effects tied to the number of days in the sim.
    # Now all of the rows are temporarily stored and all added to the
    # DF in a single step at the end.

    # ---------------------------------------------------------------------
    # Calculates the contents of columns containing data
    # regarding the behavior performed and subject who performed it.
    # ---------------------------------------------------------------------

    # Calculate the values of fields related to the subject's supervisor.
    # This is only relevant if a person *has* a supervisor (e.g., if he
    # isn't the factory's Production Director).
    try:
        sup_ID_to_use = person_object_u.sup.per_id
        sup_age_to_use = person_object_u.sup.age
        sup_sub_age_diff = person_object_u.sup.age - person_object_u.age
        sup_fname_to_use = person_object_u.sup.f_name
        sup_lname_to_use = person_object_u.sup.l_name
        sup_sex_to_use = person_object_u.sup.sex
        sup_role_to_use = person_object_u.sup.role
        sup_commitment_to_use = person_object_u.sup.stat_commitment
        sup_perceptiveness_to_use = person_object_u.sup.stat_perceptiveness
        sup_goodness_to_use = person_object_u.sup.stat_goodness
    except AttributeError:
        sup_ID_to_use = None
        sup_age_to_use = None
        sup_sub_age_diff = None
        sup_fname_to_use = None
        sup_lname_to_use = None
        sup_sex_to_use = None
        sup_role_to_use = None
        sup_commitment_to_use = None
        sup_perceptiveness_to_use = None
        sup_goodness_to_use = None

    # Calculate the value for the person's "Sub Colleague IDs" field.
    # Determines whether the person has a supervisor or not (e.g., if he
    # is the factory's Production Director, who has no supervisor).
    try:
        colleague_IDs_to_use = [p.per_id for p in person_object_u.colleagues]
    except TypeError:
        colleague_IDs_to_use = None

    # Calculate the value for the "Week in Series" column.
    week_in_series = utils.return_week_in_series_for_given_date(
        cfg.current_datetime_obj.date(), # the date whose week should be returned
        )

    behav_to_add_df = pd.DataFrame({
        "Sub ID": [person_object_u.per_id],
        "Sub First Name": [person_object_u.f_name],
        "Sub Last Name": [person_object_u.l_name],
        "Sub Age": [person_object_u.age],
        "Sub Sex": [person_object_u.sex],
        "Sub Shift": [person_object_u.shift.title],
        "Sub Team": [person_object_u.team.title],
        "Sub Role": [person_object_u.role.title],
        "Sub Colleague IDs": [colleague_IDs_to_use],
        "Sub Same-Sex Colleagues Prtn": [person_object_u.colleagues_of_same_sex_prtn],
        "Sub Health": [person_object_u.stat_health],
        "Sub Commitment": [person_object_u.stat_commitment],
        "Sub Perceptiveness": [person_object_u.stat_perceptiveness],
        "Sub Dexterity": [person_object_u.stat_dexterity],
        "Sub Sociality": [person_object_u.stat_sociality],
        "Sub Goodness": [person_object_u.stat_goodness],
        "Sub Strength": [person_object_u.stat_strength],
        "Sub Openmindedness": [person_object_u.stat_openmindedness],
        "Sub Workstyle": [person_object_u.workstyle],
        "Sup ID": [sup_ID_to_use],
        "Sup First Name": [sup_fname_to_use],
        "Sup Last Name": [sup_lname_to_use],
        "Sup Age": [sup_age_to_use],
        "Sup-Sub Age Difference": [sup_sub_age_diff],
        "Sup Sex": [sup_sex_to_use],
        "Sup Role": [sup_role_to_use],
        "Sup Commitment": [sup_commitment_to_use],
        "Sup Perceptiveness": [sup_perceptiveness_to_use],
        "Sup Goodness": [sup_goodness_to_use],
        "Event Datetime": [cfg.current_datetime_obj],
        "Event Date": [cfg.current_datetime_obj.date()],
        "Week in Series": week_in_series,
        "Day in Series (1-based)": [cfg.day_of_sim_iter + 1],
        "Weekday Num": [cfg.current_datetime_obj.weekday()],
        "Weekday Name": [cfg.current_datetime_obj.strftime("%A")],
        "Behavior Type": [behavior_type_u],
        "Behavior Comptype": [behavior_comptype_u],
        "Behavior Nature": [behavior_nature_u],
        "Actual Efficacy": [eff_score_u],
        "Actual Efficacy (SD)": [eff_score_u], # The SD value will be calculated later.
        "Record Type": None,
        "Record Comptype": None,
        "Record Nature": None,
        "Recorded Efficacy": None,
        "Note": None,
        "Record Conf Mat": None,
        })


    # ---------------------------------------------------------------------
    # Include a record for workers' Separation (Resignation or Termination) and 
    # Onboarding events. These events are always recorded by managers with 100%
    # accuracy, and the record is added to the DF at the same time as the
    # underlying behavior, as part of a unified event.
    #
    # (This is necessary because Separation and Onboarding is handled) at a 
    # different time of day, outside of the normal daily event cycle.)
    # ---------------------------------------------------------------------
    if include_record_u is True:
        if (behav_to_add_df["Behavior Type"].values[0] == "Separation") \
            | (behav_to_add_df["Behavior Type"].values[0] == "Onboarding"):

            # Copy the main Behavior Type and Comptype fields
            # into the corresponding record fields.
            behav_to_add_df["Record Type"].values[0] = \
                behav_to_add_df["Behavior Type"].values[0]
            behav_to_add_df["Record Comptype"].values[0] = \
                behav_to_add_df["Behavior Comptype"].values[0]

            # The lack of a Note will be represented by an empty string ("")
            # rather than a None value.
            behav_to_add_df["Note"].values[0] = ""

            # If the event was a Termination (and not a Resignation), then
            # the event's type and cause should be noted in the *record* component 
            # of the row (since it was the supervisor who initiated that event, not 
            # the subordinate) -- not in the behavior component, as is the case with
            # a Resignation event.
            # 
            # Reflect this by (1) changing the "Behavior Type" and "Behavior
            # Comptype" to None values, and (2) moving the description of the
            # cause from the "Behavior Nature" column to the "Record Nature"
            # column and filling the "Behavior Nature" field with a None value.
            #
            # Here, the event will thus have only a record component, not a behavior
            # component.
            if behav_to_add_df["Behavior Comptype"].values[0] == "Termination":

                behav_to_add_df["Behavior Type"].values[0] = None
                behav_to_add_df["Behavior Comptype"].values[0] = None

                behav_to_add_df["Record Nature"].values[0] = \
                    behav_to_add_df["Behavior Nature"].values[0]
                behav_to_add_df["Behavior Nature"].values[0] = None


    # Appends behav_to_add_df to the list of calculated behaviors
    # (each as a separate DF) that will later all be added to
    # behavs_act_df in a single step.
    cfg.list_of_behavs_to_add_to_behavs_act_df.append(behav_to_add_df)


def simulate_one_day_of_behaviors():
    """
    Simulates one day's worth of workers' actual behaviors.
    """

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Generate no behaviors and exit the function, if it's a 
    # █ Saturday or Sunday.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    # If the current weekday is Sunday, skip ahead
    # without generating any behaviors for any workers.
    if cfg.current_datetime_obj.weekday() == 6:
        return


    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Calculate values for the organization as a whole (not a 
    # █ particular person) that will be needed for determining what sort
    # █ of behaviors occur.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    # Calculate the mean of all actual Eff values generated in the org to date.
    # Only include the values from the Eff-value dictionaries up through the
    # current date of the simulation (the later values will be None).
    list_of_all_actual_eff_values = []
    for p in cfg.persons:
        list_of_all_actual_eff_values.extend(list(cfg.persons[p].dict_days_with_actual_eff_values.values())[0:(cfg.day_of_sim_iter - cfg.day_of_sim_iter_for_first_simulated_day)])

    try:
        # Remove all None values from the list of actual Efficacy values.
        list_of_all_actual_eff_values = [v for v in list_of_all_actual_eff_values if v is not None]
        cfg.org_actual_eff_values_mean = \
            statistics.mean(list_of_all_actual_eff_values)
    # This is the case at the start of the first simulated day, when
    # the length of the list of generated values will have a length of 0.
    except:
        cfg.org_actual_eff_values_mean = None

    # Calculate the mean of all Eff values recorded in the org to date.
    list_of_all_recorded_eff_values = []
    for p in cfg.persons:
        list_of_all_recorded_eff_values.extend(list(cfg.persons[p].dict_days_with_recorded_eff_values.values())[0:(cfg.day_of_sim_iter - cfg.day_of_sim_iter_for_first_simulated_day)])
    try:
        # Remove all None values from the list of recorded Efficacy values.
        list_of_all_recorded_eff_values = [v for v in list_of_all_recorded_eff_values if v is not None]
        cfg.org_recorded_eff_values_mean = \
            statistics.mean(list_of_all_recorded_eff_values)
    # This is the case at the start of the first simulated day, when
    # the length of the list of generated values will have a length of 0.
    except:
        cfg.org_recorded_eff_values_mean = None

    print("   cfg.org_actual_eff_values_mean at start of day: ", cfg.org_actual_eff_values_mean)


    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Determine each person's behaviors.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    for p in cfg.persons:

        # If a person is already separated from employment, no new
        # behaviors can be generated for that person.
        if cfg.persons[p].separated is True:
            # Skip ahead to the next person.
            continue

        # If the current weekday is Saturday, there is only a tiny
        # chance that a worker will be called in for work to handle some
        # special assignment. Such a person's supervisor will come
        # in only briefly to record the worker's behavior. The 
        # supervisor doesn't work a full, normal day and doesn't have
        # any work of his own, other than recording the worker's
        # behavior; the supervisor thus won't generate any behaviors
        # of his own (including an Attendance or Efficacy) for that day.
        if cfg.current_datetime_obj.weekday() == 5:
            if random.uniform(0.0, 1.0) > cfg.base_rate_attendance_sat:
                # Skip ahead to the next person.
                continue


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● Calculate the person's attendance status and generate a "Presence" or
        # ● "Absence" behavior.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

        # Every person has some probability of randomly generating an Absence.
        # First, check to see if that occurs.

        # If the person's modified probability of a Presence is less than
        # a random number from 0.00-1.00, the person is absent (i.e.,
        # performs an Absence behavior).
        if cfg.persons[p].prob_modified_presence < random.uniform(0.0, 1.0):
            attendance_today = "absent"

            # Add the person's "Absence" behavior to the behaviors DF.
            add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                cfg.persons[p], # Person object for the person who performed the behavior
                "Attendance", # behavior type (string)
                "Absence", # behavior subtype (string)
                None, # behavior nature (string)
                "Absence", # behavior comptype (string)
                None, # the actual Efficacy (if relevant) demonstrated in the behavior
                False, # whether to include a record (e.g., for a Separation or Onboarding event)
                )

        # If the person *doesn't* generate a random Absence behavior, check to see if he
        # generates one as a result of having had at least 1 Lapse and 1 Slip in the
        # previous 4 days.
        else:
            lapses_num_previous_4_days = 0
            day_deltas = [-4, -3, -2, -1]
            days_to_search = [cfg.day_of_sim_iter + delta for delta in day_deltas]
            for day in days_to_search:
                # Confirm that the sought day is within the simulated range.
                if day in cfg.persons[p].dict_days_with_num_of_lapse_behaviors:
                    lapses_num_previous_4_days += \
                        cfg.persons[p].dict_days_with_num_of_lapse_behaviors[day]

            slips_num_previous_4_days = 0
            day_deltas = [-4, -3, -2, -1]
            days_to_search = [cfg.day_of_sim_iter + delta for delta in day_deltas]
            for day in days_to_search:
                # Confirm that the sought day is within the simulated range.
                if day in cfg.persons[p].dict_days_with_num_of_slip_behaviors:
                    slips_num_previous_4_days += \
                        cfg.persons[p].dict_days_with_num_of_slip_behaviors[day]

            # If the person has at least 1 Lapse and 1 Slip in the previous 4 days...
            if (lapses_num_previous_4_days >= 1) & (slips_num_previous_4_days >= 1):

                # ... he has a 90% chance of having an Absence today.
                if (random.uniform(0.0, 1.0) <= 0.9):
                    attendance_today = "absent"

                    # Add the person's "Absence" behavior to the behaviors DF.
                    add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Attendance", # behavior type (string)
                        "Absence", # behavior subtype (string)
                        None, # behavior nature (string)
                        "Absence", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        False, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                # If he succeeds at the 10% roll, then he is present today.
                else:
                    attendance_today = "present"

                    # Add the person's "Presence" behavior to the behaviors DF.
                    add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                        cfg.persons[p], # Person object for the person who performed the behavior
                        "Attendance", # behavior type (string)
                        "Presence", # behavior subtype (string)
                        None, # behavior nature (string)
                        "Presence", # behavior comptype (string)
                        None, # the actual Efficacy (if relevant) demonstrated in the behavior
                        False, # whether to include a record (e.g., for a Separation or Onboarding event)
                        )

                    # Increase the person's number of days attended by 1.
                    cfg.persons[p].days_attended += 1

            # If he doesn't have at least 1 Lapse and 1 Slip in the previous 4 days,
            # then he is present today.
            else:
                attendance_today = "present"

                # Add the person's "Presence" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Attendance", # behavior type (string)
                    "Presence", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Presence", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

                # Increase the person's number of days attended by 1.
                cfg.persons[p].days_attended += 1


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
        # ● If the person is present, calculate whether (or how) he performs
        # ● particular types of behaviors.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

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

            if eff_sco_today < 0.0:
                eff_sco_today = 0.0

            # Add the person's "Efficacy" behavior to the behaviors DF.
            add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                cfg.persons[p], # Person object for the person who performed the behavior
                "Efficacy", # behavior type (string)
                None, # behavior subtype (string)
                None, # behavior nature (string)
                "Efficacy", # behavior comptype (string)
                eff_sco_today, # the actual Efficacy (if relevant) demonstrated in the behavior
                False, # whether to include a record (e.g., for a Separation or Onboarding event)
                )
            #print("Final Efficacy for person: ", eff_sco_today)

            # In this Person object's dictionary that stores the number of events of this
            # type that have occurred on each day, add the actual Efficacy value.
            # (At dict creation, the values for all days are 0.0.)
            # Note! This presumes that a person can only generate one Efficacy behavior per day.
            # The new value overwrites any existing value for the day.
            cfg.persons[p].dict_days_with_actual_eff_values[cfg.day_of_sim_iter] = eff_sco_today


            # ---------------------------------------------------------------------
            # Calculate whether the person performs an Idea
            # behavior; if so, generate an actual Idea behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate an Idea behavior...
            if cfg.persons[p].prob_modified_idea >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # In this Person object's dictionary that stores the number of events of this
                # type that have occurred on each day, increment the value for this day
                # (as the key) by 1. (At dict creation, the values for all days are 0.)
                cfg.persons[p].dict_days_with_num_of_idea_behaviors[cfg.day_of_sim_iter] += 1

                # Add the person's "Idea" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Idea", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Idea", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Lapse
            # behavior; if so, generate an actual Lapse behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Lapse behavior...
            if cfg.persons[p].prob_modified_lapse >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # In this Person object's dictionary that stores the number of events of this
                # type that have occurred on each day, increment the value for this day
                # (as the key) by 1. (At dict creation, the values for all days are 0.)
                cfg.persons[p].dict_days_with_num_of_lapse_behaviors[cfg.day_of_sim_iter] += 1

                # Add the person's "Lapse" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Lapse", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Lapse", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Feat
            # behavior; if so, generate an actual Feat behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Feat behavior...
            if cfg.persons[p].prob_modified_feat >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # Add the person's "Feat" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Feat", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Feat", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
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

                # In this Person object's dictionary that stores the number of events of this
                # type that have occurred on each day, increment the value for this day
                # (as the key) by 1. (At dict creation, the values for all days are 0.)
                cfg.persons[p].dict_days_with_num_of_slip_behaviors[cfg.day_of_sim_iter] += 1

                # Add the person's "Slip" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Slip", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Slip", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

            # If the person *doesn't* generate a random Slip behavior, check to see if he
            # generates one as a result of having had 2 or more Lapses in the
            # previous 4 days.
            else:
                lapses_num_previous_4_days = 0
                day_deltas = [-4, -3, -2, -1]
                days_to_search = [cfg.day_of_sim_iter + delta for delta in day_deltas]
                for day in days_to_search:
                    # Confirm that the sought day is within the simulated range.
                    if day in cfg.persons[p].dict_days_with_num_of_lapse_behaviors:
                        lapses_num_previous_4_days += \
                            cfg.persons[p].dict_days_with_num_of_lapse_behaviors[day]

                # If the person has 2 or more Lapses in the previous 4 days...
                if lapses_num_previous_4_days >= 2:

                    # ... he has a 90% chance of having a Slip today.
                    if (random.uniform(0.0, 1.0) <= 0.9):

                        # In this Person object's dictionary that stores the number of events of this
                        # type that have occurred on each day, increment the value for this day
                        # (as the key) by 1. (At dict creation, the values for all days are 0.)
                        cfg.persons[p].dict_days_with_num_of_slip_behaviors[cfg.day_of_sim_iter] += 1

                        # Add the person's "Slip" behavior to the behaviors DF.
                        add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Poor", # behavior type (string)
                            "Slip", # behavior subtype (string)
                            None, # behavior nature (string)
                            "Slip", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            False, # whether to include a record (e.g., for a Separation or Onboarding event)
                            )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Teamwork
            # behavior; if so, generate an actual Teamwork behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Teamwork behavior...
            if cfg.persons[p].prob_modified_teamwork >= (random.uniform(0.0, cfg.defense_roll_max_behavior_good)):

                # In this Person object's dictionary that stores the number of events of this
                # type that have occurred on each day, increment the value for this day
                # (as the key) by 1. (At dict creation, the values for all days are 0.)
                cfg.persons[p].dict_days_with_num_of_teamwork_behaviors[cfg.day_of_sim_iter] += 1

                # Add the person's "Teamwork" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Teamwork", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Teamwork", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Disruption
            # behavior; if so, generate an actual Disruption behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Disruption behavior...
            if cfg.persons[p].prob_modified_disruption >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Disruption" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Disruption", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Disruption", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
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
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Good", # behavior type (string)
                    "Sacrifice", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Sacrifice", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )

            # If the person *doesn't* generate a random Sacrifice behavior, check to see if he
            # generates one as a result of having had 2 or more Teamworks in the
            # previous 5 days.
            else:
                teamworks_num_previous_5_days = 0
                day_deltas = [-5, -4, -3, -2, -1]
                days_to_search = [cfg.day_of_sim_iter + delta for delta in day_deltas]
                for day in days_to_search:
                    # Confirm that the sought day is within the simulated range.
                    if day in cfg.persons[p].dict_days_with_num_of_teamwork_behaviors:
                        teamworks_num_previous_5_days += \
                            cfg.persons[p].dict_days_with_num_of_teamwork_behaviors[day]

                # If the person has 2 or more Teamworks in the previous 5 days...
                if teamworks_num_previous_5_days >= 2:

                    # ... he has an 80% chance of having a Sacrifice today.
                    if (random.uniform(0.0, 1.0) <= 0.8):

                        # Add the person's "Sacrifice" behavior to the behaviors DF.
                        add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                            cfg.persons[p], # Person object for the person who performed the behavior
                            "Good", # behavior type (string)
                            "Sacrifice", # behavior subtype (string)
                            None, # behavior nature (string)
                            "Sacrifice", # behavior comptype (string)
                            None, # the actual Efficacy (if relevant) demonstrated in the behavior
                            False, # whether to include a record (e.g., for a Separation or Onboarding event)
                            )

            # ---------------------------------------------------------------------
            # Calculate whether the person performs a Sabotage
            # behavior; if so, generate an actual Sabotage behavior.
            # ---------------------------------------------------------------------

            # If the person meets the threshold to generate a Sabotage behavior...
            if cfg.persons[p].prob_modified_sabotage >= (random.uniform(0.0, cfg.defense_roll_max_behavior_poor)):

                # Add the person's "Sabotage" behavior to the behaviors DF.
                add_one_behav_to_list_of_behavs_to_add_to_behavs_act_df(
                    cfg.persons[p], # Person object for the person who performed the behavior
                    "Poor", # behavior type (string)
                    "Sabotage", # behavior subtype (string)
                    None, # behavior nature (string)
                    "Sabotage", # behavior comptype (string)
                    None, # the actual Efficacy (if relevant) demonstrated in the behavior
                    False, # whether to include a record (e.g., for a Separation or Onboarding event)
                    )


    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # █ Concatenate behavs_act_df with the individual DFs for the day, each of
    # █ which is a one-row DF containing info on a particular behavior.
    # █ This can't be delayed further (to avoid exponential copying), because
    # █ it's needed in order to now calculate managers' recordings for
    # █ the given day.
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    # If len(cfg.behavs_act_df) == 0, this is the first day to have been 
    # simulated; simply concatenate all of this day's DFs to one another.
    if len(cfg.behavs_act_df) == 0:
        list_of_dfs_to_concatenate = cfg.list_of_behavs_to_add_to_behavs_act_df

    # If len(cfg.behavs_act_df) != 0, then that DF already contains one or more
    # days' worth of behaviors; concatenate all of this day's new DFs to that
    # existing cfg.behavs_act_df.
    else:
        list_of_dfs_to_concatenate = [cfg.behavs_act_df]
        list_of_dfs_to_concatenate.extend(cfg.list_of_behavs_to_add_to_behavs_act_df)

    cfg.behavs_act_df = pd.concat(
        list_of_dfs_to_concatenate,
        ignore_index=True,
        axis=0,
        )

    # Having added all of the day's behaviors to behavs_act_df,
    # reset this to an empty list.
    cfg.list_of_behavs_to_add_to_behavs_act_df = []


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for calculating metrics after the simulation's conclusion
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def calculate_metrics_for_persons_in_retained_simulated_period():
    """
    Calculate minimum, maximum, and mean Efficacy scores for each
    person during the "live" portion of the simulated period 
    that is retained for analysis (excluding any priming period).
    """

    for p in cfg.persons:

        # Prepare a DF containing only the behaviors for the given person.
        behavs_act_df_this_pers = utils.return_df_with_rows_filtered_to_one_val_in_col(
            cfg.behavs_act_df, # the input DF
            "Sub ID", # the column by which to filter rows
            cfg.persons[p].per_id, # the value to seek in the col (i.e., the restrictor)
            )

        try:
            days_present = behavs_act_df_this_pers["Behavior Comptype"].value_counts()["Presence"]
        except:
            days_present = 0

        # NOTE! These really shouldn't be thought of as "scores". They're actual behaviors.
        eff_bhv_act_min = behavs_act_df_this_pers["Actual Efficacy"].min()
        eff_bhv_act_max = behavs_act_df_this_pers["Actual Efficacy"].max()
        eff_bhv_act_mean = behavs_act_df_this_pers["Actual Efficacy"].mean()
        eff_bhv_act_sd = behavs_act_df_this_pers["Actual Efficacy"].std()

        # NOTE! This will generate an error if there *aren't* any Good or Poor
        # behaviors in the dataset -- which is possible, if the number of persons
        # or number of days simulated is very small.
        try:
            good_count = behavs_act_df_this_pers["Behavior Type"].value_counts()["Good"]
        except:
            good_count = 0
        try:
            poor_count = behavs_act_df_this_pers["Behavior Type"].value_counts()["Poor"]
        except:
            poor_count = 0

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
    defined relative to the current day (day -3, -2, -1, etc.).
    """

    # Restrict the DF to only entries for the given subject.
    temp_df = version_of_behavs_act_df_to_use_u.copy()
    temp_df = temp_df[ temp_df["Sub ID"] == person_u.per_id ]

    # Restrict the DF to only entries for the targeted date.
    target_date = cfg.current_datetime_obj + timedelta(days = DpmN_N_value_u)
    temp_df = temp_df[ temp_df["Sub ID"] == person_u.per_id ] 

    temp_df = utils.return_df_with_rows_filtered_to_one_val_in_col(
        temp_df, # the input DF
        "Event Datetime", # the column by which to filter rows
        target_date, # the value to seek in the col (i.e., the restrictor)
        )

    return temp_df


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
        "Sub ID", # the column by which to filter rows
        person_u.per_id, # the value to seek in the col (i.e., the restrictor)
        )
    temp_df_TP_good = temp_df[ 
        (temp_df["Behavior Type"] == "Good") \
        & (temp_df["Record Conf Mat"] == "True Positive")
        ]
    #print("Length of temp_df_TP_good for this person: ", len(temp_df_TP_good))

    # Check for an accurately recorded behavior of the given type
    # on D-3. Only run this check if the current day of the simulation
    # is day 4 or later.
    if cfg.day_of_sim_iter >= 4:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -3)
        temp_df_TP_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm3_good = len(temp_df_TP_good_this_day)

    # Check for an accurately recorded behavior of the given type
    # on D-2. Only run this check if the current day of the simulation
    # is day 3 or later.
    if cfg.day_of_sim_iter >= 3:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -2)
        temp_df_TP_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm2_good = len(temp_df_TP_good_this_day)

    # Check for an accurately recorded behavior of the given type
    # on D-1. Only run this check if the current day of the simulation
    # is day 2 or later.
    if cfg.day_of_sim_iter >= 2:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -1)
        temp_df_TP_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_TP_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_TP_recs_Dm1_good = len(temp_df_TP_good_this_day)
        #print("Length of temp_df_TP_good for this person for Dm1: ", len(temp_df_TP_good))


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
        "Sub ID", # the column by which to filter rows
        person_u.per_id, # the value to seek in the col (i.e., the restrictor)
        )
    temp_df_FN_good = temp_df[ 
        (temp_df["Behavior Type"] == "Good") \
        & (temp_df["Record Conf Mat"] == "False Negative")
        ]

    # Check for an inaccurately recorded behavior of the given type
    # on D-3. Only run this check if the current day of the simulation
    # is day 4 or later.
    if cfg.day_of_sim_iter >= 4:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -3)
        temp_df_FN_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm3_good = len(temp_df_FN_good_this_day)

    # Check for an inaccurately recorded behavior of the given type
    # on D-2. Only run this check if the current day of the simulation
    # is day 3 or later.
    if cfg.day_of_sim_iter >= 3:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -2)
        temp_df_FN_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm2_good = len(temp_df_FN_good_this_day)

    # Check for an inaccurately recorded behavior of the given type
    # on D-1. Only run this check if the current day of the simulation
    # is day 2 or later.
    if cfg.day_of_sim_iter >= 2:
        target_datetime = cfg.current_datetime_obj + timedelta(days = -1)
        temp_df_FN_good_this_day = utils.return_df_with_rows_filtered_to_one_val_in_col(
            temp_df_FN_good, # the input DF
            "Event Datetime", # the column by which to filter rows
            target_datetime, # the value to seek in the col (i.e., the restrictor)
            )
        num_FN_recs_Dm1_good = len(temp_df_FN_good_this_day)

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
            - 3.0 * num_FN_recs_Dm1_good * cfg.strength_of_good_FN_record_impact_on_eff \
            ) \
        * cfg.strength_of_effect

    return mod_to_eff_for_previous_TP_FN_records_good


def display_simple_behavior_statistics():

    # Get the number of Good and Poor behaviors (per person per day).
    behavs_good_num = \
        cfg.behavs_act_df["Behavior Type"].value_counts()["Good"]
    behavs_poor_num = \
        cfg.behavs_act_df["Behavior Type"].value_counts()["Poor"]

    behavs_good_num_per_pers_per_day = \
        behavs_good_num / cfg.size_of_comm_initial / cfg.num_of_days_to_simulate_for_analysis
    behavs_poor_num_per_pers_per_day = \
        behavs_poor_num / cfg.size_of_comm_initial / cfg.num_of_days_to_simulate_for_analysis

    print("Number of Good behaviors: ", behavs_good_num)
    print("Good behaviors per person per day: ", behavs_good_num_per_pers_per_day)
    print("Number of Poor behaviors: ", behavs_poor_num)
    print("Poor behaviors per person per day: ", behavs_poor_num_per_pers_per_day)

    # Get the number of Resignations of various types.
    temp_df = cfg.behavs_act_df.copy()
    temp_df = temp_df[ temp_df["Behavior Comptype"] == "Resignation"]
    print( temp_df["Behavior Nature"].value_counts() )

    # Get the number of Terminations of various types (technically
    # these are records rather than behaviors).
    temp_df = cfg.behavs_act_df.copy()
    temp_df = temp_df[ temp_df["Record Comptype"] == "Termination"]
    print( temp_df["Record Nature"].value_counts() )



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