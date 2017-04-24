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

if __name__ == '__main__':
	
	# Parse command line arguments
	arguments = docopt(__doc__, version="1.0.0")
	
	import urllib
	import os
	import sys
	import platform
	
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
		call("java  -cp BTagger.jar LCS_WDiff2L  tmp/LemmaOutTagged.txt".split() + [outputFile, "1", "3"], shell=is_windows)
		