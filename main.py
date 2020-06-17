#########################################################
#                                                       #
#   main.py / Probability Runner                        #
#                                                       #
#   Author: Braden Dubois (braden.dubois@usask.ca)      #
#   Written for: Dr. Eric Neufeld                       #
#                                                       #
#########################################################

from probability_structures.CausalGraph import *
from regression_tests.RegressionTesting import *

import os               # Used to list directory contents to select graphs
from config.config_mgr import *

# If set, run any tests before starting up
if access("run_regression_tests_on_launch"):

    # (success_boolean, message) tuple returned
    results = validate_all_regression_tests()

    if not results[0] and access("output_regression_results") == "failure":
        print(results)
    elif access("output_regression_results") == "always":
        print(results)

    if not results[0] and access("exit_if_regression_failure"):
        exit(-1)

# Does the directory of graphs exist?
if os.path.isdir(access("graph_file_folder")):

    # Find all JSON files in that directory
    files = sorted([file_name for file_name in os.listdir(access("graph_file_folder")) if file_name.endswith(".json")])

    # Only one file, just select it
    if len(files) == 1:
        graph_file = files[0]

    # Multiple files, list them and get a selection
    else:
        print("Files located in:", access("graph_file_folder"))
        for file_index in range(len(files)):
            print("  ", str(file_index+1) + ")", files[file_index])
        print("  ", str(len(files)+1) + ") Exit")

        selection = input("Selection: ")
        while not selection.isdigit() and 1 <= int(selection) <= len(files) + 1:
            selection = input("Selection: ")

        if selection == str(len(files)+1):
            exit(0)

        graph_file = files[int(selection) - 1]

    print("\nLoading:", graph_file, "\n")
    CG = CausalGraph(access("graph_file_folder") + "/" + graph_file)

# No directory, load whatever default is specified in the Causal Graph
else:
    # Specify a path to a graph file if desired
    CG = CausalGraph()

# Start the software
CG.run()