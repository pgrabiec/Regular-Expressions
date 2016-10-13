#############################################################
### Usage: <program_file_name> <*.html files directory path>
#############################################################

import os
import sys
import re
import codecs


#############################################################
# I have configured the code template from the subject site
# and have declared functions that need to be implemented.
# I also have finished the first one at the bottom.
#                                                      ~Piotr
#############################################################

# TODO
def extract_department(content):
    return ''


# TODO
def extract_keywords(content):
    return []


# TODO
def count_sentences(content):
    return 0


# TODO
def count_abbreviations(content):
    return 0


# TODO
def count_float_numbers(content):
    return 0


# TODO
def count_dates(content):
    return 0


# TODO
def count_emails(content):
    return 0


# TODO
def count_integers(content):
    return 0



def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:" + str(extract_author(content)))
    print("dzial:" + str(extract_department(content)))
    print("slowa kluczowe:" + str(extract_keywords(content)))
    print("liczba zdan:" + str(count_sentences(content)))
    print("liczba skrotow:" + str(count_abbreviations(content)))
    print("liczba liczb calkowitych z zakresu int:" + str(count_integers(content)))
    print("liczba liczb zmiennoprzecinkowych:" + str(count_float_numbers(content)))
    print("liczba dat:" + str(count_dates(content)))
    print("liczba adresow email:" + str(count_emails(content)))
    print("\n")

# Done - PG
def extract_author(content):
    pattern = r'<\s*META\s*NAME=\s*"\s*AUTOR\s*"\s*CONTENT\s*=\s*"(.*?)"\s*>'
    compiled = re.compile(pattern)
    results = compiled.search(string=content)
    author = results.group(1)
    return author



################################################
### MAIN CODE
################################################


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)

tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)
