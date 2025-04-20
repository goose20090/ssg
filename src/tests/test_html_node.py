import unittest

from src.html_node import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a paragraph")
        node_2 = HTMLNode("p", "this is a paragraph")
        self.assertEqual(node, node_2)

    def test_not_eq(self):
        node = HTMLNode("p", "this is a paragraph")
        node_2 = HTMLNode("p", "this is another paragraph")
        self.assertNotEqual(node, node_2)

    def test_props_to_attrs(self):
        test_props = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        node = HTMLNode("a", "this is a link", None, test_props)

        expected_result = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)



if __name__ == "__main__":
    unittest.main()
