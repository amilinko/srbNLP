"""stem.py
 
Usage:
  stem.py <StemmerID> <InputFile> <OutputFile>
  stem.py -h | --help
  stem.py --version
 
Options:
  -h --help              Show this screen.
  --version              Show version.
 
"""

from utils.docopt import docopt

if __name__ == '__main__':
	
	arguments = docopt(__doc__, version="1.0.0")
	
	from subprocess import call
	import urllib, os, platform, fileinput

	# Parse command line arguments
	stemmerID = arguments["<StemmerID>"]
	inputFile = arguments["<InputFile>"]
	outputFile = arguments["<OutputFile>"]
	outputFileStem = outputFile + ".stem"
	
	NUM_TAG = "<NUM>"
	
	is_windows = True if platform.system()=="Windows" else False
	command = "java -jar SCStemmers.jar".split()

	# Check if SCStemmers.jar is in the current directory
	if(not os.path.isfile("SCStemmers.jar")):
		print ("Downloading SCStemmers.jar...")
		urllib.urlretrieve ("https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar", "SCStemmers.jar")
	
	# Call Serbian stemmers jar from Python
	call(command + [stemmerID, inputFile, outputFileStem], shell=is_windows)

	print ("Replacing numbers with <NUM> tags...")
	output = open(outputFile, "w")
	for line in fileinput.input(outputFileStem):
		sentence = [NUM_TAG if word.isdigit() else word for word in line.split()]
		output.write(" ".join(sentence))
		output.write("\n")
		
	output.close()