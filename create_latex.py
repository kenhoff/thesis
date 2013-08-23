from games import Game, GameList
content = ""

content += GameList('game_summaries').latex_output("subsubsection")

f = open('GameSummaries.tex', 'w')
f.write(content)
f.close()
