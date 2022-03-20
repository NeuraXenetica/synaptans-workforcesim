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
This module handles visualization of the simulation’s results. It is
capable of generating a wide range of histograms, bar plots,
scatterplots, and other plots illustrating temporal trends and the
relationships between
particular variables.
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

import io
import os


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import matplotlib.pyplot as plt
from PIL import Image


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

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for generating PNG plots as variables stored in memory
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def plot_distribution_of_WRKR_CAP_scores_hist():
    """
    Save to file and return a PNG histogram plot of WRKR_CAP scores.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    # fig.patch.set_visible(False) #This "turns off" the frame, leaving only the axis visible.

    ax.hist(cfg.persons_df["WRKR_CAP"], bins=100, color=cfg.plot_hist_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of persons\n in given WRKR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Distribution of values of persons'\n worker capacity (WRKR_CAP) score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_distribution_of_WRKR_CAP_scores_hist = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_distribution_of_WRKR_CAP_scores_hist.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_distribution_of_WRKR_CAP_scores_hist


def plot_distribution_of_MNGR_CAP_scores_hist():
    """
    Save to file and return a PNG histogram plot of MNGR_CAP scores.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.hist(cfg.persons_df["MNGR_CAP"], bins=100, color=cfg.plot_hist_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('MNGR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of persons\n in given MNGR_CAP score range', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Distribution of values of persons'\n managerial capacity (MNGR_CAP) score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_distribution_of_MNGR_CAP_scores_hist = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_distribution_of_MNGR_CAP_scores_hist.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_distribution_of_MNGR_CAP_scores_hist
    

def MNGR_CAP_vs_WRKR_CAP_scores_scatter():
    """
    Save to file and return a PNG scatterplot of MNGR_CAP
    versus WRKR_CAP scores.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.scatter(cfg.persons_df["WRKR_CAP"], cfg.persons_df["MNGR_CAP"], alpha=0.4, color=cfg.plot_scatter_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('MNGR_Cap score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of each person’s\n WRKR_CAP and MNGR_CAP scores", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter


def plot_MNGR_CAP_by_age_scatter():
    """
    Save to file and return a PNG scatterplot of MNGR_CAP scores by age.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.scatter(cfg.persons_df["Age"], cfg.persons_df["MNGR_CAP"], alpha=0.4, color=cfg.plot_scatter_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Age', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('MNGR_Cap score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of each person’s age\n and MNGR_CAP score", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_by_age_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_by_age_scatter.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_MNGR_CAP_by_age_scatter


def plot_WRKR_CAP_by_shift_bar():
    """
    Save to file and return a PNG bar plot of WRKR_CAP scores by shift.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.bar(cfg.persons_df["Shift"], cfg.persons_df["WRKR_CAP"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Shift', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n WRKR_CAP scores by shift", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_by_shift_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_by_shift_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_WRKR_CAP_by_shift_bar


def plot_MNGR_CAP_by_role_bar():
    """
    Save to file and return a PNG bar plot of MNGR_CAP scores by shift.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.bar(
        cfg.persons_df["Role"],
        cfg.persons_df["MNGR_CAP"],
        color=cfg.plot_line_data_color,
        )

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Organizational role', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average MNGR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(rotation=90, fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n MNGR_CAP scores by role filled", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_MNGR_CAP_by_role_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_MNGR_CAP_by_role_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_MNGR_CAP_by_role_bar


def plot_WRKR_CAP_by_team_bar():
    """
    Save to file and return a PNG bar plot of WRKR_CAP scores by team.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.bar(cfg.persons_df["Team"], cfg.persons_df["WRKR_CAP"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Team', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Average WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(rotation=90, fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Average value of persons’\n WRKR_CAP scores by team", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_by_team_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_by_team_bar.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_WRKR_CAP_by_team_bar
    

def plot_WRKR_CAP_vs_mean_Eff_scatter():
    """
    Save to file and return a PNG scatterplot of WRKR_CAP scores
    versus mean Efficacy.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.scatter(cfg.persons_df["WRKR_CAP"], cfg.persons_df["Mean Eff"], alpha=0.4, color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('WRKR_CAP score', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Mean Efficacy during simulated period', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Values of persons’\n WRKR_CAP scores and mean daily Efficacy", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_WRKR_CAP_vs_mean_Eff_scatter.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_WRKR_CAP_vs_mean_Eff_scatter


def plot_num_Good_vs_Poor_actions_by_person_hist2d():
    """
    Save to file and return a PNG 2D histogram plot of Good
    versus poor actions by person.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)

    ax.hist2d(cfg.persons_df["Num Goods"], cfg.persons_df["Num Poors"], bins=20)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Number of Good workplace actions per person', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Number of Poor workplace actions per person', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Number of persons’ Good and Poor\n workplace actions performed", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_num_Good_vs_Poor_actions_by_person_hist2d.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_num_Good_vs_Poor_actions_by_person_hist2d


def plot_Eff_by_weekday_bar():
    """
    Save to file and return a PNG bar plot of Efficacy scores by weekday.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Weekday Num", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.bar(df_to_plot["Weekday Num"], df_to_plot["Actual Efficacy"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Weekday', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by weekday", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_Eff_by_weekday_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_Eff_by_weekday_bar.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_Eff_by_weekday_bar


def plot_Eff_by_age_bar():
    """
    Save to file and return a PNG bar plot of Efficacy scores by weekday.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Age", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.bar(df_to_plot["Age"], df_to_plot["Actual Efficacy"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Age', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by age", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_Eff_by_age_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_Eff_by_age_bar.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_Eff_by_age_bar


def plot_Eff_by_colleagues_of_same_gender_bar():
    """
    Save to file and return a PNG bar plot of Efficacy scores by 
    the proportion of a person's teammates who are of the same gender.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Same-Sex Colleagues Prtn", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.bar(df_to_plot["Same-Sex Colleagues Prtn"], df_to_plot["Actual Efficacy"], color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Age', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by age", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_Eff_by_same_gender_colleagues_prtn_bar = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_Eff_by_same_gender_colleagues_prtn_bar.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_Eff_by_same_gender_colleagues_prtn_bar


def plot_Eff_by_colleagues_of_same_gender_line():
    """
    Save to file and return a PNG line plot of Efficacy scores by 
    the proportion of a person's teammates who are of the same gender.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Same-Sex Colleagues Prtn", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.plot(
        df_to_plot["Same-Sex Colleagues Prtn"],
        df_to_plot["Actual Efficacy"],
        color=cfg.plot_line_data_color,
        linewidth=cfg.plot_line_data_width,
        )
    ax.set_ylim(0, None)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Proportion of Same-Gender Colleagues', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by the proportion of same-gender colleagues", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_Eff_by_same_gender_colleagues_prtn_line = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_Eff_by_same_gender_colleagues_prtn_line.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_Eff_by_same_gender_colleagues_prtn_line


def plot_Eff_by_colleagues_of_same_gender_scatter():
    """
    Save to file and return a PNG scatterplot of Efficacy scores by 
    the proportion of a person's teammates who are of the same gender.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)



    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
#    df_to_plot = df_to_plot.groupby("Same-Sex Colleagues Prtn", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.scatter(df_to_plot["Same-Sex Colleagues Prtn"], df_to_plot["Actual Efficacy"], alpha=0.4, color=cfg.plot_bar_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Proportion of Same-Gender Colleagues', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by the proportion of same-gender colleagues", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_Eff_by_same_gender_colleagues_prtn_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_Eff_by_same_gender_colleagues_prtn_scatter.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )
    
    return cfg.png_plt_Eff_by_same_gender_colleagues_prtn_scatter


def plot_Eff_by_sub_sup_age_difference_scatter():
    """
    Save to file and return a PNG scatterplot of (1) the difference in ages
    between a person and his supervisor and (2) the person's mean Efficacy.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()


    ax.scatter(df_to_plot["Sub-Sup Age Difference"], df_to_plot["Actual Efficacy"], alpha=0.4, color=cfg.plot_scatter_data_color)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Subject-supervisor age difference', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by subject-supervisor age difference", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_sub_sup_age_diff_vs_eff_scatter = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_sub_sup_age_diff_vs_eff_scatter.png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_sub_sup_age_diff_vs_eff_scatter


def plot_Eff_by_sub_sup_age_difference_line():
    """
    Save to file and return a PNG line plot of (1) the difference in ages
    between a person and his supervisor and (2) the person's mean Efficacy.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub-Sup Age Difference", as_index=False).agg({"Actual Efficacy": 'mean'})


    ax.plot(
        df_to_plot["Sub-Sup Age Difference"],
        df_to_plot["Actual Efficacy"],
        color=cfg.plot_bar_data_color,
        linewidth=cfg.plot_line_data_width,
        )
    ax.set_ylim(0, None)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Subject-supervisor age difference', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Actual Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average actual Efficacy\n by subject-supervisor age difference", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()    
    
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_sub_sup_age_diff_vs_eff_line = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_sub_sup_age_diff_vs_eff_line.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_sub_sup_age_diff_vs_eff_line


def plot_recorded_Eff_by_sub_sup_age_difference_line():
    """
    Save to file and return a PNG line plot of (1) the difference in ages
    between a person and his supervisor and (2) the person's *recorded* 
    mean Efficacy.
    """

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=cfg.plot_figsize)
    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)


    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub-Sup Age Difference", as_index=False).agg({"Recorded Efficacy": 'mean'})


    ax.plot(
        df_to_plot["Sub-Sup Age Difference"],
        df_to_plot["Recorded Efficacy"],
        color=cfg.plot_bar_data_color,
        linewidth=cfg.plot_line_data_width,
        )
    ax.set_ylim(0, None)

    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)
    plt.xlabel('Subject-supervisor age difference', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.ylabel('Recorded Efficacy', fontsize=cfg.plot_xy_label_fontsize, labelpad=cfg.plot_xy_label_pad, color=cfg.plot_xy_label_color)
    plt.xticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.yticks(fontsize=cfg.plot_xy_ticks_fontsize, color=cfg.plot_xy_ticks_color)
    plt.title("Level of persons’ average recorded Efficacy\n by subject-supervisor age difference", fontsize=cfg.plot_title_fontsize, color=cfg.plot_title_color)

    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()

    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    cfg.png_plt_sub_sup_age_diff_vs_recorded_eff_line = Image.open(buffer_m)

    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            "png_plt_sub_sup_age_diff_vs_recorded_eff_line.png",           
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return cfg.png_plt_sub_sup_age_diff_vs_recorded_eff_line








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