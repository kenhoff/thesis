import random

class Question:
	def __init__(self, qtype):
		num_alts = 4
		x = 25
		self.type = qtype
		self.alts = []
		self.a = random.randrange(-100, 100)
		self.b = random.randrange(-100, 100)
		if (qtype == "add"):
			self.opchar = "+"
			self.answer = self.a + self.b
		elif (qtype == "sub"):
			self.opchar = "-"
			self.answer = self.a - self.b
		elif (qtype == "mult"):
			self.opchar = "*"
			
			self.a = random.randrange(x/4, x)
			self.b = random.randrange(x/4, x)
			self.answer = self.a * self.b
		elif (qtype == "div"):

			a = random.randrange(x/4, x)
			b = random.randrange(x/4, x)
			result = a * b

			self.a = result
			self.b = b
			self.answer = a


			self.opchar = "/"

		for alt in range(num_alts):
			self.alts.append(random.randrange(self.answer - 20, self.answer + 20))
		self.alts.append(self.answer)
		random.shuffle(self.alts)



	def pprint(self):
		print("{} {} {} = {} {}".format(self.a, self.opchar, self.b, self.answer, self.alts))



def main():
	questions = ["div"] * 10
	print questions
	random.shuffle(questions)
	# print questions
	for q in questions:
		Question(q).pprint()


def gen_question(qtype):
	return Question(qtype)

if __name__ == "__main__":
	main()