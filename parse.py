import sys
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

# Parse command line arguments
if len(sys.argv)<>3:
	print "Usage: python parse.py <filename> <column>"
	sys.exit(1)

filename = sys.argv[1]
column = int(sys.argv[2])

# Parse in streaming mode
xmltodict.parse(GzipFile(filename), item_depth=2, item_callback=handle, dict_constructor=dict)