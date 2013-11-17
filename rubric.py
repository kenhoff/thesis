import json

class Rubric:
	def __init__(self, infile):
		f = open(infile, 'r')
		content = json.load(f)
		self.items = []
		rubricItems = content['rubricitems']

		for item in rubricItems:
			self.items.append(RubricItem(item['id'], item['name'], item['description'], item['scale'], item['prompt']))
		f.close()

	def latex_output(self, nestlevel = "section"):
		content = ""
		for item in self.items:
			content += item.latex_output(nestlevel)
		return content

	def latex_survey_output(self, nestlevel = "subsubsection"):
		content = ""
		for item in self.items:
			content += item.latex_survey_output(nestlevel)
		return content


class RubricItem:
	def __init__(self, id, name, description, scale, prompt):
		self.id = id
		self.name = name
		self.description = description
		self.scale = scale
		self.prompt = prompt


	def latex_survey_output(self, nestlevel):
		content = "\{0}".format(nestlevel)
		content += "{{{0}}}".format(self.name)
		content += self.prompt
		for scaleitem in self.scale:
			content += "\paragraph"
			content += "{{{0}}}".format(scaleitem['value'])
			content += "{0}".format(scaleitem['description'])
		return content


	def latex_output(self, nestlevel = "section"):
		# content = "\{1}{{{foooooo}}}".format(self, nestlevel)
		# print self.description
		content = "\{0}".format(nestlevel)
		content += "{{{0.name}}}".format(self)

		content += "{{{0.description}}}".format(self) + self.latex_scale_output()

		return content

	def latex_scale_output(self):
		content = ""
		for item in self.scale:
			# print item
			content += "\paragraph" + "{{{0}}}".format(item['value']) + "{{{0}}}".format(item['description'])
		return content