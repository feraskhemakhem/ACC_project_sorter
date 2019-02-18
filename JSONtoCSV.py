import json
import csv

def read_json(filepath):
	print("reading from", filepath)

	# open json, read from it, close it
	file = open(filepath, 'r', encoding='utf-8')
	data = json.load(file)
	file.close()
	return data

def concat_csv(csvfilepath):
	print("concatinating csv files...")
	with open(csvfilepath, 'r', newline = '') as csvfile:
		csvreader = csv.reader(csvfile, quotechar = ',')
		for entry in csvreader:
			print(entry)

	return

def write_csv(jsonfilepath, csvfilepath):
	print("writing to", csvfilepath)
	# open json, read from it, close it
	data = read_json(jsonfilepath)

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
	outputfilename = "sample/projectlist.csv"
	concatfilename = "sample/returninglist.csv"

	#write_csv(jsonfilename, outputfilename)
	concat_csv(concatfilename)