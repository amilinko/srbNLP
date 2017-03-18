# Description
This project is a set of tools for extracting, modifying and vectorizing text written in Serbian language.
These are `parse`, `filter`, `stem`, `lemmatize` and `vectorize`. Each one of them is described below.

## Dependencies
Before describing and running the tools, it is highly recommended to install `Pip` as each tool uses external modules. 
### Pip
`Pip` is a package management system used to install and manage software packages written in Python. If you don't have it installed, run:
    
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ [sudo] python get-pip.py

# Usage

## Parse
This tool is used for parsing the data from Serbian Web Corpus (srWaC). The whole corpus is divided into several archives which can be found [here](https://www.clarin.si/repository/xmlui/handle/11356/1063).
This module has one dependency. It uses external module called [xmltodict](http://omz-software.com/pythonista/docs/ios/xmltodict.html) which can be easily installed by running this command:

	$ [sudo] pip install xmltodict
This is a Python module that makes working with XML feel like you are working with JSON. It parses and converts XML files to Python dictionaries.
Now, we can run the parser:

    $ python parse.py <filename> <column>
where `filename` is the path to one of the **srWaC** **xml.gz** archives, and `column` is the number of column to parse. This will print parsed data on `stdout`.
To save parsed data in a file, run (in Linux):

    $ python parse.py <filename> <column> >> parsed_data.txt
	
## Filter
This tool doesn't have any dependency, so we can simply run it:

	$ python filter.py <filename>
where `filename` is the path to input file which contains parsed sentences. This will print filtered data on `stdout`.
To save filtered data in a file, run (in Linux):

	$ python filter.py <filename> >> filtered_data.txt
	
## Parse & Filter
These two scripts can work in parallel. Run this command:

	$ python parse.py <filename> <column> | python filter.py > data.txt
	
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
TO DO
