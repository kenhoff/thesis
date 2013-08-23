def generateGameSummaryDict():
	f = open('game_summaries', 'r')
	content = f.read()
	result = []
	gameArray = content.split('\n\n')
	for game in gameArray:
		gameInfo = {}
		info = game.split('\n')
		gameInfo['name'] = info[0]
		result.append(gameInfo)
	print result
