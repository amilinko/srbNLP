import codecs

def tokenize (inputFile, outputFile):
	
	with open (inputFile, "r") as fin:
		lines = fin.readlines()
	
	sentences = []
	for line in lines:
		sentences.append("\n".join([word for word in line.split()]))
	
	with open (outputFile, "w") as fout:
		fout.write("\n\n".join(sentences))
		
def glue (inputFile, outputFile):
	
	with open (inputFile, "r") as fin:
		text = fin.read()
	
	lines = [line.replace('\n', ' ') for line in text.split("\n\n")]
	
	with open (outputFile, "w") as fout:
		fout.write('\n'.join(lines))
	
def decodeBTaggerLemmaTags (inFileName, outFileName):
	
	inFile = codecs.open(inFileName,'r','utf-8')
	outFile = codecs.open(outFileName,'w','utf-8')
	
	for line in inFile:
		words = line.split(' ')
		if len(words) == 3:
			word = words[0]
			tag = words[-1][0:-1]
			if "@*@" in tag:
				prefix_split = tag.split("@*@")
				prefixparts = prefix_split[0].split("#")
				prefix_remove = prefixparts[0][1:]
				prefix_add = prefixparts[1]
				word = word[int(prefix_remove):]
				if len(prefix_add) >= 1:
					word = prefix_add + word
				tag = prefix_split[-1]
			tagparts = tag.split("+")
			tag_remove = tagparts[0]
			tag_add = tagparts[1]
			if int(tag_remove) <= len(word):
				word = word[0:len(word)-int(tag_remove)]
				if len(tagparts[1]) >= 1:
					word = word + tag_add
				outFile.write(words[0] + '\t' + words[1] + '\t' + word)
				outFile.write('\n')
		
		if line == '\n':
			outFile.write('\n')
			
	inFile.close()
	outFile.close()
	
def parseDecodedLemmas (decodedLemmas, output):
	
	with open (decodedLemmas, "r") as fin:
		decoded = fin.read()
	
	sentences = []
	for line in decoded.split("\n\n"):
		words = line.splitlines()
		sentences.append(" ".join([word.split('\t')[2] for word in words]))
		
	lines = [line.replace('\n', ' ') for line in decoded.split("\n\n")]
	with open (output, "w") as fout:
		fout.write('\n'.join(sentences))
		
	