# This Python file uses the following encoding: utf-8

"""filter.py
 
Usage:
  filter.py (-l | -s | --ReLDI) <InputFile>
  filter.py -h | --help
  filter.py --version
 
Options:
  -l           Filter input for lemmatizator
  -s           Filter input for stemmer
  --ReLDI      Filter input text after ReLDI lemmatization
  -h --help    Show this screen.
  --version    Show version.
 
"""

import re
from utils.docopt import docopt
from utils.common import isNumber, isURL, NUM_TAG, URL_TAG

en_stop_words = [
    "of", "is", "so", "the", "for", "it", "as", "an", "when", "were", "was", 
    "who", "are", "am", "by", "this", "but", "or", "and", "be", "he", "her", 
    "him", "over", "in", "you", "she", "we", "why", "what", "how", "not",
    "that", "my", "your", "hers", "one", "did", "does", "there", "here",
    "has", "once", "because", "about", "must", "will", "shall", "should",
    "may", "can", "could", "might", "whom", "whose", "up", "over"]

def is_english (sentence):
    count = 0
    for word in sentence:
        if len(set(word).intersection(english_letters)) > 0 or (word in en_stop_words):
            count = count + 1
            
    return float(count)/len(sentence) > 0.2

def regex_filter (input_text, regex):
    global stem, lem, reldi
    
    for paragraph in input_text.split("\n\n"):
        sentence = []
        output = []
        words = paragraph.splitlines()
        for word in words:
            original, POS, lemma = word.split("\t")
            
            # Stemmer replacing tags and filtering
            if stem:
                if isNumber(original):
                    original = NUM_TAG
                elif isURL(original):
                    original = URL_TAG
                else:
                    original = apply_regex(original, regex)
            
            # Lemmatizer filtering
            else:
                original = apply_regex(original, regex)
            
            # Appending words to create sentence
            if original:
                sentence.append(original)
                if reldi:
                    lemma = apply_regex(lemma, regex)
                    output.append(original + "\t" + POS + "\t" +lemma)
        
        # Pring out the result
        if acceptable(sentence):
            if reldi:
                print "\n".join([o for o in output]).encode('utf-8')
                print ""
            elif stem:
                print " ".join([s for s in sentence]).encode('utf-8')
            else:
                print "\n".join([s for s in sentence]).encode('utf-8')
                print ""
            
def apply_regex (text, regex):
    return re.sub(regex, "", unicode(text, "utf-8"))

def acceptable(sentence):
    return len(sentence) > 0 and not is_english(sentence)
    
if __name__ == '__main__':
    
    # Parse command line arguments
    arguments = docopt(__doc__, version="1.0.0")

    inputFile = arguments["<InputFile>"]
    lem = arguments["-l"]
    stem = arguments["-s"]
    reldi = arguments["--ReLDI"]
    
    # Letters, digits and characters used in filtering
    serbian_letters = u"AaBbVvGgDdĐđEeŽžZzIiJjKkLlMmNnOoPpRrSsTtĆćUuFfHhCcČčŠš"
    english_letters = u"QqWwYyXx"
    allowed_punctuation_lem = u".,:;\"\'?!\-/"
    allowed_punctuation_stem = u"\'\-"
    digits = "0123456789"

    # Allowed punctuation characters differ when lemmatizing and stemming
    allowed_punctuation = allowed_punctuation_lem if (lem or reldi) else allowed_punctuation_stem
    regex = "[^" + serbian_letters + english_letters + allowed_punctuation + digits + " ]"
    
    # Reading parsed corpus
    with open (inputFile, "r") as fin:
        text = fin.read()
    
    # Apply filter
    regex_filter(text, regex)
                