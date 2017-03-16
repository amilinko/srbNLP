## Dependencies
There are several dependencies which are used in this project. 
### Pip
`Pip` is a package management system used to install and manage software packages written in Python. If you don't have it installed, run:
    
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ [sudo] python get-pip.py

### xmltodict
This is a Python module that makes working with XML feel like you are working with JSON. It parses and converts XML files to Python dictionaries. To install, run:

    $ [sudo] pip install xmltodict
### Usage
    python parse.py <filename> <column>
where `filename` is one of the **srWaC** **xml.gz** archives, and `column` is the number of column to parse. 
