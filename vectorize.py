"""vectorize.py
 
Usage:
  vectorize.py [--size=<dimension>] [--min_count=<number>] [--workers=<number>] [--sg=<value>] [--window=<distance>] [--cbow_mean=<value>] [--hs=<value>] [--negative=<value>] <InputFile> <OutputFile>
  vectorize.py -h | --help
  vectorize.py --version
 
Options:
  --size=<dimension>     The dimension of word vector [default: 100].
  --min_count=<number>   Ignore all words with total frequency lower than this [default: 5].
  --workers=<number>     The dimension of word vector [default: 1].
  --sg=<value>           Training algorithm. 0 is CBOW, 1 is skip-gram [default: 0].
  --window=<distance>    The maximum distance between the current and predicted word within a sentence [default: 5].
  --cbow_mean=<value>    If 0, use the sum of the context word vectors. If 1,use the mean. Only applies when cbow is used [default: 1].
  --hs=<value>           If 1, hierarchical softmax will be used for model training. If set to 0, and negative is non-zero, negative sampling will be used [default: 0].
  --negative=<value>     If > 0, negative sampling will be used, the int for negative specifies how many "noise words" should be drawn (usually between 5-20). If set to 0, no negative samping is used. [default: 5].
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

	inputFile = arguments["<InputFile>"]
	outputFile = arguments['<OutputFile>']
	_size = int(arguments['--size'])
	_min_count = int(arguments['--min_count'])
	_workers = int(arguments['--workers'])
	_sg = int(arguments['--sg'])
	_window = int(arguments['--window'])
	_cbow_mean = int(arguments['--cbow_mean'])
	_hs = int(arguments['--hs'])
	_negative = int(arguments['--negative'])
	
	# Set up logging and message format
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	# Vectorize input sentences
	sentences = Sentences(inputFile)
	model = gensim.models.Word2Vec(sentences, size=_size, min_count=_min_count, workers=_workers, sg=_sg, window=_window, cbow_mean=_cbow_mean, hs=_hs, negative=_negative)

	# Save model in a txt format
	model.wv.save_word2vec_format(outputFile, binary=False)
