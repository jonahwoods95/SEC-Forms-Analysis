import pandas as pd
from subprocess import PIPE, run
import urllib3
from collections import Counter
import re
from operator import itemgetter
import nltk
from nltk.corpus import stopwords
import spacy
import os
import time
import SEC_Forms_to_Text

'''
Parse_SEC_Forms.main() requires that a set of text files are located in text_forms directory.
Goal is to analyze text for patterns and predict actionable items within the forms.
"Actionable" here describes goals, processes, requirements, etc. for a company to implement.
'''

def clean_text(text):
    '''TODO: implement cleaning method to speed up spaCy NLP
    '''

    return clean_forms


def run_nlp(forms, num_forms=50):
    '''Runs spaCy natural language processing on all forms
    as one text file.

    Keyword arguments:
    forms -- forms as text files to be parsed
    num_forms -- number of forms to be included in spaCy nlp parser (default=50)
        -> more that 50 consumes approximately 30Gb of space.
    '''

    print('\n\n\nRunning natural language processing using spaCy...')
    print('This will take a while (up to 10 minutes)...\n\n\n')

    #join the files together
    #spaCy takes too much memory to run nlp on all forms at once
    #we can only run nlp on 50 with a reason amount of memory
    all_text = ''.join(forms[:num_forms])

    txt_file_name = "all_text_file"

    #if file exists, do not rewrite the file
    if not os.path.isfile(txt_file_name):
        file = open(txt_file_name, 'w')
        file.write(all_text)

    #use spacy nlp english
    nlp = spacy.load('en')
    #extend the text length because the text is quite large
    nlp.max_length = 7000000

    #if spacy hasn't parsed text,
    #then parse the text
    if not os.path.isfile('nlp_all_text'):
        print('Text has already been parsed')
        parsed_text = nlp(all_text)
        parsed_text.to_disk('nlp_all_text')

    #if spacy has parsed text,
    #then only need to read the file on disk
    else:
        parsed_text = spacy.tokens.Doc(nlp.vocab).from_disk('nlp_all_text')

    return parsed_text

def print_freq_table(parsed_text, num_top_words=50):
    '''Prints a frequency table from the given spaCy parsed text

    Keyword arguments:
    parsed_text -- spaCy parsed text
    num_top_words -- number of words to include in frequency distribution(default=50)
    '''

    #use nltk stopwords to skip over
    nltk.download('stopwords')
    stop = set(stopwords.words('english'))

    def create_freq_table_without_stop_punct_space_length(p_text, stop_list, length):
        '''
        Requires an nlp parsed text.
        Create a frequency table without stop words, punctuation, spaces,
        and less than a specified length
        '''
        freq_table = Counter()
        for token in p_text:
            print(token.lemma_.lower())
            lemma = token.lemma_.lower()
            if not (lemma in stop_list or token.pos_ == 'PUNCT' or token.pos_ == 'SPACE' or len(token)<length):
                freq_table[lemma] += 1
        return freq_table

    freq_table = create_freq_table_without_stop_punct_space_length(parsed_text, stop, 3)

    #sorts and prints the list on frequency rank
    sorted_list = sorted(freq_table.items(), reverse = True, key=itemgetter(1))
    print('Rank'.ljust(10), 'Lemma'.ljust(20), 'Raw Count')
    for i in range(50):
        print(str(i+1).ljust(10), sorted_list[i][0].ljust(20), sorted_list[i][1])

def main():
    '''Generates frequency table from text files in "text_forms/" directory

    returns a frequency table without
    stopwords, punctuation, spaces, and words shorter than 3 chars
    '''

    SEC_Forms_to_Text.main()
    txt_dir = r'text_forms/'
    forms = [open(txt_dir+file, 'r').read() for file in os.listdir(txt_dir)]

    parsed_text = run_nlp(forms)
    print("\n\n\nText has been parsed by spacy nlp\n\n\n")

    print_freq_table(parsed_text)

if __name__ == "__main__":
   main()
