# This Python file uses the following encoding: utf-8

import fileinput
import re

serbian_letters = u"AaBbVvGgDdĐđEeŽžZzIiJjKkLlMmNnOoPpRrSsTtĆćUuFfHhCcČčŠš"
english_letters = u"QqWwYyXx"
allowed_punctuation = u""

def is_english (sentence):
	count = 0
	for word in sentence:
		if len(set(word).intersection(english_letters)) > 0 :
			count = count + 1
			
	return float(count)/len(sentence) > 0.2

# Filter line by line
for line in fileinput.input():
	line = unicode(line, "utf-8")
	line = re.sub("[^" + serbian_letters + english_letters + allowed_punctuation + " ]", "", line)
	sentence = line.split()
	if len(line) > 10 and len(sentence) > 3 and len(sentence) < 128 and not is_english(sentence):
		print " ".join([word for word in sentence]).encode('utf-8')
        
        