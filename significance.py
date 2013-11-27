def main(N, md, sd):
	from scipy.stats import t
	from math import sqrt

	p = 0.95
	a = 1 - p


	ta = t.interval(p, N - 1) # confidence limits


	c = (ta[1] * sd) / sqrt(N)

	print c

	print md-c, md+c



if __name__ == "__main__":

	N = 116 # number of responses
	md = 0.028448276 # mean of the differences
	sd = 0.122337883 # std dev of the differences

	main(N, md, sd)