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
	
		
	