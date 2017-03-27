# Description
This project is a set of tools for extracting, modifying and vectorizing text written in Serbian language.
These are `parse`, `filter`, `stem`, `lemmatize` and `vectorize`. Each one of them is described below.

# Usage

## Parse
This tool is used for parsing the data from Serbian Web Corpus (srWaC). The whole corpus is divided into several archives which can be found [here](https://www.clarin.si/repository/xmlui/handle/11356/1063).
To run, type:

    $ python parse.py [<filename>...]
where `filename` is the path to one (or more) **srWaC xml** files(s). This will print parsed data on `stdout`. In case no `filename` is specified, the tool will use `stdin` as input data.
To save parsed data in a file, run:

    $ python parse.py [<filename>...] > parsed_data.txt
	
## Filter
This tool is used for filtering the data (usually output from `parse` tool). Only English and Serbian latin alphabet letters are allowed. 
To run, type:

	$ python filter.py [<filename>...]
where `filename` is the path to one (or more) input file(s) which contain parsed sentences. This will print filtered data on `stdout`. In case no `filename` is specified, the tool will use `stdin` as input data.
To save filtered data in a file, run:

	$ python filter.py [<filename>...] > filtered_data.txt
	
## Parse & Filter
These two scripts can work in parallel. For example:

	$ python parse.py [<filename>...] | python filter.py > data.txt
	
This will parse and filter input data in parallel. The output of `parse.py` will be the input of `filter.py`.

## Stem
This tool is a Python wrapper around the collection of 4 stemmers for Serbian language which are taken from [here](https://github.com/vukbatanovic/SCStemmers).
This tool has one dependency which is the **jar** archive of all 4 stemmers. To download it, run this command (in Linux):

	$ wget https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar
Make sure that this archive is located in the same directory as the `stem` tool.
Now, let's run the stemmer:

	$ python stem.py <StemmerID> <InputFile> <OutputFile>
where the command line arguments are the same as they are described [here](https://github.com/vukbatanovic/SCStemmers#command-line-interface).

## Lemmatize
TO DO

## Vectorize
This tool is used to generate vectors for each word in the input set of sentences. It is basically a wrapper around `gensim word2vec` module. To install `gensim` package, follow the instructions from this [link](https://radimrehurek.com/gensim/install.html).
To run this tool, type:

	$ python vectorize.py [--size=<dimension>] [--min_count=<number>] [--workers=<number>] --input=<file> --output=<file>
where `input` is the path to the file which contains preprocessed sentences using one (or more) of the tools described above. `output` is the name of the file where the `word2vec` model will be saved. The model will be saved as a simple text file.
