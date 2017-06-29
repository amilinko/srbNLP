import fileinput
import HTMLParser

is_serbian = False
htmlParser = HTMLParser.HTMLParser()

for line in fileinput.input():
    if line.startswith('<p'):
        is_serbian = 'lang="sr"' in line
    elif line == '</p>':
        is_serbian = False
    elif is_serbian:
        if line == '<s>\n':
            empty = True
        elif line == '</s>\n':
            if not empty:
                print ""
        elif line.startswith('<'):
            pass
        else:
            empty = False
            decoded = htmlParser.unescape(line.decode('utf-8'))
            original, diacritic, lemma, pos = decoded.split('\t')
            word = diacritic[0].upper() + diacritic[1:] + "\t" + pos.rstrip() + "\t" + lemma if lemma[0].isupper() else diacritic + "\t" + pos.rstrip() + "\t" + lemma
            print word.encode('utf-8')