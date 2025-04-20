from .extraction_helpers import extract_markdown_images, extract_markdown_links
from ..text_node import TextNode, TextType

def split_nodes_link(old_nodes):
    new_nodes = []

   # for each node in nodes
    for node in old_nodes:

        # add to result and move on unless node is a text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # extract links from text

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text

        for idx, link in enumerate(links):
            anchor_test, href = link
            split_nodes = text.split(f"[{anchor_test}]({href})", 1)

            # as long as there's preceding text, append it as a text node

            if (split_nodes[0] != ""):
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))

            new_nodes.append(TextNode(anchor_test, TextType.LINK, href))


            # if this is the last link found, the remainder must be text (if it exists)
            if ( idx == len(links) - 1 ) and ( split_nodes[1] != "" ):
                new_nodes.append(TextNode(split_nodes[1], TextType.TEXT))
            else:
                # make the text search string the remainder of the text
                text = split_nodes[1]

    # return result
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

   # for each node in nodes
    for node in old_nodes:

        # add to result and move on unless node is a text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # extract images from text

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text

        for idx, image in enumerate(images):
            anchor_test, href = image
            split_nodes = text.split(f"![{anchor_test}]({href})", 1)

            # as long as there's preceding text, append it as a text node

            if (split_nodes[0] != ""):
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))

            new_nodes.append(TextNode(anchor_test, TextType.IMAGE, href))


            # if this is the last image found, the remainder must be text (if it exists)
            if ( idx == len(images) - 1 ) and ( split_nodes[1] != "" ):
                new_nodes.append(TextNode(split_nodes[1], TextType.TEXT))
            else:
                # make the text search string the remainder of the text
                text = split_nodes[1]

    # return result
    return new_nodes
