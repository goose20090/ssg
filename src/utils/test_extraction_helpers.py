from src.utils.extraction_helpers import extract_markdown_links, extract_markdown_images

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

    def test_extract_images_no_images(self):
        text = "This text has no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_images_one_image(self):
        text = "Look at this ![alt text](image.jpg)."
        expected = [("alt text", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_images_multiple_images(self):
        text = "See ![img1](url1.png) and ![img2](url2.gif)."
        expected = [("img1", "url1.png"), ("img2", "url2.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_images_ignore_links(self):
        text = "An ![image](i) and a [link](l)."
        expected = [("image", "i")]
        self.assertEqual(extract_markdown_images(text), expected)

if __name__ == "__main__":
    unittest.main()
