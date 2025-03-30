from html_node import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Value is required for LeafNode.")
        super().__init__(tag=tag, value=value, children=None, props=props)
