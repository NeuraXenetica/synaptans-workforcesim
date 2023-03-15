# SYNAPTANS WORKFORCESIM

Synaptans WorkforceSim is a free, open-source, Python-based web app for simulating the complex dynamics of a factory workforce – including workers’ daily job performance, personal interactions with their peers and supervisors, and attrition. The simulated activity is analyzed visually and outputted in a CSV file. The outputted datasets’ format and contents have been designed for use in training machine-learning models to identify hidden trends and correlations in workers’ behavior and to facilitate objective assessments of the accuracy of differing approaches to predictive workplace analytics. Such datasets can be further analyzed using the open-source Comport_AI web app, a predictive analytics package for HR.

WorkforceSim utilizes FastAPI, Uvicorn, Jinja2, NumPy, Pandas, Matplotlib, Seaborn, and PIL. It is developed by Matthew E. Gladden (with support from Cognitive Firewall LLC and NeuraXenetica LLC) and is made available for use under GNU General Public License Version 3. Please see https://www.gnu.org/licenses/gpl-3.0.html.

![Plots exported from Synaptans WorkforceSim](https://github.com/NeuraXenetica/synaptans-workforcesim/blob/c17de568c551cc1b7c620c02918bba1f1189bb54/docs/assets/images/Synaptans_WorkforceSim_exported_plots_01.png)

___
## CONCEPTUAL OVERVIEW

The simulation’s logic operates at three levels:

- **LEVEL 1: WORKFORCE CONSTRUCTION.** Here the software constructs a simulated workforce of a desired size, whose members possess a randomly-distributed array of psychological and demographic characteristics and abilities that will influence their daily behavior and performance in the workplace.

- **LEVEL 2: WORKERS’ BEHAVIORS.** Here the software simulates the concrete actions performed by frontline factory workers each day (e.g., by determining the actual degree of efficacy with which each worker operates a production machine on a given day and determining exactly when workers cause workplace accidents or devise and implement business-process improvements).

- **LEVEL 3: MANAGERS’ RECORDS.** Here the software simulates the behavior of such workers’ immediate managers in noticing (or overlooking) and accurately (or inaccurately) recording workers’ actions in an HRM/ERP system that seeks to document workers’ performance. Managers do not have access to worker’ hidden, internal psychological characteristics; they can only attempt to observe and record workers’ externally visible behaviors.

The contents of Levels 2 and 3 are interrelated, with causal impacts flowing in both directions: managers don’t simply record their observations of workers’ behavior; the fact that a given manager has (or has not) accurately recorded the activities of his or her subordinates can have an encouraging or demoralizing impact that will affect what behaviors the employees will generate in the following days.

___
## CONSTITUENT MODULES

In addition to `__init__.py`, this Python package includes the following modules:

- `config.py` • This module stores configuration settings and constants and variables that are used by multiple modules.

- `io_file_manager.py` • This module handles the reading of files from disk (e.g., pickled files or PNG images) and the writing of files to disk (e.g., saving DataFrames as CSV files or Matplotlib plots as PNG images).

- `wfs_utilities.py` • This module includes general initialization functions that don’t relate to just a single level of the simulation’s logic, along with other general time-saving utility functions.

- `wfs_personnel.py` • This module handles the logic connected with creation of the members of the workforce and determining and determining of their (more or less) permanent personal characteristics.

- `wfs_behaviors.py` • This module handles the logic that simulates the *actual* behaviors performed by workers during each day of the simulated time period. These behaviors reflect the “reality” of the daily productivity and interpersonal interactions of workers in the factory.

- `wfs_records.py` • This module handles the logic that simulates frontline managers’ personal *observations* of workers’ daily behaviors and the *records* of such behaviors that they enter into their factory’s (simulated) HRM/ERP system. Of critical importance is the fact that those records *may* or *may not* accurately reflect workers’ actual behaviors: a manager who is overworked, inattentive, dishonest, or unskilled in use of the HRM/ERP system may fail to record some worker behaviors, may record behaviors that didn’t actually occur, or may record behaviors in a distorted manner.

- `wfs_visualizer.py` • This module handles visualization of the simulation’s results. It is capable of generating a range of histograms, bar plots, scatterplots, and heatmaps illustrating temporal trends and the relationships between particular variables.

- `wfs_executor.py` • This simple module runs the simulation, accepting the arguments provided by a user to (1) create a simulated workforce; (2) simulate workers’ daily activity for a specified number of days and quantity of workers; (3) generate the (potentially inaccurate) records of such workplace behaviors made by workers’ frontline managers; (4) employ AI in an attempt to discover trends and correlations in the records’ data and generate predictions; and then (5) assess the accuracy of those analyses and predictions by comparing them with what we know to be the case regarding workers’ actual past and expected future behaviors.

![Plots exported from Synaptans WorkforceSim](https://github.com/NeuraXenetica/synaptans-workforcesim/blob/c17de568c551cc1b7c620c02918bba1f1189bb54/docs/assets/images/Synaptans_WorkforceSim_exported_plots_02.png)

___
## STRUCTURE AND DYNAMICS OF THE SIMULATED WORKFORCE

### ORGANIZATIONAL ROLES

The simulated workforce comprises a group of employees organized into four hierarchical levels, as described below:

- **Production Director**. Regardless of how many employees it has, the simulated factory possesses a single Production Director who bears overall responsibility for all aspects of production operations. The Production Director has no supervisor (within the context of the simulation), no peers, and three direct subordinates (i.e., the Shift Managers). The Production Director can be understood as the employee situated at the “top” of the organizational hierarchy.

- **Shift Managers**. The simulated factory has three Shift Managers, each of whom oversees one of the factory’s successive daily shifts. Each Shift Manager reports directly to the Production Director, has the other two Shift Managers as peers, and serves as the supervisor of eight Team Leaders.

- **Team Leaders**. Each shift has eight Team Leaders, each of whom oversees a team of one or more Laborers. Each Team Leader reports directly to the Shift Manager of the relevant shift, has the other seven Team Leaders of the same shift as peers, and serves as the supervisor of one or more Laborers.

- **Laborers**. The factory has a variable number of specialized Laborers, with the exact number depending on input provided by a user. Each Laborer reports directly to the relevant Team Leader, does not supervise any other persons, and has a variable number of fellow team-member Laborers as peers (depending on the size of the workforce specified by the user).

### ASSIGNING RANDOMIZED PERSONAL CHARACTERISTICS

Each person in the simulated workforce possesses a number of characteristics that are generated by the simulator in a manner that is quasi-randomized, as guided by certain parameters established by the software’s user. (The way in which such characteristics are generated and their relationship to user-supplied arguments is explained in more detail later in this document.) We can divide such personal characteristics into “demographic traits” and “core stats,” as discussed below.

#### DEMOGRAPHIC TRAITS

- **ID** (`per_id`) is a person’s organizational employee ID number. Each member of the workforce has a unique ID.

- A person’s **first name** (`f_name`) and **last name** (`l_name`) are randomly selected from a list of possible names. It is possible for multiple persons in the factory to have the same full name (although their ID numbers will be unique).

- **Age** (`age`) is a person’s age in years at the start of the simulated time period; it is randomly generated to fall between the minimum and maximum ages specified by the user.

- **Sex** (`sex`) is a person’s sex; in this version of the software, a person is randomly assigned either “M” or “F” as a sex.

#### CORE STATS

A person’s core stats are numbers that reflect the degree to which the individual possesses or manifests particular abilities or behaviors. The value of each core stat is independently generated for each person in the simulated workforce. The values of these stats are randomly generated to fall between 0.0 and 1.0, using a mean value and standard deviation specified by the user. In general, core stats are constructed in such a way that a high value is “better” than a low value.

- **Health** (`health`) represents a person’s overall degree of physical hardiness, which influences his or her rate of attendance at work. In terms of the simulation, a Laborer with a low Health stat will generate more Absence behaviors (i.e., will be more frequently absent from the workplace).

- **Commitment** (`commitment`) reflects a person’s overall level of dedication to his or her job in the factory and the degree of thoroughness and effort that the person manifests in his or her daily work. In terms of the simulation, a Laborer with high Commitment will generate fewer Absence behaviors, more Sacrifice behaviors, fewer Sabotage behaviors, and a higher average daily Efficacy. 

- **Perceptiveness** (`perceptiveness`) reflects a person’s natural ability to notice details in the workplace, detect trends, draw connections, and identify possible solutions to problems. In terms of the simulation, a Laborer with high Perceptiveness will generate more Idea behaviors and fewer Lapse behaviors.

- **Dexterity** (`dexterity`) reflects a person’s natural ability to quickly and accurately perform manual tasks and to avoid physical errors or accidents. In terms of the simulation, a Laborer with high Dexterity will generate more Feat behaviors, fewer Slip behaviors, and a higher daily Efficacy.

- **Sociality** (`sociality`) reflects a person’s ability to successfully collaborate with, support, inspire, and mentor his or her coworkers. In terms of the simulation, a Laborer with high Sociality will generate more Teamwork behaviors and fewer Disruption behaviors.

- **Goodness** (`goodness`) reflects a person’s overall level of integrity and virtue, including the ability to deal constructively with adversity or disappointments in the workplace. In terms of the simulation, a Laborer with high Goodness will generate more Sacrifice behaviors and fewer Sabotage behaviors.

- **Strength** (`strength`) and **Open-mindedness** (`openmindedness`) are "control stats" that have no influence on any of a person’s behaviors and no relationship to any other stats or variables. They have been added to make it easier to assess the extent to which certain factors (e.g., a small workforce size or small number of days simulated) can give rise to apparent correlations between variables where no underlying causal connections exist.

#### RELATIONSHIP OF CORE STATS TO DAILY BEHAVIORS

As indicated above, various relationships exist between a Laborer’s personal characteristics and the behaviors that he or she performs daily in the workplace. For example, in general, a person with a high Dexterity and Commitment will demonstrate a higher average daily Efficacy than one with low Dexterity and Commitment. However, due to the randomizing elements introduced into the simulation, it is quite possible that on any given day, a person with low Dexterity and Commitment will generate a greater Efficacy behavior for that day than one with high Dexterity and Commitment.

### COMPOSITE CAPACITY SCORES

In addition to randomly generating the values of the “raw” core stats possessed by each person in the workforce, the simulator also calculates the values of certain composite capacity scores that present a more generalized, synthetic overview of some aspect of an employee’s potential.

- A person’s **“worker capacity score”** (`WRKR_CAP`) is a calculated score that attempts to capture his or her general long-term ability to successfully carry out routine frontline production work within the factory (e.g., operating some machine on an assembly line or transporting materials within the factory). It is a weighted average of a person’s Health, Commitment, Dexterity, Goodness, Perceptiveness, and Sociality stats, with more weight being given to a person’s Health and Commitment stats, which jointly influence a person’s rate of attendance in the workplace. (This reflects the fact that attendance is the most basic prerequisite for being able to carry out work: as noted above, if someone is not able to present in the workplace, then none of his or her other strengths or weaknesses will be relevant.) 

- A person’s **“managerial capacity score”** (`MNGR_CAP`) is a calculated score designed to reflect his or her general long-term ability to fill a managerial role (e.g., as Team Leader, Shift Manager, or Production Director) within the factory. It is a weighted average of a person’s Health, Commitment, Perceptiveness, and Goodness, stats, with more weight being given to a person’s Health and Commitment stats.

#### RELATIONSHIP OF WRKR_CAP AND MNGR_CAP SCORES

While, for example, manual dexterity is fairly important for a frontline factory worker, it isn’t so essential for a manager. Such distinctions are reflected in the manner in which the `WRKR_CAP` and `MNGR_CAP` scores are calculated: there is some overlap in constituent factors, but other stats contribute to only one of the two scores. It is thus possible for a person to have higher `WRKR_CAP` score than `MNGR_CAP` score, or vice versa. This reflects the real-world fact that the skills needed to successfully perform frontline work in a given organization may differ significantly from the skills needed to successfully oversee *other* persons who are performing such work. Someone who is an excellent frontline worker may or may not thrive when promoted into a managerial position, while someone who struggles in a frontline position might excel when asked to supervise others who are performing such work.

### ASSIGNING ROLES WITHIN THE ORGANIZATION

The simulated factory is designed to model a real-world organization. In real-world competitive contexts, running a factory with hundreds or thousands of workers is an incredibly complex undertaking, and (in the absence of nepotism, corruption, incompetence, or neglect on the part of an organization’s board or directors), one may generally presume that the persons who have been assigned to senior management roles have been selected to bear such responsibility because they are well-trained, highly qualified, and have proven (and honed) their managerial abilities through years of experience. The software models this dynamic in the following manner:

- From among all persons in the pool of employees, the one individual with the highest `MNGR_CAP` score is algorithmically assigned to the role of Production Director.

- The individuals with the three next-highest `MNGR_CAP` scores are then algorithmically assigned to roles as the Shift Managers.

- All of the remaining individuals within the organization are randomly assigned to the role of either Team Leader or Laborer – without regard to their particular `MNGR_CAP` or `WRKR_CAP` scores. This reflects the fact that when new employees join a production company in an entry-level position, it is often not immediately apparent which individuals possess exactly which strengths and weaknesses, and which of them would thrive (or struggle) if they were promoted to the position of Team Leader. The persons assigned to serve as Team Leaders thus may or may not actually be the persons who are theoretically best-qualified to fill such roles.

___
## RUNNING THE SIMULATION

There are various ways of running the simulation, depending on how Python has been configured on one’s system. For example, presuming that one has successfully installed the workforcesim package (e.g., through `python -m pip install workforcesim`) and its dependencies, from within Windows PowerShell, one can open the workforcesim folder that contains the module files listed above and type: `uvicorn wfs_app:app` to launch the web app, which can then be accessed through a web browser at `http://127.0.0.1:8000/`.

It is possible for a user to configure a number of the the simulation’s parameters from within the web app’s interface.

___
### VIEWING THE RESULTS OF A SIMULATION

Once the program has calculated each worker’s actual behaviors (and each manager’s recording of behaviors) for all days of the period simulated, the web interface
will automatically reload to display a number of figures that visualize various aspects of the results. A CSV file containing raw data on all of the simulated
behaviors can be downloaded by clicking the green button at the bottom of the web app’s interface.

___
## DEVELOPMENT

Synaptans WorkforceSim™ is free open-source software developed by Matthew E. Gladden, with support from Cognitive Firewall LLC and NeuraXenetica LLC. 

The choice of the name “Synaptans” acknowledges the origins of some of the simulation’s underlying code in code written for a computer game in the “Utopian Confederation” game series, inspired by the seminal 16th-century philosophical text of St. Thomas More. In that game, “synaptans” is one of many ranks found within the administrative hierarchy of the Utopian Confederation, as it exists in the 22nd century.

Synaptans WorkforceSim code and documentation ©2021-2023 NeuraXenetica LLC