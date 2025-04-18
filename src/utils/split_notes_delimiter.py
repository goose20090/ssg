from ..text_node import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

   # for each node in nodes
    for node in old_nodes:

        # add to result and move on unless node is a text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # split the node by the delimiter

        split_nodes = node.text.split("`")

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


