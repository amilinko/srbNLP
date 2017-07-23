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
    import urllib, os, platform

    # Parse command line arguments
    stemmerID = arguments["<StemmerID>"]
    inputFile = arguments["<InputFile>"]
    outputFile = arguments["<OutputFile>"]
    
    is_windows = True if platform.system()=="Windows" else False
    command = "java -jar SCStemmers.jar".split()

    # Check if SCStemmers.jar is in the current directory
    if(not os.path.isfile("SCStemmers.jar")):
        print ("Downloading SCStemmers.jar...")
        urllib.urlretrieve ("https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar", "SCStemmers.jar")
    
    # Call Serbian stemmers jar from Python
    print ("Running stemmer. Output of stemmer will be saved to " + outputFile + ".")
    call(command + [stemmerID, inputFile, outputFile], shell=is_windows)
