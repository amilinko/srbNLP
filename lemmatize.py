"""lemmatize.py
 
Usage:
  lemmatize.py BTagger <InputFile> <OutputFile> <PoS_scr> <PoS_fea> <Lem_scr> <Lem_fea>
  lemmatize.py CSTLemma <InputFile> <OutputFile> <HunPos_settings> <Dictionary> <Patterns>
  lemmatize.py ReLDI <InputFile> <OutputFile>
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
    import platform
    import sys
    
    from subprocess import call
    from utils.common import parseDecodedLemmas
     
    inputFile = arguments["<InputFile>"]
    outputFile = arguments["<OutputFile>"]
    
    is_windows = True if platform.system()=="Windows" else False
    
    # Constants
    BTAGGER = "BTagger.jar"
    TMP = "tmp"
        
    # Create TMP directory for storing intermediate results
    if(not os.path.isdir(TMP)):
            call(["mkdir", TMP], shell=is_windows)
    
    # BTagger
    if (arguments["BTagger"]):
        
        from utils.common import decodeBTaggerLemmaTags, filter_btagger
        
        # BTagger arguments
        LEMMA_WEIGHT = arguments["<Lem_fea>"]
        LEMMA_SCRIPT = arguments["<Lem_scr>"]
        POS_WEIGHT = arguments["<PoS_fea>"]
        POS_SCRIPT = arguments["<PoS_scr>"]
        
        # Check if Btagger.jar exists in the current directory
        if(not os.path.isfile(BTAGGER)):
            print ("Downloading BTagger.jar...")
            urllib.urlretrieve ("http://clcl.unige.ch/btag/BTagger.jar", BTAGGER)
            
        # Run POS tagger
        call(("java -cp BTagger.jar bTagger/BTagger -p " + TMP + "/PosOut").split() + [inputFile,POS_WEIGHT,POS_SCRIPT], shell=is_windows)
        
        # Run lemmatizer
        call(("java -cp BTagger.jar bTagger/BTagger -p " + TMP + "/LemmaOut").split() + [TMP + "/PosOutTagged.txt",LEMMA_WEIGHT,LEMMA_SCRIPT], shell=is_windows)
        
        # Decode lemma tags
        decodeBTaggerLemmaTags (TMP + "/LemmaOutTagged.txt", TMP + "/decodedLemmas.txt")
        
        # Parse decoded lemmatized input and prepare for vectorization
        parseDecodedLemmas(TMP + "/decodedLemmas.txt", outputFile, filter_btagger)
    
    # CSTLemma
    if (arguments["CSTLemma"]):
        if (is_windows):
            print "This lemmatizer can only be run on Linux system! Aborting!"
            sys.exit(-1)
        else:
            # CSTLemma arguments
            HUNPOS_SETTINGS = arguments["<HunPos_settings>"]
            DICTIONARY = arguments["<Dictionary>"]
            PATTERNS = arguments["<Patterns>"]
            
            # Run HunPos tagger
            call("cat " + inputFile + " | hunpos-tag " + HUNPOS_SETTINGS + " > " + TMP + "/PosOutTaggedCST.txt" , shell=True)
            
            # Run CST lemmatizer
            call(["cstlemma", "-L", "-i", TMP + "/PosOutTaggedCST.txt", "-I", "$w\\t$t\\t\\n", "-d", DICTIONARY, "-f", PATTERNS, "-eU", "-o", outputFile, "-t", "-H0", "-l", "-u", "-U"])
            
    # ReLDI
    if (arguments["ReLDI"]):
        
        from utils.common import filter_reldi
        parseDecodedLemmas(inputFile, outputFile, filter_reldi)
        
        