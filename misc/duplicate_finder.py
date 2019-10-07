import json

#### helper functions ####
def read_json(filepath):
	print("reading from", filepath)

	# open json, read from it, close it
	file = open(filepath, 'r', encoding='utf-8')
	data = json.load(file)
	file.close()
	return data


# main function
if __name__ == "__main__":
	jsonfilename = "output/sorted_groups.json"
	outputfilename = "output/project_list.csv"
	# concatfilename = "output/full_list.csv"

	write_csv(jsonfilename, outputfilename)
	# concat_csv(concatfilename)
	# signal_slack_bot(outputfilename)