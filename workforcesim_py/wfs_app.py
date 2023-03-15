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
This module creates the FastAPI app and specifies the URL at which
the program's interface can be accessed in a user's web browser.
"""

import os

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Import other modules from this package.
import config as cfg
import wfs_executor as exec
import io_file_manager as iofm


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/datasets", StaticFiles(directory="datasets"), name="datasets")

# Set up the directory structure for input files, output files, etc.
iofm.specify_directory_structure()


@app.get('/', response_class=HTMLResponse)
def get_webpage(request: Request):
    """
    Loads the WorkforceSim interface as a webpage in the user's
    web browser.
    """

    # Delete any existing plots in the plots directory
    # that might remain from previous simulations.
    for file in os.listdir(cfg.PLOTS_DIR):
        os.remove(os.path.join(cfg.PLOTS_DIR, file))

    # Display the initial webpage so that the user can provide input.
    # Pass the default values for variables to be updated by the user 
    # in the form.
    return templates.TemplateResponse(
        'wfs_interface.html',
        {
            "request": request,
            "visualization_data_source_to_display": \
                cfg.visualization_data_source,
            "SIM_STARTING_DATE_to_display": cfg.SIM_STARTING_DATE,
            "SIM_STARTING_DATE_FOR_ANALYSIS_to_display": \
                cfg.SIM_STARTING_DATE_FOR_ANALYSIS,
            "NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS_to_display": \
                cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS,
            "NUM_OF_LABORERS_PER_TEAM_to_display": \
                cfg.NUM_OF_LABORERS_PER_TEAM,
            "OTHER_STATS_STAT_MEAN_to_display": cfg.OTHER_STATS_STAT_MEAN,
            "OTHER_STATS_STAT_SDEV_to_display": cfg.OTHER_STATS_STAT_SDEV,
            "RANDOM_SEED_A_to_display": cfg.RANDOM_SEED_A,
            "BASE_RATE_ATTENDANCE_to_display": cfg.BASE_RATE_ATTENDANCE,
            "BASE_RATE_EFFICACY_to_display": cfg.BASE_RATE_EFFICACY,
            "BASE_MAX_EFFICACY_VARIABILITY_to_display": \
                cfg.BASE_MAX_EFFICACY_VARIABILITY,
            "BASE_RATE_RECORDING_ACCURACY_to_display": \
                cfg.BASE_RATE_RECORDING_ACCURACY,
            "plots_to_display_list": [],
            "dataset_csv_for_download_url_to_display": None,
            }
        )


@app.post('/', response_class=HTMLResponse)
def post_webpage(
    request: Request,
    visualization_data_source_from_form: str = Form(...),
    SIM_STARTING_DATE_from_form: str = Form(...),
    SIM_STARTING_DATE_FOR_ANALYSIS_from_form: str = Form(...),
    NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS_from_form: int = Form(...),
    NUM_OF_LABORERS_PER_TEAM_from_form: int = Form(...),
    OTHER_STATS_STAT_MEAN_from_form: float = Form(...),
    OTHER_STATS_STAT_SDEV_from_form: float = Form(...),
    RANDOM_SEED_A_from_form: int = Form(...),
    BASE_RATE_ATTENDANCE_from_form: float = Form(...),
    BASE_RATE_EFFICACY_from_form: float = Form(...),
    BASE_MAX_EFFICACY_VARIABILITY_from_form: float = Form(...),
    BASE_RATE_RECORDING_ACCURACY_from_form: float = Form(...),
    ):
    """
    Sends the form data inputted by the user in the webpage to be
    processed and generated an updated webpage with visualizations
    and a link to download the CSV file with the raw simulation data.
    """

    # Delete any plots in the plots directory
    # that might remain from previous simulations.
    for file in os.listdir(cfg.PLOTS_DIR):
        os.remove(os.path.join(cfg.PLOTS_DIR, file))

    # Delete any user-generated datasets in the datasets/user_generated
    # directory that might remain from previous simulations.
    for file in os.listdir(os.path.join(cfg.DATASETS_DIR, "user_generated")):
        os.remove(os.path.join(cfg.DATASETS_DIR, "user_generated", file))

    # Reset selected variables to their factory-original state.
    cfg.persons = {}
    cfg.persons_df = None
    cfg.roles = {}
    cfg.shifts = {}
    cfg.teams = {}
    cfg.num_of_leaders_needed = []
    cfg.spheres = {}
    cfg.sphere_of_given_team = []
    cfg.SIZE_OF_COMM_INITIAL = 0
    cfg.behavs_act_df = None
    cfg.pers_day_df = None
    cfg.behavs_act_df_w_priming_period = None
    cfg.list_of_behavs_to_add_to_behavs_act_df = []
    cfg.plots_to_display_list = []

    # Update variables stored in config.py with the 
    # user-provided values received through the form.
    cfg.visualization_data_source = visualization_data_source_from_form
    cfg.SIM_STARTING_DATE = SIM_STARTING_DATE_from_form
    cfg.SIM_STARTING_DATE_FOR_ANALYSIS = \
        SIM_STARTING_DATE_FOR_ANALYSIS_from_form
    cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS = \
        NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS_from_form
    cfg.NUM_OF_LABORERS_PER_TEAM = NUM_OF_LABORERS_PER_TEAM_from_form
    cfg.OTHER_STATS_STAT_MEAN = OTHER_STATS_STAT_MEAN_from_form
    cfg.OTHER_STATS_STAT_SDEV = OTHER_STATS_STAT_SDEV_from_form
    cfg.RANDOM_SEED_A = RANDOM_SEED_A_from_form
    cfg.BASE_RATE_ATTENDANCE = BASE_RATE_ATTENDANCE_from_form
    cfg.BASE_RATE_EFFICACY = BASE_RATE_EFFICACY_from_form
    cfg.BASE_MAX_EFFICACY_VARIABILITY = \
        BASE_MAX_EFFICACY_VARIABILITY_from_form
    cfg.BASE_RATE_RECORDING_ACCURACY = BASE_RATE_RECORDING_ACCURACY_from_form

    print("cfg.visualization_data_source: ", cfg.visualization_data_source)
    if cfg.visualization_data_source == "newly_generated_dataset":
        exec.run_simulation_from_scratch_using_config_settings()

    elif cfg.visualization_data_source == "stored_dataset":
        exec.load_saved_dataset_from_previous_simulation_run()
        iofm.save_wfs_behaviors_records_df_as_csv_or_pickle_for_distribution(
            "CSV"
            )

    cfg.plots_to_display_list = os.listdir(cfg.PLOTS_DIR)
    print("plots_to_display_list: ", cfg.plots_to_display_list)

    return templates.TemplateResponse(
        'wfs_interface.html',
        {
            "request": request,
            "visualization_data_source_to_display": \
                cfg.visualization_data_source,
            "SIM_STARTING_DATE_to_display": cfg.SIM_STARTING_DATE,
            "SIM_STARTING_DATE_FOR_ANALYSIS_to_display": \
                cfg.SIM_STARTING_DATE_FOR_ANALYSIS,
            "NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS_to_display": \
                cfg.NUM_OF_DAYS_TO_SIMULATE_FOR_ANALYSIS,
            "NUM_OF_LABORERS_PER_TEAM_to_display": \
                cfg.NUM_OF_LABORERS_PER_TEAM,
            "OTHER_STATS_STAT_MEAN_to_display": cfg.OTHER_STATS_STAT_MEAN,
            "OTHER_STATS_STAT_SDEV_to_display": cfg.OTHER_STATS_STAT_SDEV,
            "RANDOM_SEED_A_to_display": cfg.RANDOM_SEED_A,
            "BASE_RATE_ATTENDANCE_to_display": cfg.BASE_RATE_ATTENDANCE,
            "BASE_RATE_EFFICACY_to_display": cfg.BASE_RATE_EFFICACY,
            "BASE_MAX_EFFICACY_VARIABILITY_to_display": \
                cfg.BASE_MAX_EFFICACY_VARIABILITY,
            "BASE_RATE_RECORDING_ACCURACY_to_display": \
                cfg.BASE_RATE_RECORDING_ACCURACY,
            "plots_to_display_list": cfg.plots_to_display_list,
            "dataset_csv_for_download_url_to_display": \
                cfg.dataset_csv_for_download_url
            }
        )


# Run the app using uvicorn.
if __name__ == '__main__':
    uvicorn.run("wfs_app:app", reload=True)


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