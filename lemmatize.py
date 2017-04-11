"""lemmatize.py
 
Usage:
  lemmatize.py BTagger <InputFile> <OutputFile>
  lemmatize.py -h | --help
  lemmatize.py --version
 
Options:
  -h --help              Show this screen.
  --version              Show version.
 
"""

from utils.docopt import docopt

if __name__ == '__main__':
	
	# Parse command line arguments
	arguments = docopt(__doc__, version="1.0.0")
	
	import urllib
	import os
	import sys
	
	from subprocess import call
	
	inputFile = arguments["<InputFile>"]
	outputFile = arguments["<OutputFile>"]
	
	# BTagger
	if (arguments["BTagger"]):
		
		# Constants
		BTAGGER = "BTagger.jar"
		PARAM = "param"
		TMP = "tmp"
		LEMMA_WEIGHT = PARAM + os.sep + "lem.fea"
		LEMMA_SCRIPT = PARAM + os.sep + "lem.scr"
		POS_WEIGHT = PARAM + os.sep + "pos.fea"
		POS_SCRIPT = PARAM + os.sep + "pos.scr"
		
		# Check if Btagger.jar exists in the current directory
		if(not os.path.isfile(BTAGGER)):
			print ("Downloading BTagger.jar...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/BTagger.jar", BTAGGER)
			
		# Check if predefined models for lemmatization and tagging are downloaded
		if(not os.path.isdir(PARAM)):
			call(["mkdir", PARAM])
			
		if(not os.path.isfile(LEMMA_WEIGHT)):
			print ("Downloading lemmatisation weight file...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/lem.fea", LEMMA_WEIGHT)
			
		if(not os.path.isfile(LEMMA_SCRIPT)):
			print ("Downloading lemmatisation script file...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/lem.scr", LEMMA_SCRIPT)
			
		if(not os.path.isfile(POS_WEIGHT)):
			print ("Downloading POS weight file...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/pos.fea", POS_WEIGHT)
			
		if(not os.path.isfile(POS_SCRIPT)):
			print ("Downloading POS script file...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/pos.scr", POS_SCRIPT)
			
		if(not os.path.isdir(TMP)):
			call(["mkdir", TMP])
			
		# Run POS tagger
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/PosOut".split() + [inputFile,"param/pos.fea","param/pos.scr"])
		
		# Run lemmatizer
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/LemmaOut".split() + ["tmp/PosOutTagged.txt","param/lem.fea","param/lem.scr"])
		
		# Decode lemma tags
		call("java  -cp BTagger.jar LCS_WDiff2L  tmp/LemmaOutTagged.txt".split() + [outputFile, "1", "3"])
		