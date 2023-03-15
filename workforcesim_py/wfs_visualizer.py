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
This module handles visualization of the simulation’s results. It is
capable of generating a range of histograms, bar plots, scatterplots, 
and heatmaps illustrating temporal trends and the relationships 
between particular variables.
"""

import io
import os
import colorsys
import warnings

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
from PIL import Image
from PIL import ImageColor
import pandas as pd

# Import other modules from this package.
import config as cfg
import wfs_utilities as utils


def generate_plot_return_png_and_save_to_file(
    plot_type_u,
    data_x_u,
    data_y_u,
    x_axis_label_u,
    y_axis_label_u,
    x_tick_labels_rotation_u,
    xy_tick_labels_custom_fontsize_u,
    data_color_main_u,
    data_alpha_main_u,
    color_mapping_for_legend_u,
    plot_title_u,
    wfs_logo_location_u,
    name_for_file_u
    ):
    """
    This is the most generalized plotting function, which is capable of 
    generating plots of various types. It will be called by higher-order
    functions that use it to generate one particular type of plot.

    PARAMETERS
    ----------
    plot_type_u : str
        The type of plot to be generated ("column", "hist", "hist2d",
        "line", "scatter", "heatmap")
    data_x_u
        The x-series of the data
    data_y_u
        The y-series of the data (optional for some plot types)
    x_axis_label_u
        The x-axis label
    y_axis_label_u
        The y-axis label (optional for some plot types)
    x_tick_labels_rotation_u
        Rotation of the x-tick labels
    xy_tick_labels_custom_fontsize_u
        Any custom xy-tick label fontsize
    data_color_main_u
        The main color for use in displaying the data
    data_alpha_main_u
        An optional alpha value for the data
    color_mapping_for_legend_u
        The color mapping for use in the legend
    plot_title_u : str
        The title for the whole plot
    wfs_logo_location_u : str
        The desired location where the WorkforceSim logo should appear
        in the plot (e.g., "upper right")
    name_for_file_u
        The desired name for the PNG file to be saved
    """

    # ------------------------------------------------------------------
    # Create the empty figure where data will be plotted.
    # ------------------------------------------------------------------

    # This uses a non-interactive backend, which helps avoid errors
    # produced by the fact that Matplotlib isn't thread-safe and plots 
    # are being generated outside of the main thread.
    matplotlib.use('agg')

    plt.rcParams['figure.dpi'] = cfg.PLOT_FIGURE_DPI
    plt.rcParams['savefig.dpi'] = cfg.PLOT_SAVEFIG_DPI

    # Seaborn heatmaps are square.
    if plot_type_u == "heatmap":
        fig = plt.figure(figsize=(
            cfg.PLOT_FIGSIZE[0]*1.0, cfg.PLOT_FIGSIZE[0]*0.9
            ))

    # Plots of predicted and actual values are square.
    elif (plot_type_u == "model_cont_val_preds_scatter") \
            or (plot_type_u == "model_cont_val_preds_scatter"):
        fig = plt.figure(figsize=(
            cfg.PLOT_FIGSIZE[0]*1.0,cfg.PLOT_FIGSIZE[0]*0.9
            ))

    # All remaining plots have a landscape-orientation rectangular size.
    else:
        fig = plt.figure(figsize=cfg.PLOT_FIGSIZE)

    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
    fig.patch.set_facecolor(cfg.PLOT_COLOR_DARK_PLUM)
    ax.patch.set_facecolor(cfg.PLOT_COLOR_BLACK)

    # ------------------------------------------------------------------
    # Plot the data using a particular plot type.
    # ------------------------------------------------------------------

    # A chart with simple vertical columns (i.e., a rotated bar plot).
    if plot_type_u == "bar":
        ax.bar(
            data_x_u,
            data_y_u,
            alpha=data_alpha_main_u,
            color=data_color_main_u,
            linewidth=0,
            )

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
            bins=[12,5],
            )

    # A line graph (a generic "plot", in Matplotlib terms).
    elif plot_type_u == "line":
        ax.plot(
            data_x_u,
            data_y_u,
            color=data_color_main_u,
            linewidth=cfg.PLOT_LINE_DATA_WIDTH,
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
            class_colors = list(color_mapping_for_legend_u.values())
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
                fontsize=cfg.PLOT_XY_TICKS_FONTSIZE,
                facecolor=cfg.PLOT_COLOR_DARK_PLUM, # darkest plum
                labelcolor="white",
                )

    # A heatmap.
    elif plot_type_u == "heatmap":

        # Note! Importing Seaborn seems to overwrite the already 
        # configured Matplotlib settings and disrupt elements of the 
        # other (non-Seaborn) Matplotlib graphs. Such heatmaps should
        # thus be generated as the final plots.
        import seaborn as sns

        color_rgb = ImageColor.getcolor(cfg.PLOT_COLOR_GOLD, "RGB")

        # The color doesn't work correctly, as colorsys generates an HLS
        # color, but Seaborn interprets it as an HULS color.
        color_hls = colorsys.rgb_to_hls(
            color_rgb[0], color_rgb[1], color_rgb[2]
            )

        # By default, Seaborn heatmaps -1.0 and +1.0 colors using 
        # opposite ends of the colormap; however, it's possible to set 
        # it to use the absolute value of numbers when selecting colors 
        # (so that correlations of -1.0 and +1.0 will have the same 
        # color and 0.0 will be the color at the opposite end of the 
        # spectrum).
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

        # These lines may or may not be necessary.
        plt.grid(visible=None)
        ax.grid(False)

        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(
            labelsize=cfg.PLOT_XY_LABEL_FONTSIZE,
            color=cfg.PLOT_COLOR_LAVENDER,
            labelcolor=cfg.PLOT_COLOR_LAVENDER,
            )

    # A specialized scatterplot for displaying predicted versus 
    # actual values.
    elif plot_type_u == "model_cont_val_preds_scatter":
        ax.scatter(
            data_x_u,
            data_y_u,
            alpha=data_alpha_main_u,
            color=data_color_main_u,
            s=0.15,
            zorder=3,
            )

        # For this type of plot, override the background color 
        # that has already been set.
        ax.patch.set_facecolor("white")

        ax.set_aspect("equal")

        # Set both x and y max values to the largest x or y value.
        xy_max_value = max(
            max(cfg.y_preds_target_curr),
            cfg.y_valid_slctd_df.iloc[:,0].max()
            )
        ax.set_xlim(0.0, xy_max_value)
        ax.set_ylim(0.0, xy_max_value)

        # These values may be overriden elsewhere.
        ax.set_xlabel("Predicted values")
        ax.set_ylabel("Actual values")

        # A diagonal line between the lower left and upper right 
        # corners.
        ax.plot(
            [0.03,0.97],
            [0.03,0.97],
            transform=ax.transAxes,
            color="#fc8293",
            linewidth=0.05,
            linestyle="dashed",
            zorder=2,
            )

        # A diagonal line raised by 0.1 and the corresponding area 
        # shaded above it.
        ax.plot(
            [0.0, xy_max_value-0.1],
            [0.1, xy_max_value],
            alpha=0.4,
            color="#ff00ff",
            linewidth=0.3,
            zorder=4,
            )
        plt.fill_between(
            [0.0, xy_max_value-0.1],
            [0.1, xy_max_value],
            xy_max_value,
            alpha=0.05,
            color="#34343C",
            zorder=1,
            )

        # A diagonal line lowered by 0.1 and the corresponding area 
        # shaded beneath it.
        ax.plot(
            [0.1, xy_max_value],
            [0.0, xy_max_value-0.1],
            alpha=0.4,
            color="#ff00ff",
            linewidth=0.3,
            zorder=4,
            )
        plt.fill_between(
            [0.1, xy_max_value],
            0.0,
            [0.0, xy_max_value-0.1],
            alpha=0.05,
            color="#34343C",
            zorder=1,
            )

        # Add a legend -- but only if something other than None
        # was passed as the value of color_mapping_for_legend_u.
        if color_mapping_for_legend_u is not None:

            classes = list(color_mapping_for_legend_u.keys())
            class_colors = list(color_mapping_for_legend_u.values())
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
                fontsize=cfg.PLOT_XY_TICKS_FONTSIZE,
                facecolor=cfg.PLOT_COLOR_DARK_PLUM,
                labelcolor="white",
                )

    # A specialized scatterplot for displaying model results
    # in the form of a continuous value with likely floor-ceiling range.
    elif plot_type_u == "model_cont_val_with_range_preds_scatter":
        ax.scatter(
            data_x_u,
            data_y_u,
            alpha=data_alpha_main_u,
            color=data_color_main_u,
            s=0.5,
            zorder=3,
            marker="o",
            )

        # For this type of plot, override the background color 
        # that has already been set.
        ax.patch.set_facecolor("white")

        # Set both x and y max values to the largest x or y value.
        x_max_value = max(data_x_u)
        y_max_value = max( max(data_y_u), abs(min(data_y_u)) )

        ax.set_xlim(0.0, None)
        ax.set_ylim( -y_max_value, y_max_value )

        # These values may be overriden elsewhere.
        ax.set_xlabel("Predicted values")
        ax.set_ylabel("Actual values")

        # A horizontal line at y = 0.0.
        ax.plot(
            [0.0, x_max_value],
            [0.0, 0.0],
            color="#fc8293",
            linewidth=0.05,
            linestyle="dashed",
            zorder=2,
            )

        # A diagonal upward line and the corresponding area shaded 
        # above it.
        ax.plot(
            [0.0, y_max_value],
            [0.0, y_max_value],
            alpha=0.4,
            color="#ff00ff",
            linewidth=0.3,
            #linestyle="dashed",
            zorder=4,
            )
        plt.fill_between(
            [0.0, y_max_value],
            [0.0, y_max_value],
            y_max_value,
            alpha=0.05,
            color="#34343C",
            zorder=1,
            )

        # A diagonal downward line and the corresponding area 
        # shaded below it.
        ax.plot(
            [0.0, y_max_value],
            [0.0, -y_max_value],
            alpha=0.4,
            color="#ff00ff",
            linewidth=0.3,
            #linestyle="dashed",
            zorder=4,
            )
        plt.fill_between(
            [0.0, y_max_value],
            [0.0, -y_max_value],
            -y_max_value,
            alpha=0.05,
            color="#34343C",
            zorder=1,
            )

        # Add a legend -- but only if something other than None
        # was passed as the value of color_mapping_for_legend_u.
        if color_mapping_for_legend_u is not None:

            classes = list(color_mapping_for_legend_u.keys())
            class_colors = list(color_mapping_for_legend_u.values())
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
                fontsize=cfg.PLOT_XY_TICKS_FONTSIZE,
                facecolor=cfg.PLOT_COLOR_DARK_PLUM,
                labelcolor="white",
                )

    # ---------------------------------------------------------------------
    # Add supplemental plot elements that are common to (almost) 
    # all plot types.
    # ---------------------------------------------------------------------
    if xy_tick_labels_custom_fontsize_u is None:
        plot_xy_tick_label_fontsize_to_use = cfg.PLOT_XY_TICKS_FONTSIZE
    else:
        plot_xy_tick_label_fontsize_to_use = xy_tick_labels_custom_fontsize_u

    plt.xlabel(
        x_axis_label_u,
        fontsize=cfg.PLOT_XY_LABEL_FONTSIZE,
        labelpad=cfg.PLOT_XY_LABEL_PAD,
        color=cfg.PLOT_COLOR_LAVENDER,
        )
    plt.ylabel(
        y_axis_label_u,
        fontsize=cfg.PLOT_XY_LABEL_FONTSIZE,
        labelpad=cfg.PLOT_XY_LABEL_PAD,
        color=cfg.PLOT_COLOR_LAVENDER,
        )
    plt.xticks(
        fontsize=plot_xy_tick_label_fontsize_to_use,
        color=cfg.PLOT_COLOR_SALMON,
        rotation = x_tick_labels_rotation_u,
        )
    plt.yticks(
        fontsize=plot_xy_tick_label_fontsize_to_use,
        color=cfg.PLOT_COLOR_SALMON,
        )
    plt.title(
        plot_title_u,
        fontsize=cfg.PLOT_TITLE_FONTSIZE,
        color=cfg.PLOT_COLOR_CYAN,
        )

    plt.grid(visible=None)
    ax.grid(False)
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)

    # Add a WorkforceSim logo.
    if wfs_logo_location_u is not None:
        logo_path_and_name = os.path.join(
            cfg.GRAPHICS_DIR,
            "WorkforceSim_logo_02_1120-B_02.png"
            )
        im = plt.imread(logo_path_and_name)
        imagebox = OffsetImage(im, zoom=0.018)
        ab = AnchoredOffsetbox(
            loc=wfs_logo_location_u,
            child=imagebox,
            frameon=False
            )
        logo_ax = fig.add_axes([0,0,1,1])
        logo_ax.grid(False)
        logo_ax.spines[
            ['top', 'bottom', 'left', 'right']
            ].set_visible(False)
        logo_ax.set(xticklabels=[])
        logo_ax.set(yticklabels=[])
        logo_ax.tick_params(left=False, bottom=False)
        plt.gca().set_position([0,0,1,1])
        logo_ax.set_facecolor('none')
        logo_ax.add_artist(ab)

    warnings.filterwarnings(
        "ignore", 
        message="This figure includes Axes that are not compatible with " \
            + "tight_layout, so results might be incorrect.")

    # This is needed to prevent x- and y-tick labels from sometimes 
    # being cut off.
    fig.tight_layout()

    # ------------------------------------------------------------------
    # Save the plot to a PNG file and return the plot as a variable.
    # ------------------------------------------------------------------

    # Read the plot image data into the buffer.
    buffer_m = io.BytesIO()
    plt.savefig(
        buffer_m, format='png',
        facecolor=fig.get_facecolor(),
        edgecolor='none'
        )
    buffer_m.seek(0)
    generated_PNG_plot_as_var = Image.open(buffer_m)

    # Save the plot as a PNG.
    plt.savefig(
        os.path.join(
            cfg.PLOTS_DIR,
            name_for_file_u,
            ),
        bbox_inches='tight',
        facecolor=fig.get_facecolor(),
        edgecolor='none',
        )

    return generated_PNG_plot_as_var


# ----------------------------------------------------------------------
# Below are the more particular functions for generating specific
# types of plots, each of which calls the the generalized plotting 
# function generate_plot_return_png_and_save_to_file, while passing to 
# it arguments specific to its particular type of plot.
# ----------------------------------------------------------------------

def plot_distribution_of_MNGR_CAP_scores_hist():
    """
    Save to file and return a PNG histogram plot of MNGR_CAP scores.
    """
    # Prepare the data.
    df_to_plot = cfg.persons_df.copy()

    generate_plot_return_png_and_save_to_file(
        "hist",
        df_to_plot["MNGR_CAP"],
        None,
        'MNGR_CAP score range',
        'Number of persons\n in given MNGR_CAP score range',
        0,
        None,
        cfg.PLOT_COLOR_MAGENTA,
        None,
        None,
        "Distribution of values of persons'\n managerial capacity (MNGR_CAP) score",
        "lower right",
        "png_plt_distribution_of_MNGR_CAP_scores_hist.png"
        )


def plot_Eff_by_weekday_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores by 
    weekday.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby(
        "Weekday Num", as_index=False).agg({"Actual Efficacy": 'mean'}
        )
    generate_plot_return_png_and_save_to_file(
        "bar",
        df_to_plot["Weekday Num"],
        df_to_plot["Actual Efficacy"],
        'Weekday',
        'Actual Efficacy',
        0,
        None,
        cfg.PLOT_COLOR_GOLD,
        1.0,
        None,
        "Level of persons’ average actual Efficacy\n by weekday",
        "lower left",
        "png_plt_Eff_by_weekday_bar.png"
        )


def plot_recorded_Eff_by_sub_sup_age_difference_line():
    """
    Save to file and return a PNG line plot of (1) the difference in 
    ages between a subject and his supervisor and (2) the subject's mean
    Recorded Efficacy.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby(
        "Sup-Sub Age Difference", as_index=False).agg({"Recorded Efficacy": 'mean'}
        )
    generate_plot_return_png_and_save_to_file(
        "line",
        df_to_plot["Sup-Sub Age Difference"],
        df_to_plot["Recorded Efficacy"],
        'Subject-supervisor age difference',
        'Recorded Efficacy',
        0,
        None,
        cfg.PLOT_COLOR_CYAN,
        None,
        None,
        "Level of persons’ average recorded Efficacy\n by subject-supervisor age difference",
        "lower right",
        "png_plt_sub_sup_age_diff_vs_recorded_eff_line.png"
        )


def plot_Eff_mean_vs_Eff_sd_with_workstyles_scatter():
    """
    Save to file and return a PNG scatter plot of the mean and SD of 
    subjects' Actual Efficacy scores, colored by a subject's Workstyle 
    group.
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
        "Group A": cfg.PLOT_COLOR_GREEN,
        "Group B": cfg.PLOT_COLOR_MAGENTA,
        "Group C": cfg.PLOT_COLOR_LAVENDER,
        "Group D": "#FF534F", # red
        "Group E": "#FFFD27", # yellow
        }
    generate_plot_return_png_and_save_to_file(
        "scatter",
        df_to_plot["Actual Efficacy"],
        df_to_plot["Actual Efficacy (SD)"],
        'Actual Efficacy (mean)',
        'Actual Efficacy (standard deviation)',
        0,
        None,
        df_to_plot["Sub Workstyle"].map(colors),
        0.5,
        colors,
        "Persons’ mean Efficacy versus the SD of their actual " \
            + "daily Efficacy colored by Workstyle group",
        "lower left",
        "png_plt_Eff_mean_vs_Eff_sd_with_workstyle_group_bar.png"
        )


def plot_mday_series_Eff_for_behav_comptype_bar(
    d0_event_col_name_u,
    d0_event_name_u,
    data_color_u,
    ):
    """
    Save to file and return a PNG bar plot showing the mean Actual 
    Efficacy behaviors for subjects on the days before and after a 
    certain type of actual behavior (i.e., an mday series).

    PARAMETERS
    ----------
    d0_event_col_name_u : str
        Name of the column (e.g., "Behavior Type", "Record Conf Mat") in
        which the D0 event is noted
    d0_event_name_u : str
        Name of the D0 event type (e.g., "Good", "False Negative")
    data_color_u
        Desired color for the bars
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    # Extract only those rows containing the selected Behavior Type
    # or Behavior Comptype.
    df_to_plot \
        = df_to_plot[df_to_plot[d0_event_col_name_u] == d0_event_name_u]

    # Flatten the DataFrame to only include a row for its mean values.
    df_to_plot \
        = df_to_plot.groupby(d0_event_col_name_u, as_index=False).agg(
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

    # Extract only those columns containing the mday series Actual 
    # Efficacy values.
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

    # Specify as Y values for the plot the contents of the lone row of 
    # the DF (i.e., the mean Actual Efficacy values for each day in the 
    # mday series).
    data_y = df_to_plot.loc[0, :].values.tolist()

    generate_plot_return_png_and_save_to_file(
        "bar",
        data_x,
        data_y,
        "Day relative to analyzed D0 event",
        'Actual Efficacy',
        0,
        None,
        data_color_u,
        1.0,
        None,
        "Persons’ average actual Efficacy on days before and after D0 event '" \
            + d0_event_col_name_u + ": " + d0_event_name_u + "'",
        "lower right",
        "png_plt_mday_series_Eff_for_" \
            + d0_event_col_name_u + "_" + d0_event_name_u + ".png"
        )


def plot_ideas_mean_by_workstyle_group_bar():
    """
    Save to file and return a PNG bar plot of the mean number of
    Ideas per subject, by subjects' Workstyle group membership.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()

    df_to_plot_OHE_Behavior_Comptype = pd.get_dummies(
        df_to_plot["Behavior Comptype"],
        prefix = "BC",
        prefix_sep = " "
        )
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
    df_to_plot = df_to_plot.groupby(
        "Sub Workstyle", as_index=False).agg({"BC Idea": 'mean'}
        )

    generate_plot_return_png_and_save_to_file(
        "bar",
        df_to_plot["Sub Workstyle"],
        df_to_plot["BC Idea"],
        'Sub Workstyle',
        'Mean number of Ideas per person in Workstyle group',
        0,
        None,
        cfg.PLOT_COLOR_LAVENDER,
        1.0,
        None,
        "Mean number of Idea behaviors per person by Workstyle group",
        "lower right",
        "png_plt_ideas_mean_by_workstyle_group_bar.png"
        )


def generate_event_row_internal_correlations_heatmap():
    """
    Save to file and return a PNG with a heatmap showing correlations of
    certain variables that all appear on the *same row* of behavs_act_df
    (i.e., that are all recorded as part of a single behavior-record 
    event).

    This treats each *behavior-record* event row (not each subject) as 
    the fundamental data-point to be compared with others.

    Note: this uses Seaborn, whose import disrupts existing Matplotlib 
    settings. This function should only be run after all desired 
    (non-Seaborn) Matplotlib plots have been created.
    """

    # Prepare the data.
    correlations_df = utils.return_df_with_selected_cols_from_df(
        cfg.behavs_act_df,
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
            ],
        )

    # It's important to convert all columns to a numerical type, to keep
    # Pandas from eliminating some of the (non-numerical) columns.
    correlations_df = correlations_df.astype(float)
    correlations_df = correlations_df.corr()

    generate_plot_return_png_and_save_to_file(
        "heatmap",
        correlations_df,
        None,
        None,
        None,
        90,
        7.5,
        None,
        None,
        None,
        "Correlations between elements within a single behavior-record " \
            + "event\n(dataset for " + str(cfg.SIZE_OF_COMM_INITIAL) \
            + " persons and " \
            + str(cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS) + " days)",
        "lower left",
        "heatmap1.png"
        )


def generate_interpersonal_correlations_heatmap():
    """
    Save to file and return a PNG with a heatmap showing correlations 
    between different subjects' stats and events (e.g., between the 
    number of Lapses and average Efficacy).

    This treats each *subject* (not each *behavior-record* event row) as
    the fundamental data-point to be compared with others.

    Note: this uses Seaborn, whose import disrupts existing Matplotlib 
    settings. This function should only be run after all desired 
    (non-Seaborn) Matplotlib plots have been created.
    """

    # Prepare the data.
    correlations_df = cfg.behavs_act_df.copy()

    correlations_df_OHE_Behavior_Comptype = \
        pd.get_dummies(correlations_df["Behavior Comptype"].astype(
            pd.CategoricalDtype(categories=[
                "Presence",
                "Idea",
                "Lapse",
                "Feat",
                "Slip",
                "Teamwork",
                "Disruption",
                "Sacrifice",
                "Sabotage"
                ])),
            prefix = "BC",
            prefix_sep = " ",
        )

    correlations_df = pd.merge(
        left = correlations_df,
        right = correlations_df_OHE_Behavior_Comptype,
        left_index=True,
        right_index=True,
        )

    correlations_df_OHE_Record_Conf_Mat = \
        pd.get_dummies(
            correlations_df["Record Conf Mat"],
            prefix = "RCM",
            prefix_sep = " "
            )

    correlations_df = pd.merge(
        left = correlations_df,
        right = correlations_df_OHE_Record_Conf_Mat,
        left_index=True,
        right_index=True,
        )

    correlations_df = utils.return_df_with_selected_cols_from_df(
        correlations_df,
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
            ],
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
        correlations_df,
        ["Sub ID"],
        )

    # It's important to convert all columns to a numerical type, to keep
    # Pandas from eliminating some of the (non-numerical) columns.
    correlations_df = correlations_df.astype(float)
    correlations_df = correlations_df.corr()

    generate_plot_return_png_and_save_to_file(
        "heatmap",
        correlations_df,
        None,
        None,
        None,
        90,
        5.5,
        None,
        None,
        None,
        "Correlations between a single person’s " \
            + "total/mean elements\n(dataset for " \
            + str(cfg.SIZE_OF_COMM_INITIAL) + " persons and " \
                + str(cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS) + " days)",
        "lower left",
        "heatmap2.png"
        )


def plot_Eff_by_day_in_series_bar():
    """
    Save to file and return a PNG bar plot of Actual Efficacy scores
    by the day in the portion of the simulated series retained for analysis.
    """

    # Prepare the data.
    df_to_plot = cfg.behavs_act_df.copy()
    df_to_plot = df_to_plot.groupby(
        "Day in Series (1-based)", as_index=False
        ).agg({"Actual Efficacy": 'mean'})

    generate_plot_return_png_and_save_to_file(
        "bar",
        df_to_plot["Day in Series (1-based)"],
        df_to_plot["Actual Efficacy"],
        'Day in Series',
        'Actual Efficacy',
        0,
        None,
        cfg.PLOT_COLOR_GOLD,
        1.0,
        None,
        "Level of persons’ average actual Efficacy\n by day in series",
        "lower left",
        "png_plt_Eff_by_day_in_series_bar.png"
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