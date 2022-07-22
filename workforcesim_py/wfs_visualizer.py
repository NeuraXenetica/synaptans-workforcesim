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
relationships between particular variables.
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
import colorsys
import warnings


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
from PIL import Image
from PIL import ImageColor
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

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Functions for generating PNG plots as variables stored in memory
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def add_gradientbars_to_ax_plot(
    bars_to_have_gradient_added,
    data_color_main_u,
    ):
    """
    This helper function adds a color gradient to
    bars on an ax that already has a bar plot.
    """

    data_color_main_u_rgb = matplotlib.colors.to_rgb(data_color_main_u)

    # Changing the order of colors (from top to bottom of the gradient)
    # and the number of times a color is repeated is how the appearance
    # of the gradient can be modified.
    colors_vertical_grad_m = [
        data_color_main_u_rgb,
        data_color_main_u_rgb,
        data_color_main_u_rgb,
        cfg.plot_bar_bottom_grad_color,
        cfg.ops_results_section_fig_axis_bg_color,
        cfg.ops_results_section_fig_axis_bg_color,
        cfg.ops_results_section_fig_axis_bg_color,
        cfg.ops_results_section_fig_axis_bg_color,
        ]

    colormap_m = LinearSegmentedColormap.from_list(
        "Custom", colors_vertical_grad_m, N=100
        )

    gradient = np.atleast_2d(np.linspace(0,1,256)).T
    ax = bars_to_have_gradient_added[0].axes
    limits = ax.get_xlim() + ax.get_ylim()
    for bar in bars_to_have_gradient_added:
        bar.set_zorder(1)
        bar.set_facecolor("none")
        x, y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        ax.imshow(
            gradient,
            cmap = colormap_m,
            extent=[x, x+w, y, y+h], aspect="auto", zorder=0
            )
    ax.axis(limits)


# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
# ● High-level plotting functions (generalized functions that control
# ● multiple plot types, for use in the user interface)
# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

def generate_simple_plot_return_PNG_and_save_to_file(
    plot_type_u, # plot type ("column", "hist", "hist2d", "line", "scatter", "heatmap")
    data_x_u, # x-series of the data
    data_y_u, # y-series of the data (optional)
    x_axis_label_u, # x-axis label
    y_axis_label_u, # y-axis label (optional)
    x_tick_labels_rotation_u, # rotation of x-tick labels
    xy_tick_labels_custom_fontsize_u, # custom xy-tick label fontsize
    data_color_main_u, # the main color for the data
    data_alpha_main_u, # optional alpha value for the data
    color_mapping_for_legend_u, # the color mapping for use in legend
    plot_title_u, # title for the whole plot
    wfs_logo_location_u, # location for WorkforceSim logo (e.g., "upper right")
    name_for_file_u # name for PNG file
    ):

    # ---------------------------------------------------------------------
    # Create the empty figure where data will be plotted.
    # ---------------------------------------------------------------------

    plt.rcParams['figure.dpi'] = cfg.plot_figure_dpi
    plt.rcParams['savefig.dpi'] = cfg.plot_savefig_dpi

    # Typical plots have a landscape-orientation rectangular size.
    if plot_type_u != "heatmap":
        fig = plt.figure(figsize=cfg.plot_figsize)
    # Seaborn heatmaps are square.
    elif plot_type_u == "heatmap":
        fig = plt.figure(figsize=(cfg.plot_figsize[0]*1.0,cfg.plot_figsize[0]*0.9))

    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

    fig.patch.set_facecolor(cfg.ops_results_section_fig_bg_color)
    #fig.patch.set_visible(False) #This "turns off" the frame, leaving only the axis visible.


    # ---------------------------------------------------------------------
    # Plot the actual data using a unique plot type.
    # ---------------------------------------------------------------------

    # A chart with simple vertical columns (i.e., a rotated bar plot).
    if plot_type_u == "bar":
        barplot_this = ax.bar(
            data_x_u,
            data_y_u,
            alpha=data_alpha_main_u,
            color=data_color_main_u,
            linewidth=0,
            )
        #add_gradientbars_to_ax_plot(
        #    barplot_this,
        #    data_color_main_u,
        #    )

    # A horizontal histogram (e.g., a normal distribution curve).
    elif plot_type_u == "hist":
        ax.hist(
            data_x_u,
            bins=100,
            color=data_color_main_u,
            linewidth=0,
            )

    # A 2D "heatmap" histogram with rectangular cells.
    elif plot_type_u == "hist2d":
        ax.hist2d(
            data_x_u,
            data_y_u,
            bins=30,
            )

    # A line graph (a generic "plot", in Matplotlib terms).
    elif plot_type_u == "line":
        ax.plot(
            data_x_u,
            data_y_u,
            color=data_color_main_u,
            linewidth=cfg.plot_line_data_width,
            )
        ax.set_ylim(0, None)

    # A scatterplot.
    elif plot_type_u == "scatter":
        ax.scatter(
            data_x_u,
            data_y_u,
            alpha=data_alpha_main_u,
            color=data_color_main_u,
            )

        # Add a legend -- but only if something other than None
        # was passed as the value of color_mapping_for_legend_u.
        if color_mapping_for_legend_u is not None:

            classes = list(color_mapping_for_legend_u.keys())
            #print(classes)

            class_colors = list(color_mapping_for_legend_u.values())
            #print(class_colors)

            rectangles = []

            for i in range(len(class_colors)):
                rectangles.append(mpatches.Rectangle(
                    (0,0),
                    1, 1,
                    facecolor=class_colors[i],
                    linewidth=0,
                    ))

            plt.legend(
                rectangles,
                classes,
                loc="best",
                fancybox=True,
                framealpha=0.25,
                fontsize=cfg.plot_xy_ticks_fontsize,
                facecolor=cfg.figure_background_facecolor, # darkest plum
                labelcolor="white",
                )

    # A heatmap.
    elif plot_type_u == "heatmap":

        # Note! Importing Seaborn unfortunately seems to overwrite the already 
        # configured Matplotlib settings and disrupt elements of the other 
        # (non-Seaborn) Matplotlib graphs.
        import seaborn as sns

        color_rgb = ImageColor.getcolor(cfg.plot_bar_data_color, "RGB")

        # The color doesn't work correctly, as colorsys generates an HLS
        # color, but Seaborn interprets it as an HULS color.
        color_hls = colorsys.rgb_to_hls(color_rgb[0], color_rgb[1], color_rgb[2])

        # By default, Seaborn heatmaps -1.0 and +1.0 colors using opposite
        # ends of the colormap; however, it's possible to set it to use 
        # the absolute value of numbers when selecting colors (so that
        # correlations of -1.0 and +1.0 will have the same color and 0.0 will
        # be the color at the opposite end of the spectrum).
        cmap_absolute_valued = sns.diverging_palette(
            color_hls[0],
            color_hls[0],
            s=100,
            l=50,
            as_cmap=True,
            center='dark',
            )

        sns.set(font_scale=0.8)

        sns.heatmap(
            data_x_u,
            ax = ax,
            annot=True,
            annot_kws={"size":3},
            fmt='.2f', # 2 decimal places
            cmap=cmap_absolute_valued,
            vmin=-1.0,
            vmax=1.0,
            xticklabels=1,
            yticklabels=1,
            )

        # It's unclear whether these are really necessary.
        ax.grid(b=None)
        ax.grid(False)

        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(
            labelsize=cfg.plot_xy_label_fontsize,
            color=cfg.plot_xy_label_color,
            labelcolor=cfg.plot_xy_label_color,
            )


    # ---------------------------------------------------------------------
    # Add supplemental plot elements common to (almost) all plot types.
    # ---------------------------------------------------------------------
    ax.patch.set_facecolor(cfg.ops_results_section_fig_axis_bg_color)

    if xy_tick_labels_custom_fontsize_u is None:
        plot_xy_tick_label_fontsize_to_use = cfg.plot_xy_ticks_fontsize
    else:
        plot_xy_tick_label_fontsize_to_use = xy_tick_labels_custom_fontsize_u

    plt.xlabel(
        x_axis_label_u,
        fontsize=cfg.plot_xy_label_fontsize,
        labelpad=cfg.plot_xy_label_pad,
        color=cfg.plot_xy_label_color,
        )
    plt.ylabel(
        y_axis_label_u,
        fontsize=cfg.plot_xy_label_fontsize,
        labelpad=cfg.plot_xy_label_pad,
        color=cfg.plot_xy_label_color,
        )
    plt.xticks(
        fontsize=plot_xy_tick_label_fontsize_to_use,
        color=cfg.plot_xy_ticks_color,
        rotation = x_tick_labels_rotation_u,
        )
    plt.yticks(
        fontsize=plot_xy_tick_label_fontsize_to_use,
        color=cfg.plot_xy_ticks_color,
        )
    plt.title(
        plot_title_u,
        fontsize=cfg.plot_title_fontsize,
        color=cfg.plot_title_color,
        )

    plt.grid(b=None)
    ax.grid(False)
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)


    # Add a WorkforceSim logo.
    if wfs_logo_location_u is not None:
        logo_path_and_name = os.path.join(cfg.input_files_dir, "WorkforceSim_logo_02_1120-A_02.png")
        im = plt.imread(logo_path_and_name)
        imagebox = OffsetImage(im, zoom=0.018)
        ab = AnchoredOffsetbox(loc=wfs_logo_location_u, child=imagebox, frameon=False)
        logo_ax = fig.add_axes([0,0,1,1])
        logo_ax.grid(False)
        logo_ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)
        logo_ax.set(xticklabels=[])
        logo_ax.set(yticklabels=[])
        logo_ax.tick_params(left=False, bottom=False)
        plt.gca().set_position([0,0,1,1])
        logo_ax.set_facecolor('none')
        logo_ax.add_artist(ab)

    warnings.filterwarnings("ignore", message="This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.")
    #
    # This is needed to prevent x- and y-tick labels from sometimes being cut off.
    fig.tight_layout()


    # ---------------------------------------------------------------------
    # Save the plot to a PNG file and return the plot as a variable.
    # ---------------------------------------------------------------------

    # Read the plot image data into the buffer.
    buffer_m = io.BytesIO()
    plt.savefig(buffer_m, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer_m.seek(0)
    generated_PNG_plot_as_var = Image.open(buffer_m)

    # Save the plot as a PNG.
    plt.savefig(
        os.path.join(
            cfg.output_files_dir,
            name_for_file_u + ".png",
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return generated_PNG_plot_as_var


# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
# ● Low-level (particular) plotting functions, controlled by the
# ● high-level generalized plotting functions and user interface
# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

def plot_distribution_of_WRKR_CAP_scores_hist():
    """
    Save to file and return a PNG histogram plot of WRKR_CAP scores.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "hist", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["WRKR_CAP"], # x-series of the data
        None, # y-series of the data (optional)
        'WRKR_CAP score range', # x-axis label
        'Number of persons\n in given WRKR_CAP score range', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_hist_data_color, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Distribution of values of persons'\n worker capacity (WRKR_CAP) score", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_distribution_of_WRKR_CAP_scores_hist.png" # name for PNG file
        )


def plot_distribution_of_MNGR_CAP_scores_hist():
    """
    Save to file and return a PNG histogram plot of MNGR_CAP scores.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "hist", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["MNGR_CAP"], # x-series of the data
        None, # y-series of the data (optional)
        'MNGR_CAP score range', # x-axis label
        'Number of persons\n in given MNGR_CAP score range', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_hist_data_color, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Distribution of values of persons'\n managerial capacity (MNGR_CAP) score", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_distribution_of_MNGR_CAP_scores_hist.png" # name for PNG file
        )


def MNGR_CAP_vs_WRKR_CAP_scores_scatter():
    """
    Save to file and return a PNG scatterplot of MNGR_CAP
    versus WRKR_CAP scores.
    """
    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["WRKR_CAP"], # x-series of the data
        df_to_plot["MNGR_CAP"], # y-series of the data (optional)
        'WRKR_CAP score', # x-axis label
        'MNGR_CAP score', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_scatter_data_color, # the main color for the data
        0.4, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Values of each person’s\n WRKR_CAP and MNGR_CAP scores", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_MNGR_CAP_vs_WRKR_CAP_scores_scatter.png" # name for PNG file
        )


def plot_MNGR_CAP_by_age_scatter():
    """
    Save to file and return a PNG scatterplot of MNGR_CAP scores by age.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Age"], # x-series of the data
        df_to_plot["MNGR_CAP"], # y-series of the data (optional)
        'Sub Age', # x-axis label
        'MNGR_CAP score', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_scatter_data_color, # the main color for the data
        0.5, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Values of each person’s age\n and MNGR_CAP score", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_MNGR_CAP_by_age_scatter.png" # name for PNG file
        )


def plot_WRKR_CAP_by_shift_bar():
    """
    Save to file and return a PNG bar plot of WRKR_CAP scores by shift.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    # Flatten the DF to only include a row for its mean values.
    # This approach to flattening involves simpler code, but it 
    # calculates the mean for *all* columns (including those that
    # don't need to be plotted).
    df_to_plot = df_to_plot.groupby("Sub Shift", as_index=False).mean()

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Shift"], # x-series of the data
        df_to_plot["WRKR_CAP"], # y-series of the data (optional)
        'Sub Shift', # x-axis label
        'Average WRKR_CAP score', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Average value of persons’\n WRKR_CAP scores by shift", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_WRKR_CAP_by_shift_bar.png" # name for PNG file
        )


def plot_MNGR_CAP_by_role_bar():
    """
    Save to file and return a PNG bar plot of MNGR_CAP scores by role.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    # Flatten the DF to only include a row for its mean values.
    df_to_plot = df_to_plot.groupby("Sub Role", as_index=False).agg({"MNGR_CAP": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Role"], # x-series of the data
        df_to_plot["MNGR_CAP"], # y-series of the data (optional)
        'Organizational role', # x-axis label
        'Average MNGR_CAP score', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_line_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Average value of persons’\n MNGR_CAP scores by role filled", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_MNGR_CAP_by_role_bar.png" # name for PNG file
        )


def plot_WRKR_CAP_by_team_bar():
    """
    Save to file and return a PNG bar plot of WRKR_CAP scores by team.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    # Flatten the DF to only include a row for its mean values.
    df_to_plot = df_to_plot.groupby("Sub Team", as_index=False).agg({"WRKR_CAP": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Team"], # x-series of the data
        df_to_plot["WRKR_CAP"], # y-series of the data (optional)
        'Organizational role', # x-axis label
        'Average MNGR_CAP score', # y-axis label (optional)
        90, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Average value of persons’\n WRKR_CAP scores by team", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_WRKR_CAP_by_team_bar.png" # name for PNG file
        )


def plot_WRKR_CAP_vs_mean_Eff_scatter():
    """
    Save to file and return a PNG scatterplot of WRKR_CAP scores
    versus mean Efficacy.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["WRKR_CAP"], # x-series of the data
        df_to_plot["Mean Eff"], # y-series of the data (optional)
        'WRKR_CAP score', # x-axis label
        'Mean Efficacy during simulated period', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        0.4, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Values of persons’\n WRKR_CAP scores and mean daily Efficacy", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_WRKR_CAP_vs_mean_Eff_scatter.png" # name for PNG file
        )


def plot_num_Good_vs_Poor_actions_by_person_hist2d():
    """
    Save to file and return a PNG 2D histogram plot of Good
    versus Poor actions by person.
    """

    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "hist2d", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Num Goods"], # x-series of the data
        df_to_plot["Num Poors"], # y-series of the data (optional)
        'Number of Good workplace actions per person', # x-axis label
        'Number of Poor workplace actions per person', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        None, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of persons’ Good and Poor\n workplace actions performed", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_num_Good_vs_Poor_actions_by_person_hist2d.png" # name for PNG file
        )


def plot_Eff_by_weekday_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores by weekday.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Weekday Num", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Weekday Num"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Weekday', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by weekday", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_weekday_bar.png" # name for PNG file
        )


def plot_Eff_by_day_of_month_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by day of the month.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    # Add a column with the day of the month.
    df_to_plot["Day in Month"] = None
    for i in range(len(df_to_plot)):
        behav_datetime = df_to_plot["Event Datetime"].values[i]
        behav_day_in_month = pd.to_datetime(behav_datetime).day
        df_to_plot["Day in Month"].values[i] = behav_day_in_month
    df_to_plot = df_to_plot.groupby("Day in Month", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Day in Month"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Day of Month', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by the day of the month", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_day_of_month_bar.png" # name for PNG file
        )


def plot_Eff_by_day_in_series_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by the day in the simulated series.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Event Date", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Event Date"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Day in Series', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by day in the series", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_day_series_bar.png" # name for PNG file
        )


def plot_teamworks_by_day_of_month_bar():
    """
    Save to file and return a PNG bar plot of the number
    of Teamwork behaviors by day of the month.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    # Add a column with the day of the month.
    df_to_plot["Day in Month"] = None
    for i in range(len(df_to_plot)):
        behav_datetime = df_to_plot["Event Datetime"].values[i]
        behav_day_in_month = pd.to_datetime(behav_datetime).day
        df_to_plot["Day in Month"].values[i] = behav_day_in_month
    df_to_plot = df_to_plot.groupby("Day in Month", as_index=False).agg({"BC Teamwork": 'sum'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Day in Month"], # x-series of the data
        df_to_plot["BC Teamwork"], # y-series of the data (optional)
        'Day of Month', # x-axis label
        'Number of Teamwork Behaviors', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of Teamwork behaviors generated\n by the day of the month", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_teamworks_by_day_of_month_bar.png" # name for PNG file
        )


def plot_disruptions_by_day_of_month_bar():
    """
    Save to file and return a PNG bar plot of the number
    of Disruption behaviors by day of the month.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    # Add a column with the day of the month.
    df_to_plot["Day in Month"] = None
    for i in range(len(df_to_plot)):
        behav_datetime = df_to_plot["Event Datetime"].values[i]
        behav_day_in_month = pd.to_datetime(behav_datetime).day
        df_to_plot["Day in Month"].values[i] = behav_day_in_month
    df_to_plot = df_to_plot.groupby("Day in Month", as_index=False).agg({"BC Disruption": 'sum'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Day in Month"], # x-series of the data
        df_to_plot["BC Disruption"], # y-series of the data (optional)
        'Day of Month', # x-axis label
        'Number of Disruption Behaviors', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of Disruption behaviors generated\n by the day of the month", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_disruptions_by_day_of_month_bar.png" # name for PNG file
        )


def plot_slips_by_day_of_month_bar():
    """
    Save to file and return a PNG bar plot of the number
    of Slip behaviors by day of the month.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    # Add a column with the day of the month.
    df_to_plot["Day in Month"] = None
    for i in range(len(df_to_plot)):
        behav_datetime = df_to_plot["Event Datetime"].values[i]
        behav_day_in_month = pd.to_datetime(behav_datetime).day
        df_to_plot["Day in Month"].values[i] = behav_day_in_month
    df_to_plot = df_to_plot.groupby("Day in Month", as_index=False).agg({"BC Slip": 'sum'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Day in Month"], # x-series of the data
        df_to_plot["BC Slip"], # y-series of the data (optional)
        'Day of Month', # x-axis label
        'Number of Slip Behaviors', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of Slip behaviors generated\n by the day of the month", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_slips_by_day_of_month_bar.png" # name for PNG file
        )


def plot_Eff_by_age_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores by weekday.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub Age", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Age"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Sub Age', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by age", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_age_bar.png" # name for PNG file
        )


def plot_Eff_mean_by_workstyle_group_bar():
    """
    Save to file and return a PNG bar plot of mean Actual Efficacy scores by 
    subjects' Workstyle group.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub Workstyle", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Workstyle"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Sub Workstyle', # x-axis label
        'Actual Efficacy (mean)', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual daily Efficacy\n by Workstyle group", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_mean_by_workstyle_group_bar.png" # name for PNG file
        )


def plot_Eff_sd_by_workstyle_group_bar():
    """
    Save to file and return a PNG bar plot of the SD of Actual Efficacy scores by 
    subjects' Workstyle group.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub Workstyle", as_index=False).agg({"Actual Efficacy (SD)": 'std'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Workstyle"], # x-series of the data
        df_to_plot["Actual Efficacy (SD)"], # y-series of the data (optional)
        'Sub Workstyle', # x-axis label
        'Actual Efficacy (standard deviation)', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ standard deviation of actual daily Efficacy\n by Workstyle group", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_sd_by_workstyle_group_bar.png" # name for PNG file
        )


def plot_Eff_by_colleagues_of_same_sex_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores by 
    the proportion of a subject's teammates who are of the same sex.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub Same-Sex Colleagues Prtn", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Same-Sex Colleagues Prtn"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Proportion of Same-Gender Colleagues', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by the proportion of same-sex colleagues", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_same_sex_colleagues_prtn_bar.png" # name for PNG file
        )


def plot_Eff_by_colleagues_of_same_sex_line():
    """
    Save to file and return a PNG line plot of Actual Efficacy scores by 
    the proportion of a subject's teammates who are of the same sex.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub Same-Sex Colleagues Prtn", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "line", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Same-Sex Colleagues Prtn"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Proportion of Same-Gender Colleagues', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_line_data_color, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by the proportion of same-sex colleagues", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_same_sex_colleagues_prtn_line.png" # name for PNG file
        )


def plot_Eff_by_colleagues_of_same_sex_scatter():
    """
    Save to file and return a PNG scatterplot of Actual Efficacy scores by 
    the proportion of a subject's teammates who are of the same sex.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Same-Sex Colleagues Prtn"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Proportion of Same-Gender Colleagues', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        0.5, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by the proportion of same-sex colleagues", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_same_sex_colleagues_prtn_scatter.png" # name for PNG file
        )


def plot_Eff_by_sub_sup_age_difference_scatter():
    """
    Save to file and return a PNG scatterplot of (1) the difference in ages
    between a subject and his supervisor and (2) the subject's mean Actual Efficacy.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sup-Sub Age Difference"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Subject-supervisor age difference', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_scatter_data_color, # the main color for the data
        0.5, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by subject-supervisor age difference", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_sub_sup_age_diff_vs_eff_scatter.png" # name for PNG file
        )


def plot_Eff_by_sub_sup_age_difference_line():
    """
    Save to file and return a PNG line plot of (1) the difference in ages
    between a subject and his supervisor and (2) the person's mean Actual Efficacy.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sup-Sub Age Difference", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "line", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sup-Sub Age Difference"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Subject-supervisor age difference', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by subject-supervisor age difference", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_sub_sup_age_diff_vs_eff_line.png" # name for PNG file
        )


def plot_recorded_Eff_by_sub_sup_age_difference_line():
    """
    Save to file and return a PNG line plot of (1) the difference in ages
    between a subject and his supervisor and (2) the subject's mean 
    Recorded Efficacy.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sup-Sub Age Difference", as_index=False).agg({"Recorded Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "line", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sup-Sub Age Difference"], # x-series of the data
        df_to_plot["Recorded Efficacy"], # y-series of the data (optional)
        'Subject-supervisor age difference', # x-axis label
        'Recorded Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average recorded Efficacy\n by subject-supervisor age difference", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_sub_sup_age_diff_vs_recorded_eff_line.png" # name for PNG file
        )


def plot_Eff_mean_vs_Eff_sd_with_workstyles_scatter():
    """
    Save to file and return a PNG scatter plot of the mean and SD of 
    subjects' Actual Efficacy scores, colored by a subject's Workstyle group.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Sub ID", as_index=False).agg(
        {
            "Actual Efficacy": 'mean',
            "Actual Efficacy (SD)": 'std',
            "Sub Workstyle": 'last',
            }
        )

    colors = {
        "Group A": "#00FA95", # bright green
        "Group B": "#ff00ff", # magenta
        "Group C": "#9ea3ff", # lavender
        "Group D": "#FF534F", # red
        "Group E": "#FFFD27", # yellow
        }

    generate_simple_plot_return_PNG_and_save_to_file(
        "scatter", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Actual Efficacy"], # x-series of the data
        df_to_plot["Actual Efficacy (SD)"], # y-series of the data (optional)
        'Actual Efficacy (mean)', # x-axis label
        'Actual Efficacy (standard deviation)', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        df_to_plot["Sub Workstyle"].map(colors), # the main color for the data
        0.5, # optional alpha value for the data
        colors, # the color mapping for use in legend
        "Persons’ mean Efficacy versus the SD of their actual daily Efficacy colored by Workstyle group", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_mean_vs_Eff_sd_with_workstyle_group_bar.png" # name for PNG file
        )


def plot_mday_series_Eff_for_behav_comptype_bar(
    d0_event_col_name_u, # name of col (e.g., "Behavior Type", "Record Conf Mat") in which D0 event is noted
    d0_event_name_u, # name of the D0 event type (e.g., "Good", "False Negative")
    ):
    """
    Save to file and return a PNG bar plot showing the mean Actual Efficacy
    behaviors for subjects on the days before and after a certain type of
    actual behavior (i.e., an mday series).
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    # Extract only those rows containing the selected Behavior Type
    # or Behavior Comptype.
    df_to_plot = df_to_plot[df_to_plot[d0_event_col_name_u] == d0_event_name_u]

    # Flatten the DF to only include a row for its mean values.
    df_to_plot = df_to_plot.groupby(d0_event_col_name_u, as_index=False).agg(
        {
            "D-4 Eff": 'mean',
            "D-3 Eff": 'mean',
            "D-2 Eff": 'mean',
            "D-1 Eff": 'mean',
            "D0 Eff": 'mean',
            "D+1 Eff": 'mean',
            "D+2 Eff": 'mean',
            "D+3 Eff": 'mean',
            "D+4 Eff": 'mean',
            }
        )

    # Extract only those columns containing the mday series
    # Actual Efficacy values.
    df_to_plot = df_to_plot[[
        "D-4 Eff",
        "D-3 Eff",
        "D-2 Eff",
        "D-1 Eff",
        "D0 Eff",
        "D+1 Eff",
        "D+2 Eff",
        "D+3 Eff",
        "D+4 Eff",
        ]]

    # Specify as X values for the plot the names of the columns 
    # containing the mday series Actual Efficacy values.
    data_x = [
        "D-4 Eff",
        "D-3 Eff",
        "D-2 Eff",
        "D-1 Eff",
        "D0 Eff",
        "D+1 Eff",
        "D+2 Eff",
        "D+3 Eff",
        "D+4 Eff",
        ]

    # Specify as Y values for the plot the contents of the lone
    # row of the DF (i.e., the mean Actual Efficacy values for each day in the 
    # mday series).
    data_y = df_to_plot.loc[0, :].values.tolist()

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        data_x, # x-series of the data
        data_y, # y-series of the data (optional)
        "Day relative to analyzed D0 event", # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Persons’ average actual Efficacy on days before and after D0 event '" + d0_event_col_name_u + ": " + d0_event_name_u + "'", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_mday_series_Eff_for_" + d0_event_col_name_u + "_" + d0_event_name_u + ".png" # name for PNG file
        )


def plot_disruptions_mean_by_workstyle_group_bar():
    """
    Save to file and return a PNG bar plot of the mean number of
    Disruptions per subject, by subjects' Workstyle group membership.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    df_to_plot = df_to_plot.groupby("Sub ID", as_index=False).agg({
        "Sub Workstyle": 'last',
        "BC Disruption": 'sum',
        })
    df_to_plot = df_to_plot.groupby("Sub Workstyle", as_index=False).agg({"BC Disruption": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Workstyle"], # x-series of the data
        df_to_plot["BC Disruption"], # y-series of the data (optional)
        'Sub Workstyle', # x-axis label
        'Mean number of Disruptions per person in Workstyle group', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Mean number of Disruption behaviors per person by Workstyle group", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_disruptions_mean_by_workstyle_group_bar.png" # name for PNG file
        )


def plot_ideas_mean_by_workstyle_group_bar():
    """
    Save to file and return a PNG bar plot of the mean number of
    Ideas per subject, by subjects' Workstyle group membership.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    df_to_plot = df_to_plot.groupby("Sub ID", as_index=False).agg({
        "Sub Workstyle": 'last',
        "BC Idea": 'sum',
        })
    df_to_plot = df_to_plot.groupby("Sub Workstyle", as_index=False).agg({"BC Idea": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Sub Workstyle"], # x-series of the data
        df_to_plot["BC Idea"], # y-series of the data (optional)
        'Sub Workstyle', # x-axis label
        'Mean number of Ideas per person in Workstyle group', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Mean number of Idea behaviors per person by Workstyle group", # title for the whole plot
        "lower right", # location for WFS logo (e.g., "upper right")
        "png_plt_ideas_mean_by_workstyle_group_bar.png" # name for PNG file
        )



# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 
# ● Other plot types
# ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● 

def generate_event_row_internal_correlations_heatmap():
    """
    Save to file and return a PNG with a heatmap showing correlations of
    certain variables that all appear on the *same row* of behavs_act_df
    (i.e., that are all recorded as part of a single behavior-record event).

    This treats each *behavior-record* event row (not each subject) as the
    fundamental data-point to be compared with others.

    Note! This uses Seaborn, whose import disrupts
    existing Matplotlib settings. This function should only be run after
    all desired (non-Seaborn) Matplotlib plots have been created.
    """

    # Prepare the data.
    correlations_df = utils.return_df_with_selected_cols_from_df(
        cfg.behavs_act_df, # the input DF
        [
            "Sub Health",
            "Sub Commitment",
            "Sub Perceptiveness",
            "Sub Dexterity",
            "Sub Sociality",
            "Sub Goodness",
            "Sub Strength",
            "Sub Openmindedness",
            "Sub Age",
            "Sup-Sub Age Difference",
            "Sub Same-Sex Colleagues Prtn",
            "Weekday Num",
            "Actual Efficacy",
            "Recorded Efficacy",
            ], # a list of columns to keep in the new DF
        )

    # It's important to convert all columns to a numerical type,
    # to keep Pandas from eliminating some of the (non-numerical)
    # columns.
    correlations_df = correlations_df.astype(float)
    correlations_df = correlations_df.corr()

    generate_simple_plot_return_PNG_and_save_to_file(
        "heatmap", # plot type ("column", "hist", "hist2d", "line", "scatter", "heatmap")
        correlations_df, # x-series of the data
        None, # y-series of the data (optional)
        None, # x-axis label
        None, # y-axis label (optional)
        90, # rotation of x-tick labels
        7.5, # custom xy-tick label fontsize
        None, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Correlations between elements within a single behavior-record event\n(dataset for " + str(cfg.size_of_comm_initial) + " persons and " + str(cfg.num_of_days_to_simulate_for_analysis) + " days)", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "heatmap1.png" # name for PNG file
        )


def generate_interpersonal_correlations_heatmap():
    """
    Save to file and return a PNG with a heatmap showing correlations 
    between different subjects' stats and events (e.g., between the number 
    of Lapses and average Efficacy).

    This treats each *subject* (not each *behavior-record* event row) as the
    fundamental data-point to be compared with others.

    Note! This uses Seaborn, whose import disrupts
    existing Matplotlib settings. This function should only be run after
    all desired (non-Seaborn) Matplotlib plots have been created.
    """

    # Prepare the data.
    correlations_df = cfg.behavs_act_df.copy()

    correlations_df_OHE_Behavior_Comptype = pd.get_dummies(correlations_df["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    correlations_df = pd.merge(
        left = correlations_df,
        right = correlations_df_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )
    correlations_df_OHE_Record_Conf_Mat = pd.get_dummies(correlations_df["Record Conf Mat"], prefix = "RCM", prefix_sep = " ")
    correlations_df = pd.merge(
        left = correlations_df,
        right = correlations_df_OHE_Record_Conf_Mat,
        left_index=True,
        right_index=True,
        )

    correlations_df = utils.return_df_with_selected_cols_from_df(
        correlations_df, # the input DF
        [
            "Sub ID",
            "Sub Health",
            "Sub Commitment",
            "Sub Perceptiveness",
            "Sub Dexterity",
            "Sub Sociality",
            "Sub Goodness",
            "Sub Strength",
            "Sub Openmindedness",
            "Sub Age",
            "Sup-Sub Age Difference",
            "Sub Same-Sex Colleagues Prtn",
            "Weekday Num",
            "BC Presence",
            "Actual Efficacy",
            "Recorded Efficacy",
            "BC Idea",
            "BC Lapse",
            "BC Feat",
            "BC Slip",
            "BC Teamwork",
            "BC Disruption",
            "BC Sacrifice",
            "BC Sabotage",
            "RCM True Positive",
            "RCM False Negative",
            ], # a list of columns to keep in the new DF
        )

    # Flatten the DF to only include one row for each person.
    correlations_df = correlations_df.groupby("Sub ID", as_index=False).agg(
        {
            "Sub Health": 'last',
            "Sub Commitment": 'last',
            "Sub Perceptiveness": 'last',
            "Sub Dexterity": 'last',
            "Sub Sociality": 'last',
            "Sub Goodness": 'last',
            "Sub Strength": 'last',
            "Sub Openmindedness": 'last',
            "Sub Age": 'last',
            "Sup-Sub Age Difference": 'mean',
            "Sub Same-Sex Colleagues Prtn": 'mean',
            "BC Presence": 'sum',
            "Actual Efficacy": 'mean',
            "Recorded Efficacy": 'mean',
            "BC Idea": 'sum',
            "BC Lapse": 'sum',
            "BC Feat": 'sum',
            "BC Slip": 'sum',
            "BC Teamwork": 'sum',
            "BC Disruption": 'sum',
            "BC Sacrifice": 'sum',
            "BC Sabotage": 'sum',
            "RCM True Positive": 'sum',
            "RCM False Negative": 'sum',
            }
        )

    # Delete the "Sub ID" column.
    correlations_df = utils.return_df_with_selected_cols_deleted(
        correlations_df, # the input DF
        ["Sub ID"], # a list of columns to delete from the DF
        )

    # It's important to convert all columns to a numerical type,
    # to keep Pandas from eliminating some of the (non-numerical)
    # columns.
    correlations_df = correlations_df.astype(float)
    correlations_df = correlations_df.corr()

    generate_simple_plot_return_PNG_and_save_to_file(
        "heatmap", # plot type ("column", "hist", "hist2d", "line", "scatter", "heatmap")
        correlations_df, # x-series of the data
        None, # y-series of the data (optional)
        None, # x-axis label
        None, # y-axis label (optional)
        90, # rotation of x-tick labels
        5.5, # custom xy-tick label fontsize
        None, # the main color for the data
        None, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Correlations between a single person’s total/mean elements\n(dataset for " + str(cfg.size_of_comm_initial) + " persons and " + str(cfg.num_of_days_to_simulate_for_analysis) + " days)", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "heatmap2.png" # name for PNG file
        )


def plot_resignations_by_day_bar():
    """
    Save to file and return a PNG bar plot of Resignation behaviors
    by day.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(df_to_plot["Behavior Comptype"], prefix = "BC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    df_to_plot = df_to_plot.groupby("Event Date", as_index=False).agg({"BC Resignation": 'sum'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Event Date"], # x-series of the data
        df_to_plot["BC Resignation"], # y-series of the data (optional)
        'Date', # x-axis label
        'Number of Resignation Events', # y-axis label (optional)
        90, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of Resignation events by date", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_resignations_by_date_bar.png" # name for PNG file
        )


def plot_terminations_by_day_bar():
    """
    Save to file and return a PNG bar plot of Termination records
    by day.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Record_Comptype = pd.get_dummies(df_to_plot["Record Comptype"], prefix = "RC", prefix_sep = " ")
    df_to_plot = pd.merge(
        left = df_to_plot,
        right = df_to_plot_OHE_Record_Comptype,
        left_index=True,
        right_index=True,
        )

    df_to_plot = df_to_plot.groupby("Event Date", as_index=False).agg({"RC Termination": 'sum'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Event Date"], # x-series of the data
        df_to_plot["RC Termination"], # y-series of the data (optional)
        'Date', # x-axis label
        'Number of Termination Events', # y-axis label (optional)
        90, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Number of Termination events by date", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_terminations_by_date_bar.png" # name for PNG file
        )


def plot_Eff_by_day_in_series_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by the day in the portion of the simulated series retained for analysis.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Day in Series (1-based)", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Day in Series (1-based)"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Day in Series', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by day in series", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_day_in_series_bar.png" # name for PNG file
        )


def plot_Eff_by_date_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by date.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Event Date", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Event Date"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Date', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        90, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by date", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_date.png" # name for PNG file
        )


def plot_Eff_by_week_in_series_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by week in the simulated series.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby("Week in Series", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Week in Series"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Date', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by week in the series", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_week_in_series.png" # name for PNG file
        )


def plot_Eff_by_month_of_year_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by month.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot["Month of Year"] = None
    for i in range(len(df_to_plot)):
        df_to_plot["Month of Year"].values[i] = pd.to_datetime( df_to_plot["Event Datetime"].values[i]).month

    df_to_plot = df_to_plot.groupby("Month of Year", as_index=False).agg({"Actual Efficacy": 'mean'})

    generate_simple_plot_return_PNG_and_save_to_file(
        "bar", # plot type ("column", "hist", "hist2d", "line", "scatter")
        df_to_plot["Month of Year"], # x-series of the data
        df_to_plot["Actual Efficacy"], # y-series of the data (optional)
        'Month of the Year', # x-axis label
        'Actual Efficacy', # y-axis label (optional)
        0, # rotation of x-tick labels
        None, # custom xy-tick label fontsize
        cfg.plot_bar_data_color, # the main color for the data
        1.0, # optional alpha value for the data
        None, # the color mapping for use in legend
        "Level of persons’ average actual Efficacy\n by month of the year", # title for the whole plot
        "lower left", # location for WFS logo (e.g., "upper right")
        "png_plt_Eff_by_month_of_year.png" # name for PNG file
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