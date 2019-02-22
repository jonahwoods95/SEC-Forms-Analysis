import pandas as pd
from subprocess import PIPE, run
import urllib3
import os
import time
from sys import platform

'''
This code will scrape the SEC Forms website for pdf file links
and download them accordingly. The downloaded forms are converted to text and stored
in
'''

if platform == "darwin":
    windows = False
elif platform == "win32":
    windows = True

def download_pdf(download_url, pdf_file_name):
    '''Downloads a single pdf file from url and writes to pdf_forms/(file_name)

    Keyword arguments:
    download_url -- url link to a pdf file
    pdf_file_name -- form name given on SEC website with "pdf_forms/" prefix
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

def save_file_as_text(pdf_file_name, text_file_name):
    '''Converts a pdf file to a text file, then writes to proper file name

    Keyword arguments:
    pdf_file_name -- form name given on SEC website with "pdf_forms/" prefix
    text_file_name -- text file name given on SEC website with "text_forms/" prefix
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

def read_forms(form_links):
    '''Downloads pdf files from form_links, and converts them to text files

    Keyword arguments:
    form_links -- csv file with url links to pdf files stored online
        -> required format '/file_name.pdf')
    '''

    sec_urls = pd.read_csv(form_links)

    #make new directories for pdfs and text files
    if windows:
        slash = r'\\'
    else:
        slash = r'/'
    pdf_path = r'pdf_forms'+slash
    text_path = r'text_forms'+slash
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
            download_pdf(url, pdf_file_name)
            text_form = save_file_as_text(pdf_file_name, text_file_name)

            #append it to current forms list
            forms.append(text_form)

            #delay to avoid throttling
            time.sleep(.5)
    return forms

def main():

    if not os.path.isfile('SECForms.csv'):
        os.system("scrapy runspider simple-scraper.py -t csv -o SECForms.csv")

    read_forms('SECForms.csv')
    print("\n\n\nAll forms have been read")

if __name__ == "__main__":
   main()
