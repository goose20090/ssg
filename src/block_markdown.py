from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

