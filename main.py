#############################################################
### Usage: <program_file_name> <*.html files directory path>
#############################################################

import codecs
import os
import re
import sys


def count_dates(content):
    """
    Finds number of unique dates of the formats:
    + dd-mm-yyyy
	+ dd/mm/yyyy
	+ dd.mm.yyyy
	+ yyyy-dd-mm
	+ yyyy/dd/mm
    + yyyy.dd.mm
    :param content string to be processed
    :rtype int
    """
    pattern = r'(?<!\d)'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02]))[.]\d{4})|'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02]))[.]\d{4})|'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02]))[/]\d{4})|'
    pattern += r'(?:(?:(?:[0-2]\d)|(?:3[0-1]))-(?:(?:0[13578])|(?:1[02]))-\d{4})|'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11))[-]\d{4})|'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11))[.]\d{4})|'
    pattern += r'(?:(?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11))[/]\d{4})|'
    pattern += r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[.](?:(?:02))[.]\d{4})|'
    pattern += r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[/](?:(?:02))[/]\d{4})|'
    pattern += r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[-](?:(?:02))[-]\d{4})|'
    pattern += r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:3[0-1]))[-](?:(?:0[13578])|(?:1[02])))|'
    pattern += r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02])))|'
    pattern += r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02])))|'
    pattern += r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11)))|'
    pattern += r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11)))|'
    pattern += r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11)))|'
    pattern += r'(?:\d{4}[-](?:(?:[0-1][0-9])|(?:2[0-9]))[-](?:(?:02)))|'
    pattern += r'(?:\d{4}[/](?:(?:[0-1][0-9])|(?:2[0-9]))[/](?:(?:02)))|'
    pattern += r'(?:\d{4}[.](?:(?:[0-1][0-9])|(?:2[0-9]))[.](?:(?:02)))'
    pattern += r'(?!\d)'
    compiled = re.compile(pattern=pattern)
    results = re.findall(pattern=compiled, string=content)
    results = set(results)

    return results


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()
    fp.close()

    print("Nazwa pliku: \t" + str(extract_filename(filepath)))
    print("Autor: \t\t\t" + str(extract_author(content)))
    print("Dzial: \t\t\t" + str(extract_department(content)))
    print("Slowa kluczowe: " + str(extract_keywords(content)))
    # TODO
    print("Liczba zdan: \t" + str(count_sentences(content)))
    print("Liczba skrotow: " + str(count_abbreviations(content)))
    print("Liczba liczb calkowitych z zakresu int: " + str(count_integers(content)))
    print("Liczba liczb zmiennoprzecinkowych: \t\t" + str(count_float_numbers(content)))
    print("Liczba dat: \t\t\t" + str(count_dates(content)))
    print("Liczba adresow email: \t" + str(count_emails(content)))
    print("\n")


################################################
#               REGEX FUNCTIONS                #
################################################

def count_sentences(content):
    return 0


def count_abbreviations(content):
    return 0


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


def count_emails(content):
    return 0


def extract_filename(filepath):
    pattern = r'(\/*)(\w*.html)'
    compiled = re.compile(pattern)
    result = compiled.search(filepath)
    filename = result.group(2)
    return filename


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


def extract_department(content):
    pattern = r'\w*<META NAME="DZIAL" CONTENT="\w*\/(.*?)">'
    compiled = re.compile(pattern)
    result = compiled.search(content)
    department = result.group(1)
    return department


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
