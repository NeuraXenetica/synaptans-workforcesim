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
This module handles the reading of files from disk (e.g., pickled files
or PNG images) and the writing of files to disk (e.g., saving 
DataFrames as CSV files or Matplotlib plots as PNG images).
"""

import os
import datetime
import pickle

# Import other modules from this package.
import config as cfg


def specify_directory_structure():
    """
    Specifies the directory structure for file reading and writing.
    """

    cfg.CURRENT_WORKING_DIR = os.getcwd()
    cfg.STATIC_DIR = os.path.abspath(
        os.path.join(cfg.CURRENT_WORKING_DIR, 'static'))
    cfg.PLOTS_DIR = os.path.abspath(
        os.path.join(cfg.STATIC_DIR, 'plots'))
    cfg.GRAPHICS_DIR = os.path.abspath(
        os.path.join(cfg.STATIC_DIR, 'graphics'))
    cfg.DATASETS_DIR = os.path.abspath(
        os.path.join(cfg.CURRENT_WORKING_DIR, 'datasets'))


def generate_unique_file_prefix_code_for_simulation_run():
    """
    Generates a unique code for this run of the simulation, which can 
    be used as a prefix for the files to be saved that are associated 
    with this run.
    """

    # Get current date and time.
    datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    persons_num = ((cfg.NUM_OF_LABORERS_PER_TEAM + 1) \
        * cfg.NUM_OF_TEAMS_PER_SHIFT) *3 + 3 + 1

    cfg.unique_file_prefix_code_for_simulation_run = \
        "[" + str(persons_num) + "p-" + \
            str(cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS) + "d-" \
                + str(cfg.RANDOM_SEED_A) + "r_" + datetime_str +"]_"

    # This variant can be used as a suffix instead of a prefix.
    cfg.unique_file_suffix_code_for_simulation_run = \
        "_[" + str(persons_num) + "p-" + \
            str(cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS) + "d-" \
                + str(cfg.RANDOM_SEED_A) + "r_" + datetime_str +"]"


def save_df_to_xlsx_file(input_df_u, filename_u):
    """
    Saves a DataFrame to disk as an XLSX file.

    PARAMETERS
    ----------
    input_df_u
        The DataFrame to be saved
    filename_u
        The desired filename (without prefix code or .xlsx ending)
    """

    full_filename = cfg.unique_file_prefix_code_for_simulation_run \
        + filename_u + ".xlsx"
    filename_and_path = os.path.join(
        cfg.DATASETS_DIR, "user_generated", full_filename)
    input_df_u.to_excel(filename_and_path)


def save_df_to_csv_file(input_df_u, filename_u):
    """
    Saves a DataFrame to disk as a CSV file.

    PARAMETERS
    ----------
    input_df_u
        The DataFrame to be saved
    filename_u
        The desired filename (without prefix code or .csv ending)
    """

    if cfg.visualization_data_source == "newly_generated_dataset":
        full_filename = filename_u \
            + cfg.unique_file_suffix_code_for_simulation_run + ".csv"
        filename_and_path = os.path.join(
            cfg.DATASETS_DIR, "user_generated", full_filename)
        input_df_u.to_csv(
            filename_and_path,
            encoding="utf-8-sig",
            index=False)
        cfg.dataset_csv_for_download_url = \
            "/datasets/user_generated/" + full_filename

    # This is to handle the case of a loaded (rather than 
    # just-generated) dataset; it doesn't need to be saved, because it 
    # already exists (which is how it was able to be loaded).
    elif cfg.visualization_data_source == "stored_dataset":
        full_filename = filename_u + ".csv"
        filename_and_path = os.path.join(
            cfg.DATASETS_DIR, "pregenerated", full_filename)
        cfg.dataset_csv_for_download_url = \
            "/datasets/pregenerated/wfs_behaviors_and_records_[148p-90d-99r_20230208092751].csv"


def save_df_to_pickle_file(input_df_u, filename_u):
    """
    Saves a DataFrame to disk as a pickle file.

    PARAMETERS
    ----------
    input_df_u
        The DataFrame to be saved
    filename_u
        The desired filename (without prefix code or .xlsx ending)
    """

    full_filename = filename_u \
        + cfg.unique_file_suffix_code_for_simulation_run + ".pickle"
    filename_and_path = os.path.join(
        cfg.DATASETS_DIR, "user_generated", full_filename)
    input_df_u.to_pickle(filename_and_path)


def save_key_vars_to_pickled_file():
    """
    Exports key variables to a file via pickling.
    """

    full_filename = cfg.unique_file_prefix_code_for_simulation_run \
        + "wfs_exported_variables"
    filename_and_path = os.path.join(
        cfg.DATASETS_DIR, "user_generated", full_filename)

    with open(filename_and_path, 'wb') as file_to_write:
        pickle.dump(
            [
                cfg.SIZE_OF_COMM_INITIAL,
                cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS,
                cfg.OTHER_STATS_STAT_MEAN,
                cfg.OTHER_STATS_STAT_SDEV,
                cfg.RANDOM_SEED_A,
                cfg.WORKSTYLE_EFF_LEVEL_MODIFIER,
                cfg.WORKSTYLE_EFF_MAX_DAILY_VARIABILITY,
                cfg.EFF_BONUS_MAX_FROM_PERSON_AGE,
                cfg.EFF_BONUS_MAX_FROM_WEEKDAY,
                cfg.EFF_BONUS_MAX_FROM_TEAMMATE_SEXES,
                cfg.EFF_PENALTY_MAX_FROM_SUP_AGE_DIFF,
                cfg.BASE_RATE_ATTENDANCE,
                cfg.BASE_RATE_IDEA,
                cfg.BASE_RATE_LAPSE,
                cfg.BASE_RATE_FEAT,
                cfg.BASE_RATE_SLIP,
                cfg.BASE_RATE_TEAMWORK,
                cfg.BASE_RATE_DISRUPTION,
                cfg.BASE_RATE_SACRIFICE,
                cfg.BASE_RATE_SABOTAGE,
                cfg.BASE_RATE_EFFICACY,
                cfg.BASE_RATE_FALSE_POSITIVE,
                cfg.STRENGTH_OF_EFFECT,
                cfg.STAT_TO_PROB_MOD_CONV_FACTOR,
                cfg.BASE_MAX_EFFICACY_VARIABILITY,
                cfg.BASE_RATE_RECORDING_ACCURACY,
                cfg.VARIANCE_TO_EFF_AS_RECORDED_BY_MANAGER,
                cfg.STRENGTH_OF_GOOD_TP_RECORD_IMPACT_ON_EFF,
                cfg.STRENGTH_OF_GOOD_FN_RECORD_IMPACT_ON_EFF,
                cfg.DEFENSE_ROLL_MAX_BEHAVIOR_GOOD,
                cfg.DEFENSE_ROLL_MAX_BEHAVIOR_POOR,
                cfg.DEFENSE_ROLL_MAX_RECORDING_TP,
                cfg.behavs_act_df,
                cfg.persons,
                cfg.persons_df,
                cfg.unique_file_prefix_code_for_simulation_run,
                ],
            file_to_write)


def load_key_vars_from_pickled_file(
    full_name_of_pickled_file_to_import_u):
    """
    Imports key variables from a pickled file.

    PARAMETERS
    ----------
    full_name_of_pickled_file_to_import_u
        Full name of the pickled file to import
    """

    filename_and_path = os.path.join(
        cfg.DATASETS_DIR, "pregenerated", 
        full_name_of_pickled_file_to_import_u
        )

    with open(filename_and_path, 'rb') as file_to_read:
        cfg.SIZE_OF_COMM_INITIAL, \
        cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS, \
        cfg.OTHER_STATS_STAT_MEAN, \
        cfg.OTHER_STATS_STAT_SDEV, \
        cfg.RANDOM_SEED_A, \
        cfg.WORKSTYLE_EFF_LEVEL_MODIFIER, \
        cfg.WORKSTYLE_EFF_MAX_DAILY_VARIABILITY, \
        cfg.EFF_BONUS_MAX_FROM_PERSON_AGE, \
        cfg.EFF_BONUS_MAX_FROM_WEEKDAY, \
        cfg.EFF_BONUS_MAX_FROM_TEAMMATE_SEXES, \
        cfg.EFF_PENALTY_MAX_FROM_SUP_AGE_DIFF, \
        cfg.BASE_RATE_ATTENDANCE, \
        cfg.BASE_RATE_IDEA, \
        cfg.BASE_RATE_LAPSE, \
        cfg.BASE_RATE_FEAT, \
        cfg.BASE_RATE_SLIP, \
        cfg.BASE_RATE_TEAMWORK, \
        cfg.BASE_RATE_DISRUPTION, \
        cfg.BASE_RATE_SACRIFICE, \
        cfg.BASE_RATE_SABOTAGE, \
        cfg.BASE_RATE_EFFICACY, \
        cfg.BASE_RATE_FALSE_POSITIVE, \
        cfg.STRENGTH_OF_EFFECT, \
        cfg.STAT_TO_PROB_MOD_CONV_FACTOR, \
        cfg.BASE_MAX_EFFICACY_VARIABILITY, \
        cfg.BASE_RATE_RECORDING_ACCURACY, \
        cfg.VARIANCE_TO_EFF_AS_RECORDED_BY_MANAGER, \
        cfg.STRENGTH_OF_GOOD_TP_RECORD_IMPACT_ON_EFF, \
        cfg.STRENGTH_OF_GOOD_FN_RECORD_IMPACT_ON_EFF, \
        cfg.DEFENSE_ROLL_MAX_BEHAVIOR_GOOD, \
        cfg.DEFENSE_ROLL_MAX_BEHAVIOR_POOR, \
        cfg.DEFENSE_ROLL_MAX_RECORDING_TP, \
        cfg.behavs_act_df, \
        cfg.persons, \
        cfg.persons_df, \
        cfg.unique_file_prefix_code_for_simulation_run, \
        = pickle.load(file_to_read)


def save_wfs_behaviors_records_df_as_csv_or_pickle_for_distribution(
    file_format_u
    ):
    """
    Exports wfs_behaviors-records_df in CSV or pickle format for 
    distribution within the package and/or uploading to sites (e.g., 
    Kaggle).

    PARAMETERS
    ----------
    file_format_u : str
        Is either "CSV" or "PICKLE", indicating the desired save format.
    """

    wfs_behaviors_records_df_for_distribution = cfg.behavs_act_df.rename(
        columns={
            "Sub ID": "sub_ID",
            "Sub First Name": "sub_fname",
            "Sub Last Name": "sub_lname",
            "Sub Age": "sub_age",
            "Sub Sex": "sub_sex",
            "Sub Shift": "sub_shift",
            "Sub Team": "sub_team",
            "Sub Role": "sub_role",
            "Sub Colleague IDs": "sub_coll_IDs",
            "Sub Same-Sex Colleagues Prtn": "sub_colls_same_sex_prtn",
            "Sub Health": "sub_health_h",
            "Sub Commitment": "sub_commitment_h",
            "Sub Perceptiveness": "sub_perceptiveness_h",
            "Sub Dexterity": "sub_dexterity_h",
            "Sub Sociality": "sub_sociality_h",
            "Sub Goodness": "sub_goodness_h",
            "Sub Strength": "sub_strength_h",
            "Sub Openmindedness": "sub_openmindedness_h",
            "Sub Workstyle": "sub_workstyle_h",
            "Sup ID": "sup_ID",
            "Sup First Name": "sup_fname",
            "Sup Last Name": "sup_lname",
            "Sup Age": "sup_age",
            "Sup-Sub Age Difference": "sup_sub_age_diff",
            "Sup Sex": "sup_sex",
            "Sup Role": "sup_role",
            "Sup Commitment": "sup_commitment_h",
            "Sup Perceptiveness": "sup_perceptiveness_h",
            "Sup Goodness": "sup_goodness_h",
            "Event Date": "event_date",
            "Week in Series": "event_week_in_series",
            "Day in Series (1-based)": "event_day_in_series",
            "Weekday Num": "event_weekday_num",
            "Weekday Name": "event_weekday_name",
            "Behavior Comptype": "behav_comptype_h",
            "Behavior Nature": "behav_cause_h",
            "Actual Efficacy": "actual_efficacy_h",
            "Record Comptype": "record_comptype",
            "Record Nature": "record_cause",
            "Recorded Efficacy": "recorded_efficacy",
            "Note": "recorded_note_from_sup",
            "Record Conf Mat": "record_conf_matrix_h",
        })

    wfs_behaviors_records_df_for_distribution = \
        wfs_behaviors_records_df_for_distribution[[
            "sub_ID",
            "sub_fname",
            "sub_lname",
            "sub_age",
            "sub_sex",
            "sub_shift",
            "sub_team",
            "sub_role",
            "sub_coll_IDs",
            "sub_colls_same_sex_prtn",
            "sub_health_h",
            "sub_commitment_h",
            "sub_perceptiveness_h",
            "sub_dexterity_h",
            "sub_sociality_h",
            "sub_goodness_h",
            "sub_strength_h",
            "sub_openmindedness_h",
            "sub_workstyle_h",
            "sup_ID",
            "sup_fname",
            "sup_lname",
            "sup_age",
            "sup_sub_age_diff",
            "sup_sex",
            "sup_role",
            "sup_commitment_h",
            "sup_perceptiveness_h",
            "sup_goodness_h",
            "event_date",
            "event_week_in_series",
            "event_day_in_series",
            "event_weekday_num",
            "event_weekday_name",
            "behav_comptype_h",
            "behav_cause_h",
            "actual_efficacy_h",
            "record_comptype",
            "record_cause",
            "recorded_efficacy",
            "recorded_note_from_sup",
            "record_conf_matrix_h",
            ]]

    if file_format_u == "CSV":
        save_df_to_csv_file(
            wfs_behaviors_records_df_for_distribution,
            "wfs_behaviors_and_records"
            )

    elif file_format_u == "PICKLE":
        save_df_to_pickle_file(
            wfs_behaviors_records_df_for_distribution,
            "wfs_behaviors_and_records"
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