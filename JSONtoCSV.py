import json
import csv

def read_settings_data_json(jsonfilepath, csvfilepath):
	print("running read_settings_data...")
	# open json, read from it, close it
	file = open(jsonfilepath, 'r', encoding='utf-8')
	data = json.load(file)
	file.close()

	#open csv
	with open(csvfilepath, 'w', newline = '') as csvfile:
		csvwriter = csv.writer(csvfile, quotechar = ',', quoting = csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Project Name', 'Project Manager', 'Team Member', 'Member Email', 'Slack Username'])

		# iterate through the projects and insert to the csv
		for project in data:
			# print the name of the row... V2 - ADD THE NAME AND EMAIL OF THE PM
			csvwriter.writerow([project])

			# add members
			for user in data[project]["members"]:
				print("user is", user["name"])
				csvwriter.writerow(['', '', user["name"], user["email"], user["slack"]])
	

	return

# main function
if __name__ == "__main__":
	jsonfilename = "sample/output.json"
	csvfilename = "sample/projectlist.csv"

	read_settings_data_json(jsonfilename, csvfilename)