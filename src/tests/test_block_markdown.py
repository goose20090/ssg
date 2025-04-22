import unittest
import textwrap
from src.block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_nodes


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_code_block_to_block_type(self):
        blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]

        block_types = [block_to_block_type(block) for block in blocks]

        self.assertEqual(block_types, [ BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST ])

    def test_paragraph(self):
        blocks = [
            "This is a simple paragraph.",
            "Another paragraph with _italic_ text."
        ]
        expected = [BlockType.PARAGRAPH, BlockType.PARAGRAPH]
        self.assertEqual(list(map(block_to_block_type, blocks)), expected)

    def test_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2"
        ]
        expected = [BlockType.HEADING, BlockType.HEADING]
        self.assertEqual(list(map(block_to_block_type, blocks)), expected)

    def test_code(self):
        blocks = [
            "```\ncode here\n```",
            "```python\ndef foo():\n    pass\n```"
        ]
        expected = [BlockType.CODE, BlockType.CODE]
        self.assertEqual(list(map(block_to_block_type, blocks)), expected)

    def test_unordered_list(self):
        blocks = [
            "- item 1\n- item 2",
            "- apple\n- banana"
        ]
        expected = [BlockType.UNORDERED_LIST, BlockType.UNORDERED_LIST]
        self.assertEqual(list(map(block_to_block_type, blocks)), expected)

    def test_ordered_list(self):
        blocks = [
            "1. first\n2. second",
            "1. apple\n2. banana\n3. cherry"
        ]
        expected = [BlockType.ORDERED_LIST, BlockType.ORDERED_LIST]
        self.assertEqual(list(map(block_to_block_type, blocks)), expected)

    def test_quote(self):
        blocks = [
                ">Quoted line ova 'ere!",
                ">Frankly my dear, I don't give a damn"
        ]
        expected = [BlockType.QUOTE, BlockType.QUOTE]
        self.assertListEqual(list(map(block_to_block_type, blocks)), expected)
        
    def test_paragraphs(self):
            md = textwrap.dedent("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """)

            node = markdown_to_html_nodes(md)
            html = node.to_html()

            self.assertMultiLineEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
            )

    def test_codeblock(self):
            md = textwrap.dedent("""
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """)

            node = markdown_to_html_nodes(md)
            html = node.to_html()
            self.assertMultiLineEqual(
                html,
                "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
            )
