def main(data, n, m, k):

	# n = 10 # number of games
	# m = 5 # number of raters
	# k = 3 # number of options for an item

	sum_over_i = 0

	for game in data:
		for option in game:
			sum_over_i += option**2

	# print sum_over_i # works!

	# pj - the percentage of each option

	total = [0.0] * k

	for i in range(k):
		for game in data:
			total[i] += game[i]

	# print total

	total_sum = sum(total)

	pj = [0.0] * k

	for i in range(k):
		pj[i] = total[i] / total_sum

	# print pj



	qj = [0.0] * k

	for i in range(k):
		qj[i] = 1 - pj[i]

	# print qj

	pj_x_qj = [0.0] * k

	for i in range(k):
		pj_x_qj[i] = pj[i] * qj[i]

	# print sum(pj_x_qj)

	kappa = 1 - ( ( (n * m**2) - sum_over_i) / (n * m * (m - 1) * sum(pj_x_qj)))

	# print "Kappa: {}".format(kappa)

	return kappa







if __name__ == "__main__":

	n = 10 # number of games
	m = 5 # number of raters
	k = 3 # number of options for an item

	# for me, n = 10, m = 15?, and k = 5 

	sample_data = [	[0, 5, 0],
					[0, 0, 5],
					[0, 0, 5],
					[5, 0, 0],
					[3, 0, 2],
					[1, 3, 1],
					[5, 0, 0],
					[0, 4, 1],
					[1, 0, 4],
					[3, 0, 2] ]

	main(sample_data, n, m, k)