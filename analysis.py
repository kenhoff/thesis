import os, csv, json, sqlite3, copy

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def main():

	cols = create_table()

	for root, dirs, filenames in os.walk("data_files"):
		for f in filenames:
			with open(os.path.join(root, f), 'r') as csvfile:
				resultreader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
				resultreader.next()
				for row in resultreader:
					store_row(row, cols) # dump array of responses into SQLite
	print_table()
	gradeAll()
	# printGrades()
	scoreDifferenceMean()
	conn.close()



def create_table():
	cols = ['gameid', 'workerid', 'acceptTime', 'submitTime']
	for i in range(1, 11):
		cols.append("prequestion{}".format(i))

	# insert survey/rubric stuff
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
	cols += full_keys

	for i in range(1, 11):
		cols.append("postquestion{}".format(i))

	# print(cols)

	exec_string = '''CREATE TABLE results ({})'''.format(', '.join(cols))
	c.execute(exec_string)
	exec_string = '''ALTER TABLE results ADD preScore'''
	c.execute(exec_string)
	exec_string = '''ALTER TABLE results ADD postScore'''
	c.execute(exec_string)
	conn.commit()
	return cols

def print_table():
	f = open('rubric_information.json')
	rubric = json.loads(f.read())
	rubric_keys = []
	for item in rubric['rubricitems']:
		rubric_keys.append(item['id'])
	exec_string = '''SELECT {} FROM results'''.format(', '.join(['gameid'] + rubric_keys))
	c.execute(exec_string)
	for row in c.fetchall():
		print "{0}: {1}".format(row[0], ', '.join(row[1:]))
	print ', '.join(rubric_keys)



def store_row(row, cols):
	gameid = row[2]
	quiz_games = ['oregon','lightbot','darfur','munchers']
	regular_games = ['machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']

	# print row

	newrow = []

	for item in row:
		item = item.replace("'", "''")
		item = item.replace('\n', ' ')
		item = item.replace('\r', ' ')
		newrow .append("'{}'".format(item))
		# print(item)

	# print row
	# print(newrow)

	# if result is for a quiz game, insert the full record, minus the first 8 cols
	if (quiz_games.count(gameid) > 0):
		# cols needs to be gameid, workerid, acceptTime, submitTime, prequestions, survey + rubric, postquestions
		# vals needs to be row[2], row[4], row[6], row[7], row[8:, ]
		vals = [newrow[2], newrow[4], newrow[6], newrow[7]] + newrow[8:]
		# print(vals)
		vals.pop()
		# print (len(cols), len(vals))
		exec_string = '''INSERT INTO results ({0}) VALUES ({1})'''.format(', '.join(cols), ', '.join(vals))

	# if result is for a non-quiz game, insert the full record minus the first 18 cols and the last 10

	else: # remove the questions from the cols, and only use row[8:]
		trimmedcols = copy.deepcopy(cols)
		for i in range(1, 11):
			trimmedcols.remove("prequestion{}".format(i))
			trimmedcols.remove("postquestion{}".format(i))
		vals = [newrow[2], newrow[4], newrow[6], newrow[7]] + newrow[8:]
		vals.pop()
		# print (len(trimmedcols), len(vals))

		exec_string = '''INSERT INTO results ({0}) VALUES ({1})'''.format(', '.join(trimmedcols), ', '.join(vals))

	# print (exec_string)
	c.execute(exec_string)
	conn.commit()

# grade all the quizzes in the database
def gradeAll():
	exec_string = '''SELECT * FROM results'''
	c.execute(exec_string)
	for row in c.fetchall():
		gradeQuiz(row)


# grade one quiz
def gradeQuiz(quiz):
	# print(quiz)
	quiz_games = ['oregon','lightbot','darfur','munchers']
	if (quiz_games.count(quiz[0]) > 0):
		# open appropriate quiz file
		f = open('./turk_stuff/{}.json'.format(quiz[0]), 'r')
		json_data = json.loads(f.read())
		key_answers = []
		for q in json_data['questions']:
			key_answers.append(q['correct'])
		# print(key_answers)
		worker_pre_answers = []
		worker_post_answers = []
		for r in quiz[4:14]:
			worker_pre_answers.append(int(r))
		# print(worker_pre_answers)
		for r in quiz[51:61]:
			worker_post_answers.append(int(r))
		# print(worker_post_answers)


		preScore = 0.0
		postScore = 0.0

		for i in range(10):
			if (worker_pre_answers[i] == key_answers[i]):
				preScore += 0.1

		for i in range(10):
			if (worker_post_answers[i] == key_answers[i]):
				postScore += 0.1



		exec_string = '''UPDATE results SET preScore = '{0}', postScore = '{1}' WHERE workerid = '{2}' AND gameid = '{3}' '''.format(preScore, postScore, quiz[1], quiz[0])
		c.execute(exec_string)
	else:
		return 


# print the scores of all the quizzes
def printGrades():
	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0'''
	c.execute(exec_string)
	for row in c.fetchall():
		print str(row[0]), str(row[1])

def scoreDifferenceMean():
	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0'''
	c.execute(exec_string)
	diffs = []
	for row in c.fetchall():
		diffs.append(float(row[1]) - float(row[0]))
	print "Avg change: {}".format(sum(diffs)/len(diffs))







# code for opening survey json
# f = open('./turk_stuff/basic.json', 'r')
# survey = json.loads(f.read())

if __name__ == "__main__":
	main()