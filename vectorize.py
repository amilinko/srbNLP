import gensim
import sys

class Sentences(object):
	def __init__(self, filename):
		self.filename = filename
 
	def __iter__(self):
		for line in open(self.filename):
			yield line.split()

# Parse command line arguments
if len(sys.argv) <> 3:
	print "Usage: python vectorize.py <InputFile> <OutputFile>"
	sys.exit(1)
	
inputFile, outputFile = sys.argv[1:]

# Vectorize input sentences
sentences = Sentences(inputFile)
model = gensim.models.Word2Vec(sentences, workers=6)

# Save model in a txt format
model.wv.save_word2vec_format(outputFile, binary=False)