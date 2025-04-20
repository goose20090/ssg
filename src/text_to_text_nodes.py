from src.utils.split_notes_delimiter import split_nodes_delimiter
from src.text_node import TextNode, TextType
from src.utils.split_link_and_image_nodes import split_nodes_link, split_nodes_image

def text_to_text_nodes(text):

    inline_delimiters = [
        ("**", TextType.BOLD),
        ("`", TextType.CODE),
        ("_", TextType.ITALIC),
    ]

    nodes = [TextNode(text, TextType.TEXT)]

    for delim_lst in inline_delimiters:
        delimiter, text_type = delim_lst
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    return split_nodes_image(split_nodes_link(nodes))
