# -*- coding: utf-8 -*-

import unittest

import requests_mock

from strainer.fetcher import TitleFetcher


class TestFetcher(unittest.TestCase):

    def test_fetcher_happy(self):
        with requests_mock.mock() as mock:
            mock.get('http://mail.google.com', text='<title>Gmail</title>')
            actual = TitleFetcher.fetch_title('http://mail.google.com')
            self.assertEqual(u'Gmail', actual)

    def test_fetcher_no_title(self):
        with requests_mock.mock() as mock:
            mock_html = "<html><head>simple</head><body>simple</body></html>"
            mock.get('http://foobar', text=mock_html)
            actual = TitleFetcher.fetch_title('http://foobar')
            self.assertEqual(u'', actual)

    def test_fetcher_empty_title(self):
        with requests_mock.mock() as mock:
            mock_html = "<html><head>simple</head><title></title></html>"
            mock.get('http://empty.title', text=mock_html)
            actual = TitleFetcher.fetch_title('http://empty.title')
            self.assertEqual(u'', actual)

    def test_fetcher_spl_chars_in_title(self):
        with requests_mock.mock() as mock:
            mock_html = "<html><head>simple</head><title>#%!$^&</title></html>"
            mock.get('http://special.chars', text=mock_html)
            actual = TitleFetcher.fetch_title('http://special.chars')
            self.assertEqual('#%!$^&', actual)

    def test_fetcher_unicode_chars_in_title(self):
        with requests_mock.mock() as mock:
            mock_html = (u'<html><head>simple</head><title>Unicode® character '
                         u'table</title></html>')
            mock.get('http://unicode.chars', text=mock_html)
            actual = TitleFetcher.fetch_title('http://unicode.chars')
            self.assertEqual(u'Unicode® character table', actual)

    # (note): There should be tests here for testing the timeout
