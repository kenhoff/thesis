def main(N, md, sd, p):
	from scipy.stats import t
	from math import sqrt

	a = 1 - p


	ta = t.interval(p, N - 1) # confidence limits
	# print ta



	c = (ta[1] * sd) / sqrt(N)

	# print c

	# print md-c, md+c

	return (md-c, c, md+c) # as long as md-c > 0, then we don't have the null hypothesis!






if __name__ == "__main__":

	N = 116 # number of responses
	md = 0.028448276 # mean of the differences
	sd = 0.122337883 # std dev of the differences
	p = 0.90

	main(N, md, sd, p)