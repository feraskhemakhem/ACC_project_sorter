import math
from collections import defaultdict
from datetime import datetime
from pprint import pprint
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from models import User
from scipy.optimize import linear_sum_assignment
import json

SMALL = 0.05
MEDIUM = 0.08
LARGE = 0.11
X_LARGE = 0.14

PROJECT_MAP = {
    "Voxel Engine (LO)": {"_id": 0, "size": SMALL},
    "Finance Web App (PO)": {"_id": 1, "size": LARGE},
    "GrocerEZ (LO)": {"_id": 2, "size": MEDIUM},
    "Random Conlang Generator (LO)": {"_id": 3, "size": MEDIUM},
    "LeetCamp (LO)": {"_id": 4, "size": LARGE},
    "Meal Maximizer (LO)": {"_id": 5, "size": SMALL},
    "Dungeons and Debugging (LO)": {"_id": 6, "size": SMALL},
    "BugHunter (LO)": {"_id": 7, "size": MEDIUM},
    "Aggie Access (PO)": {"_id": 8, "size": SMALL},
    "Study Buddy (LO)": {"_id": 9, "size": MEDIUM},

}


def load_csv(file_name):
    """Loads a project signup CSV.

    Args:
        file_name: The file to open.
    Returns:
        A pandas DataFrame.
    """
    columns = [ # changed every semester
        "Timestamp",
        "Email Address",
        "What is your full name?",
        "What is your TAMU email?",
        "What is your Slack display name (not the same as full name - can be found under user settings)?",
        "Please choose your first pick!",
        "Please choose your second choice!",
        "Please choose your third choice!",
    ]
    return pd.read_csv(file_name, usecols=columns).fillna("")


def build_preferences(first, second, third):
    """Given three preferences, reduces them in order to unique choices.

    Args:
        first: project name
        second: project name
        third: project name
    Returns:
        List[str]
    """
    end_result = []
    for pref in (first, second, third):
        if pref not in end_result and pref:
            end_result.append(pref)
    return end_result


def build_users(df):
    """Creates a list of users and their preferences.

    Args:
        df: A pandas DataFrame
    Returns:
        A list of users
    """
    ids = defaultdict(lambda: len(ids))
    everybody = {}
    for ( # this has to match columns in load_csv
        _,
        timestamp,
        _,
        name,
        email,
        slack,
        first_choice,
        second_choice,
        third_choice,
    ) in df.itertuples():
        timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
        preferences = build_preferences(first_choice, second_choice, third_choice)
        if name in everybody: # in case of multiple submissions
            if everybody[name]["timestamp"] < timestamp:
                everybody[name]["timestamp"] = User(name, email, preferences, slack)
        else:
            everybody[name] = {
                "user": User(name, email, preferences, slack),
                "timestamp": timestamp,
            }
    return [e["user"] for e in everybody.values()]


def build_cost_matrix(users):
    """Given a list of users and a dictionary of projects, create a cost matrix,
    where A[i][j] is the `i`th user's ranking of the `j`th project.

    Args:
        users: A list of `User`s.
        projects: A dictionary of projects.
    Returns:
        A numpy ndarray (2D)
    """
    num_cols = 0
    for key in PROJECT_MAP:
        colspan = None
        if type(PROJECT_MAP[key]["size"]) is int:
            colspan = PROJECT_MAP[key]["size"]
        else:
            colspan = math.ceil(len(users) * PROJECT_MAP[key]["size"])
        PROJECT_MAP[key]["slice"] = slice(num_cols, num_cols + colspan)
        num_cols += colspan
    cost_matrix = np.full(shape=(len(users), num_cols), fill_value=999)
    for i in range(len(users)):
        user = users[i]
        for j in range(len(user.preferences)):
            project = user.preferences[j]
            cost_matrix[i][PROJECT_MAP[project]["slice"]] = j
    return cost_matrix


def get_project(col):
    id_to_project = {v["_id"]: k for k, v in PROJECT_MAP.items()}
    for _id in id_to_project:
        key = id_to_project[_id]
        colspan = PROJECT_MAP[key]["slice"]
        if colspan.start <= col and col <= colspan.stop:
            return key


##### TODO - create project map #####


df = load_csv("../data/data.csv")
users = build_users(df)

cost_matrix = build_cost_matrix(users)

# This function outputs the indices for the optimal solution
row_indices, column_indices = linear_sum_assignment(cost_matrix)

teams = {}
raw_row = 0
for row, col in zip(row_indices, column_indices):
    key = get_project(col)
    if key not in teams:
        teams[key] = {"members": [users[row].dictify()]}
    else:
        teams[key]["members"].append(users[row].dictify())
    raw_row += 1

json.dump(teams, open("../data/sorted_groups.json", "w+"))
print("Allocation successful. Output can be found in 'output.json'")
