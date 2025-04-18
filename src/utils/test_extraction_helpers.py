from src.utils.extraction_helpers import extract_markdown_links

import unittest


class TestExtractionHelpers(unittest.TestCase):
    def test_extract_links_no_links(self):
        text = "This text has no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_one_link(self):
        text = "Here is a [link](http://example.com)."
        expected = [("link", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_links_multiple_links(self):
        text = "Check [link1](url1) and [link2](url2)."
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_links_ignore_images(self):
        text = "A [real link](l) and an ![image link](i)."
        expected = [("real link", "l")]
        self.assertEqual(extract_markdown_links(text), expected)
