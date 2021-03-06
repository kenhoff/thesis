import os, csv, json, sqlite3, copy, interrater, math, plottest

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
	createQuizGraphs()
	survey_likert()
	game_likert()
	gamelists_and_comments()
	whatilearned_and_gamecomments()

	times()


	m = 22 # number of raters

	data = prepInterRaterData(m)
	# print data
	interrater_info = {}
	for k,v in data.iteritems():
		interrater_info[k] = interrater.main(v, 10, m, 5)


	# print "Inter-rater kappa vals for [1,2,3,4,5]"
	# for k, v in interrater_info.iteritems():
	# 	print k, "{0:.2f}".format(v)

	plottest.interrater_plot(interrater_info, "full_five")

	inner_3 = modify_inner_3(data)

	# print "Inter-rater kappa vals for [1, [2,3,4], 5]"
	# print inner_3
	interrater_info = {}
	for k,v in inner_3.iteritems():
		interrater_info[k] = interrater.main(v, 10, m, 3)
	# for k, v in interrater_info.iteritems():
	# 	print k, "{0:.2f}".format(v)
	plottest.interrater_plot(interrater_info, "inner_3")

	# debugging()


	outer_3 = modify_outer_3(data)

	# print "Inter-rater kappa vals for [[1,2], 3, [4,5]]"
	interrater_info = {}
	for k,v in outer_3.iteritems():
		interrater_info[k] = interrater.main(v, 10, m, 3)
	# for k, v in interrater_info.iteritems():
	# 	print k, "{0:.2f}".format(v)
	plottest.interrater_plot(interrater_info, "outer_3")



	# outer_3




	conn.close()

def times():
	import time_analysis
	time_analysis.main(c)

def modify_inner_3(data):
	output = {}
	for k, v in data.iteritems():
		output[k] = []
		for game in v:
			output[k].append([game[0], sum(game[1:4]), game[4]])
	return output

def modify_outer_3(data):
	output = {}
	for k, v in data.iteritems():
		output[k] = []
		for game in v:
			output[k].append([sum(game[0:2]), game[2], sum(game[3:5])])
	return output

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
	# exec_string = '''SELECT {} FROM results'''.format(', '.join(['gameid'] + rubric_keys))
	exec_string = '''SELECT * FROM results'''
	c.execute(exec_string)
	for row in c.fetchall():
		# print row
		pass
	# count = 0
	# for row in c.fetchall():
	# 	count += 1
	# 	print "{2} {0}: {1}".format(row[0], ', '.join(row[1:]), count)
	# print ', '.join(rubric_keys)



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
		# print item
		# item = item.decode("utf-8")
		try:
			item = item.encode("ascii", "ignore")
		except:
			item = 'error'
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
		# print cols
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

	import plottest

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0'''
	c.execute(exec_string)
	diffs = []
	count = 0
	for row in c.fetchall():
		diffs.append(float(row[1]) - float(row[0]))
		count += 1

	mean = sum(diffs)/len(diffs)

	c.execute(exec_string)
	squared_diffs_from_mean = []
	count = 0
	for row in c.fetchall():
		squared_diffs_from_mean.append( (mean - (float(row[1]) - float(row[0])))**2 )
		count += 1
	variance = sum(squared_diffs_from_mean) / count
	standard_deviation = math.sqrt(variance)


	# print "\nAggregated"
	# print "{} responses".format(count)
	# print "Mean: {}".format(mean)
	# print "Variance: {}".format(variance)
	# print "Standard Deviation: {}".format(standard_deviation)

	import significance
	sig = {}

	sig = {.9: significance.main(count, mean, standard_deviation, .9), .95: significance.main(count, mean, standard_deviation, .95)}
	plottest.tdist_graph(sig, "Aggregated t-distribution", "aggregated", count)



	quiz_games = ['oregon','lightbot','darfur','munchers']
	for game in quiz_games:
		exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "{}"'''.format(game)
		c.execute(exec_string)
		diffs = []
		count = 0
		for row in c.fetchall():
			diffs.append(float(row[1]) - float(row[0]))
			count += 1

		mean = sum(diffs)/len(diffs)

		c.execute(exec_string)
		squared_diffs_from_mean = []
		count = 0
		for row in c.fetchall():
			squared_diffs_from_mean.append( (mean - (float(row[1]) - float(row[0])))**2 )
			count += 1
		variance = sum(squared_diffs_from_mean) / count
		standard_deviation = math.sqrt(variance)

		# print "\n" + game
		# print "{} responses".format(count)
		# print "Mean: {}".format(mean)
		# print "Variance: {}".format(variance)
		# print "Standard Deviation: {}".format(standard_deviation)

		import significance
		sig = {}
		sig = {.9: significance.main(count, mean, standard_deviation, .9), .95: significance.main(count, mean, standard_deviation, .95)}
		# print sig
		plottest.tdist_graph(sig, "{} t-distribution".format(game), game, count)


def createQuizGraphs():
	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0'''
	c.execute(exec_string)
	buckets = [0] * 20
	for row in c.fetchall():
		diff = float(row[1]) - float(row[0])
		# print diff
		buckets[int((diff * 10) + 10)] += 1

	import plottest
	plottest.quiz_results(buckets, 'general_results.png', "Aggregated score differences for all games")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "darfur"'''
	c.execute(exec_string)
	buckets = [0] * 20
	for row in c.fetchall():
		diff = float(row[1]) - float(row[0])
		buckets[int((diff * 10) + 10)] += 1

	plottest.quiz_results(buckets, 'darfur_results.png', "Score differences for Darfur is Dying")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "oregon"'''
	c.execute(exec_string)
	buckets = [0] * 20
	for row in c.fetchall():
		diff = float(row[1]) - float(row[0])
		buckets[int((diff * 10) + 10)] += 1

	plottest.quiz_results(buckets, 'oregon_results.png', "Score differences for The Oregon Trail")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "lightbot"'''
	c.execute(exec_string)
	buckets = [0] * 20
	for row in c.fetchall():
		diff = float(row[1]) - float(row[0])
		buckets[int((diff * 10) + 10)] += 1

	plottest.quiz_results(buckets, 'lightbot_results.png', "Score differences for Light Bot")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "munchers"'''
	c.execute(exec_string)
	buckets = [0] * 20
	for row in c.fetchall():
		diff = float(row[1]) - float(row[0])
		buckets[int((diff * 10) + 10)] += 1

	plottest.quiz_results(buckets, 'munchers_results.png', "Score differences for Number Munchers")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0'''
	c.execute(exec_string)
	pre_buckets = [0] * 11
	post_buckets = [0] * 11
	for row in c.fetchall():
		# print int(float(row[0]) * 10) 
		pre_buckets[int(float(row[0]) * 10)] += 1
		post_buckets[int(float(row[1]) * 10)] += 1

	plottest.quiz_pre_and_post(pre_buckets, "general_pre.png", "Aggregated scores from the pre-quizzes")
	plottest.quiz_pre_and_post(post_buckets, "general_post.png", "Aggregated scores from the post-quizzes")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "munchers"'''
	c.execute(exec_string)
	pre_buckets = [0] * 11
	post_buckets = [0] * 11
	for row in c.fetchall():
		# print int(float(row[0]) * 10) 
		pre_buckets[int(float(row[0]) * 10)] += 1
		post_buckets[int(float(row[1]) * 10)] += 1

	plottest.quiz_pre_and_post(pre_buckets, "munchers_pre.png", "Pre-quiz scores for Number Munchers")
	plottest.quiz_pre_and_post(post_buckets, "munchers_post.png", "Post-quiz scores for Number Munchers")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "darfur"'''
	c.execute(exec_string)
	pre_buckets = [0] * 11
	post_buckets = [0] * 11
	for row in c.fetchall():
		# print int(float(row[0]) * 10) 
		pre_buckets[int(float(row[0]) * 10)] += 1
		post_buckets[int(float(row[1]) * 10)] += 1

	plottest.quiz_pre_and_post(pre_buckets, "darfur_pre.png", "Pre-quiz scores for Darfur is Dying")
	plottest.quiz_pre_and_post(post_buckets, "darfur_post.png", "Post-quiz scores for Darfur is Dying")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "lightbot"'''
	c.execute(exec_string)
	pre_buckets = [0] * 11
	post_buckets = [0] * 11
	for row in c.fetchall():
		# print int(float(row[0]) * 10) 
		pre_buckets[int(float(row[0]) * 10)] += 1
		post_buckets[int(float(row[1]) * 10)] += 1

	plottest.quiz_pre_and_post(pre_buckets, "lightbot_pre.png", "Pre-quiz scores for Light Bot")
	plottest.quiz_pre_and_post(post_buckets, "lightbot_post.png", "Post-quiz scores for Light Bot")

	exec_string = '''SELECT preScore, postScore FROM results WHERE preScore >= 0 AND gameid = "oregon"'''
	c.execute(exec_string)
	pre_buckets = [0] * 11
	post_buckets = [0] * 11
	for row in c.fetchall():
		# print int(float(row[0]) * 10) 
		pre_buckets[int(float(row[0]) * 10)] += 1
		post_buckets[int(float(row[1]) * 10)] += 1

	plottest.quiz_pre_and_post(pre_buckets, "oregon_pre.png", "Pre-quiz scores for The Oregon Trail")
	plottest.quiz_pre_and_post(post_buckets, "oregon_post.png", "Post-quiz scores for The Oregon Trail")




def prepInterRaterData(m):
	import plottest
	# print "********************inter-rater data*************************"
	data = {}
	responses = m

	rubricitems = ["encyclopedia_location", "encyclopedia_content", "referential_amount", "referential_popularity", "referential_rewards", "adaptive_difficulty", "contextual_tutorials", "resource_penalty", "reset_penalty", "checkpoint_frequency", "exploration_freedom", "iterative_feedback", "problem_solving"]
	games = ['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']
	for rubricitem in rubricitems:
		# rubricitem = "adaptive_difficulty"

		results = []
		for i in range(len(games)):
			results.append([0] * 5)

		for i in range(len(games)):
			exec_string = '''SELECT {2} FROM results WHERE gameid = "{0}" LIMIT {1}'''.format(games[i], responses, rubricitem)
			c.execute(exec_string)
			for row in c.fetchall():
				# print games[i], row[0]
				results[i][int(row[0])-1] += 1
				# print results
			# print sum(results[i])

		data[rubricitem] = results
	# print "Rubric item data: {}".format(data)

	for rubricitem in rubricitems:
		plottest.rubricitem_scores(data[rubricitem], rubricitem)
		# print rubricitem
		# for game in data[rubricitem]:
		# 	print str(game).strip('[]')

	plottest.game_scores(data)
	return data

def survey_likert():
	# print "***********survey likert data***********"
	fields = ['fun_can_be_educational', 'most_fun_are_educational', 'educational_can_be_fun', 'most_educational_are_fun', 'more_fun_when_competitive', 'more_fun_by_yourself', 'more_fun_online', 'more_educational_when_cooperative', 'more_educational_by_yourself', 'more_educational_online']
	data = []
	for i in range(len(fields)):
		data.append([0] * 4)
	exec_string = '''SELECT {} from results'''.format(', '.join(fields))
	c.execute(exec_string)
	count = 0
	for row in c.fetchall():
		for i in range(len(fields)):
			if (row[i] == "Stronglydisagree"):
				data[i][0] += 1
			if (row[i] == "Disagree"):
				data[i][1] += 1
			if (row[i] == "Agree"):
				data[i][2] += 1
			if (row[i] == "StronglyAgree"):
				data[i][3] += 1
		count += 1
		# print row
	# print data

	import numpy as np
	import matplotlib.pyplot as plt

	stronglydisagree = []
	disagree = []
	agree = []
	stronglyagree = []
	for field in data:
		stronglydisagree.append(field[0])
		disagree.append(field[1])
		agree.append(field[2])
		stronglyagree.append(field[3])

	# print "Strongly disagrees: {}".format(str(stronglydisagree))

	N = len(fields)
	ind = np.arange(N)
	width = .15
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, stronglydisagree, width, color = (1, 0, 0))
	rects2 = ax.bar(ind + (width * 1), disagree, width, color = (.66, 0, .33))
	rects3 = ax.bar(ind + (width * 2), agree, width, color = (.33, 0, .66))
	rects4 = ax.bar(ind + (width * 3), stronglyagree, width, color = (0, 0, 1))

	ax.set_title("Likert scale responses for survey (N = {})".format(count))
	ax.set_ylabel("Number of responses")
	ax.set_xlabel("Question")
	ax.set_xticks(ind + width)
	ax.set_xticklabels(fields, rotation = 90)

	ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ("Strongly Disagree", "Disagree", "Agree", "Strongly Agree"), bbox_to_anchor = (1.5, 1))

	plt.savefig("survey_likert.png", bbox_inches = 'tight')

def game_likert():
	games = ['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']
	for game in games:
		# print "***********{} likert data***********".format(game)
		fields = ['this_game_was_fun', 'i_had_fun', 'this_game_was_educational', 'i_learned_something']
		data = []
		for i in range(len(fields)):
			data.append([0] * 4)
		exec_string = '''SELECT {} from results WHERE gameid = "{}"'''.format(', '.join(fields), game)
		c.execute(exec_string)
		count = 0
		for row in c.fetchall():
			if (game == 'pandemic'):
				print "{}: {}".format(game, row[0])
			count += 1 
			for i in range(len(fields)):
				if (row[i] == "Stronglydisagree"):
					data[i][0] += 1
				if (row[i] == "Disagree"):
					data[i][1] += 1
				if (row[i] == "Agree"):
					data[i][2] += 1
				if (row[i] == "StronglyAgree"):
					data[i][3] += 1
			# print row
		# print data

		import numpy as np
		import matplotlib.pyplot as plt

		stronglydisagree = []
		disagree = []
		agree = []
		stronglyagree = []
		for field in data:
			stronglydisagree.append(field[0])
			disagree.append(field[1])
			agree.append(field[2])
			stronglyagree.append(field[3])

		# print "Strongly disagrees: {}".format(str(stronglydisagree))

		N = len(fields)
		ind = np.arange(N)
		width = .15
		fig, ax = plt.subplots()
		rects1 = ax.bar(ind, stronglydisagree, width, color = (1, 0, 0))
		rects2 = ax.bar(ind + (width * 1), disagree, width, color = (.66, 0, .33))
		rects3 = ax.bar(ind + (width * 2), agree, width, color = (.33, 0, .66))
		rects4 = ax.bar(ind + (width * 3), stronglyagree, width, color = (0, 0, 1))

		ax.set_title("Likert scale responses for {} (N = {})".format(game, count))
		ax.set_ylabel("Number of responses")
		ax.set_xlabel("Question")
		ax.set_xticks(ind + width)
		ax.set_xticklabels(fields, rotation = 90)

		ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ("Strongly Disagree", "Disagree", "Agree", "Strongly Agree"), bbox_to_anchor = (1.5, 1))

		plt.savefig("{}_likert.png".format(game), bbox_inches = 'tight')


def gamelists_and_comments():

	fields = ['fun_game_list', 'educational_game_list', 'comments_on_survey']
	exec_string = '''SELECT {} from results'''.format(', '.join(fields))
	c.execute(exec_string)
	fungames = []
	edugames = []
	comments_on_survey = []
	for row in c.fetchall():
		fungames.append(row[0])
		edugames.append(row[1])
		comments_on_survey.append(row[2])

	open('fungames.txt', 'w+').write(scrub_latex('\n'.join(fungames)))
	open('edugames.txt', 'w+').write(scrub_latex('\n'.join(edugames)))
	open('comments_on_survey.txt', 'w+').write(scrub_latex('\n'.join(comments_on_survey)))

def whatilearned_and_gamecomments():
	for game in ['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']:
		fields = ['what_did_you_learn', 'comments_on_game']
		exec_string = '''SELECT {} from results WHERE gameid = "{}"'''.format(', '.join(fields), game)
		c.execute(exec_string)
		whatilearned = []
		comments_on_game = []
		for row in c.fetchall():
			whatilearned.append(row[0])
			comments_on_game.append(row[1])

		open('{}_whatilearned.txt'.format(game), 'w+').write(scrub_latex('\n'.join(whatilearned)))
		open('{}_comments_on_game.txt'.format(game), 'w+').write(scrub_latex('\n'.join(comments_on_game)))


def scrub_latex(text):

	return text.replace('&', '\&').replace('%', '\%').replace('$', '\$')

def debugging():
	exec_string = '''SELECT adaptive_difficulty from results WHERE gameid = "baseball"'''
	c.execute(exec_string)
	for row in c.fetchall():
		# print row
		pass

# code for opening survey json
# f = open('./turk_stuff/basic.json', 'r')
# survey = json.loads(f.read())

if __name__ == "__main__":
	main()