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

# TODO - PG
def count_dates(content):
    """
    + dd-mm-rrrr
	+ dd/mm/rrrr
	+ dd.mm.rrrr
	+ rrrr-dd-mm
	+ rrrr/dd/mm
    + rrrr.dd.mm
    """
    pattern = r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02]))[.]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02]))[/]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[-](?:(?:0[13578])|(?:1[02]))[-]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11))[-]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11))[.]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11))[/]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[.](?:(?:02))[.]\d{4})|'  # 29 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[/](?:(?:02))[/]\d{4})|'  # 29 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[-](?:(?:02))[-]\d{4})|'  # 29 days
    r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:3[0-1]))[-](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[-](?:(?:[0-1][0-9])|(?:2[0-9]))[-](?:(?:02)))|'  # 29 days
    r'(?:\d{4}[/](?:(?:[0-1][0-9])|(?:2[0-9]))[/](?:(?:02)))|'  # 29 days
    r'(?:\d{4}[.](?:(?:[0-1][0-9])|(?:2[0-9]))[.](?:(?:02)))'  # 29 days
    compiled = re.compile(pattern=pattern)
    results = re.findall(pattern=compiled, string=content)
    print(results)
    return set(results)

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

# TODO - WB
def count_sentences(content):
    return 0

# TODO - WB
def count_abbreviations(content):
    return 0

# Done - PG
def count_float_numbers(content):
    pattern = r'(?<!\w)[+-]?(?:(?:\d+[.]\d*)|(?:[.]\d+)|(?:\d+[.]\d+[e][+-]?\d+)|(?:\d+[e][+-]?\d+))(?!\w)'
    compiled = re.compile(pattern)
    results = re.findall(pattern=compiled, string=content)
    if results is None:
        return 0
    results = set(results)
    length = len(results)
    if length < 1:
        return 0
    return length

# Done - PG
def count_integers(content):
    """
    Counts occurrences of integers between -32768 and 32767 (inclusive) in a given string
    :param content string to be processed
    :rtype int
    """
    pattern = r'(?<!\d|[.])(?:(?:-0*(?:(?:[1-3][0-2][0-9]{2}[0-8])|(?:[1-9][0-9]{,3})))|(?:0*(?:(?:[1-3][0-2][0-9]{2}[0-7])|(?:[1-9][0-9]{,3})))|0+)(?![.]|(?:[.]\d)|\d)'
    compiled = re.compile(pattern)
    results = re.findall(pattern=compiled, string=content)
    if results is None:
        return 0
    results = set(results)
    length = len(results)
    if length < 1:
        return 0
    return length

# TODO - WB
def count_emails(content):
    return 0

# Done - WB
def extract_filename(filepath):
    pattern = r'(\/*)(\w*.html)'
    compiled = re.compile(pattern)
    result = compiled.search(filepath)
    filename = result.group(2)
    return filename


# Done - PG
def extract_author(content):
    pattern = r'<META\s*NAME\s*=\s*"AUTOR"\s*CONTENT\s*=\s*"(.*?)".*?>'
    compiled = re.compile(pattern)
    results = compiled.search(string=content)
    if results is None:
        return ""
    author = results.group(1)
    if author is None:
        return ""
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
