import docopt
import xmltodict
from gzip import GzipFile

global column

def parse_sentences(sentences, column):
	for sentence in sentences:
		text = sentence if type(sentence) is unicode else sentence['#text']
		lines = text.split('\n')
		parsed = [line.split()[column] for line in lines if line]
		print " ".join(parsed).encode('utf-8')
	
def handle(path, item):
	lang = path[1][1]['lang']
	sentences = item['s'] if (lang == 'sr') and (item['s'] is not None) else []
	
	if type(sentences) is not list:
		sentences = [sentences]
	
	parse_sentences (sentences, column)
	return True
	
file = '../srWaC/gz/srWaC1.1.01.xml.gz'
#file = '../srWaC/gz/small.xml.gz'

column = 0

xmltodict.parse(GzipFile(file), item_depth=2, item_callback=handle, dict_constructor=dict)