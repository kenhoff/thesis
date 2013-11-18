import json

def basic():
	content = "\subsection{Basic Survey}"
	survey = json.loads(open('./turk_stuff/basic.json', 'r').read())
	for question in survey['questions']:
		if (question['id'] == 'survey'):
			content += rubric()
		else:
			content += "\subsubsection{" + question['text'] + '}'
			if (question['type'] == 'likert'):
				content += "\\begin{itemize} \item Strongly Agree \item Agree \item Disagree \item Strongly Disagree \end{itemize}"
			if (question['type'] == 'freeform'):
				content += " (An empty text box where workers can write anything) "
			if (question['type'] == 'number'):
				content += " (An empty text box where workers can only enter numbers) "
			if (question['id'] == 'gender'):
				content += "\\begin{itemize} \item Male \item Female \end{itemize}"

		# print question
	open('survey2.tex', 'w').write(content)

def rubric():
	content = "\subsection{Rubric}"
	rubric = json.loads(open('rubric_information.json', 'r').read())
	for item in rubric['rubricitems']:
		content += "\subsubsection{" + item['prompt'] + '} \\begin{enumerate}'
		for scaleitem in item['scale']:
			content += " \item " + scaleitem['description']
		content += "\\end{enumerate}"

	return content

def quizgen(gameid):
	content = "\subsection{" + gameid + " Quiz}"
	quiz = json.loads(open('./turk_stuff/{}.json'.format(gameid), 'r').read())
	for question in quiz['questions']:
		scrub = question['text'].replace('{', '\{').replace('}', '\}').replace('"', '\\"').replace('&', '\&').replace('\n', ' ')
		content += "\subsubsection{" + scrub + "} \\begin{enumerate}"
		for answer in question['options']:
			content += " \item " + answer['text']
		content += "\end{enumerate}"
	open('{}.tex'.format(gameid), 'w').write(content)

def lightbotquizgen():
	content = "\subsection{Lightbot Quiz}"
	quiz = json.loads(open('./turk_stuff/{}.json'.format("lightbot"), 'r').read())
	for question in quiz['questions']:
		scrub = question['text'].replace('{', '\{').replace('}', '\}').replace('&', '\&')
		# scrub = "Examine the following code: \n\n int count = 0; \n while ( count \&lt;= 6 ) \n \{ \n System.out.print( count + \" \" ); \n count = count + 2; \n\} \n System.out.println(  ); \n\n What does this code print on the monitor?"
		content += " \subsubsection{} " + scrub + " \\begin{enumerate} "
		for answer in question['options']:
			content += " \item " + answer['text']
		content += " \end{enumerate} "
	open('{}.tex'.format('lightbot'), 'w').write(content)

basic()
quizgen('darfur')
quizgen('munchers')
lightbotquizgen()
quizgen('oregon')