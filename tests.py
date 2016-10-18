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
    for subject in list_arg:
        input_string, expected_result = subject
        result = function(input_string)
        if result != expected_result:
            print("Expected: " + str(expected_result) + "  computed: " + str(result))
            print("input: " + input_string)
        self.failUnless(result == expected_result)


class RegExprTests(unittest.TestCase):
    def test_extract_keywords(self):
        pass

    def test_count_sentences(self):
        pass

    def test_count_abbreviations(self):
        pass

    def test_count_emails(self):
        list_arg = [
            ('a1@a.a.a.com a1@a.a a@a.a', 3),
            (' 1a@a.a a@a..a a.a@a.a  ', 0)
        ]
        test(self, list_arg, model.count_emails)
        pass

    def test_count_integers(self):
        list_arg = [
            ('\n  123 -342 000000000000000000002 0000000000000 -32768 32767', 6),
            ('\n -327.69 327.679 1498321478934918 0000000032768 -00000000000032769 23.4 33333 -33333', 0),
            ('123', 1),
            ('23-40 32+35', 4)
        ]
        test(self, list_arg, model.count_integers)
        pass

    def test_count_float_numbers(self):
        list_arg = [
            ('a-3.2e-2a 1.2 .3 234.52 s-3.12e-2.\n.8,', 6),
            (' 1e10 2e+10 4e-32 ', 0)
        ]
        test(self, list_arg, model.count_float_numbers)
        pass

    def test_count_dates(self):
        list_arg = [
            (r'05-03-2009a w13/03/1995d 29.02.1111 2222-21-10 ', 4),
            (r' 00-00-0000 02-00-1111 00-32-2222 234-55-2345 88-03-2003 ', 0)
        ]
        test(self, list_arg, model.count_dates)
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
