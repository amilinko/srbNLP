"""vectorize.py
 
Usage:
  vectorize.py [--size=<dimension>] [--min_count=<number>] [--workers=<number>] --input=<file> --output=<file>
  vectorize.py -h | --help
  vectorize.py --version
 
Options:
  --size=<dimension>     The dimension of word vector [default: 100].
  --min_count=<number>   Ignore all words with total frequency lower than this [default: 5].
  --workers=<number>     The dimension of word vector [default: 1].
  --input=<file>         File which contains preprocessed sentences.
  --output=<file>        File where word2vec model is saved.
  -h --help              Show this screen.
  --version              Show version.
 
"""

from utils.docopt import docopt

class Sentences(object):
	def __init__(self, filename):
		self.filename = filename
 
	def __iter__(self):
		for line in open(self.filename):
			yield line.split()

if __name__ == '__main__':

	import gensim, logging
	
	# Parse command line arguments
	arguments = docopt(__doc__, version="1.0.0")

	inputFile = arguments['--input']
	outputFile = arguments['--output']
	dimension = int(arguments['--size'])
	count = int(arguments['--min_count'])
	processes = int(arguments['--workers'])
	
	# Set up logging and message format
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	# Vectorize input sentences
	sentences = Sentences(inputFile)
	model = gensim.models.Word2Vec(sentences, size=dimension, min_count=count, workers=processes)

	# Save model in a txt format
	model.wv.save_word2vec_format(outputFile, binary=False)