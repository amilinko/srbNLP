"""stem.py
 
Usage:
  stem.py <StemmerID> <InputFile> <OutputFile> [<StemOutput>]
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
    from utils.common import NUM_TAG

    # Parse command line arguments
    stemmerID = arguments["<StemmerID>"]
    inputFile = arguments["<InputFile>"]
    outputFile = arguments["<OutputFile>"]
    outputFileStem = outputFile + ".stem" if arguments["<StemOutput>"]==None else arguments["<StemOutput>"]
    
    is_windows = True if platform.system()=="Windows" else False
    command = "java -jar SCStemmers.jar".split()

    # Check if SCStemmers.jar is in the current directory
    if(not os.path.isfile("SCStemmers.jar")):
        print ("Downloading SCStemmers.jar...")
        urllib.urlretrieve ("https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar", "SCStemmers.jar")
    
    # Call Serbian stemmers jar from Python
    print ("Running stemmer. Output of stemmer will be saved to " + outputFileStem + ".")
    call(command + [stemmerID, inputFile, outputFileStem], shell=is_windows)

    print ("Replacing numbers with <NUM> tags...")
    output = open(outputFile, "w")
    for line in fileinput.input(outputFileStem):
        sentence = [NUM_TAG if word.isdigit() else word for word in line.split()]
        output.write(" ".join(sentence))
        output.write("\n")
        
    output.close()