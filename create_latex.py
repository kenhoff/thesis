from games import Game, GameList
content = ""

content += GameList('game_summaries').latex_output("subsection")

f = open('GameSummaries.tex', 'w')
f.write(content)
f.close()


from rubric import Rubric, RubricItem

content = ""

content += Rubric('rubric_information').latex_output("subsection")

f = open('Rubric.tex', 'w')
f.write(content)
f.close()