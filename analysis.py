import os, csv, json

survey_data = [] # array of survey response dicts - contain likert scales and rubric data
prequiz_data = []
postquiz_data = []

def main():
	for root, dirs, filenames in os.walk("data_files"):
		for f in filenames:
			with open(os.path.join(root, f), 'r') as csvfile:
				resultreader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
				resultreader.next()
				for row in resultreader:
					store_row(row) # take array of responses and pack it into appropriate data sets
	for row in survey_data:
		print('\n')
		for k,v in row.iteritems():
			print("{}: {}".format(k,v))

def store_row(row):
	gameid = row[2]
	print(gameid)
	quiz_games = ['oregon','lightbot','darfur','munchers']
	regular_games = ['machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']
	if (quiz_games.count(gameid) > 0):
		survey_dict = pack_survey_data_dict(row[18:55]) # send only survey data section
	else:
		survey_dict = pack_survey_data_dict(row[8:45])
	survey_dict['gameid'] = gameid
	survey_data.append(survey_dict)



def pack_survey_data_dict(row):
	f = open('./turk_stuff/basic.json', 'r')
	survey = json.loads(f.read())
	survey_keys = []
	for question in survey['questions']:
		survey_keys.append(question['id'])
	f.close()
	f = open('rubric_information.json')
	rubric = json.loads(f.read())
	rubric_keys = []
	for item in rubric['rubricitems']:
		rubric_keys.append(item['id'])

	full_keys = survey_keys[:survey_keys.index("survey")] + rubric_keys + survey_keys[survey_keys.index("survey")+1:]

	result = dict(zip(full_keys, row))

	return result






# code for opening survey json
# f = open('./turk_stuff/basic.json', 'r')
# survey = json.loads(f.read())

if __name__ == "__main__":
	main()