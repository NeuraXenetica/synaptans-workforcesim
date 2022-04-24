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
XLSX files or Matplotlib plots as PNG images; and the saving of complex
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
import datetime
import pickle


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

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
        os.chdir(cwd + r"/drive/MyDrive/MEG_PY_Colab_workground/workforcesim-package")

    cfg.current_working_dir = os.getcwd()

    cfg.input_files_dir = os.path.abspath(
        os.path.join(cfg.current_working_dir, 'input_files'))
    #print("cfg.input_files_dir:", cfg.input_files_dir)

    cfg.output_files_dir = os.path.abspath(
        os.path.join(cfg.current_working_dir, 'output_files'))
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
            str(cfg.num_of_days_to_simulate) + "d-" \
                + str(cfg.random_seed_A) + "r_" + datetime_str +"]_"


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
                cfg.num_of_days_to_simulate,
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
        cfg.num_of_days_to_simulate, \
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
        cfg.persons_df, \
        cfg.unique_file_prefix_code_for_simulation_run, \
        = pickle.load(file_to_read)



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