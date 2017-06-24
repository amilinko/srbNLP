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

def is_english (sentence):
    count = 0
    for word in sentence:
        if len(set(word).intersection(english_letters)) > 0 :
            count = count + 1
            
    return float(count)/len(sentence) > 0.2

def regex_filter (input_text, regex):
    for text in input_text:
        words = text.splitlines()
        line = " ".join([word.split('\t')[0] for word in words])
        line = apply_regex(line, regex)
        sentence = line.split()
        if acceptable(line, sentence):
                print "\n".join([word for word in sentence]).encode('utf-8')
                print ""

def apply_regex (text, regex):
    return re.sub(regex, "", unicode(text, "utf-8"))

def acceptable(line, sentence):
    return len(line) > 10 and len(sentence) > 3 and not is_english(sentence)
    
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
    allowed_punctuation_lem = u".,:;\"\'?!\-"
    allowed_punctuation_stem = u"\'\-"
    digits = "0123456789"

    # Allowed punctuation characters differ when lemmatizing and stemming
    allowed_punctuation = allowed_punctuation_lem if (lem or reldi) else allowed_punctuation_stem
    regex = "[^" + serbian_letters + english_letters + allowed_punctuation + digits + " ]"
    
    # Reading parsed corpus
    with open (inputFile, "r") as fin:
        text = fin.read()
    
    # Filtering for stemmers and lemmatizers
    if stem or lem:
        regex_filter(text.split("\n\n"), regex)
    
    # Filtering after ReLDI lemmatization
    if reldi:
        for txt in text.split("\n\n"):
            sentence = []
            output = []
            words = txt.splitlines()
            for word in words:
                original, POS, lemma = word.split("\t")
                original = apply_regex(original, regex)
                lemma = apply_regex(lemma, regex)
                if original:
                    sentence.append(original)
                    output.append(original + "\t" + POS + "\t" +lemma)
            
            line = " ".join([w for w in sentence])
            if acceptable(line,sentence):
                print "\n".join([o for o in output]).encode('utf-8')
                print ""
                