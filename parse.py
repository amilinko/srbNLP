import collections
import xmltodict
from gzip import GzipFile

def parse_sentence (sentence, column):
	lines = sentence.split('\n')
	parsed = []
	for line in lines:
		words = line.split()
		if len(words) > 0:
			word = words[column]
			parsed.append(word)
		
	print " ".join(parsed).encode('utf-8')
	
def handle(path, item):
	#print (path[1][1]['lang'])
	
	sentence = item['s']
	if type(sentence) is unicode:
		parse_sentence (sentence,0)
	
	if type(sentence) is list:
		for s in sentence:
			if type(s) is unicode:
				parse_sentence(s,0)
			else:
				parse_sentence (s['#text'],0)
	
	if type(sentence) is collections.OrderedDict:
		parse_sentence(sentence['#text'],0)
		
	return True
	
file = '../srWaC/gz/srWaC1.1.01.xml.gz'
#file = '../srWaC/gz/small.xml.gz'

xmltodict.parse(GzipFile(file), item_depth=2, item_callback=handle)