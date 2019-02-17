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

def download_SEC_file(download_url, pdf_file_name):
    '''
    Downloads a single file and writes to pdf_forms/(pdf_file_name)
    where pdf_file_name is the form name given on SEC website
    '''
    #if file is already there, don't overwrite
    if not os.path.isfile(pdf_file_name):

        #Download file
        print(f"Downloading {pdf_file_name} PDF file...")
        http = urllib3.PoolManager()
        response = http.request('GET', download_url)

        #Write to local pdf_files
        local_file = open(pdf_file_name, 'wb')
        pdf = response.data
        local_file.write(pdf)
        response.close()
        local_file.close()

    else:
        print(f"{pdf_file_name} already stored in pdf_forms")

def write_form(pdf_file_name, text_file_name):
    '''
    Converts a pdf file to a text file,
    then appends it to the current list
    Parameters
    forms: the list of forms to append to
    pdf_file_name: as written
    text_file_name: as written
    '''

    #if file is already there, don't overwrite
    if not os.path.isfile(text_file_name):

        #Convert pdf file to text
        command = ['pdf2txt.py', pdf_file_name]
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        #Write text file
        print(f"Writing {text_file_name} text file...")
        local_file = open(text_file_name, 'w')
        for line in str(result.stdout):
            local_file.write(line)
        return str(result.stdout)
    else:
        print(f"{text_file_name} already stored in text_forms")
        return open(text_file_name, 'r').read()

def read_forms(forms_file_name):
    '''
    Reads the files in forms_file_name as urls.
    The urls are used to download pdf files
    and convert them into text documents

    This can be used for a list of online pdf urls
    (required format '/file_name.pdf')
    '''

    sec_urls = pd.read_csv(forms_file_name)

    #make new directories for pdfs and text files
    pdf_path = r'pdf_forms/'
    text_path = r'text_forms/'
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)
    if not os.path.exists(text_path):
        os.makedirs(text_path)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    forms = []
    for url in sec_urls['url']:
        if url=="url": break

        #get correct file path names
        pdf_file_name = pdf_path + url.split(r'/')[-1]
        text_file_name = text_path + url.split(r'/')[-1].split('.')[0] + '.txt'

        #make sure pdf file
        if pdf_file_name.split('.')[1] == 'pdf':
            download_SEC_file(url, pdf_file_name)
            text_form = write_form(pdf_file_name, text_file_name)

            #append it to current forms list
            forms.append(text_form)

            #delay to avoid throttling
            time.sleep(.5)
    return forms

def run_nlp(forms):
    '''
    Runs spaCy natural language processing on all forms
    as one text file.

    The goal is to find the most frequent words used by the SEC
    and see what verbs we can pick out that are actionable.
    '''

    print('\n\n\nRunning natural language processing using spaCy...')
    print('This will take a while (up to 10 minutes)...\n\n\n')

    #join the files together
    all_text = ''.join(forms)
    txt_file_name = "all_text_file"

    if not os.path.isfile(txt_file_name):
        file = open(txt_file_name, 'w')
        file.write(all_text)

    nlp = spacy.load('en')
    nlp.max_length = 7000000

    #if spacy hasn't parsed text,
    #then parse the text
    if not os.path.isfile('nlp_all_text'):
        parsed_text = nlp(all_text)
        parsed_text.to_disk('nlp_all_text')

    #if spacy has parsed text,
    #then only need to read the file on disk
    else:
        parsed_text = spacy.tokens.Doc(nlp.vocab).from_disk('nlp_all_text')

    return parsed_text

def print_freq_table(parsed_text):
    '''
    Prints a frequency table from the given spaCy parsed text
    Prin
    '''
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

    if not os.path.isfile('SECForms.csv'):
        os.system("scrapy runspider simple-scraper.py -t csv -o SECForms.csv")

    forms = read_forms('SECForms.csv')
    print("\n\n\nAll forms have been read")

    run_nlp(forms)
    print("\n\n\nText has been parsed by spacy nlp\n\n\n")

    print_freq_table(parsed_text)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
