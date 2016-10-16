#############################################################
### Usage: <program_file_name> <*.html files directory path>
#############################################################

import codecs
import os
import re
import sys

"""
Changelog:

# I have configured the code template from the subject site
# and have declared functions that need to be implemented.
# I also have finished the first one at the bottom.
#                                                      ~Piotr

# ~WB
# + added department
# + modified 'processFile()' to have information more-readable displayed
# + added 'extract_filename()' to show only 'file-name' without 'folder-name/'
# + added 'extract_keywords()'

"""


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

    print("Nazwa pliku: \t" + str(extract_filename(filepath)))
    print("Autor: \t\t\t" + str(extract_author(content)))
    print("Dział: \t\t\t" + str(extract_department(content)))
    print("Słowa kluczowe: " + str(extract_keywords(content)))
    # TODO
    print("Liczba zdań: \t" + str(count_sentences(content)))
    print("Liczba skrotów: " + str(count_abbreviations(content)))
    print("Liczba liczb całkowitych z zakresu int: " + str(count_integers(content)))
    print("Liczba liczb zmiennoprzecinkowych: \t\t" + str(count_float_numbers(content)))
    print("Liczba dat: \t\t\t" + str(count_dates(content)))
    print("Liczba adresów email: \t" + str(count_emails(content)))
    print("\n")


################################################
#               REGEX FUNCTIONS                #
################################################

# Done - WB
def extract_filename(filepath):
    pattern = r'(\/*)(\w*.html)'
    compiled = re.compile(pattern)
    result = compiled.search(filepath)
    filename = result.group(2)
    return filename


# Done - PG
def extract_author(content):
    pattern = r'<\s*META\s*NAME=\s*"\s*AUTOR\s*"\s*CONTENT\s*=\s*"(.*?)"\s*>'
    compiled = re.compile(pattern)
    results = compiled.search(string=content)
    author = results.group(1)
    return author


# Done - WB
def extract_department(content):
    pattern = r'\w*<META NAME="DZIAL" CONTENT="\w*\/(.*?)">'
    compiled = re.compile(pattern)
    result = compiled.search(content)
    department = result.group(1)
    return department


# Done - WB
def extract_keywords(content):
    pattern = r'\w*<META NAME="KLUCZOWE_\d?" CONTENT="(.*)">'
    compiled = re.compile(pattern)
    results_as_list = compiled.findall(content)
    results_as_strings = ", ".join(repr(e) for e in results_as_list if e != '')
    return results_as_strings


################################################
#                   MAIN CODE                  #
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
