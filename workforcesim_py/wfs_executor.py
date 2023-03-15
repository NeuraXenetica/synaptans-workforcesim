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
This module runs the simulation, accepting the arguments provided
by a user to (1) create a simulated workforce; (2) simulate workers’
daily activity for a specified number of days and quantity of workers;
and (3) generate the (potentially inaccurate) records of such workplace
behaviors made by workers’ frontline managers.
"""

import datetime
from datetime import timedelta
import random

import matplotlib.pyplot as plt
import numpy as np

# Import other modules from this package.
import config as cfg
import io_file_manager as iofm
import wfs_behaviors as bhv
import wfs_utilities as utils
import wfs_visualizer as vis
import wfs_personnel as pers
import wfs_records as rec


# ----------------------------------------------------------------------
# The functions below are sub-functions that will be called as needed
# by the main function that oversees the processing of a run of the
# simulation.
# ----------------------------------------------------------------------

def advance_date_by_one_day():
    """
    Increments the number of days simulated by 1. Advances the value of 
    the current datetime object by one day.
    """

    cfg.day_of_sim_iter += 1
    cfg.current_datetime_obj += timedelta(days = 1)
    utils.update_current_day_in_month_1_indexed_num()


def run_one_time_simulation_setup_steps():
    """
    Runs a number of one-time setup steps that must be executed once 
    when initializing the simulation.
    """

    utils.begin_tracking_elapsed_processing_time()
    iofm.generate_unique_file_prefix_code_for_simulation_run()
    cfg.current_datetime_obj = datetime.datetime.strptime(
        cfg.SIM_STARTING_DATE, '%Y-%m-%d')

    # Calculate how many days should be simulated in total, after
    # the number of days for the priming period (if any) is added to
    # NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS.
    calculate_NUM_OF_DAYS_TO_SIMULATE()

    # Calculate the initial value of cfg.day_of_sim_iter. If the 
    # simulation is being run without any priming period, then 
    # cfg.day_of_sim_iter will initially be 0. If, e.g., it's being run 
    # with a 3-day priming period, then cfg.day_of_sim_iter will have 
    # an initial value of -3.
    cfg.day_of_sim_iter = 0 - cfg.NUM_OF_DAYS_IN_PRIMING_PERIOD

    # This number will be stored permanently as a reference; it will not
    # be updated with each new simulated day.
    cfg.day_of_sim_iter_for_first_simulated_day = cfg.day_of_sim_iter

    utils.update_current_day_in_month_1_indexed_num()
    print("current date: ", cfg.current_datetime_obj)
    print(
        "final date to simulate: ", 
        utils.return_date_of_final_day_to_simulate()
        )

    # ------------------------------------------------------------------
    # Execute functions to set up the workforce.
    # ------------------------------------------------------------------

    random.seed(cfg.RANDOM_SEED_A)
    np.random.seed(cfg.RANDOM_SEED_A)

    pers.calculate_id_starting_value()
    pers.create_all_possible_roles()
    pers.create_shift_objects()
    pers.create_team_objects()
    pers.create_all_possible_spheres()
    # create_initial_set_of_tasks()
    # create_initial_set_of_activities()

    pers.create_initial_population_of_persons()
    print("len(cfg.persons): ", len(cfg.persons))

    pers.assign_initial_role_to_each_person()
    pers.assign_initial_shift_to_each_person()
    pers.assign_initial_team_to_each_person()
    pers.assign_initial_sphere_to_each_person()
    pers.assign_supervisor_to_each_person()
    pers.assign_colleagues_to_all_persons()
    pers.update_persons_colleagues_of_same_sex_prtn()
    pers.assign_subordinates_to_all_supervisors()

    bhv.configure_behavs_act_df()
    # update_current_tasks()
    cfg.persons_df = \
        pers.create_df_with_selected_attributes_of_all_persons()


def delete_behavs_act_df_data_for_priming_period():
    """
    Deletes from behavs_act_df_global data for behaviors and events for 
    any priming period at the beginning of the simulated period whose 
    contents should be deleted, as the simulation's dynamics hadn't yet 
    had an opportunity to "settle". This doesn't delete event data from 
    the priming period that's stored, e.g., in dictionaries attached to 
    Person objects.
    """

    # This deletes all rows with dates prior to the start of the
    # period to be retained for analysis.
    SIM_STARTING_DATE_FOR_ANALYSIS_datetime_obj = \
        datetime.datetime.strptime(
            cfg.SIM_STARTING_DATE_FOR_ANALYSIS, '%Y-%m-%d')
    cfg.behavs_act_df = \
        cfg.behavs_act_df[cfg.behavs_act_df["Event Datetime"] \
            >= SIM_STARTING_DATE_FOR_ANALYSIS_datetime_obj]

    # This deletes all rows with dates *later than* the ending date
    # of the simulation. (Such an entry could hypothetically be 
    # generated if, e.g., a worker were terminated on the final 
    # simulated day and that triggered automatic generation of an 
    # Onboarding event for his replacement dated to the following day. 
    # At present, such Onboarding occurs on the same day as the
    # Separation.)
    sim_ending_date_for_analysis_datetime_obj = \
        SIM_STARTING_DATE_FOR_ANALYSIS_datetime_obj + \
        timedelta(days = cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS - 1)
    cfg.behavs_act_df = \
        cfg.behavs_act_df[cfg.behavs_act_df["Event Datetime"] \
        <= sim_ending_date_for_analysis_datetime_obj]


def run_one_time_simulation_finalization_steps():
    """
    Runs a number of one-time setup steps that must be executed once 
    when concluding the simulation, after the core work of simulating 
    the days' behaviors is done.
    """

    # Save an archival "full" copy of events before deleting any entries
    # from the priming period (which is excluded from analysis and
    # visualization).
    cfg.behavs_act_df_w_priming_period = cfg.behavs_act_df

    # Delete data from behavs_act_df_global for any priming period 
    # at the beginning of the simulated period.
    delete_behavs_act_df_data_for_priming_period()

    # These totals and statistics exclude events (e.g., Attendance)
    # that occurred during any priming period.
    bhv.calculate_metrics_for_persons_in_retained_simulated_period()

    cfg.persons_df = \
        pers.create_df_with_selected_attributes_of_all_persons()

    # Generate and display some simple statistics.
    try:
        pers.display_simple_personnel_statistics()
    except:
        pass
    rec.display_simple_record_accuracy_statistics()
    bhv.display_simple_behavior_statistics()

    # Adding the mday series data to behavs_act_df is necessary for
    # generating some types of plots (e.g., ones that track the impact
    # of supervisors' recording practices on their workers' future
    # Efficacy).
    print("Beginning addition of mday series.")
    rec.add_eff_mday_series_to_behavs_act_df()

    # Export key variables to file via pickling.
    iofm.save_key_vars_to_pickled_file()


def generate_visualizations():
    """
    Creates a number of visualizations. This can only be run after
    behaviors and records have been simulated (or imported).
    """

    # Before creating any new plots, it's necessary to manually delete
    # any existing matplotlib plots from memory -- otherwise, warning
    # messages will be generated after there are 20 plots in memory.
    plt.close("all")
    #
    print("Simulation results have been calculated or loaded. " \
        + "Preparing visualizations.")

    # This prevents a warning from being displayed that "More than 20 
    # figures have been opened."
    plt.rcParams.update({'figure.max_open_warning': 0})

    # ------------------------------------------------------------------
    # Generate (selected) visualizations.
    # ------------------------------------------------------------------

    vis.plot_Eff_mean_vs_Eff_sd_with_workstyles_scatter()
    vis.plot_ideas_mean_by_workstyle_group_bar()
    vis.plot_distribution_of_MNGR_CAP_scores_hist()
    vis.plot_Eff_by_weekday_bar()
    vis.plot_Eff_by_day_in_series_bar()
    vis.plot_recorded_Eff_by_sub_sup_age_difference_line()
    vis.generate_event_row_internal_correlations_heatmap()
    vis.generate_interpersonal_correlations_heatmap()
    try:
        vis.plot_mday_series_Eff_for_behav_comptype_bar(
            "Record Conf Mat",
            "True Positive",
            cfg.PLOT_COLOR_GREEN,
            )
    except:
        pass
    try:
        vis.plot_mday_series_Eff_for_behav_comptype_bar(
            "Record Conf Mat",
            "False Negative",
            cfg.PLOT_COLOR_SALMON,
            )
    except:
        pass


def calculate_NUM_OF_DAYS_TO_SIMULATE():
    """
    Calculates the total number of days to be simulated (including both 
    the days in the priming period (to be later discarded) and the 
    number of days in the focal period to be retained for analysis and 
    visualization).
    """

    SIM_STARTING_DATE_datetime_obj = \
        datetime.datetime.strptime(cfg.SIM_STARTING_DATE, '%Y-%m-%d')
    SIM_STARTING_DATE_FOR_ANALYSIS_datetime_obj = \
        datetime.datetime.strptime(
            cfg.SIM_STARTING_DATE_FOR_ANALYSIS, '%Y-%m-%d')
    cfg.NUM_OF_DAYS_IN_PRIMING_PERIOD = \
        (SIM_STARTING_DATE_FOR_ANALYSIS_datetime_obj \
            - SIM_STARTING_DATE_datetime_obj).days
    cfg.NUM_OF_DAYS_TO_SIMULATE = \
        cfg.NUM_OF_DAYS_IN_PRIMING_PERIOD \
            + cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS


def run_simulation_of_personnel_behaviors_records():
    """
    Runs the core simulation of workers' behaviors and their managers'
    (more or less accurate) records of those behaviors.
    """

    run_one_time_simulation_setup_steps()

    # Simulate the desired number of days of activities.
    for d in range(
        cfg.day_of_sim_iter_for_first_simulated_day,
        cfg.day_of_sim_iter_for_first_simulated_day \
            + cfg.NUM_OF_DAYS_TO_SIMULATE
        ):

        print("Beginning simulation for day " + str(d) + ".")
        print("   Elapsed processing time: " \
            + utils.return_elapsed_processing_time())

        # If the current weekday is a Monday, there is a chance that a 
        # given Laborer will be transferred to a new Team within the 
        # same Shift (during the supervisors' planning of the week's 
        # work, and before it's known whether or not the Laborer will 
        # actually show up for work on the given day). If such a 
        # transfer occurs, the Laborer will swap Teams with a randomly 
        # selected Laborer on the Team to which he's being transferred.
        if cfg.current_datetime_obj.weekday() == 0:
            pers.check_for_and_execute_worker_swaps()

        # Rebuild selected supervisor, colleague, and subordinate 
        # relationships to reflect the actual state of things after any 
        # separations from employment or swaps of workers between Teams.
        pers.rebuild_selected_personal_relationships()

        # This is necessary to avoid modifiers mistakenly accumulating
        # (potentially in expotential fashion) from day to day.
        pers.reset_modified_probs_to_base_probs_for_all_persons()

        #print("Calculating person modifiers.")
        pers.calculate_person_modifiers_to_implement_dependencies_and_covariance()

        # Run one day of workers' behaviors.
        bhv.simulate_one_day_of_behaviors()

        # Run one day of supervisors' recordings of workers' behaviors.
        rec.simulate_one_day_of_records()

        pers.check_for_and_execute_worker_separation_and_replacement()
        advance_date_by_one_day()

    run_one_time_simulation_finalization_steps()


# ----------------------------------------------------------------------
# The functions below provide two ways of preparing simulation data
# to be visualized and made available for download:
# 
#    Option 1: Run the simulation from scratch, using the current 
#    settings found in config.py.
# 
#    Option 2: Load a saved dataset from a previous run of the 
#    simulation.
# ----------------------------------------------------------------------

def run_simulation_from_scratch_using_config_settings():
    """
    # Runs the simulation from scratch, using the current settings
    # found in config.py.
    """

    run_simulation_of_personnel_behaviors_records()
    print("len(cfg.persons): ", len(cfg.persons))
    print("cfg.behavs_act_df.shape: ", cfg.behavs_act_df.shape)
    generate_visualizations()
    iofm.save_wfs_behaviors_records_df_as_csv_or_pickle_for_distribution(
        "CSV"
        )


def load_saved_dataset_from_previous_simulation_run():
    """
    Loads a saved dataset from a previous run of the simulation.
    """

    iofm.load_key_vars_from_pickled_file(
        "[148p-90d-99r_20230208092751]_wfs_exported_variables")
    print("len(cfg.persons): ", len(cfg.persons))
    print("cfg.behavs_act_df.shape: ", cfg.behavs_act_df.shape)
    generate_visualizations()


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