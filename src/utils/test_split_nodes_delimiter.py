import unittest

from src.text_node import TextNode, TextType
from src.utils.split_notes_delimiter import split_nodes_delimiter

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), ])

    def test_bad_input(self):
        node = TextNode("This is a `bad input", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
