███████████████████████████████████████████████████████
OVERVIEW OF THE PACKAGE
███████████████████████████████████████████████████████

Synaptans WorkforceSim is a free open-source platform for simulating the dynamics of a factory workforce and assessing various AI-based approaches to predictive analytics in the workplace. The program exists as a Python package that allows users to configure the simulation’s parameters, run the simulation, and view an array of charts and graphs that visualize the results.

The software is developed by Matthew E. Gladden – with support from Cognitive Firewall LLC and NeuraXenetica LLC – and is made available for use under GNU General Public License Version 3 (please see https://www.gnu.org/licenses/gpl-3.0.html).

The simulation’s logic is intended to operate at four levels:

▶ LEVEL 0: “WORKFORCE CONSTRUCTION.” Here the software constructs a simulated workforce of a desired size, whose members possess a randomly-distributed array of demographic characteristics and abilities that will influence their daily behavior and performance in the workplace.

▶ LEVEL 1: “WORKERS’ BEHAVIORS.” Here the software simulates the concrete actions performed by frontline factory workers each day (e.g., by determining the actual degree of Efficacy with which each worker operates a production machine on a given day and determining exactly when workers cause workplace accidents or devise and implement business-process improvements).

▶ LEVEL 2: “MANAGERS’ RECORDS.” Here the software simulates the behavior of such workers’ immediate managers in noticing (or overlooking) and accurately (or inaccurately) recording workers’ actions in an HRM/ERP system that seeks to document workers’ performance.

▶ LEVEL 3: “AI-BASED ANALYSIS.” Here the software employs various forms of machine learning and AI to attempt to identify trends and causal connections, classify workers, and predict workers’ future behaviors on the basis of the information recorded by managers in the organization’s enterprise system at Level 2. Just as in a real workplace, the AI doesn’t have direct access to the sum of workers’ actual behaviors; it can only access, analyze, and draw conclusions on the basis of the data that have actually been recorded in an organization’s HRM/ERP systems – and depending on the degree of attentiveness, thoroughness, and fairness displayed by managers, such data may or may not accurately reflect the reality of workers’ actual behaviors.

▶ LEVEL 4: “ASSESSEMENT OF THE AI-BASED ANALYSIS.” In a real-world organization, it’s incredibly difficult to gauge the accuracy of AI-generated analysis of workers’ behaviors, as data scientists and senior executives have no access to what’s actually happening at Level 1; they only have access to the relatively tiny quantity of worker behaviors that are captured (often inaccurately) by information systems at Level 2. The utility of a workforce simulation like this one lies in the fact that we actually know the reality of each worker’s personality, capacities, and daily behaviors – because a user has specified (and is able to view) all workers’ characteristics (including attitudes, strengths, and weaknesses that are normally invisible in a workplace setting) and has algorithmically determined exactly what actions he or she performs each day. This makes it possible to compare AI-based analysis not only against the observations that managers recorded at Level 2 but against the actual behaviors performed by workers at Level 1 and the true capacities possessed by workers at Level 0. In this way, it becomes possible to evaluate which AI-based approaches can most accurately model workplace behaviors identify an organization’s best workers – and what degree of confidence can be placed in various forms of predictive analytics.

In the current version of the program, the code for Levels 0, 1, and 2 has been partially implemented and a development roadmap has been prepared for Levels 3-4.

███████████████████████████████████████████████████████
CONSTITUENT MODULES
███████████████████████████████████████████████████████

In addition to __init__.py, this Python package includes the following modules:

▶ config.py (imported as cfg) | This module stores configuration settings and variables that are used by multiple modules.

▶ io_file_manager.py (imported as iofm) | This module handles the reading of files from disk (e.g., XLSX files or PNG images); the writing of files to disk (e.g., saving DataFrames as XLSX files or Matplotlib plots as PNG images; and the saving of complex objects as file-like objects assigned to variables in memory (e.g., Matplotlib plots as in-memory PNGs for display in a GUI).

▶ wfs_utilities.py (imported as utils) | This module includes general initialization functions that don’t relate to just a single level of the simulation’s logic, along with other general time-saving utility functions.

▶ wfs_personnel.py (imported as pers) | This module handles the simulation’s “Level 0” logic, which involves the creation of the members of the workforce and determining and determining of their (more or less) permanent personal characteristics.

▶ wfs_behaviors.py (imported as bhv) | This module handles the simulation’s “Level 1” logic, which simulates the *actual* behaviors performed by workers during each day of the simulated time period. These behaviors reflect the “reality” of the daily productivity and interpersonal interactions of production workers in the factory.

▶ wfs_records.py (imported as rec) | This module handles the simulation’s “Level 2” logic, which simulates frontline managers’ personal *observations* of workers’ daily behaviors and the *records* of such behaviors that they enter into their factory’s (simulated) HRM/ERP system. Of critical importance is the fact that those records *may* or *may not* accurately reflect workers’ actual behaviors: a manager who is overworked, inattentive, dishonest, or unskilled in use of the HRM/ERP system may fail to record some worker behaviors, may record behaviors that didn’t actually occur, or may record behaviors in a distorted manner.

▶ wfs_ai (imported as ai) | This module handles the simulation’s “Level 3” logic, which uses various machine-learning techniques in an attempt to identify meaningful trends, causal relationships, and other correlations relating to workers’ personal characters and workplace behaviors and to attempt to predict workers’ future behavior – either absolutely or in response to particular changes that might be implemented in the workplace. In generating such analyses and predictions, the AI *does not* have access to workers’ actual personal characteristics or behaviors; rather, it only has access to the records made in the organization’s HRM/ERP system by its frontline managers – which may or may not reflect workers’ actual characteristics and behaviors in a fully accurate manner.

▶ wfs_evaluator (imported as eval) | This module handles the simulation’s “Level 4” logic, which evaluates the accuracy and business value of the analyses and predictions made by various machine-learning techniques at Level 3 by comparing them to workers’ *actual* characteristics and behaviors (generated at Levels 0 and 1). This makes it possible to assess, for example, (1) what types of information regarding workers’ behaviors must be recorded, with what frequency, and for how large a workforce in order for the data present in the HRM/ERP system to allow machine learning algorithms to accurately predict future worker behaviors; (2) how much variation (e.g., in perceptiveness, objectivity, and completeness) can exist between individual managers’ approches to recording workers’ behaviors without undermining AI’s ability to detect certain trends and correlations or compromising the AI’s ability to accurately distinguish between the organization’s “more effective” and “less effective” workers; and (3) which forms of machine learning and AI are able to best predict workers’ future behaviors despite the “noise” produced by certain managers’ fragmentary, biased, or otherwise inaccurate manner of recording workers’ past behaviors in the HRM/ERP system.

▶ wfs_visualizer.py (imported as vis) | This module handles visualization of the simulation’s results. It is capable of generating a wide range of histograms, bar plots, scatterplots, and other plots illustrating temporal trends and the relationships between particular variables.

▶ wfs_executor.py | This simple module runs the simulation, accepting the arguments provided by a user to (1) create a simulated workforce; (2) simulate workers’ daily activity for a specified number of days and quantity of workers; (3) generate the (potentially inaccurate) records of such workplace behaviors made by workers’ frontline managers; (4) employ AI in an attempt to discover trends and correlations in the records’ data and generate predictions; and then (5) assess the accuracy of those analyses and predictions by comparing them with what we know to be the case regarding workers’ actual past and expected future behaviors.

███████████████████████████████████████████████████████
STRUCTURE AND DYNAMICS OF THE SIMULATED WORKFORCE
███████████████████████████████████████████████████████

●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
ORGANIZATIONAL ROLES
●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

The simulated workforce comprises a group of employees organized into four hierarchical levels, as described below:

▶ Production Director. Regardless of how many employees it has, the simulated factory possesses a single Production Director who bears overall responsibility for all aspects of production operations. The Production Director has no supervisor (within the context of the simulation), no peers, and three direct subordinates (i.e., the Shift Managers). The Production Director can be understood as the employee situated at the “top” of the organizational hierarchy.

▶ Shift Managers. The simulated factory has three Shift Managers, each of whom oversees one of the factory’s successive daily shifts. Each Shift Manager reports directly to the Production Director, has the other two Shift Managers as peers, and serves as the supervisor of eight Team Leaders.

▶ Team Leaders. Each shift has eight Team Leaders, each of whom oversees a team of one or more Laborers. Each Team Leader reports directly to the Shift Manager of the relevant shift, has the other seven Team Leaders of the same shift as peers, and serves as the supervisor of one or more Laborers.

▶ Laborers. The factory has a variable number of specialized Laborers, with the exact number depending on input provided by a user. Each Laborer reports directly to the relevant Team Leader, does not supervise any other persons, and has a variable number of fellow team-member Laborers as peers (depending on the size of the workforce specified by the user).

●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
ASSIGNING RANDOMIZED PERSONAL CHARACTERISTICS
●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

Each person in the simulated workforce possesses a number of characteristics that are generated by the simulator in a manner that is quasi-randomized, as guided by certain parameters established by the software’s user. (The way in which such characteristics are generated and their relationship to user-supplied arguments is explained in more detail later in this document.) We can divide such personal characteristics into “demographic traits” and “core stats,” as discussed below.

DEMOGRAPHIC TRAITS

▶ “ID” is a person’s organizational employee ID number. Each member of the workforce has a unique ID.

▶ A person’s “FIRST NAME” and “LAST NAME” are randomly selected from a list of possible names. It is possible for multiple persons in the factory to have the same full name (although their ID numbers will be unique).

▶ “AGE” is a person’s age in years at the start of the simulated time period; it is randomly generated to fall between the minimum and maximum ages specified by the user.

▶ “SEX” is a person’s sex; in this version of the software, a person is randomly assigned either “M” or “F” as a sex.

CORE STATS

A person’s core stats are numbers that reflect the degree to which the individual possesses or manifests particular abilities or behaviors. The value of each core stat is independently generated for each person in the simulated workforce. The values of these stats are randomly generated to fall between -1.0 and +1.0, using a mean value and standard deviation specified by the user. In general, core stats are constructed in such a way that a high value is “better” than a low value. (E.g., there is a stat for one’s rate of attendance, rather than one’s rate of absence.)

▶ “HEALTH” represents a person’s overall degree of physical hardiness, which influences his or her rate of attendance at work. In terms of the simulation, a Laborer with a low Health stat will generate more Absence behaviors (i.e., will be more frequently absent from the workplace).

▶ “COMMITMENT” reflects a person’s overall level of dedication to his or her job in the factory and the degree of thoroughness and effort that the person manifests in his or her daily work. In terms of the simulation, a Laborer with high Commitment will generate fewer Absence behaviors, more Sacrifice behaviors, fewer Sabotage behaviors, and a higher average daily Efficacy. 

▶ “PERCEPTIVENESS” reflects a person’s natural ability to notice details in the workplace, detect trends, draw connections, and identify possible solutions to problems. In terms of the simulation, a Laborer with high Perceptiveness will generate more Idea behaviors and fewer Lapse behaviors.

▶ “DEXTERITY” reflects a person’s natural ability to quickly and accurately perform manual tasks and to avoid physical errors or accidents. In terms of the simulation, a Laborer with high Dexterity will generate more Feat behaviors, fewer Slip behaviors, and a higher daily Efficacy.

▶ “SOCIALITY” reflects a person’s ability to successfully collaborate with, support, inspire, and mentor his or her coworkers. In terms of the simulation, a Laborer with high Sociality will generate more Teamwork behaviors and fewer Disruption behaviors

▶ “GOODNESS” reflects a person’s overall level of integrity and virtue, including the ability to deal constructively with adversity or disappointments in the workplace. In terms of the simulation, a Laborer with high Goodness will generate more Sacrifice behaviors and fewer Sabotage behaviors.

RELATIONSHIP OF CORE STATS TO DAILY BEHAVIORS

As indicated above, various relationships exist between a Laborer’s personal characteristics and the behaviors that he or she performs daily in the workplace. For example, in general, a person with a high Dexterity and Commitment will demonstrate a higher average daily Efficacy than one with low Dexterity and Commitment. However, due to the randomizing elements introduced into the simulation, it is quite possible that on any given day, a person with low Dexterity and Commitment will generate a greater Efficacy behavior for that day than one with high Dexterity and Commitment.

●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
COMPOSITE CAPACITY SCORES
●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

In addition to randomly generating the values of the “raw” core stats possessed by each person in the workforce, the simulator also calculates the values of certain composite capacity scores that present a more generalized, synthetic overview of some aspect of an employee’s potential.

▶ A person’s “worker capacity score” (WRKR_CAP) is a calculated score that attempts to capture his or her general long-term ability to successfully carry out routine frontline production work within the factory (e.g., operating some machine on an assembly line or transporting materials within the factory). It is a weighted average of a person’s Health, Commitment, Dexterity, Goodness, Perceptiveness, and Sociality stats, with more weight being given to a person’s Health and Commitment stats, which jointly influence a person’s rate of attendance in the workplace. (This reflects the fact that attendance is the most basic prerequisite for being able to carry out work: as noted above, if someone is not able to present in the workplace, then none of his or her other strengths or weaknesses will be relevant.) 

▶ A person’s “managerial capacity score” (MNGR_CAP) is a calculated score designed to reflect his or her general long-term ability to fill a managerial role (e.g., as Team Leader, Shift Manager, or Production Director) within the factory. It is a weighted average of a person’s Health, Commitment, Perceptiveness, and Goodness, stats, with more weight being given to a person’s Health and Commitment stats.

RELATIONSHIP OF WRKR_CAP AND MNGR_CAP SCORES

While, for example, manual dexterity is fairly important for a frontline factory worker, it isn’t so essential for a manager. Such distinctions are reflected in the manner in which the WRKR_CAP and MNGR_CAP scores are calculated: there is some overlap in constituent factors, but other stats contribute to only one of the two scores. It is thus possible for a person to have higher WRKR_CAP score than MNGR_CAP score, or vice versa. This reflects the real-world fact that the skills needed to successfully perform frontline work in a given organization may differ significantly from the skills needed to successfully oversee *other* persons who are performing such work. Someone who is an excellent frontline worker may or may not thrive when promoted into a managerial position, while someone who struggles in a frontline position might excel when asked to supervise others who are performing such work.

●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
ASSIGNING ROLES WITHIN THE ORGANIZATION
●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

The simulated factory is designed to model a real-world organization. In real-world competitive contexts, running a factory with hundreds or thousands of workers is an incredibly complex undertaking, and (in the absence of nepotism, corruption, incompetence, or neglect on the part of an organization’s board or directors), one may generally presume that the persons who have been assigned to senior management roles have been selected to bear such responsibility because they are well-trained, highly qualified, and have proven (and honed) their managerial abilities through years of experience. The software models this dynamic in the following manner:

▶ From among all persons in the pool of employees, the one individual with the highest MNGR_CAP score is algorithmically assigned to the role of Production Director.

▶ The individuals with the three next-highest MNGR_CAP scores are then algorithmically assigned to roles as the Shift Managers.

▶ All of the remaining individuals within the organization are randomly assigned to the role of either Team Leader or Laborer – without regard to their particular MNGR_CAP or WRKR_CAP scores. This reflects the fact that when new employees join a production company in an entry-level position, it is often not immediately apparent which individuals possess exactly which strengths and weaknesses, and which of them would thrive (or struggle) if they were promoted to the position of Team Leader. The persons assigned to serve as Team Leaders thus may or may not actually be the persons who are theoretically best-qualified to fill such roles.

███████████████████████████████████████████████████████
RUNNING THE SIMULATION
███████████████████████████████████████████████████████

It is possible for a user to configure the simulation’s parameters by manually modifying the value of certain variables defined in the config.py module, including the number of Laborers who belong to each Team (which determines the overall size of the factory’s workforce) and the number of days of activity to be simulated.

Assuming that all necessary external packages have been installed and dependencies have been satisfied, the WorkforceSim package can be executed by running its executor.py module.

●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
VIEWING THE RESULTS OF A SIMULATION
●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

Once the program has calculated each worker’s actual behaviors (and each manager’s recording of behaviors) for all days of the period simulated, it will generate a number of figures that visualize various aspects of the results. These are outputted as PNG files saved in the package’s “output files” folder. An XLSX file containing selected info regarding the organizational workforce is also generated.

███████████████████████████████████████████████████████
DEVELOPMENT
███████████████████████████████████████████████████████

Synaptans WorkforceSim™ is free open-source software developed by Matthew E. Gladden, with support from Cognitive Firewall LLC and NeuraXenetica LLC. 

The choice of the name “Synaptans” acknowledges the origins of some of the simulation’s underlying code in code written for a computer game in the “Utopian Confederation” game series, inspired by the seminal 16th-century philosophical text of St. Thomas More. In that game, “synaptans” is one of many ranks found within the administrative hierarchy of the Utopian Confederation, as it exists in the 22nd century.

Synaptans WorkforceSim code and documentation ©2021-2022 NeuraXenetica LLC