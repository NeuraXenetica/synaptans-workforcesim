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
This simple module runs the simulation, accepting the arguments provided
by a user to (1) create a simulated workforce; (2) simulate workers’
daily activity for a specified number of days and quantity of workers;
(3) generate the (potentially inaccurate) records of such workplace
behaviors made by workers’ frontline managers; (4) employ AI in an
attempt to discover trends and correlations in the records’ data and
generate predictions; and then (5) assess the accuracy of those analyses
and predictions by comparing them with what we know to be the case
regarding workers’ actual past and expected future behaviors.
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

#from datetime import datetime
import datetime
from datetime import timedelta
import random


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import config as cfg
import io_file_manager as iofm # The IO file manager
import wfs_behaviors as bhv # WorkforceSim logic, level 01 (workers' actual behaviors)
import wfs_utilities as utils
import wfs_visualizer as vis
import wfs_personnel as pers
import wfs_records as rec


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for running the simulation
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def advance_date_by_one_day():
    """
    Increment the number of days simulated by 1. Advance the value of 
    the current datetime object by one day (as long as the current
    weekday isn't Friday) or three days (if the current weekday
    is Friday).
    """

    cfg.day_of_sim_iter += 1

    # If the current weekday is Friday, skip over the weekend to Monday.
    if cfg.current_datetime_obj.weekday() == 4:
        cfg.current_datetime_obj += timedelta(days = 3)
    else:
        cfg.current_datetime_obj += timedelta(days = 1)

    # print(cfg.current_datetime_obj.date() )


def run_one_time_simulation_setup_steps():
    """
    Runs a number of one-time setup steps that must be
    run once when initializing the simulation.
    """

    iofm.generate_unique_file_prefix_code_for_simulation_run()

    iofm.specify_directory_structure()

    cfg.current_datetime_obj = datetime.datetime.strptime(cfg.sim_starting_date, '%Y-%m-%d')
    cfg.day_of_sim_iter = 0

    print("current date: ", cfg.current_datetime_obj)
    print("final date to simulate: ", utils.return_date_of_final_day_to_simulate())


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # RUN FUNCTIONS TO SET UP WORKFORCE BASED ON INPUTTED VARIABLES
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    random.seed(cfg.random_seed_A)
    np.random.seed(cfg.random_seed_A)

    pers.calculate_id_starting_value()

    pers.create_all_possible_roles()
    #print("len(cfg.roles): ", len(cfg.roles))

    pers.create_shift_objects()
    #print("len(cfg.shifts): ", len(cfg.shifts))

    pers.create_team_objects()
    #print("len(cfg.teams): ", len(cfg.teams))

    pers.create_all_possible_spheres()
    #print("len(cfg.spheres): ", len(cfg.spheres))

    # create_initial_set_of_tasks()
    # create_initial_set_of_activities()

    pers.create_initial_population_of_persons()
    print("len(cfg.persons): ", len(cfg.persons))

    pers.assign_initial_role_to_each_person()
    pers.assign_initial_shift_to_each_person()
    pers.assign_initial_team_to_each_person()
    pers.assign_initial_sphere_to_each_person()
    pers.assign_initial_supervisor_to_each_person()
    pers.assign_initial_colleagues_to_all_persons()
    pers.update_persons_colleagues_of_same_sex_prtn()
    pers.assign_initial_subordinates_to_all_supervisors()

    bhv.configure_behavs_act_df()

    # update_current_tasks()

    pd.set_option('display.max_rows', 100)
    # pd.set_option('display.max_colwidth', 0)
    # pd.set_option('display.min_rows', 100)

    cfg.persons_df = pers.create_df_with_selected_attributes_of_all_persons()
    #print("cfg.persons_df just created:", cfg.persons_df)


def run_one_time_simulation_finalization_steps():
    """
    Runs a number of one-time setup steps that must be
    run once when concluding the simulation, after the
    core work of simulating the days' behaviors is done.
    """

    bhv.calculate_metrics_for_persons_in_simulated_period()

    cfg.persons_df = pers.create_df_with_selected_attributes_of_all_persons()

    # Before creating any new plots, it's necessary to manually delete
    # any existing matplotlib plots from memory -- otherwise, warning
    # messages will be generated after there are 20 plots in memory.
    plt.close("all")
    #
    # Here we generate the *full spectrum* of results graphics that
    # the simulator is capable of generating, regardless of whether
    # they will all be displayed for the user in a particular GUI.

    # Generate and display some simple statistics.
    #pers.display_simple_personnel_statistics()
    rec.display_simple_record_accuracy_statistics()
    bhv.display_simple_behavior_statistics()

    # One-hot encode the "True Positive", "False Negative",
    # etc., columns.
    cfg.behavs_act_df = utils.return_df_with_col_one_hot_encoded(
        cfg.behavs_act_df, # the input DF
        "Record Conf Mat", # the column to one-hot encode
        )

    print("Beginning addition of mday series.")
    rec.add_eff_mday_series_to_behavs_act_df()

    print("Simulation results have been calculated. Ready to prepare visualizations.")

    # Export key variables to file via pickling.
    iofm.save_key_vars_to_pickled_file()


def generate_visualizations():
    """
    Creates a number of visualizations. Can only be run after
    behaviors and records have been simulated (or imported).
    """

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Generate (selected) visualizations.
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #"""
    png_plt_disruptions_mean_by_workstyle_group_bar = vis.plot_disruptions_mean_by_workstyle_group_bar()
    png_plt_ideas_mean_by_workstyle_group_bar = vis.plot_ideas_mean_by_workstyle_group_bar()
    png_plt_Eff_mean_vs_Eff_sd_with_workstyle_group_bar = vis.plot_Eff_mean_vs_Eff_sd_with_workstyles_scatter()
    png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter = vis.MNGR_CAP_vs_WRKR_CAP_scores_scatter()
    png_plt_MNGR_CAP_by_age_scatter = vis.plot_MNGR_CAP_by_age_scatter()
    png_plt_WRKR_CAP_vs_mean_Eff_scatter = vis.plot_WRKR_CAP_vs_mean_Eff_scatter()
    png_plt_distribution_of_WRKR_CAP_scores_hist = vis.plot_distribution_of_WRKR_CAP_scores_hist()
    png_plt_distribution_of_MNGR_CAP_scores_hist = vis.plot_distribution_of_MNGR_CAP_scores_hist()
    png_plt_WRKR_CAP_by_shift_bar = vis.plot_WRKR_CAP_by_shift_bar()
    png_plt_MNGR_CAP_by_role_bar = vis.plot_MNGR_CAP_by_role_bar()
    png_plt_WRKR_CAP_by_team_bar = vis.plot_WRKR_CAP_by_team_bar()
    png_plt_num_Good_vs_Poor_actions_by_person_hist2d = vis.plot_num_Good_vs_Poor_actions_by_person_hist2d()
    png_plt_Eff_by_weekday_bar = vis.plot_Eff_by_weekday_bar()
    png_plt_Eff_by_age_bar = vis.plot_Eff_by_age_bar()
    png_plt_Eff_by_same_sex_colleagues_prtn_line = vis.plot_Eff_by_colleagues_of_same_sex_line()
    png_plt_sub_sup_age_diff_vs_eff_line = vis.plot_Eff_by_sub_sup_age_difference_line()
    png_plt_sub_sup_age_diff_vs_recorded_eff_line = vis.plot_recorded_Eff_by_sub_sup_age_difference_line()
    png_plt_Eff_mean_by_workstyle_group_bar= vis.plot_Eff_mean_by_workstyle_group_bar()
    png_plt_Eff_sd_by_workstyle_group_bar= vis.plot_Eff_sd_by_workstyle_group_bar()
    behavior_row_internal_correlations_heatmap = vis.generate_behavior_row_internal_correlations_heatmap()
    between_behaviors_correlations_heatmap = vis.generate_between_behaviors_correlations_heatmap()
    #"""

    # Some visualizations can only be prepared after mday series
    # are added to cfg.behavs_act_df.
    #"""
    png_plt_mday_series_Eff_for_behav_type_good_bar = \
        vis.plot_mday_series_Eff_for_behav_comptype_bar(
            "Behavior Type", # name of col (e.g., "Behavior Type", "Record Conf Mat") in which D0 event is noted
            "Good", # name of the D0 event type (e.g., "Good", "False Negative")
            )
    png_plt_mday_series_Eff_for_rec_conf_mat_TP_bar = \
        vis.plot_mday_series_Eff_for_behav_comptype_bar(
            "Record Conf Mat", # name of col (e.g., "Behavior Type", "Record Conf Mat") in which D0 event is noted
            "True Positive", # name of the D0 event type (e.g., "Good", "False Negative")
            )
    png_plt_mday_series_Eff_for_rec_conf_mat_FN_bar = \
        vis.plot_mday_series_Eff_for_behav_comptype_bar(
            "Record Conf Mat", # name of col (e.g., "Behavior Type", "Record Conf Mat") in which D0 event is noted
            "False Negative", # name of the D0 event type (e.g., "Good", "False Negative")
            )
    #"""


def run_simulation_of_personnel_behaviors_records():
    """
    Runs the core simulation.
    """

    run_one_time_simulation_setup_steps()

    # Simulate the desired number of days of activities.
    for d in range(cfg.num_of_days_to_simulate):

        pers.calculate_person_modifiers_to_implement_dependencies_and_covariance()

        # Run one day of workers' behaviors.
        bhv.simulate_one_day_of_behaviors()

        # Run one day of managers' recordings.
        rec.simulate_one_day_of_records()

        # Advance the simulation by one day.
        advance_date_by_one_day()

    run_one_time_simulation_finalization_steps()


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for cleanup and debugging of the simulation
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def copy_selected_vars_to_globals():
    """
    Copies selected variables to global variables in config.py, so that
    they (e.g.) will be visible in Spyder's "Variable Explorer" window,
    to aid with debugging.
    """

    global persons_df_global
    persons_df_global = cfg.persons_df
    #print("cfg.persons_df: ", cfg.persons_df)


    persons_df_names_only = utils.return_df_with_selected_cols_from_df(
        cfg.persons_df, # the input DF
        [
            "First Name",
            "Last Name",
        ], # a list of columns to keep in the new DF
        )
    global persons_df_names_only_global
    persons_df_names_only_global = persons_df_names_only


    persons_df_trimmed_wo_object_cols = utils.return_df_with_selected_cols_deleted(
        cfg.persons_df, # the input DF
        [
            "Supervisor",
            "Colleagues",
            "Subordinates",
        ], # a list of columns to delete from the DF
        )
    global persons_df_trimmed_wo_object_cols_global
    persons_df_trimmed_wo_object_cols_global = persons_df_trimmed_wo_object_cols


    global behavs_act_df_global
    behavs_act_df_global = cfg.behavs_act_df


    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
    # ● Export selected DataFrames to file.
    # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

    iofm.save_df_to_xlsx_file(
        cfg.persons_df, # the input DF
        "wfs_persons_df", # the desired filename (without prefix code or .xlsx ending)
        )

    iofm.save_df_to_xlsx_file(
        cfg.behavs_act_df, # the input DF
        "wfs_behaviors-records_df", # the desired filename (without prefix code or .xlsx ending)
        )



# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ EXECUTION STEPS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Conduct necessary housekeeping
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# If running this module in Google Colab, it's possible that matplotlib
# will be an older version that generates errors and which needs
# to be updated.
import matplotlib
if matplotlib.__version__ != '3.5.1':
    %pip install -U matplotlib # type: ignore


# This is the current way of running the simulation, executing it
# without a standalone GUI and viewing its results (e.g., generated PNGs)
# in an IDE like Spyder.

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Run personnel-behaviors-records sim (or import previous sim results)
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# Either (1) simulate personnel, persons' behaviors, and managers' 
# recording of persons' behaviors, or (2) load a previous simulation's
# results from a pickled file.

# ---------------------------------------------------------------------
# Option 1: run the simulation from scratch, 
# using the current configuration.
# ---------------------------------------------------------------------
#run_simulation_of_personnel_behaviors_records()

# ---------------------------------------------------------------------
# Option 2: load a saved dataset from a previous run of the simulation.
# ---------------------------------------------------------------------
iofm.specify_directory_structure()
iofm.load_key_vars_from_pickled_file(
    "[124p-30d-4r_20220423155036]_wfs_exported_variables", # full name of the pickled file to import
    )


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Analyze and visualize simulation results
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
generate_visualizations()
copy_selected_vars_to_globals()
#print(cfg.num_of_days_to_simulate)



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