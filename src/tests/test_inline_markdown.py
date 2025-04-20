import unittest

from src.text_node import TextNode, TextType
from src.inline_markdown import split_nodes_image, split_nodes_delimiter, split_nodes_link, extract_markdown_images, extract_contents_of_regular_brackets, extract_contents_of_square_brackets, extract_markdown_links, text_to_text_nodes


class TestInlineMarkdown(unittest.TestCase):

    def test_baseline(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_text_nodes(input), expected_output)

    #  Splitting nodes on a delimiter
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), ])

    def test_bad_input(self):
        node = TextNode("This is a `bad input", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_bold(self):
        node = TextNode("This is text with a *bold* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT), ])
        
    
    # Extraction helpers
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



    # Splitting Link Nodes
    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ], new_nodes
        )

    def test_link_at_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" some more text", TextType.TEXT),
            ], new_nodes
        )

    def test_link_at_end(self):
        node = TextNode(
            "some text at the beginning here [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text at the beginning here ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ], new_nodes
        )

    def multiple_nodes(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        bold_node = TextNode("bold node", TextType.BOLD)
        code_node = TextNode("code node", TextType.CODE)
        new_nodes = split_nodes_link([code_node, node, bold_node])
        self.assertListEqual(
            [
                code_node,
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                bold_node
            ], new_nodes
        )


    # Splitting image nodes
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" some more text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "some text at the beginning here ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text at the beginning here ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_multiple_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        bold_node = TextNode("bold node", TextType.BOLD)
        code_node = TextNode("code node", TextType.CODE)
        new_nodes = split_nodes_image([code_node, node, bold_node])
        self.assertListEqual(
            [
                code_node,
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                bold_node,
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
