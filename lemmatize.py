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
    INPUT_FILENAME = os.path.basename(os.path.splitext(inputFile)[0])
        
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
        
        # File names
        POS_OUT = TMP + "/PosOut_" + INPUT_FILENAME + "_"
        POS_OUT_TAGGED = POS_OUT + "Tagged.txt"
        LEMMA_OUT = TMP + "/LemmaOut_" + INPUT_FILENAME + "_"
        LEMMA_OUT_TAGGED = LEMMA_OUT + "Tagged.txt"
        LEMMAS_DECODED = TMP + "/DecodedLemmas_" + INPUT_FILENAME + ".txt"
        
        # Check if Btagger.jar exists in the current directory
        if(not os.path.isfile(BTAGGER)):
            print ("Downloading BTagger.jar...")
            urllib.urlretrieve ("http://clcl.unige.ch/btag/BTagger.jar", BTAGGER)
            
        # Run POS tagger
        print "Running Pos tagger"
        call(("java -cp BTagger.jar bTagger/BTagger -p " + POS_OUT).split() + [inputFile,POS_WEIGHT,POS_SCRIPT], shell=is_windows)
        
        # Run lemmatizer
        print "Running Lemmatizer"
        call(("java -cp BTagger.jar bTagger/BTagger -p " + LEMMA_OUT).split() + [POS_OUT_TAGGED, LEMMA_WEIGHT,LEMMA_SCRIPT], shell=is_windows)
        
        # Decode lemma tags
        print "Decoding lemma tags"
        decodeBTaggerLemmaTags (LEMMA_OUT_TAGGED, LEMMAS_DECODED)
        
        # Parse decoded lemmatized input and prepare for vectorization
        print "Parsing decoded lemmas"
        parseDecodedLemmas(LEMMAS_DECODED, outputFile, filter_btagger)
    
    # CSTLemma
    if (arguments["CSTLemma"]):
        if (is_windows):
            print "This lemmatizer can only be run on Linux system! Aborting!"
            sys.exit(-1)
        else:
            
            from utils.common import filter_cst
            
            # CSTLemma arguments
            HUNPOS_SETTINGS = arguments["<HunPos_settings>"]
            DICTIONARY = arguments["<Dictionary>"]
            PATTERNS = arguments["<Patterns>"]
            
            # File names
            POS_OUT_TAGGED = TMP + "/PosOutTaggedCST_" + INPUT_FILENAME + ".txt"
            POS_OUT_TAGGED_EOL = TMP + "/PosOutTaggedCST_EOL_" + INPUT_FILENAME + ".txt"
            LEMMAS_DECODED = TMP + "/CSTDecodedLemmas_" + INPUT_FILENAME + ".txt"
            LEMMAS_DECODED_CLEAN = TMP + "/CSTDecodedLemmasClean_" + INPUT_FILENAME + ".txt"
            
            # Run HunPos tagger
            print "Running HunPos tagger"
            call("cat " + inputFile + " | hunpos-tag " + HUNPOS_SETTINGS + " > " + POS_OUT_TAGGED , shell=True)
            
            # Adding <EOL> tags so sentences can be separated after CST lemmatizing
            print "Adding <EOL> tags"
            call("cat " + POS_OUT_TAGGED + " | sed -r 's/^$/<EOL>\t<EOL>\t/g' > " + POS_OUT_TAGGED_EOL, shell=True)
            
            # Run CST lemmatizer
            print "Running CST lemmatizer"
            call(["cstlemma", "-L", "-i", POS_OUT_TAGGED_EOL, "-I", "$w\\t$t\\t\\n", "-d", DICTIONARY, "-f", PATTERNS, "-eU", "-o", LEMMAS_DECODED, "-t", "-H0", "-u", "-U"])
            
            # Removing <EOL> tags
            print "Removing <EOL> tags"
            call("cat " + LEMMAS_DECODED + " | sed -r 's/<EOL>\t<EOL>\t<EOL>//g' > " + LEMMAS_DECODED_CLEAN, shell=True)
            
            # Parse decoded lemmas
            print "Parsing decoded lemmas"
            parseDecodedLemmas(LEMMAS_DECODED_CLEAN, outputFile, filter_cst)
            
    # ReLDI
    if (arguments["ReLDI"]):
        
        from utils.common import filter_reldi
        parseDecodedLemmas(inputFile, outputFile, filter_reldi)
        
        