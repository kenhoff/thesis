import xml.dom.minidom, json

xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd"></QuestionForm>"""


def main():


	# basic survey
	f = open('./turk_stuff/basic.json', 'r')

	survey = json.loads(f.read())

	xml = "  <Overview><Title>Survey</Title></Overview>"

	for question in survey['questions']:
		xml += convert_question_to_xml(question)

	f.close()

	new_xml = """<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">""" + xml + """</QuestionForm>"""

	write_to_survey(new_xml, "basic")




	# complicated surveys
	quizzes = [	'oregon',
				'lightbot',
				'darfur',
				'munchers',
				]

	for quiz in quizzes:
		quiz_xml = "  <Overview><Title>Quiz</Title><Text>Without using outside resources (e.g. looking things up on the internet or using a calculator), please answer the following questions to the best of your ability.</Text></Overview>"
		f = open('./turk_stuff/' + quiz + '.json', 'r')
		quiz_json = json.loads(f.read())

		for question in quiz_json['questions']:
			quiz_xml += convert_question_to_xml(question)

		write_to_survey("""<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">""" + quiz_xml + xml + quiz_xml + """</QuestionForm>""", quiz)

		f.close()


def write_to_survey(xml_string, title):
	f = open('./turk_stuff/' + title + '.question', 'w') # survey.question is an XML file, indicating questions for turkers to answer

	# print xml_string
	xml_stuff = xml.dom.minidom.parseString(xml_string)

	# production/oneline mode
	f.write("""<?xml version="1.0" encoding="UTF-8"?>""" + xml_string)

	# debug/prettyprinted mode
	print xml_stuff.toprettyxml()

	f.close()

def convert_question_to_xml(question):
	if (question['id'] == 'survey'): return rubric()
	content = "<Question>" + question_identifier(question['id']) + required(question['required']) + questiontext(question['text']) + options(question)

	content += "</Question>"
	return content


def question_identifier(id):
	return "<QuestionIdentifier>" + str(id) + "</QuestionIdentifier>"

def required(required):
	if (required == 1): val = "true"
	else: val = "false"
	return "<IsRequired>" + val + "</IsRequired>"

def questiontext(text):
	return "<QuestionContent><Text>" + text + "</Text></QuestionContent>"

def options(question):

	content = "<AnswerSpecification>"
	if (question['type'] == "multiple-choice"):
		content += "<SelectionAnswer><MinSelectionCount>1</MinSelectionCount><MaxSelectionCount>1</MaxSelectionCount><StyleSuggestion>radiobutton</StyleSuggestion><Selections>"
		for option in question['options']:
			content += "<Selection>"
			content += "<SelectionIdentifier>" + str(option['id']) + "</SelectionIdentifier>"
			content += "<Text>" + option['text'] + "</Text>"
			content += "</Selection>"

		content += "</Selections></SelectionAnswer>"

	if (question['type'] == 'number'):
		content += "<FreeTextAnswer><Constraints><IsNumeric /></Constraints><DefaultText></DefaultText><NumberOfLinesSuggestion>1</NumberOfLinesSuggestion></FreeTextAnswer>"

	if (question['type'] == 'likert'):
		content += "<SelectionAnswer><MinSelectionCount>1</MinSelectionCount><MaxSelectionCount>1</MaxSelectionCount><StyleSuggestion>radiobutton</StyleSuggestion><Selections><Selection><SelectionIdentifier>StronglyAgree</SelectionIdentifier><Text>Strongly Agree</Text></Selection><Selection><SelectionIdentifier>Agree</SelectionIdentifier><Text>Agree</Text></Selection><Selection><SelectionIdentifier>Disagree</SelectionIdentifier><Text>Disagree</Text></Selection><Selection><SelectionIdentifier>Stronglydisagree</SelectionIdentifier><Text>Strongly Disagree</Text></Selection></Selections></SelectionAnswer>"

	if (question['type'] == 'freeform'):
		content += "<FreeTextAnswer><DefaultText></DefaultText></FreeTextAnswer>"


	content += "</AnswerSpecification>"
	return content

def rubric():
	content = "<Overview><Title>Game</Title><Text>For the following questions, please refer to this game.</Text><Text>${gameurl}</Text></Overview>"
	f = open('rubric_information.json', 'r')
	rubric = json.loads(f.read())
	for item in rubric['rubricitems']:
		content += "<Question>"
		content += "<QuestionIdentifier>" + item['id'] + "</QuestionIdentifier>"
		content += "<IsRequired>true</IsRequired>"
		content += "<QuestionContent><Title>" + item['name'] + "</Title><Text>" + item['prompt'] + "</Text></QuestionContent>"
		content += "<AnswerSpecification><SelectionAnswer><MinSelectionCount>1</MinSelectionCount><MaxSelectionCount>1</MaxSelectionCount><StyleSuggestion>radiobutton</StyleSuggestion><Selections>"

		for scale_item in item['scale']:
			content += "<Selection><SelectionIdentifier>" + str(scale_item['value']) + "</SelectionIdentifier><Text>" + scale_item['description'] + "</Text></Selection>"


		content += "</Selections></SelectionAnswer></AnswerSpecification>"
		content += "</Question>"
	return content






main()
