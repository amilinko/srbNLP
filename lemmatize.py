"""lemmatize.py
 
Usage:
  lemmatize.py BTagger <InputFile> <OutputFile> <PoS_scr> <PoS_fea> <Lem_scr> <Lem_fea>
  lemmatize.py -h | --help
  lemmatize.py --version
 
Options:
  -h --help              Show this screen.
  --version              Show version.
 
"""

from utils.docopt import docopt

def decodeLemmaTags (inFileName, outFileName):
	
	inFile = codecs.open(inFileName,'r','utf-8')
	outFile = codecs.open(outFileName,'w','utf-8')
	
	for line in inFile:
		words = line.split(' ')
		if len(words) == 3:
			word = words[0]
			tag = words[-1][0:-1]
			if "@*@" in tag:
				prefix_split = tag.split("@*@")
				prefixparts = prefix_split[0].split("#")
				prefix_remove = prefixparts[0][1:]
				prefix_add = prefixparts[1]
				word = word[int(prefix_remove):]
				if len(prefix_add) >= 1:
					word = prefix_add + word
				tag = prefix_split[-1]
			tagparts = tag.split("+")
			tag_remove = tagparts[0]
			tag_add = tagparts[1]
			if int(tag_remove) <= len(word):
				word = word[0:len(word)-int(tag_remove)]
				if len(tagparts[1]) >= 1:
					word = word + tag_add
				outFile.write(word)
			outFile.write("\n")
			
	inFile.close()
	outFile.close()
	
if __name__ == '__main__':
	
	# Parse command line arguments
	arguments = docopt(__doc__, version="1.0.0")
	
	import urllib
	import os
	import sys
	import platform
	import codecs
	
	from subprocess import call
	
	inputFile = arguments["<InputFile>"]
	outputFile = arguments["<OutputFile>"]
	
	is_windows = True if platform.system()=="Windows" else False
	
	# BTagger
	if (arguments["BTagger"]):
		
		# Constants
		BTAGGER = "BTagger.jar"
		TMP = "tmp"
		
		# BTagger arguments
		LEMMA_WEIGHT = arguments["<Lem_fea>"]
		LEMMA_SCRIPT = arguments["<Lem_scr>"]
		POS_WEIGHT = arguments["<PoS_fea>"]
		POS_SCRIPT = arguments["<PoS_scr>"]
		
		# Check if Btagger.jar exists in the current directory
		if(not os.path.isfile(BTAGGER)):
			print ("Downloading BTagger.jar...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/BTagger.jar", BTAGGER)
						
		if(not os.path.isdir(TMP)):
			call(["mkdir", TMP], shell=is_windows)
			
		# Run POS tagger
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/PosOut".split() + [inputFile,POS_WEIGHT,POS_SCRIPT], shell=is_windows)
		
		# Run lemmatizer
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/LemmaOut".split() + ["tmp/PosOutTagged.txt",LEMMA_WEIGHT,LEMMA_SCRIPT], shell=is_windows)
		
		# Decode lemma tags
		decodeLemmaTags ("tmp/LemmaOutTagged.txt", outputFile)
		