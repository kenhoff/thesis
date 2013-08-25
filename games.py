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
			self.games.add(Game(info[0], info[1], info[2]))
		f.close()

	def latex_output(self, nestlevel = "section"):
		content = ""
		for game in self.games:
			content += game.latex_output(nestlevel)
		return content


class Game:
	def __init__(self, id, name, url = None, description = None):
		self.name = name
		self.url = url
		self.description = description
		self.id = id

	def latex_output(self, nestlevel = "section"):
		# print self.name
		content = "\{1}{{{0.name}}}\url{{{0.url}}}".format(self, nestlevel)
		# print self.id
		return content
