import random

def main():
	for i in range(10):
		print (conditionals())


def conditionals():
	return "{0}(({1}{2}) {3} ({4}{5})) {6} {7}(({8}{9}) {10} ({11}{12}))".format(isnot(), isnot(), truefalse(), andor(), isnot(), truefalse(), andor(), isnot(), isnot(), truefalse(), andor(), isnot(), truefalse())

def isnot():
	return random.choice(["not ", ""])

def truefalse():
	return random.choice(["true", "false"])

def andor():
	return random.choice(["and", "or"])




if __name__ == "__main__":
	main()