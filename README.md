# SEC Form Web Scrape and Text Analysis

Project aims to parse and analyze the text of SEC financial regulation forms.
These types of formal documents are lengthyThere are three import parts to this project.
  1) Scraping of SEC PDF Forms from their website.
  2) Converting the PDFs to text.
  3) Analyzing the text for patterns and actionable items.
Actionable here means that a company can implement this particular phrase into a policy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

A standard Python environment needs the following packages installed
  * spacy
  * pdfMiner.six
  * nltk
  * urllib3
  * pandas

### Installing

Running 'python Parse_SEC_Forms.py' in any python enabled shell will start the code.
The output will be a frequency distribution of the first 50 forms. 
More forms than this will cause a memory error for systems with 16Gb of RAM.

The following is a sample of the output

| Rank     | Lemma              | Raw Count |
| -------- | ------------------ | --------- |
| 1        | form               | 2168
| 2        | security           | 1701
| 3        | -pron-             | 1628
| 4        | information        | 1537
| 5        | item               | 1368
|...       |...                 |...
| 45       | respect            | 366
| 46       | business           | 361
| 47       | asset              | 352
| 48       | requirement        | 349
| 49       | make               | 340
| 50       | dealer             | 335



## Built With

* Atom Text Editor

## Authors

* **Jonah Woods** - *Initial work* - https://github.com/jonahwoods95

## Acknowledgments

* Raja Sooriamurthi, Carnegie Mellon University instructor 
  -> base code for scrapy web scraping was given by Dr. Sooriamurthi in CMU-95885 -- Data Science and Big Data
