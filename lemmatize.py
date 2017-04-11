"""lemmatize.py
 
Usage:
  lemmatize.py btagger <InputFile> <OutputFile>
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
	from subprocess import call
	
	inputFile = arguments["<InputFile>"]
	outputFile = arguments["<OutputFile>"]
	
	# BTagger
	if (arguments["btagger"]):
		
		# Check if Btagger.jar exists in the current directory
		if(not os.path.isfile("BTagger.jar")):
			print ("Downloading BTagger.jar...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/BTagger.jar", "BTagger.jar")
			
		# Check if predefined models for lemmatization and tagging are downloaded
		if(not os.path.isdir("param")):
			call(["mkdir", "param"])
			
		if(not os.path.isfile("param/lem.fea")):
			print ("Downloading lea.fea...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/lem.fea", "param/lem.fea")
			
		if(not os.path.isfile("param/lem.scr")):
			print ("Downloading lem.scr...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/lem.scr", "param/lem.scr")
			
		if(not os.path.isfile("param/pos.fea")):
			print ("Downloading pos.fea...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/pos.fea", "param/pos.fea")
			
		if(not os.path.isfile("param/pos.scr")):
			print ("Downloading pos.scr...")
			urllib.urlretrieve ("http://clcl.unige.ch/btag/param/sr/pos.scr", "param/pos.scr")
			
		if(not os.path.isdir("tmp")):
			call(["mkdir", "tmp"])
			
		# Run POS tagger
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/PosOut".split() + [inputFile,"param/pos.fea","param/pos.scr"])
		
		# Run lemmatizer
		call("java -cp BTagger.jar bTagger/BTagger -p tmp/LemmaOut".split() + ["tmp/PosOutTagged.txt","param/lem.fea","param/lem.scr"])
		
		# Decode lemma tags
		call("java  -cp BTagger.jar LCS_WDiff2L  tmp/LemmaOutTagged.txt".split() + [outputFile, "1", "3"])
		
		
		