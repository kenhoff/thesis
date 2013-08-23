import games

games.generateGameSummaryDict()

content = "data"

f = open('KenHoffThesis.tex', 'w')
f.write('\documentclass{article}')
f.write('\\begin{document}')
f.write(content)
f.write('\end{document}')