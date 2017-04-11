from subprocess import call
import sys
import urllib
import os
import platform

# Parse command line arguments
if len(sys.argv)<>4:
	print "Usage: python stem.py <StemmerID> <InputFile> <OutputFile>"
	sys.exit(1)

is_windows = True if platform.system()=="Windows" else False
command = "java -jar SCStemmers.jar".split()
arguments = sys.argv[1:]

# Check if SCStemmers.jar is in the current directory
if(not os.path.isfile("SCStemmers.jar")):
	urllib.urlretrieve ("https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar", "SCStemmers.jar")
	
# Call Serbian stemmers jar from Python
call(command + arguments, shell=is_windows)
