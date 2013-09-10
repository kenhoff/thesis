import json

class GameList:
	def __init__(self, infile):
		f = open(infile, 'r')
		content = json.load(f)
		self.games = set()
		# gameArray = content.split('\n\n')

		# gameArray.pop(0) # remove keys section

		for game in content["gamelist"]:
			self.games.add(Game(game["id"], game["title"], game["url"], game["description"], game['education'], game['images'][0]['path'], game['images'][1]['path']))
		f.close()

	def latex_output(self, nestlevel = "section"):
		content = ""
		for game in self.games:
			content += game.latex_output(nestlevel)
		return content


class Game:
	def __init__(self, id, name, url = None, description = None, education = None, title_screen = None, screenshot = None):
		self.name = name
		self.url = url
		self.description = description
		self.id = id
		self.education = education
		self.title = "img/" + title_screen
		self.screen = "img/" + screenshot

	def latex_output(self, nestlevel = "section"):
		# print self.name
		content = "\{}".format(nestlevel) + "{{{}}}".format(self.name) + "\subparagraph{}" + "\includegraphics[width = \\textwidth]{{{0}}}".format(self.title) + "\subparagraph{URL}" + "\url{{{}}}".format(self.url) + "\subparagraph{Description}" + "{}".format(self.description) + "\subparagraph{Educational Content}" + "{}".format(self.education) + "\subparagraph{}" + "\includegraphics[width = \\textwidth]{{{0}}}".format(self.screen) # + "\\newpage"
		# print self.id
		return content
