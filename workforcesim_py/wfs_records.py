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
This module handles the simulation’s “Level 2” logic, which simulates
frontline managers’ personal *observations* of workers’ daily behaviors
and the *records* of such behaviors that they enter into their factory’s
(simulated) HRM/ERP system. Of critical importance is the fact that
those records *may* or *may not* accurately reflect workers’ actual
behaviors: a manager who is overworked, inattentive, dishonest, or
unskilled in use of the HRM/ERP system may fail to record some worker
behaviors, may record behaviors that didn’t actually occur, or may
record behaviors in a distorted manner.
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
from datetime import timedelta


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

#from pip._internal import main as pip
#pip(['install', '--user', 'scikit-learn'])
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import config as cfg
import wfs_personnel as pers
import wfs_utilities as utils


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

def simulate_one_day_of_records():
    """
    Simulates one day's worth of managers' recordings, which (depending
    on various personal and environmental factors) may or may
    not accurately reflect workers' actual underlying behaviors.
    """

    # First determine how a manager records all of those *actual behaviors*
    # that a worker performed and which thus already have entry rows
    # in cfg.behavs_act_df.
    #
    # In other words, determine whether those actual behaviors should be
    # recorded accurately (a "True Positive") or not noticed and recorded
    # (a "False Negative") by a manager.

    current_date = cfg.current_datetime_obj.date()

    for i in range(len(cfg.behavs_act_df)):

        # Only run the steps farther below if the given row is for the *current
        # day* (i.e., hasn't already been dealt with in a previous day).
        if cfg.behavs_act_df["Behavior Date"].values[i] == current_date:

            # Get the identity of the manager (if any) for the person
            # who had the actual behavior.
            recording_sup = pers.person_object_with_given_sub_ID(
                cfg.behavs_act_df["Supervisor ID"].values[i], # the subject ID for the person object being sought
                )
            #print("recording_sup: ", recording_sup)

            # If the person who performed the actual behavior had no 
            # supervisor (i.e., is the Production Director),
            # then no record will be made. Only proceed if the person who
            # performed the actual behavior had a manager.
            if recording_sup:

                # ---------------------------------------------------------------------
                # Record workers' Attendance (i.e., Presence or Absence).
                # A worker's Attendance behavior is always recorded by managers
                # with 100% accuracy.
                # ---------------------------------------------------------------------
                if cfg.behavs_act_df["Behavior Type"].values[i] == "Attendance":

                    # Copy the main Behavior Type and Comptype fields.
                    cfg.behavs_act_df["Record Type"].values[i] = \
                        cfg.behavs_act_df["Behavior Type"].values[i]
                    cfg.behavs_act_df["Record Comptype"].values[i] = \
                        cfg.behavs_act_df["Behavior Comptype"].values[i]


                # ---------------------------------------------------------------------
                # Record workers' Efficacy.
                # If an OEE system is in use, recording of Efficacy by managers will be
                # 100% accurate. If no OEE system is in use, managers will make
                # subjective (and potentially inaccurate) estimates of workers'
                # Efficacy.
                # ---------------------------------------------------------------------

                elif cfg.behavs_act_df["Behavior Type"].values[i] == "Efficacy":

                    # Copy the main Behavior Type and Comptype fields.
                    cfg.behavs_act_df["Record Type"].values[i] = \
                        cfg.behavs_act_df["Behavior Type"].values[i]
                    cfg.behavs_act_df["Record Comptype"].values[i] = \
                        cfg.behavs_act_df["Behavior Comptype"].values[i]

                    # Copy the OHE of the Behavior Type and Comptype.
                    cfg.behavs_act_df["Efficacy (Record Type)"].values[i] = \
                        cfg.behavs_act_df["Efficacy (Behavior Type)"].values[i]

                    cfg.behavs_act_df["Efficacy (Record Comptype)"].values[i] = \
                        cfg.behavs_act_df["Efficacy (Behavior Comptype)"].values[i]

                    # If an OEE system is in use (record Eff with full accuracy)...
                    if cfg.oee_system_in_use == True:

                        # Copy the exact numerical Efficacy value from
                        # the worker's actual Efficacy behavior.
                        cfg.behavs_act_df["Recorded Efficacy"].values[i] = \
                            cfg.behavs_act_df["Actual Efficacy"].values[i]

                    # If no OEE system is in use (record a rounded Eff estimate)...
                    else: 

                        # Start with the worker's actual Efficacy level.
                        eff_estimated = cfg.behavs_act_df["Actual Efficacy"].values[i]

                        # Adjust the actual Efficacy by a ± random amount.
                        # NOTE! This is currently a plain random number; changing it to
                        # a randomized number using a mean and SD would be more realistic. 
                        eff_estimated = eff_estimated * (
                            1 + (random.uniform(-cfg.variance_to_eff_as_recorded_by_manager, cfg.variance_to_eff_as_recorded_by_manager))
                            )

                        # Round the estimated Efficacy to the nearest 10%.
                        # Note! Does this only round up, or is it capable of rounding
                        # down, as well -- as is desired?
                        eff_estimated = round( eff_estimated*10.0, 0) / 10.0

                        cfg.behavs_act_df["Recorded Efficacy"].values[i] = eff_estimated


                # ---------------------------------------------------------------------
                # Record or ignore workers' Good and Poor behaviors (i.e., Ideas,
                # Lapses, Feats, Slips, Teamworks, Disruptions, Sacrifices, and
                # Sabotages).
                # ---------------------------------------------------------------------
                elif (cfg.behavs_act_df["Behavior Type"].values[i] == "Good") \
                        | (cfg.behavs_act_df["Behavior Type"].values[i] == "Poor"):

                    # If the manager meets the threshold to generate a True Positive record...
                    if recording_sup.prob_modified_recording_accurately >= (random.uniform(0.0, cfg.defense_roll_max_recording_TP)):

                        # Accurately copy the main Behavior Type and Comptype fields.
                        cfg.behavs_act_df["Record Type"].values[i] = \
                            cfg.behavs_act_df["Behavior Type"].values[i]
                        cfg.behavs_act_df["Record Comptype"].values[i] = \
                            cfg.behavs_act_df["Behavior Comptype"].values[i]

                        # Mark the record as a True Positive.
                        cfg.behavs_act_df["Record Conf Mat"].values[i] = "True Positive"

                        # Add to the record a note written by the manager
                        # who's making the entry.

                        note_text = return_note_to_be_added_to_entry(
                            cfg.behavs_act_df["Record Comptype"].values[i], # the Record Comptype for the given entry (e.g., "Lapse")
                            cfg.behavs_act_df["First Name"].values[i], # First name of the person who performed the behavior
                            )
                        cfg.behavs_act_df["Note"].values[i] = note_text

                    # Otherwise, the manager falls short of the threshold to generate a True Positive record...
                    else:

                        # Inaccurately mark None as the main Behavior Type and Comptype fields.
                        cfg.behavs_act_df["Record Type"].values[i] = None
                        cfg.behavs_act_df["Record Comptype"].values[i] = None

                        # Mark the record as a False Negative.
                        cfg.behavs_act_df["Record Conf Mat"].values[i] = "False Negative"


def display_simple_record_accuracy_statistics():
    """
    Calculates and displays some simple statistics regarding
    the accuracy of managers' recording of workers' behaviors.
    """

    # Get the number of particular events by Comptype.
    print("*****")
    print("Number of Presences: ", cfg.behavs_act_df["Presence (Behavior Comptype)"].sum())
    print("Number of Absences: ", cfg.behavs_act_df["Absence (Behavior Comptype)"].sum())
    print("Number of Ideas: ", cfg.behavs_act_df["Idea (Behavior Comptype)"].sum())
    print("Number of Lapses: ", cfg.behavs_act_df["Lapse (Behavior Comptype)"].sum())
    print("Number of Feats: ", cfg.behavs_act_df["Feat (Behavior Comptype)"].sum())
    print("Number of Slips: ", cfg.behavs_act_df["Slip (Behavior Comptype)"].sum())
    print("Number of Teamworks: ", cfg.behavs_act_df["Teamwork (Behavior Comptype)"].sum())
    print("Number of Disruptions: ", cfg.behavs_act_df["Disruption (Behavior Comptype)"].sum())
    print("Number of Sacrifices: ", cfg.behavs_act_df["Sacrifice (Behavior Comptype)"].sum())
    print("Number of Sabotages: ", cfg.behavs_act_df["Sabotage (Behavior Comptype)"].sum())
    print("*****")

    # Get the number of True Positives and False Negatives.
    true_positives_num = \
        cfg.behavs_act_df["Record Conf Mat"].value_counts()["True Positive"]
    false_negatives_num = \
        cfg.behavs_act_df["Record Conf Mat"].value_counts()["False Negative"]

    # Get the number of Good TPs and Good FNs.
    temp_df = cfg.behavs_act_df.copy()
    temp_df[temp_df["Behavior Type"] == "Good"]
    true_positives_good_num = \
        temp_df["Record Conf Mat"].value_counts()["True Positive"]
    temp_df = cfg.behavs_act_df.copy()
    temp_df[temp_df["Behavior Type"] == "Poor"]
    false_negatives_good_num = \
        temp_df["Record Conf Mat"].value_counts()["False Negative"]


    # Calculate the MSE for managers' Efficacy records.
    # First, delete rows that have an NaN for Actual
    # or Recorded Efficacy.
    temp_df = cfg.behavs_act_df.copy()

    #Delete rows containing an NA value for certain fields.
    temp_df = utils.return_df_with_rows_deleted_that_containing_na_in_col(
        temp_df, # the input DF whose rows should be deleted
        "Actual Efficacy", # the column in which an Na value will cause row deletion
        )
    temp_df = utils.return_df_with_rows_deleted_that_containing_na_in_col(
        temp_df, # the input DF whose rows should be deleted
        "Recorded Efficacy", # the column in which an Na value will cause row deletion
        )

    actual_eff = temp_df["Actual Efficacy"]
    recorded_eff = temp_df["Recorded Efficacy"]
    recorded_eff_mse = mean_squared_error(actual_eff, recorded_eff)
    recorded_eff_mae = mean_absolute_error(actual_eff, recorded_eff)

    # Display the results.
    print("Number of Good True Positives: ", true_positives_good_num)
    print("Number of Good False Negatives: ", false_negatives_good_num)
    print("Number of True Positive Good/Poor records:", true_positives_num)
    print("Number of False Negative Good/Poor records:", false_negatives_num)
    print("MSE for Efficacy records:", recorded_eff_mse)
    print("MAE for Efficacy records:", recorded_eff_mae)


def add_eff_mday_series_to_behavs_act_df():
    """
    Adds to cfg.behavs_act_df a new set of 'mday series' columns that
    reflect the given subject's Efficacy on the days before or after
    the day that is the focus of row (i.e., D0, the day on which the
    row's main entry was recorded).
    """

    # Create the new columns whose values will be populated.
    cfg.behavs_act_df["D-4 Eff"] = None
    cfg.behavs_act_df["D-3 Eff"] = None
    cfg.behavs_act_df["D-2 Eff"] = None
    cfg.behavs_act_df["D-1 Eff"] = None
    cfg.behavs_act_df["D0 Eff"] = None
    cfg.behavs_act_df["D+1 Eff"] = None
    cfg.behavs_act_df["D+2 Eff"] = None
    cfg.behavs_act_df["D+3 Eff"] = None
    cfg.behavs_act_df["D+4 Eff"] = None

    # Create a dictionary that contains a key for each person's ID,
    # and each of their values is a dictionary with a separate
    # key for each week in the dataset. Each of those values is a DF
    # with the entries for just that person in just that week.
    dict_of_behavs_act_Eff_dfs_by_person_ID_and_week = {}

    print("length of dict_of_behavs_act_Eff_dfs_by_person_ID_and_week: ", len(dict_of_behavs_act_Eff_dfs_by_person_ID_and_week))

    # Calculate how many weeks are in the series comprising
    # the dataset. That can be done by taking the 
    final_week_in_series_num = utils.return_week_in_series_for_given_date(
        utils.return_date_of_final_day_to_simulate(), # the date whose week should be returned
        )
    #print("final_week_in_series_num: ", final_week_in_series_num)

    # For each person in the organization...
    for p in cfg.persons:

        dict_of_behavs_act_Eff_dfs_by_person_ID_and_week[cfg.persons[p].per_id] = {}

        for w in range(0, final_week_in_series_num + 1):

            # Create a temp DF with only that person's Eff behaviors
            # (and the records made of them for the person
            # by supervisors) for the given week.
            behavs_act_df_this_pers = utils.return_df_with_rows_filtered_to_one_val_in_col(
                cfg.behavs_act_df, # the input DF
                "Person ID", # the column by which to filter rows
                cfg.persons[p].per_id, # the value to seek in the col (i.e., the restrictor)
                )

            behavs_act_df_this_pers = behavs_act_df_this_pers[behavs_act_df_this_pers["Behavior Type"] == "Efficacy"]

            behavs_act_df_this_pers = utils.return_df_with_rows_filtered_to_one_val_in_col(
                behavs_act_df_this_pers, # the input DF
                "Week in Series", # the column by which to filter rows
                w, # the value to seek in the col (i.e., the restrictor)
                )

            # Add this person's Eff DF to the dictionary for all persons.
            dict_of_behavs_act_Eff_dfs_by_person_ID_and_week[cfg.persons[p].per_id][w] = behavs_act_df_this_pers

    # For each row in the main cfg.behavs_act_df...
    for i in range(len(cfg.behavs_act_df)):

        date_of_row_to_populate = cfg.behavs_act_df["Behavior Date"].values[i]
        subject_ID_in_row_to_populate = cfg.behavs_act_df["Person ID"].values[i]

        #print("date_of_sought_mday: ", date_of_sought_mday)

        # First, search in the week during which D0 falls. Then check in
        # the previous week (if it exists) and the following week (if it exists).
        focal_week = utils.return_week_in_series_for_given_date(date_of_row_to_populate)
        #print("focal_week: ", focal_week)

        weeks_to_search = [focal_week]
        if focal_week > 0:
            weeks_to_search.append(focal_week - 1)
        if focal_week < final_week_in_series_num:
            weeks_to_search.append(focal_week + 1)

        for week in weeks_to_search:
            behavs_act_Eff_df_this_sub = dict_of_behavs_act_Eff_dfs_by_person_ID_and_week[subject_ID_in_row_to_populate][week]

            # Search the correct person's DF for an Eff behavior recorded on 
            # particular mdays defined relative to that row's entry date.

            for j in range(len(behavs_act_Eff_df_this_sub)):

                # Check each desired mday, as defined relative to D0.
                for delta_days, mday_label in [
                    (-4, "D-4 Eff"),
                    (-3, "D-3 Eff"),
                    (-2, "D-2 Eff"),
                    (-1, "D-1 Eff"),
                    (0, "D0 Eff"),
                    (1, "D+1 Eff"),
                    (2, "D+2 Eff"),
                    (3, "D+3 Eff"),
                    (4, "D+4 Eff"),
                    ]:

                    # Find and note any Eff behavior from the given mday.
                    date_of_sought_mday = date_of_row_to_populate + timedelta(days = delta_days)
                    if (behavs_act_Eff_df_this_sub["Behavior Type"].values[j] == "Efficacy") \
                            & (behavs_act_Eff_df_this_sub["Behavior Date"].values[j] == date_of_sought_mday):
                        mday_eff_act = behavs_act_Eff_df_this_sub["Actual Efficacy"].values[j]
                        cfg.behavs_act_df[mday_label].values[i] = mday_eff_act


def return_note_to_be_added_to_entry(
    entry_comptype_u, # the Record Comptype for the given entry (e.g., "Lapse")
    person_first_name_u, # First name of the person who performed the behavior
    ):
    """
    Returns a note from the recording manager to be added to a record
    when it's entered in the system. Not all Record Comptypes have 
    notes; None will be returned if no note is generated.
    """

    # A note is created by concatenating four text elements:
    # 
    # - An explanation of how the manager gained the info about the
    #   purported behavior (e.g., "I noticed that ", "I suspect that ",
    #   "I was told by a worker that ", etc.). Note that this element 
    #   can be "", in which case the note starts with the second element.
    #
    # - The first name of the worker who is the subject of the entry.
    #
    # - The verbal phrase explaining what it is that the subject did
    #   (e.g., "had a great new idea ", "slipped and spilled the 
    #   contents of a container")
    #
    # - A modifying phrase that qualifies the verbal phrase to add
    #   variety (e.g., "while working in Warehouse 2.", "right after
    #   finishing a break", "after failing to notice that the door was 
    #   locked", etc.).
    #
    # Elements 1 and 2 are determined in an identical fashion for all
    # Record Comptypes; the possible contents of elements 3 and 4 are
    # specific to particular Comptypes.


    # ---------------------------------------------------------------------
    # Calculate element 3.
    # It is calculated first, because if it returns None, the function ends
    # and there's no need to calculate the other three elements' values.
    # ---------------------------------------------------------------------

    if entry_comptype_u == "Idea":
        note_element_3_option_contents = [
            "had a great idea ",
            "came up with a brilliant solution to a recurring glitch ",
            "developed an ingenious new approach to solving a longstanding problem ",
            "devised a clever way of improving the quality of our operations ",
            "identified some hidden inefficiencies in our current process ",
            "had a good suggestion for how to change the order of steps ",
            "started teaching other personnel a better way of carrying out the work ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Lapse":
        note_element_3_option_contents = [
            "neglected to turn on ",
            "forgot to turn off ",
            "overloaded ",
            "used the wrong settings for ",
            "forgot the passcode needed for ",
            "chose the wrong diagnostic mode for ",
            "failed to notice the warning indicator on ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Feat":
        note_element_3_option_contents = [
            "managed to complete twice (!) the nominal maximum number of jobs on ",
            "manually (without any tools!) reconfigured ",
            "leapt out of nowhere to catch a neural filament tube that had fallen off of ",
            "jumped onto an out-of-control automated transport container and stopped it just before it smashed into ",
            "successfully attached all of the first-cycle manipulator arms before the Pinnacle Server had even managed to awaken ",
            "set a new organizational record for the number of consecutive flips without an error on ",
            "was able to simultaneously juggle (and resolve!) twelve open orders on ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Slip":
        note_element_3_option_contents = [
            "tripped and – while falling – ripped one of the articulators off of ",
            "knocked over a full tank of the genobaric fluid needed to operate ",
            "somehow forgot the control arrangement on the Heavy Material Transporter and drove it right into ",
            "grabbed the wrong release handle (twice in one shift) when trying to operate ",
            "moved too slowly hitting the startup cycle button and got trapped inside ",
            "stumbled and spilled a whole box of quantum fuses down the drains next to ",
            "pushed too hard and broke the recapitulator mechanism on ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Teamwork":
        note_element_3_option_contents = [
            "filled in for a teammate who didn’t yet feel comfortable climbing into ",
            "helped a colleague who was struggling to unpackage ",
            "taught several coworkers a better way of cooling down ",
            "took my place at the Ingraham Array when I needed to go troubleshoot an urgent problem with ",
            "took the lead in organizing a peer training session regarding proper insulation of ",
            "offered to serve as a mentor to colleagues who aren’t yet certified on ",
            "encouraged (and cleaned up after) a teammate who’d become discouraged after breaking ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Disruption":
        note_element_3_option_contents = [
            "forced R&D personnel to wait half an hour to use ",
            "angrily refused my request to show the new hire how to unclog ",
            "started a completely unnecessary argument with teammates over ",
            "continued to spread completely baseless rumors about the supposed “biomagnetic dangers” associated with working on ",
            "refused to use the new procedure for activating ",
            "kept running the Sonomattica-7 at full power while others were trying to hold a meeting to discuss changes to ",
            "refused (once again) to let anyone else work on ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Sacrifice":
        note_element_3_option_contents = [
            "volunteered to work late today, because ",
            "agreed to come in early, because ",
            "offered to take a later vacation this year, because ",
            "once again (for at least the second time in the last week) volunteered to manually reprogram the Sonomattica-7, because ",
            "skipped two breaks today, in an attempt to make up the backlog created by the fact that ",
            "suggested switching to the Electrum-9 machine (even though it’s less pleasant to use), because ",
            "didn’t complain when I suggested crawling inside the Photon-5 to clean it out again, because ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Sabotage":
        note_element_3_option_contents = [
            "loosened a bolt on ",
            "deactivated the security lock on ",
            "changed the passcode to prevent anyone else from opening ",
            "removed some of the extra fuses that are supposed to be stored inside ",
            "“borrowed” the emergency ionic stimulator from ",
            "secretly disassembled ",
            "purposefully erased all the preconfigured models from ",
            ]
        note_element_3_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_3 = random.choices(
            note_element_3_option_contents,
            weights=note_element_3_option_weights,
            k=1,
            )[0]

    else:
        return None


    # ---------------------------------------------------------------------
    # Calculate element 4.
    # ---------------------------------------------------------------------

    if entry_comptype_u == "Idea":
        note_element_4_option_contents = [
            "regarding maintenance of the Photon-3 machine.",
            "connected with the regular cleaning of the Electrum-8 system.",
            "regarding upgrades to the Photon-5 machine’s manipulator assembly.",
            "related to the Sonomattica-7 system’s daily reset cycle.",
            "regarding placement of the main RF scanner on the operations floor.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Lapse":
        note_element_4_option_contents = [
            "the Sonomattica-7 analyzer at the end of the shift.",
            "the Platinum-383 supercondensor during its cooldown cycle.",
            "the RF scanner when moving it into its recharging position.",
            "the new Electrum-43 device, mistakenly thinking that it was one of the old Electrum-41 models, instead.",
            "the quantum isolator unit.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Feat":
        note_element_4_option_contents = [
            "the RF scanner.",
            "the new Electrum-43.",
            "the old Electrum-41.",
            "the Sonomattica-7.",
            "the Photon-3.",
            "the Data Section’s aggregator array.",
            "the Engineering Section’s ZX-4721.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Slip":
        note_element_4_option_contents = [
            "the hydraulic loading ramp.",
            "the lower door to Secure Warehouse B.",
            "the retractable lighting array.",
            "one of the particulate analyzer vats.",
            "one of the sub-ionic sterilizers.",
            "the R&D Section’s main data transducer.",
            "the neuro-aquatic simulator.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Teamwork":
        note_element_4_option_contents = [
            "a quantum fuse compiler.",
            "a Sirtizant-B torogenic recycler.",
            "the control passage suspended above the particulate analyzer vats.",
            "the neuro-aquatic simulator.",
            "a Photon-5.",
            "the RF scanner’s spectral differentiator.",
            "a virtual hibernation pod.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Disruption":
        note_element_4_option_contents = [
            "the Platinum-383 supercondensor.",
            "the RF scanner.",
            "the sub-ionic sterilizers.",
            "the neuro-aquatic simulator.",
            "the old Electrum-41.",
            "the Sonomattica-7.",
            "the Photon-3.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Sacrifice":
        note_element_4_option_contents = [
            "the others still don’t know how to use the resonation decoder yet.",
            "there hasn’t been enough time to set up and test the new Genomentor.",
            "the other teams have already broken three conducer arrays, and the next shipment won’t arrive for a month.",
            "most of the others had to attend a special safety training session today.",
            "no one else is qualified to perform the E-Type reconfiguration process.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]

    elif entry_comptype_u == "Sabotage":
        note_element_4_option_contents = [
            "the quantum isolator unit’s lateral manifold assembly.",
            "the RF scanner’s spectral differentiator.",
            "the Photon-5 without permission.",
            "the R&D Section’s Platinum-383 supercondensor.",
            "my production-line workstation.",
            ]
        note_element_4_option_weights = [
            1,
            1,
            1,
            1,
            1,
            ]
        note_element_4 = random.choices(
            note_element_4_option_contents,
            weights=note_element_4_option_weights,
            k=1,
            )[0]


    # ---------------------------------------------------------------------
    # Calculate element 1.
    # ---------------------------------------------------------------------

    note_element_1_option_contents = [
        "",
        "I discovered that ",
        "I noticed that ",
        "I saw that ",
        "I was informed that ",
        "A worker told me that ",
        "I overheard two workers discussing the fact that ",
        "I believe that ",
        ]
    note_element_1_option_weights = [
        100,
        8,
        7,
        5,
        3,
        3,
        1,
        1,
        ]
    note_element_1 = random.choices(
        note_element_1_option_contents,
        weights=note_element_1_option_weights,
        k=1,
        )[0]


    # ---------------------------------------------------------------------
    # Calculate element 2.
    # ---------------------------------------------------------------------
    note_element_2 = person_first_name_u + " "


    # ---------------------------------------------------------------------
    # Return the concatenated note text.
    # ---------------------------------------------------------------------
    note_to_return = note_element_1 + note_element_2 \
        + note_element_3 + note_element_4
    return note_to_return



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