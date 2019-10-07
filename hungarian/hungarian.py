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
    "Chip-8 Emulator (LO)": {"_id": 0, "size": SMALL},
    "Basic (LO)": {"_id": 1, "size": SMALL},
    "Media Tracker (LO)": {"_id": 2, "size": MEDIUM},
    "Create Your First Website (LO)": {"_id": 3, "size": SMALL},
    "Aggie Involvement Project (LO)": {"_id": 4, "size": MEDIUM},
    "Tile Gallery App (LO)": {"_id": 5, "size": SMALL},
    "Dungeons and Debugging (LO)": {"_id": 6, "size": SMALL},
    "Cloud Text Editor (LO)": {"_id": 7, "size": SMALL},
    "Aggie Agenda (LO)": {"_id": 8, "size": SMALL},
    "Leetcode Bootcamp (LO)": {"_id": 9, "size": X_LARGE},
    "Fake News Detector (LO)": {"_id": 10, "size": MEDIUM},
    "DevLink (PO)": {"_id": 11, "size": SMALL},
    "MicroMouse Maze Solving Robot (PO)": {"_id": 12, "size": SMALL},
    "BTHOspam (PO)": {"_id": 13, "size": SMALL},
    "Aggie Tool Kit (PO/LO)": {"_id": 14, "size": SMALL},
    "Club Website (PO)": {"_id": 15, "size": MEDIUM},
    "Pegasus (PO)": {"_id": 16, "size": MEDIUM},
    "Cross-Platform App for Aggie Coding Club (PO)": {"_id": 17, "size": MEDIUM},
    "Morai (PO)": {"_id": 18, "size": SMALL},
    "Automatic Aggie Scheduler (PO)": {"_id": 19, "size": MEDIUM},


    # "AI-Snake": {"_id": 0, "size": MEDIUM},
    # "Aggie Coding Club Website": {"_id": 1, "size": MEDIUM},
    # "Aggie Tool Kit": {"_id": 2, "size": MEDIUM},
    # "Barhoppery": {"_id": 3, "size": MEDIUM},
    # "Chrome Calories": {"_id": 4, "size": MEDIUM},
    # "Class Material Reminder": {"_id": 5, "size": MEDIUM},
    # "Dog Nutrition +": {"_id": 6, "size": MEDIUM},
    # "Easter Pop": {"_id": 7, "size": MEDIUM},
    # "FlipFlop": {"_id": 8, "size": MEDIUM},
    # "Hackathon Regristration System Project": {"_id": 9, "size": MEDIUM},
    # "OneStop Notifications": {"_id": 10, "size": MEDIUM},
    # "Safe Driving Detection System": {"_id": 11, "size": MEDIUM},
}


def load_csv(file_name):
    """Loads a project signup CSV.

    Args:
        file_name: The file to open.
    Returns:
        A pandas DataFrame.
    """
    columns = [
        "Timestamp",
        "What is your full name?",
        "Please choose your first pick!",
        "Please choose your second choice!",
        "Please choose your third choice!",
        "What is your TAMU email?",
        "What is your Slack display name (not the same as full name - can be found under user settings)?",
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
    for (
        _,
        timestamp,
        email,
        name,
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


df = load_csv("data.csv")
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

json.dump(teams, open("../output/sorted_groups.json", "w+"))
print("Allocation successful. Output can be found in 'output.json'")
