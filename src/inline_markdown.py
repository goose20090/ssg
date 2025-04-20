from src.text_node import TextType, TextNode
import re


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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

   # for each node in nodes
    for node in old_nodes:

        # add to result and move on unless node is a text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # split the node by the delimiter

        split_nodes = node.text.split(delimiter)

        # unless the resulting list has an even number of elements

        if len(split_nodes) % 2 == 0:

            # this is a bad input, the delimiter input isn't closed, so raise an error
            raise ValueError("Invalid markdown, opening delimiter isn't closed")


        # then for each elem in the resulting list

        for idx, node in enumerate(split_nodes):
            # if the index is even
            if idx % 2 == 0:
                # append the result to results as a text node
                new_nodes.append(TextNode(node, TextType.TEXT))
            # if the index is odd
            else:
                # append the result to results as the type of node passed in the original method call
                new_nodes.append(TextNode(node, text_type))

    # return result
    return new_nodes


def extract_markdown_links(text):
    result = []

    links = re.findall(r"(?<!!)\[.*?\]\(.*?\)", text)

    for link in links:
        anchor_text = extract_contents_of_square_brackets(link)
        href = extract_contents_of_regular_brackets(link)


        result.append((anchor_text, href))

    return result


def extract_markdown_images(text):
    result = []

    images = re.findall(r"!\[.*?\]\(.*?\)", text)

    for image in images:
        anchor_text = extract_contents_of_square_brackets(image)
        href = extract_contents_of_regular_brackets(image)


        result.append((anchor_text, href))

    return result




def extract_contents_of_square_brackets(text):
        inner_text = re.search(r'\[(.*?)\]', text)
        if inner_text:
            inner_text = inner_text.group(1)
        else:
            raise Exception("something seriously wrong's gone on here")
        return inner_text


def extract_contents_of_regular_brackets(text):
        inner_text = re.search(r'\((.*?)\)', text)
        if inner_text:
            inner_text = inner_text.group(1)
        else:
            raise Exception("something seriously wrong's gone on here")
        return inner_text

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
