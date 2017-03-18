from subprocess import call
import sys

# Parse command line arguments
if len(sys.argv)<>4:
	print "Usage: python stem.py <StemmerID> <InputFile> <OutputFile>"
	sys.exit(1)

command = "java -jar SCStemmers.jar".split()
arguments = sys.argv[1:]

# Call Serbian stemmers jar from Python
call(command + arguments)
