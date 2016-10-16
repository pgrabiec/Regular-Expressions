# coding=utf-8
import unittest
import main as model

def test(self, list_arg, function):
    """
    Parameters:
    self     - pass the argument from the test* functions
    list_arg - list of binary tuples of the form: [(z, y), ...]
               where x is the string to be processed,
               y is the expected result for the function passed
               as 3rd argument to this function for the argument x.
    function - function returning string result,
               taking a single string as the only parameter
    Fails the test unless the function evaluations for all inputs are equal to their expected values
    """
    for tuple in list_arg:
        input, expected_result = tuple
        result = function(input)
        self.failUnless(result == expected_result)

class RegExprTests(unittest.TestCase):
    def test_extract_keywords(self):
        pass

    def test_count_sentences(self):
        pass

    def test_count_abbreviations(self):
        pass

    def test_count_emails(self):
        pass

    def test_count_integers(self):
        pass

    def test_count_float_numbers(self):
        pass

    def test_count_dates(self):
        pass

    def test_extract_department(self):
        pass

    def test_extract_author(self):
        list_arg = [(
                '\n <META NAME = "AUTOR" CONTENT = " Danuta Walewska,Wiesława Mazur">\n',
                " Danuta Walewska,Wiesława Mazur"
        )]
        test(self, list_arg, model.extract_author)

def execute():
    unittest.main()

if __name__ == '__main__':
    execute()