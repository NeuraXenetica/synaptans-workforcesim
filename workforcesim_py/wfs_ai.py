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
This module handles the simulation’s “Level 3” logic, which uses various
machine-learning techniques in an attempt to identify meaningful trends,
causal relationships, and other correlations relating to workers’
personal characters and workplace behaviors and to attempt to predict
workers’ future behavior – either absolutely or in response to
particular changes that might be implemented in the workplace. In
generating such analyses and predictions, the AI *does not* have access
to workers’ actual personal characteristics or behaviors; rather, it
only has access to the records made in the organization’s HRM/ERP system
by its frontline managers – which may or may not reflect workers’ actual
characteristics and behaviors in a fully accurate manner.
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
    import wfs_utilities as utils
else:
    try:
        from . import config as cfg
    except:
        import config as cfg
    try:
        from . import wfs_utilities as utils
    except:
        import wfs_utilities as utils


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

def add_eff_mday_series_to_behavs_act_df():
    """
    Adds to cfg.behavs_act_df a new set of 'mday series' columns that
    reflect the given subject's Efficacy on the days before or after
    the day that is the focus of row (i.e., D0, the day on which the
    row's main entry was recorded).
    """

    utils.begin_tracking_elapsed_processing_time()

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

    # Calculate how many weeks are in the series comprising
    # the dataset. That can be done by taking the 
    final_week_in_series_num = utils.return_week_in_series_for_given_date(
        utils.return_date_of_final_day_to_simulate(), # the date whose week should be returned
        )

    for p in cfg.persons:
        dict_of_behavs_act_Eff_dfs_by_person_ID_and_week[cfg.persons[p].per_id] = {}

        for w in range(0, final_week_in_series_num + 1):

            # Create a temp DF with only that person's Eff behaviors
            # (and the records made of them for the person
            # by supervisors) for the given week.
            behavs_act_df_this_pers = utils.return_df_with_rows_filtered_to_one_val_in_col(
                cfg.behavs_act_df, # the input DF
                "Sub ID", # the column by which to filter rows
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

        date_of_row_to_populate = cfg.behavs_act_df["Event Date"].values[i]
        subject_ID_in_row_to_populate = cfg.behavs_act_df["Sub ID"].values[i]

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
                            & (behavs_act_Eff_df_this_sub["Event Date"].values[j] == date_of_sought_mday):
                        mday_eff_act = behavs_act_Eff_df_this_sub["Actual Efficacy"].values[j]
                        cfg.behavs_act_df[mday_label].values[i] = mday_eff_act

    print("   Elapsed processing time for mday series: " + utils.return_elapsed_processing_time())


def return_df_of_persons_for_analysis_type_A():
    """
    Returns a DataFrame in which each row is one person in the workforce,
    with columns containing certain demographic info about the person
    and data regarding his performance during the simulated period
    (sum, mean, or standard deviation for selected actions).
    """

    pass



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