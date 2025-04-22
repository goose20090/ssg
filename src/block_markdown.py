from enum import Enum
import re

from parent_node import ParentNode
from utils.text_node_to_html_node import text_node_to_html_node
from inline_markdown import text_to_text_nodes
from leaf_node import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode():
    def __init__(self, block_type, block):
        self.block_type = block_type
        self.block = block
        self.tag = self.get_tag()
        self.text = self.get_text()
        self.children = self.text_to_children()
    def to_html_node(self):
        return ParentNode(self.tag, self.text_to_children())

    def get_tag(self):
        match self.block_type:
            case BlockType.HEADING:
                header_prefix = re.match(r"^(#+)", self.block)
                if header_prefix is None:
                    raise Exception("something wrong with this header")
                header_type = len(header_prefix.group(1))
                return f"h{header_type}"
            case BlockType.CODE:
                return "pre"
            case BlockType.QUOTE:
                return "blockquote"
            case BlockType.UNORDERED_LIST:
                return "ul"
            case BlockType.ORDERED_LIST:
                return "ol"
            case _:
                return "p"

    def get_text(self):
        match self.block_type:
            case BlockType.HEADING:
                return self.block.removeprefix(self.get_header_prefix())
            case BlockType.CODE:
                return self.block[3:-3]
            case BlockType.PARAGRAPH:
                return self.block.replace("\n", " ")
            case _: return self.block

    def get_header_prefix(self):
        header_prefix = re.match(r"^(#+ )", self.block)
        if header_prefix is None:
            raise Exception("something wrong with this header")
        return header_prefix.group(1)



    def text_to_children(self):
        match self.block_type:
            case BlockType.QUOTE:
                lines = self.text.split("\n")
                lines = [line.removeprefix(">") for line in lines]
                lines = [line.removeprefix(" ") for line in lines]

                quote = "\n".join(lines)
                html_nodes = text_nodes_to_html_nodes(text_to_text_nodes(quote))
                return html_nodes

            case BlockType.UNORDERED_LIST:
                lines = self.text.split("\n")
                lines = [line.removeprefix("- ") for line in lines]
                return [ParentNode("li", text_nodes_to_html_nodes(text_to_text_nodes(line))) for line in lines]
            case BlockType.ORDERED_LIST:
                lines = self.text.split("\n")
                de_prefixed_lines = []
                for line in lines:
                    ordered_list_prefix = re.match(r"^(\d+. )", line)
                    if ordered_list_prefix is None:
                        raise Exception("something wrong man")
                    de_prefixed_lines.append(line.removeprefix(ordered_list_prefix.group(1)))
                return [ParentNode("li", text_nodes_to_html_nodes(text_to_text_nodes(line))) for line in de_prefixed_lines]
            case BlockType.CODE:
                return [LeafNode("code", self.text)]
            case _:
                return [text_node_to_html_node(node) for node in text_to_text_nodes(self.text)]






def markdown_to_html_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
    html_block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = BlockNode(block_type, block)
        html_block_nodes.append(block_node.to_html_node())

    return ParentNode("div", html_block_nodes)



def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block]
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST

    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE

    else:
        return BlockType.PARAGRAPH

def is_ordered_list(block):
    numbers = []
    lines = block.split("\n")
    for line in lines:
        match = re.match(r"^(\d+)\. ", line)
        if not match:
            return False
        numbers.append(int(match.group(1)))
    return numbers == list(range(1, len(numbers) + 1))


def extract_header_from_markdown(markdown):
    blocks = markdown_to_blocks(markdown)
    main_header = next(block for block in blocks if re.match(r"^# ", block))

    if main_header == None:
        raise Exception("No header found in markdown")

    return main_header.removeprefix("# ")


def text_nodes_to_html_nodes(nodes):
    return [text_node_to_html_node(node) for node in nodes]

