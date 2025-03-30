import unittest

from leaf_node import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "my_link", { "href": "example.com" })
        self.assertEqual(node.to_html(), '<a href="example.com">my_link</a>')

if __name__ == "__main__":
    unittest.main()
