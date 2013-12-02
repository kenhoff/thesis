import numpy as np
import matplotlib.pyplot as plt
import random

def quiz_results(stats, savefile, title):

	import numpy as np
	import matplotlib.pyplot as plt
	import random

	N = 20 # the number of bars on the graph - between 0.0 and 1.0
	# number = range(20) # how many there were with each score - an array of len 20
	number = stats


	ind = np.arange(N) # the x locations of the groups?
	width = .3 

	fig, ax = plt.subplots() # ???
	rects1 = ax.bar(ind, number, width)

	locs, labels = plt.xticks()

	# print locs
	# for label in labels:
	# 	print label

	# ticks = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]

	ax.set_xticks(range(21)) # 0 is -1.0, 19 is +1.0
	ax.set_xticklabels([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, "+1", "+2", "+3", "+4", "+5", "+6", "+7", "+8", "+9", "+10"])
	ax.set_title(title + " (N = {})".format(sum(number)))
	ax.set_ylabel("Number of quizzes")
	ax.set_xlabel("Individual change in pre-quiz and post-quiz scores")

	plt.savefig(savefile, bbox_inches = 'tight')

def quiz_pre_and_post(stats, game, title):

	import numpy as np
	import matplotlib.pyplot as plt
	import random

	N = 11 # the number of bars on the graph - between 0.0 and 1.0
	number = stats # an array of len 11, from 0 to 100%


	ind = np.arange(N) # the x locations of the groups?
	width = .3 

	fig, ax = plt.subplots() # ???
	rects1 = ax.bar(ind, number, width)

	locs, labels = plt.xticks()

	# print locs
	# for label in labels:
	# 	print label

	# ticks = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]

	ax.set_xticks(range(11)) # 0 is -1.0, 19 is +1.0
	ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"])

	ax.set_title(title + " (N = {})".format(sum(number)))
	ax.set_ylabel("Number of quizzes")
	ax.set_xlabel("Score")

	plt.savefig(game, bbox_inches = 'tight')

def rubricitem_scores(rubricitem_data, name):
	N = 10

	# print name, rubricitem_data

	ones = []
	twos = []
	threes = []
	fours = []
	fives = []

	for game in rubricitem_data:
		ones.append(game[0])
		twos.append(game[1])
		threes.append(game[2])
		fours.append(game[3])
		fives.append(game[4])

	ind = np.arange(N)
	width = 0.15

	fig, ax = plt.subplots()

	rects1 = ax.bar(ind, ones, width, color = (1, 0, 0))
	rects2 = ax.bar(ind+(width*1), twos, width, color = (.75, 0, .25))
	rects3 = ax.bar(ind+(width*2), threes, width, color = (.5, 0, .5))
	rects4 = ax.bar(ind+(width*3), fours, width, color = (.25, 0, .75))
	rects5 = ax.bar(ind+(width*4), fives, width, color = (0, 0, 1))

	ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0]), ("1 - worst", 2, 3, 4, "5 - best"), bbox_to_anchor = (1.3, 1))

	ax.set_title(name)

	ax.set_ylabel("Number of responses with a given score")
	ax.set_xlabel("Games")
	ax.set_xticks(ind+width)
	ax.set_xticklabels(['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings'], rotation=90)

	plt.ylim(0, 20)

	plt.savefig("{}_scores.png".format(name), bbox_inches = 'tight')

def game_scores(all_rubricitem_data):
	# first, rework all rubricitem data into game data

	games = ['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']
	rubricitems = ["encyclopedia_location", "encyclopedia_content", "referential_amount", "referential_popularity", "referential_rewards", "adaptive_difficulty", "contextual_tutorials", "resource_penalty", "reset_penalty", "checkpoint_frequency", "exploration_freedom", "iterative_feedback", "problem_solving"]

	game_data = {}

	for game in games:
		game_data[game] = []

	for i in range(len(games)):
		for k, v in all_rubricitem_data.iteritems():
			# print k, v[i]
			# print all_rubricitem_data[rubricitems[]]
			game_data[games[i]].append(v[i])

	# print all_rubricitem_data
	# print game_data


	for k, v in game_data.iteritems():
		N = 13

		# print name, rubricitem_data

		ones = []
		twos = []
		threes = []
		fours = []
		fives = []

		for rubricitem in v:
			ones.append(rubricitem[0])
			twos.append(rubricitem[1])
			threes.append(rubricitem[2])
			fours.append(rubricitem[3])
			fives.append(rubricitem[4])

		ind = np.arange(N)
		width = 0.15

		fig, ax = plt.subplots()

		rects1 = ax.bar(ind, ones, width, color = (1, 0, 0))
		rects2 = ax.bar(ind+(width*1), twos, width, color = (.75, 0, .25))
		rects3 = ax.bar(ind+(width*2), threes, width, color = (.5, 0, .5))
		rects4 = ax.bar(ind+(width*3), fours, width, color = (.25, 0, .75))
		rects5 = ax.bar(ind+(width*4), fives, width, color = (0, 0, 1))

		ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0]), ("1 - worst", 2, 3, 4, "5 - best"), bbox_to_anchor = (1.3, 1))

		ax.set_title(k)

		ax.set_ylabel("Number of responses with a given score")
		ax.set_xlabel("Rubric Items")
		ax.set_xticks(ind+width)
		ax.set_xticklabels(rubricitems, rotation=90)
		plt.ylim(0, 20)


		plt.savefig("{}_scores.png".format(k), bbox_inches = 'tight')








def tdist_graph(stats, title, game, N):
	import matplotlib.pyplot as plt
	import numpy as np
	plt.clf()

	f, ax = plt.subplots()
	ax.set_title("{} (N = {})".format(title, N))
	ax.set_xlabel("The probability that our value of the t distribution is within the confidence limits")
	ax.set_ylabel("Mean difference in scores, confidence limits")

	point9_stats = stats[.9]
	point95_stats = stats[.95]

	plt.plot(.9, point9_stats[1], 'bo')
	lower_err = point9_stats[1] - point9_stats[0]
	upper_err = point9_stats[2] - point9_stats[1]
	# print lower_err, upper_err
	plt.errorbar(.9, point9_stats[1], yerr = [[lower_err], [upper_err]], ecolor = 'b')
	# plt.axis([.88, .97, 0, .08])
	plt.plot(.95, point95_stats[1], 'bo')
	lower_err = point95_stats[1] - point95_stats[0]
	upper_err = point95_stats[2] - point95_stats[1]
	# print lower_err, upper_err
	plt.errorbar(.95, point95_stats[1], yerr = [[lower_err], [upper_err]], ecolor = 'b')

	plt.xlim(.85, 1)

	plt.axhline()




	plt.savefig("{}_tdist.png".format(game), bbox_inches = 'tight')


def interrater_plot(data, title):
	N = 13
	ticklabels = []
	bardata = []
	for k, v in data.iteritems():
		ticklabels.append(k)
		bardata.append(v)

	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars

	fig, ax = plt.subplots()

	
	rects1 = ax.bar(ind, bardata, width)

	ax.set_ylabel('Kappa - amount of agreement/disagreement')
	ax.set_title(title)
	ax.set_xticks(ind+width)
	ax.set_xticklabels(ticklabels, rotation=90)

	plt.ylim(-.1, .3)
	plt.axhline()



	plt.savefig("{}_stats.png".format(title), bbox_inches = 'tight')


