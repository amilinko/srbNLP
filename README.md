## Dependencies
There are several dependencies which are used in this project. 
### Pip
`Pip` is a package management system used to install and manage software packages written in Python. If you don't have it installed, run:
    
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ [sudo] python get-pip.py

### xmltodict
This is a Python module that makes working with XML feel like you are working with JSON. It parses and converts XML files to Python dictionaries. To install, run:

    $ [sudo] pip install xmltodict
## Usage

### Parse
    $ python parse.py <filename> <column>
where `filename` is the path to one of the **srWaC** **xml.gz** archives, and `column` is the number of column to parse. This will print parsed data on `stdout`.
To save parsed data in a file, run (in Linux):

    $ python parse.py <filename> <column> >> parsed_data.txt
	
### Filter
	$ python filter.py <filename>
where `filename` is the path to input file which contains parsed sentences. This will print filtered data on `stdout`.
To save filtered data in a file, run (in Linux):

	$ python filter.py <filename> >> filtered_data.txt
	
### Parse & Filter
These two scripts can work in paralel. Run this command:

	$ python parse.py <filename> <column> | python filter.py > data.txt
	
This will parse and filter input data in parallel. The output of `parse.py` will be the input of `filter.py`.
