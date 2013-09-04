class Rubric:
	def __init__(self, infile):
		f = open(infile, 'r')
		content = f.read()
		self.items = set()
		rubricItems = content.split('\n\n')

		rubricItems.pop(0) # remove keys section

		for item in rubricItems:
			info = item.split('\n')
			# print info
			self.items.add(RubricItem(info[0], info[1], info[2], info[3], [info[4], info[5], info[6], info[7], info[8]]))
		f.close()

	def latex_output(self, nestlevel = "section"):
		content = ""
		for item in self.items:
			content += item.latex_output(nestlevel)
		return content


class RubricItem:
	def __init__(self, id, name, description, weight, scale):
		self.id = id
		self.name = name
		self.description = description
		self.weight = weight
		self.scale = scale


	def latex_output(self, nestlevel = "section"):
		# content = "\{1}{{{foooooo}}}".format(self, nestlevel)
		content = "\{1}{{{0.name}}}{{{0.description}}} ".format(self, nestlevel) + self.latex_scale_output()
		return content

	def latex_scale_output(self):
		content = ""
		for index in xrange(len(self.scale)):
			content += "\paragraph" + "{{{0}}}".format(index + 1) + "{0}".format(self.scale[index])
		return content

	def latex_weight_output(self):
		return "\paragraph{Weight:}" + "{{{0.weight}}}".format(self)