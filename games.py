import json

class GameList:
	def __init__(self, infile):
		f = open(infile, 'r')
		content = json.load(f)
		self.games = set()
		# gameArray = content.split('\n\n')

		# gameArray.pop(0) # remove keys section

		for game in content["gamelist"]:
			self.games.add(Game(game["id"], game["title"], game["url"], game["description"], game['education'], game['images']))
		f.close()

	def latex_output(self, nestlevel = "section"):
		content = ""
		for game in self.games:
			content += game.latex_output(nestlevel)
		return content


class Game:
	def __init__(self, id, name, url, description, education, images):
		self.name = name
		self.url = url
		self.description = description
		self.id = id
		self.education = education
		self.images = images

	def latex_output(self, nestlevel = "section"):
		# print self.name
		content = "\\newpage" + "\{}".format(nestlevel) + "{{{}}}".format(self.name) + "\subparagraph{URL}" + "\url{{{}}}".format(self.url) + "\subparagraph{Description}" + "{}".format(self.description) + "\subparagraph{Educational Content}" + "{}".format(self.education)
		for image in self.images:
			content += "\\begin{figure}[h!]" + "\centering \includegraphics[height=0.33\\textheight]{{{0}}}".format('img/' + image['path']) + "\caption{{{0}}}".format(image['caption']) + "\end{figure}"
		# print self.id
		return content
