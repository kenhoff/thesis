import dicttoxml, json
from xml.dom.minidom import parseString

open('mturk_survey.xml', 'w').write(parseString(dicttoxml.dicttoxml(json.loads(open('mturk_survey.json', 'r').read()))).toprettyxml())