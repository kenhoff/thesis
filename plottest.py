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
	ax.set_title(title)
	ax.set_ylabel("Number of quizzes")
	ax.set_xlabel("Individual change in pre-quiz and post-quiz scores")

	plt.savefig(savefile, bbox_inches = 'tight')

def quiz_pre_and_post(stats, game, title):

	import numpy as np
	import matplotlib.pyplot as plt
	import random

	N = 11 # the number of bars on the graph - between 0.0 and 1.0
	number = stats # an array of len 10, from 0 to 100%


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

	ax.set_title(title)
	ax.set_ylabel("Number of quizzes")
	ax.set_xlabel("Score")

	plt.savefig(game, bbox_inches = 'tight')