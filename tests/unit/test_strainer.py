import unittest

from strainer.strainer import MessageStrainer


class TestEmoticonStraining(unittest.TestCase):

    def test_strain_emoticons_multiple(self):
        test_input = "Good morning! (megusta) (coffee)"
        expected = ['megusta', 'coffee']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_single(self):
        test_input = "Good morning! (megusta)"
        expected = ['megusta']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_none(self):
        test_input = ("@bob @john such a cool feature; "
                      "https://twitter.com/jdorfman/status/430511497475670016")
        expected = []
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_only_emoticons_text_with_alphanum(self):
        test_input = "(blah)(blah1)(blah2)(blah3) (1234)"
        expected = ['blah', 'blah1', 'blah2', 'blah3', '1234']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_with_extra_parenthesis(self):
        test_input = "@bob @john ((success) such a (cool))) feature;"
        expected = ['success', 'cool']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_with_nested_parenthesis(self):
        test_input = "@bob @john ((success)) such a (cool))) feature;"
        expected = ['success', 'cool']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_with_adjacent_chars(self):
        test_input = "@bob @john (success)! such a feature (cool);(yo)^(aww),"
        expected = ['success', 'cool', 'yo', 'aww']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_middle_of_word(self):
        test_input = "@bob @john big(success)! such a feature (cool);"
        expected = ['success', 'cool']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_with_adjacent_whitespace(self):
        test_input = "@bob@john (success)! such a feature (cool)\t(yo)\n(aww),"
        expected = ['success', 'cool', 'yo', 'aww']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_invalid_emoticons_with_invalid_length_of_alphanum(self):
        test_input = ("@bob @john (success) such a (cool) feature; () (()) "
                      "(supercalifragilistic)!")
        expected = ['success', 'cool']
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertEqual(expected, actual)

    def test_strain_invalid_emoticons_with_invalid_parenthesis(self):
        test_input = ("@bob @john (success such a cool) feature;"
                      "We rocked it {yo) [rocked] {awesome} [woo}")
        expected = []
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertEqual(expected, actual)

    def test_strain_invalid_emoticons_with_non_alphanum_characters(self):
        test_input = "(o/) @bob @john such a (cool#) feature; (#$%^&)"
        expected = []
        actual = MessageStrainer.strain_emoticons(test_input)
        self.assertEqual(expected, actual)


class TestMentionsStraining(unittest.TestCase):

    def test_strain_mentions_multiple(self):
        test_input = "@bob @john such a cool feature;"
        expected = ['bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_emoticons_single(self):
        test_input = "you around, @chris"
        expected = ['chris']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_none(self):
        test_input = ("bob: !john: #alice: such a cool feature; "
                      "https://twitter.com/jdorfman/status/430511497475670016")
        expected = []
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_with_underscores(self):
        test_input = "@bob_ @_john @__alice__ such a cool feature;"
        expected = ['bob_', '_john', '__alice__']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_multiple_at_characters(self):
        test_input = "@alice @@bob @john@ such a cool feature;"
        expected = ['bob', 'john', 'alice']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_empty_mentions(self):
        test_input = "@ @bob @john such a cool feature;"
        expected = ['bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_long_mentions(self):
        test_input = "@abcdefghijklmnopqrtuvwxyz1234567890"
        expected = ['abcdefghijklmnopqrtuvwxyz1234567890']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_back_to_back(self):
        test_input = "@alice@bob@john such a cool feature;"
        expected = ['alice', 'bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_delimited_by_nonspace_chars(self):
        test_input = "@alice:@bob,@john; such a cool feature;"
        expected = ['alice', 'bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_accompanied_by_special_chars(self):
        test_input = "@alice! @bob^ @john, such a cool feature;"
        expected = ['alice', 'bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_occurring_middle_of_a_word(self):
        test_input = "super@alice ,,,@bob;;; @john, such a cool feature;"
        expected = ['alice', 'bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_nonword_chars_middle_of_mentions(self):
        test_input = "@al!ce @b^b @j&hn, such a cool feature;"
        expected = ['al', 'b', 'j']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_with_whitespace(self):
        test_input = "@alice\n@bob\t@john, such a cool feature;"
        expected = ['alice', 'bob', 'john']
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_mentions_invalid_mentions(self):
        test_input = "@{} @#$^%^ such a cool feature;"
        expected = []
        actual = MessageStrainer.strain_mentions(test_input)
        self.assertItemsEqual(expected, actual)


class TestURLsStraining(unittest.TestCase):

    def test_strain_urls_single(self):
        test_input = ("@bob @john (success) such a cool feature; "
                      "https://twitter.com/jdorfman/status/430511497475670016")
        expected = ['https://twitter.com/jdorfman/status/430511497475670016']
        actual = MessageStrainer.strain_urls(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_urls_multiple_http_and_https(self):
        test_input = ("Olympics are starting soon; "
                      "https://www.olympic.org/rio-2016 "
                      "http://www.nbcolympics.com ")
        expected = ['http://www.nbcolympics.com',
                    'https://www.olympic.org/rio-2016']
        actual = MessageStrainer.strain_urls(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_urls_none(self):
        test_input = "@bob @john Olympics are starting soon."
        expected = []
        actual = MessageStrainer.strain_urls(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_urls_wrapped_in_parenthesis(self):
        test_input = ("Olympics are starting soon; "
                      "(https://www.olympic.org/rio-2016) "
                      "http://www.nbcolympics.com ")
        expected = ['http://www.nbcolympics.com',
                    'https://www.olympic.org/rio-2016']
        actual = MessageStrainer.strain_urls(test_input)
        self.assertItemsEqual(expected, actual)

    def test_strain_url_without_scheme(self):
        test_input = ("Olympics are starting soon; "
                      "www.olympic.org/rio-2016 "
                      "http://www.nbcolympics.com ")
        expected = ['http://www.nbcolympics.com',
                    'www.olympic.org/rio-2016']
        actual = MessageStrainer.strain_urls(test_input)
        self.assertItemsEqual(expected, actual)
