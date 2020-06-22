# ELEN4020 - Course Project: Indexing XML Hansards
This repository contains the implementation of a XML Indexing program for the [Akomo Ntoso](http://docs.oasis-open.org/legaldocml/ns/akn/3.0) schema

- The XML dataset is contained in: `SenateHansard1979vol2.xml`
- The output of the XML parser will be stored in two respecitive csv files: `debatesBySpeakers.csv` & `speakersInDebates.csv`
- The output Bit Map will be stored in: `map.txt`


## Build Instructions
The algorithms for this lab is written in Python 3.6
The requirements for the virtual environment can be found in requirements.txt

Please ensure that the following are installed:
- `Python 3.6+`
- `pip3`
- `virtualenv`

1. Create a virtual environment
`virtualenv venv`

2. Activate the virtual environment:
`source venv/bin/activate`

3. Install the requirements for the virtual environment:
`pip3 install -r requirements.txt`

4. To deactive the virtual environment:
`deactivate`


## Commands to run the XML Indexing Algorithm:
- xml_Indexing: `python3 xml_Indexing.py`