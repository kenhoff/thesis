class GameList:
	def __init__(self, infile):
		f = open(infile, 'r')
		content = f.read()
		self.games = set()
		gameArray = content.split('\n\n')


		###############################################
		# useless shit i wrote to try to read in keys
		# keys = []
		# game_properties = gameArray[0].split('\n')
		# for prop in game_properties:
		# 	keys.append(prop.strip('<').strip('>'))

		gameArray.pop(0) # remove keys section

		for game in gameArray:
			info = game.split('\n')
			self.games.add(Game(info[0], info[1], info[2], info[3], info[4], info[5], info[6]))
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
		content = "\\newpage" + "\{}".format(nestlevel) + "{{{}}}".format(self.name) + "\subparagraph{}" + "\includegraphics[width = \\textwidth]{{{0}}}".format(self.title) + "\subparagraph{URL}" + "\url{{{}}}".format(self.url) + "\subparagraph{Description}" + "{}".format(self.description) + "\subparagraph{Educational Content}" + "{}".format(self.education) + "\subparagraph{}" + "\includegraphics[width = \\textwidth]{{{0}}}".format(self.screen)
		# print self.id
		return content
