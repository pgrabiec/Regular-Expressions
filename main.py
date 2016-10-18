#############################################################
### Usage: <program_file_name> <*.html files directory path>
#############################################################

import codecs
import os
import re
import sys

"""
Changelog:
# ~WB
# + added department
# + modified 'processFile()' to have information more-readable displayed
# + added 'extract_filename()' to show only 'file-name' without 'folder-name/'
# + added 'extract_keywords()'

# ~WB v2
# + added 'count_sentences()' and helpful function 'get_not_meta()'
# + added 'count_abbreviations()'   |   Warning: in web-browser-checkers count differs, because of polish signs !)
# + added 'count_emails()'          |   Warning: it's always (!) 0 in example files while range is from <p> to <meta> !!!

# ~WB v3
# + Corrected functions 'count_abbreviations()' and 'count_emails()'.
# + Minor changes in displaying information in 'processFile()'
"""


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()
    fp.close()

    print("Nazwa pliku: \t" + str(extract_filename(filepath)))
    print("Autor: \t\t\t" + str(extract_author(content)))
    print("Dział: \t\t\t" + str(extract_department(content)))
    print("Słowa kluczowe: " + str(extract_keywords(content)))
    print("Liczba zdań: \t" + str(count_sentences(content)))
    print("Liczba różnych skrotów: \t\t" + str(count_abbreviations(content)))
    print("Liczba różnych liczb całk. z zakresu int: \t" + str(count_integers(content)))
    print("Liczba różnych liczb zmiennoprzecinkowych: \t" + str(count_float_numbers(content)))
    print("Liczba różnych dat: \t\t\t" + str(count_dates(content)))
    print("Liczba różnych adresów email: \t" + str(count_emails(content)))
    print("\n")


################################################
# ------------- REGEX FUNCTIONS -------------- #
################################################

# PG
def count_dates(content):
    """
    + Finds number of unique dates of the formats:
    + dd-mm-yyyy
    + dd/mm/yyyy
    + dd.mm.yyyy
    + yyyy-dd-mm
    + yyyy/dd/mm
    + yyyy.dd.mm
    :param content string to be processed
    :rtype int
    """
    separators = ['.', '/', '-']
    months_length_spec = [
        (31, [
            (0, [1, 3, 5, 7, 8]),
            (1, [0, 2])
        ]),
        (30, [
            (0, [4, 6, 9]),
            (1, [1])
        ]),
        (29, [
            (0, [2])
        ])
    ]
    # Separator RegEx
    separator_regex = r'['
    for sep in separators:
        separator_regex += sep
    separator_regex += r']'
    # Pattern assembly
    separate = False
    pattern = r'(?<!\d)'
    counter = 2
    for months_spec in months_length_spec:
        day_reg, month_reg, year_reg = '', '', r'\d{4}'
        days, months_list = months_spec

        # Day RegEx
        day_reg += r'[0-' + \
                   str(max(days // 10 - 1, 0)) + \
                   r']\d' + \
                   r'|' + \
                   str(days // 10) + \
                   r'[0-' + \
                   str(days % 10) + \
                   r']'
        # Month RegEx
        insert_pipe = False
        for month_ten in months_list:
            ten_digit, one_digits_list = month_ten
            if insert_pipe:
                month_reg += r'|'
            else:
                insert_pipe = True
            month_reg += str(ten_digit) + r'['
            for one_digit in one_digits_list:
                month_reg += str(one_digit)
            month_reg += r']'
        # Include results in the pattern
        if separate:
            pattern += r'|'
        else:
            separate = True
        pattern += r'(' + day_reg + r')(' + separator_regex + r')(' + month_reg + ')\\' + str(
            counter) + r'(' + year_reg + r')|'
        counter += 4  # Updating number to reference appropriate group number of separator RegEx
        pattern += r'(' + year_reg + r')(' + separator_regex + ')(' + day_reg + ')\\' + str(
            counter) + r'(' + month_reg + ')'
        counter += 4
    pattern += r'(?!\d)'

    compiled = re.compile(pattern=pattern)
    results = re.findall(pattern=compiled, string=content)
    if results is None:
        return 0
    if results == []:
        return 0

    # Find unique dates
    # results is a list e.g. [('', '', '1016', '-', '29', '03', '', ...), (), ...]
    unique_dates = set()
    for result_tuple in results:
        result_list = list(result_tuple)
        i = 0
        while i < len(result_list):
            data = result_list[i]
            length = len(data)
            if length > 0:
                if length == 2:
                    unique_dates.add(data + result_list[i + 2] + result_list[i + 3])
                    break
                if length == 4:
                    unique_dates.add(result_list[i + 2] + result_list[i + 3] + data)
                    break
            i += 1
    print(unique_dates)
    return len(unique_dates)


# PG
def count_float_numbers(content):
    pattern = r'(?<!\d)[+-]?(?:\d+[.]\d*|[.]\d+)(?:e[+-]?\d+)?(?!\d)'
    compiled = re.compile(pattern)
    results = re.findall(pattern=compiled, string=content)
    if results is None:
        return 0
    results = set(results)
    length = len(results)
    if length < 1:
        return 0
    return length


# PG
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


# +------+
# | META |
# +------+

# WB
def extract_filename(filepath):
    pattern = r'(\/*)(\w*.html)'
    compiled = re.compile(pattern)
    result = compiled.search(filepath)
    filename = result.group(2)
    return filename


# PG
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


# WB
def extract_department(content):
    pattern = r'\w*<META NAME="DZIAL" CONTENT="\w*\/(.*?)">'
    compiled = re.compile(pattern)
    result = compiled.search(content)
    department = result.group(1)
    return department


# WB
def extract_keywords(content):
    pattern = r'\w*<META NAME="KLUCZOWE_\d?" CONTENT="(.*)">'
    compiled = re.compile(pattern)
    results_as_list = compiled.findall(content)
    results_as_strings = ", ".join(repr(e) for e in results_as_list if e != '')
    return results_as_strings


# +----------+
# | NOT-META |
# +----------+

# WB
def get_not_meta(content):
    pattern = r'<[P|p][\s\S]*?<(?:meta|META)'
    compiled = re.compile(pattern, re.MULTILINE)
    result = compiled.findall(content)
    # print(''.join(re.compile(r'<[P|p][\s\S]*?<(?:meta|META)', re.MULTILINE).findall(content)))
    result_as_list = ''.join(result)
    # result_as_string = ", ".join(repr(e) for e in result_as_list)
    return result_as_list


# WB
def count_sentences(content):
    pattern = r'.*?([a-zA-Z]{4}|\s+|\B\W)((\.|!|\?)+|( )+\n)'
    # (!) Warning: accepts any 4-letter words like 'proc.'='procent'
    # Because it's not specified exactly in homework

    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    count = 0
    for _ in my_iter:
        count += 1
        # print(element.span(), element.group(0))
        # print(element.start())
    return count


# WB
def count_abbreviations(content):
    pattern = r'\b([a-zA-Z]{1,3})\.'
    # (!) Warning: don't accept 'proc.' = 'procent' itp.
    # Because it's not specified exactly in homework

    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    dict = {}
    for e in my_iter:
        # print(_a.group(0))
        if e.group(0) not in dict:
            dict[e.group(0)] = 1
        else:
            dict[e.group(0)] += 1
    # for key, value in dict.items():
    #     print(" : " + key, value)
    return len(dict)


# WB
def count_emails(content):
    pattern = r'[\w+-]+(\.([a-zA-Z0-9])+)*@[\w-]+(\.([a-zA-Z0-9])+)+'
    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    # (!) Warning: in proposed examples it's ALWAYS 0
    # Because it's not specified exactly in homework

    dict = {}
    for e in my_iter:
        # print(_a.group(0))
        if e.group(0) not in dict:
            dict[e.group(0)] = 1
        else:
            dict[e.group(0)] += 1
    # for key, value in dict.items():
    #     print(" : " + key, value)

    return len(dict)


################################################
# ----------------- MAIN CODE ---------------- #
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
