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
This module handles the reading of files from disk (e.g., XLSX files or
PNG images); the writing of files to disk (e.g., saving DataFrames as
XLSX files or Matplotlib plots as PNG images); and the saving of complex
objects as file-like objects assigned to variables in memory (e.g.,
Matplotlib plots as in-memory PNGs for display in a GUI).
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

import os
from os.path import dirname, abspath

import datetime
import pickle


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# Imports of the form "from . import X as x" have been added for use
# in the distributed package; imports of the form "import X as x" are
# retained for use when debugging the modules in VS Code.

if __name__ == "__main__":
    import config as cfg
else:
    try:
        from . import config as cfg
    except:
        import config as cfg


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

def specify_directory_structure():
    """
    Specifies the directory structure for file reading and writing.
    """

    # Check whether the module is (likely) being run in Google Colab.
    cwd = os.getcwd()
    if cwd == "/content": # True if the module is being run in Colab.
        os.chdir(cwd + r"/drive/MyDrive/PY_Colab_workground/workforcesim-package")

    cfg.current_working_dir = os.getcwd()

    # Get the path of this module, wherever it's being run from.
    cfg.input_files_dir = \
        os.path.join( dirname(os.path.abspath(__file__)), 'input_files')
    print("cfg.input_files_dir:", cfg.input_files_dir)

    cfg.output_files_dir = os.path.abspath(
        os.path.join(cfg.current_working_dir, 'output_files'))

    # This will create an output files directory in the current
    # working directory, if it doesn't already exist.
    if not os.path.exists(cfg.output_files_dir):
        os.makedirs(cfg.output_files_dir)

    print("cfg.output_files_dir: ", cfg.output_files_dir)


def generate_unique_file_prefix_code_for_simulation_run():
    """
    Generates a unique code for this run of the simulation, which can be used
    as a prefix for the files to be saved that are associated with this run.
    """

    # Get current date and time.
    datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    persons_num = ((cfg.num_of_laborers_per_team + 1) * cfg.num_of_teams_per_shift) *3 + 3 + 1

    cfg.unique_file_prefix_code_for_simulation_run = \
        "[" + str(persons_num) + "p-" + \
            str(cfg.num_of_days_to_simulate_for_analysis) + "d-" \
                + str(cfg.random_seed_A) + "r_" + datetime_str +"]_"

    # This variant can be used as a suffix instead of a prefix.
    cfg.unique_file_suffix_code_for_simulation_run = \
        "_[" + str(persons_num) + "p-" + \
            str(cfg.num_of_days_to_simulate_for_analysis) + "d-" \
                + str(cfg.random_seed_A) + "r_" + datetime_str +"]"


def save_df_to_xlsx_file(
    input_df_u, # the input DF
    filename_u, # the desired filename (without prefix code or .xlsx ending)
    ):
    """
    Saves a DataFrame to disk as an XLSX file.
    """

    full_filename = cfg.unique_file_prefix_code_for_simulation_run + filename_u + ".xlsx"
    filename_and_path = os.path.join(cfg.output_files_dir, full_filename)
    input_df_u.to_excel(filename_and_path)


def save_df_to_csv_file(
    input_df_u, # the input DF
    filename_u, # the desired filename (without prefix code or .csv ending)
    ):
    """
    Saves a DataFrame to disk as a CSV file.
    """

    full_filename = filename_u + cfg.unique_file_suffix_code_for_simulation_run + ".csv"
    filename_and_path = os.path.join(cfg.output_files_dir, full_filename)
    input_df_u.to_csv(
        filename_and_path,
        encoding="utf-8",
        index=False)


def save_key_vars_to_pickled_file():
    """
    Exports key variables to a file via pickling.
    """

    full_filename = cfg.unique_file_prefix_code_for_simulation_run + "wfs_exported_variables"
    filename_and_path = os.path.join(cfg.output_files_dir, full_filename)

    with open(filename_and_path, 'wb') as file_to_write:
        pickle.dump(
            [
                cfg.size_of_comm_initial,
                cfg.num_of_days_to_simulate_for_analysis,
                cfg.other_stats_stat_mean,
                cfg.other_stats_stat_sdev,
                cfg.random_seed_A,
                cfg.workstyle_eff_level_modifier,
                cfg.workstyle_eff_max_daily_variability,
                cfg.eff_bonus_max_from_person_age,
                cfg.eff_bonus_max_from_weekday,
                cfg.eff_bonus_max_from_teammate_sexes,
                cfg.eff_penalty_max_from_sup_age_diff,
                cfg.base_rate_attendance,
                cfg.base_rate_idea,
                cfg.base_rate_lapse,
                cfg.base_rate_feat,
                cfg.base_rate_slip,
                cfg.base_rate_teamwork,
                cfg.base_rate_disruption,
                cfg.base_rate_sacrifice,
                cfg.base_rate_sabotage,
                cfg.base_rate_efficacy,
                cfg.base_rate_false_positive,
                cfg.strength_of_effect,
                cfg.stat_to_prob_mod_conv_factor,
                cfg.base_max_efficacy_variability,
                cfg.base_rate_recording_accuracy,
                cfg.variance_to_eff_as_recorded_by_manager,
                cfg.strength_of_good_TP_record_impact_on_eff,
                cfg.strength_of_good_FN_record_impact_on_eff,
                cfg.defense_roll_max_behavior_good,
                cfg.defense_roll_max_behavior_poor,
                cfg.defense_roll_max_recording_TP,
                cfg.behavs_act_df,
                cfg.persons,
                cfg.persons_df,
                cfg.unique_file_prefix_code_for_simulation_run,
                ],
            file_to_write)


def load_key_vars_from_pickled_file(
    full_name_of_pickled_file_to_import_u, # full name of the pickled file to import
    ):
    """
    Imports key variables from a pickled file.
    """

    filename_and_path = os.path.join(cfg.output_files_dir, full_name_of_pickled_file_to_import_u)

    with open(filename_and_path, 'rb') as file_to_read:
        cfg.size_of_comm_initial, \
        cfg.num_of_days_to_simulate_for_analysis, \
        cfg.other_stats_stat_mean, \
        cfg.other_stats_stat_sdev, \
        cfg.random_seed_A, \
        cfg.workstyle_eff_level_modifier, \
        cfg.workstyle_eff_max_daily_variability, \
        cfg.eff_bonus_max_from_person_age, \
        cfg.eff_bonus_max_from_weekday, \
        cfg.eff_bonus_max_from_teammate_sexes, \
        cfg.eff_penalty_max_from_sup_age_diff, \
        cfg.base_rate_attendance, \
        cfg.base_rate_idea, \
        cfg.base_rate_lapse, \
        cfg.base_rate_feat, \
        cfg.base_rate_slip, \
        cfg.base_rate_teamwork, \
        cfg.base_rate_disruption, \
        cfg.base_rate_sacrifice, \
        cfg.base_rate_sabotage, \
        cfg.base_rate_efficacy, \
        cfg.base_rate_false_positive, \
        cfg.strength_of_effect, \
        cfg.stat_to_prob_mod_conv_factor, \
        cfg.base_max_efficacy_variability, \
        cfg.base_rate_recording_accuracy, \
        cfg.variance_to_eff_as_recorded_by_manager, \
        cfg.strength_of_good_TP_record_impact_on_eff, \
        cfg.strength_of_good_FN_record_impact_on_eff, \
        cfg.defense_roll_max_behavior_good, \
        cfg.defense_roll_max_behavior_poor, \
        cfg.defense_roll_max_recording_TP, \
        cfg.behavs_act_df, \
        cfg.persons, \
        cfg.persons_df, \
        cfg.unique_file_prefix_code_for_simulation_run, \
        = pickle.load(file_to_read)


def save_wfs_behaviors_records_df_as_csv_for_distribution():
    """
    Exports wfs_behaviors-records_df in CSV format for distribution
    within the package and/or uploading to sites (e.g., Kaggle).
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

    wfs_behaviors_records_df_for_distribution = wfs_behaviors_records_df_for_distribution[[
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

    save_df_to_csv_file(
        wfs_behaviors_records_df_for_distribution, # the input DF
        "wfs_behaviors_and_records", # the desired filename (without prefix code or .csv ending)
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