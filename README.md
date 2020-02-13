# ACC Project Member Sorter

Multiple components exist in this sorter:

### Hungarian Sorting

Originally provided by Gabriel Britain (@SaltyQuetzals) and modified by me to be more dynamic, this algorithm sorts members into groups by desired size determined by project managers. _hungarian/hungarian.py_ accepts a CSV file of responses to a Google Form with specified questions:

* "Timestamp"
* "What is your full name?"
* "Please choose your first pick!"
* "Please choose your second pick!"
* "Please choose your third pick!"
* "What is your TAMU email?"
* "What is your Slack display name (not the same as full name - can be found under user settings)?"

It then returns a JSON that organizers user schemas into project groups to _data/sorted_groups.json_.

### JSON-to-CSV Organizer

This is a JSON parser that accepts the JSON files with the same structure as that of _data/sorted_groups.json_, which is created by the Hungarian sorting. It creates a CSV file _output/project_list.csv_ that is readible by project managers and members to be easily imported to Excel or Google Sheets.

### Slack Channel Bot

A Slack bot that will create channels and add members from each group is in the process of being made.
