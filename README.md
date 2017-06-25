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
	
The ouput is in format:
`word`    `POStag`    `lemma`

## Filter
This tool is used for filtering the data (usually output from `parse` tool). Only English and Serbian latin alphabet letters are allowed. 
To run, type:

	$ filter.py (-l | -s | --ReLDI) <InputFile>
where `InputFile` is the path to input file which contain parsed sentences (usually the output from `parse.py`. This will print filtered data on `stdout`.
Allowed characters differ in stemming and lemmatizing, so `-l` parameter means that input file will be filtered for lemmatizers, where `-s` means that it will be done for stemmers.
The `--ReLDI` parameter is passed when the input data is already lemmatized (by **ReLDI**) and needs to be filtered.
To save filtered data in a file, run:

	$ python filter.py (-l | -s | --ReLDI) <InputFile> > filtered_data.txt
	
## Stem
This tool is a Python wrapper around the collection of 4 stemmers for Serbian language which are taken from [here](https://github.com/vukbatanovic/SCStemmers).
This tool has one dependency which is the **jar** archive of all 4 stemmers. To download it, run this command (in Linux):

	$ wget https://github.com/vukbatanovic/SCStemmers/releases/download/v1.0.0/SCStemmers.jar
Make sure that this archive is located in the same directory as the `stem` tool.
Now, let's run the stemmer:

	$ python stem.py <StemmerID> <InputFile> <OutputFile>
where the command line arguments are the same as they are described [here](https://github.com/vukbatanovic/SCStemmers#command-line-interface).

## Lemmatize
This tool is a Python wrapper around 3 lemmatizers: **BTagger**, **CSTLemma** and **ReLDI**. Besides wrapping, this tool does the final filtering before it can be sent to vectorization tool.
This tool can be used in several ways.

### BTagger
    $ lemmatize.py BTagger <InputFile> <OutputFile> <PoS_scr> <PoS_fea> <Lem_scr> <Lem_fea>

When running this command, the **BTagger** is started. If it doesn't exist in the current directory, it will be automatically downloaded from internet. 
`InputFile` is the filtered data produced from `filter.py` using `-l` option. `OutputFile` is the name of the file where the final lemmatized and filtered data will be stored. This is the input in the vectorization tool.
`PoS_scr`, `PoS_fea`, `Lem_scr` and `Lem_fea` can be downloaded from [here](http://clcl.unige.ch/btag/param/sr/). Another set of these files is under `xxx` directory in the page linkd above.

### CSTLemma
    $ lemmatize.py CSTLemma <InputFile> <OutputFile>
    
*TODO*

### ReLDI
    $ lemmatize.py ReLDI <InputFile> <OutputFile>

This command doesn't run **ReLDI** lemmatizer, but only parses and filters it. The reason is because Serbian Corpus is already lemmatized by **ReLDI**, so there is no reason to run it again.
`InputFile` is the filtered data produced from `filter.py` using `--ReLDI` option. The format of the `InputFile` is the same as other lemmatizers produce.
`Output` is the name of the file where the final lemmatized and filtered data will be stored.

## Vectorize
This tool is used to generate vectors for each word in the input set of sentences. It is basically a wrapper around `gensim word2vec` module. To install `gensim` package, follow the instructions from this [link](https://radimrehurek.com/gensim/install.html).
To run this tool, type:

	$ python vectorize.py [--size=<dimension>] [--min_count=<number>] [--workers=<number>] --input=<file> --output=<file>
where `input` is the path to the file which contains preprocessed sentences using one (or more) of the tools described above. `output` is the name of the file where the `word2vec` model will be saved. The model will be saved as a simple text file.
